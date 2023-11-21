#ifndef ANTENNASIMULATE_H
#define ANTENNASIMULATE_H

#include <queue>
#include <chrono>
#include <iostream>
#include <iomanip>
#include <fstream>
#include <cmath>
#include <tuple>
#include <cstdint>
#include "PidController.h"
#include "TerminalColors.h"

#pragma once

struct Position
{
    double timeStamp;
    double azimuth;
    double elevation;
};

struct Speed
{
    double azimuth;
    double elevation;
};

struct DInputs
{
    unsigned int stowWindow     :   1;
    unsigned int stowReleased   :   1;
    unsigned int stowEngaged    :   1;
    unsigned int spare          :   5;
};

union DigitalInputs
{
    uint8_t raw;
    DInputs dInputs;
};

class AntennaSimulate
{
public:
    AntennaSimulate(long periodMs);
    ~AntennaSimulate();
    void RequestPosition(double timeStamp, float azi, float ele)
    {
        // Only accept point requested when in point mode
        if (MODE::POINT == mode)
        {
            positionRequests.push({timeStamp, azi, ele});
        }
        else
        {
            std::cerr << RED << "[-] Not in point mode:  " << modeNames[mode] << RESET_COLOR << "\n";
        }
    }
    // State machines
    bool ApplicationStateMachine();
    bool FunctionalStateMachine();
    bool ModeStateMachine();
    void HandleModeCmd(std::string modeCmd);

    void ControlSpeed();
    std::tuple<double, double, double>  SimulatePosition();
    void SimulateStowWindow();
    bool SimulateStowPin(bool insert);

    double GetCurrentTimestamp()
    {
        // Get current timestamp
        auto ts = std::chrono::system_clock::now();
        long timestampMs = std::chrono::duration_cast<std::chrono::milliseconds>(ts.time_since_epoch()).count();
        double timestamp = (double) timestampMs / 1000.0f;
        return timestamp;
    }
    
    uint8_t GetFunctionalState()
    {
        return functionalState;
    }

    uint8_t GetApplicationState()
    {
        return applicationState;
    }

    uint8_t GetMode()
    {
        return mode;
    }

    void SetMode(uint8_t newMode)
    {
        mode = (MODE )newMode;
    }

    std::string GetModeCmdName(uint32_t modeCmd)
    {
        if (MODE_CMD::MODE_CMD_LAST > modeCmd)
        {
            return modeCmdNames[modeCmd];
        }
        else
        { 
            std::string invalidCmd = "invalid command";
            return invalidCmd;
        }
    }
    DigitalInputs GetDInputs()
    {
        return dInputs;
    }

private:
    void CalculateAziDesiredPosition(double nextTimestamp, double currentTimestamp)
    {
        double timeDiff = nextTimestamp - currentTimestamp;
        desiredPosition.timeStamp = nextTimestamp;
        if (requestedPosition.timeStamp > nextTimestamp)
        {
            desiredPosition.azimuth = desiredPosition.azimuth + desiredSpeed.azimuth * (timeDiff);
        }
        else
        {
            desiredPosition.azimuth = requestedPosition.azimuth;
        }
        //std::cout << CYAN << "Desired azim = " << desiredPosition.azimuth << RESET_COLOR << "\n";
        double speed = (desiredPosition.azimuth - actualPosition.azimuth) / timeDiff;
        double output = aziPidController.Calculate(speed, requestedSpeed.azimuth); 
        LimitAziSpeed(timeDiff, output);

    //    std::cout << YELLOW << "AZI: " << actualPosition.azimuth << " " << desiredPosition.azimuth << " " << output << RESET_COLOR << "\n";
    }
    
    void LimitAziSpeed(double timeDiff, double speed)
    {
         // Check maximum accelleration
        double accel = (speed - requestedSpeed.azimuth) / timeDiff;
        if (maxAccel < accel)
        {
            speed = requestedSpeed.azimuth + maxAccel * timeDiff;
        }
        if (-maxAccel > accel)
        {
            speed = requestedSpeed.azimuth - maxAccel * timeDiff;
        }
        if (fabs(speed) > maxSpeed)
        {
            if (0 < speed)
            {
                speed = maxSpeed;
            }
            else
            {
                speed = -maxSpeed;
            }
        }
        requestedSpeed.azimuth = speed;
    }

    void CalculateEleDesiredPosition(double nextTimestamp, double currentTimestamp)
    {
        double timeDiff = nextTimestamp - currentTimestamp;
        desiredPosition.timeStamp = nextTimestamp;
        if (requestedPosition.timeStamp > nextTimestamp)
        {
            desiredPosition.elevation = desiredPosition.elevation + desiredSpeed.elevation * (timeDiff);
        }
        else
        {
            desiredPosition.elevation = requestedPosition.elevation;
        }
        //std::cout << CYAN << "Desired azim = " << desiredPosition.elevation << RESET_COLOR << "\n";
        double speed = (desiredPosition.elevation - actualPosition.elevation) / timeDiff;
        double output = elePidController.Calculate(speed, requestedSpeed.elevation); 
        LimitEleSpeed(timeDiff, output);

        //std::cout << BOLDYELLOW <<  "ELE: " << actualPosition.elevation << " " << desiredPosition.elevation << " " << output << RESET_COLOR << "\n";
    }
    
    void LimitEleSpeed(double timeDiff, double speed)
    {
         // Check maximum accelleration
        double accel = (speed - requestedSpeed.elevation) / timeDiff;
        if (maxAccel < accel)
        {
            speed = requestedSpeed.elevation + maxAccel * timeDiff;
        }
        if (-maxAccel > accel)
        {
            speed = requestedSpeed.elevation - maxAccel * timeDiff;
        }
        if (fabs(speed) > maxSpeed)
        {
            if (0 < speed)
            {
                speed = maxSpeed;
            }
            else
            {
                speed = -maxSpeed;
            }
        }
        requestedSpeed.elevation = speed;
    }

    void LimitPosition(double &position, double minPosition, double maxPosition)
    {
        if (maxPosition <= position)
        {
            position = maxPosition;
        }
        if (minPosition >= position)
        {
            position = minPosition;
        }
    }

    void ResetPointing()
    {
        // Remove all queued position requests
        while (!positionRequests.empty())
        {
            positionRequests.pop();
        }
        // Stop movement
        requestedPosition = actualPosition;
        desiredPosition = actualPosition;
    }

private:
    // Position limits
    const float maxAzimuth      = 360.0;
    const float minAzimuth      = 0.0;
    const float minElevation    = 10.0;
    const float maxElevation    = 90.0;
    const float positionError   = 0.005;
    // Speed limits
    const float maxSpeed        = 10.0;
    const float maxAccel        = 5.0;
    // Stow values
    const float stowPositionElevation = 90.0;
    const float stowWindow      = 0.01;
    const float stowPintime     = 30.0;
    uint32_t stowPinElapsed;

    // Control loop  period in seconds
    float ctlPeriod;

    Position actualPosition;
    Position desiredPosition;
    Position requestedPosition;

    std::queue<Position> positionRequests;

    Speed currentSpeed;
    Speed requestedSpeed;
    Speed desiredSpeed;

    PidController aziPidController;
    PidController elePidController;

    std::ofstream outFile;

    // Application states:
    //  Note: the string indexes must match the enum 
    enum APP_STATE {INITIALISE = 0, 
                    OPERATE,
                    STATE_LAST};

    const std::string applicationStateNames[APP_STATE::STATE_LAST] =
                    {"Initialise",
                    "Operate"};

    // Functional states:
    //  Note: the string indexes must match the enum 
    enum FUNC_STATE { BRAKED = 0,
                    MOVING,
                    ESTOP,
                    ERROR,
                    FUNC_STATE_LAST};

    const std::string funtionalStateNames[FUNC_STATE::FUNC_STATE_LAST] =
                    {"Braked",
                    "Moving",
                    "E-Stop",
                    "Error"};

    // Modes:
    //  Note: the string indexes must match the enum 
    enum MODE {IDLE = 0,
               POINT,
               STOW,
               MODE_LAST};                                   

    std:: string modeNames[MODE::MODE_LAST] =
                    {"Idle",
                    "Point",
                    "Stow"};

    enum MODE_CMD { IDLE_CMD= 0,
                    POINT_CMD,
                    STOW_CMD,
                    MODE_CMD_LAST};

    const std::string modeCmdNames[MODE_CMD::MODE_CMD_LAST] = 
                    {   "idle",
                        "point",
                        "stow"};

    // State machines
    enum FUNC_STATE functionalState;
    enum APP_STATE applicationState;
    enum MODE mode;

    enum FUNC_STATE prevFunctionalState;
    enum APP_STATE prevApplicationState;
    enum MODE prevMode;

    // Digital Inputs
    DigitalInputs dInputs;

};

#endif
