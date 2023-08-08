#ifndef ANTENNASIMULATE_H
#define ANTENNASIMULATE_H

#include <queue>
#include <chrono>
#include <iostream>
#include <iomanip>
#include <fstream>
#include <cmath>
#include <tuple>
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

class AntennaSimulate
{
public:
    AntennaSimulate(long periodMs);
    ~AntennaSimulate();
    void RequestPosition(double timeStamp, float azi, float ele)
    {
        positionRequests.push({timeStamp, azi, ele});
    }
    void ControlSpeed();
    std::tuple<double, double, double>  SimulatePosition();

    double GetCurrentTimestamp()
    {
        // Get current timestamp
        auto ts = std::chrono::system_clock::now();
        long timestampMs = std::chrono::duration_cast<std::chrono::milliseconds>(ts.time_since_epoch()).count();
        double timestamp = (double) timestampMs / 1000.0f;
        return timestamp;
    }

private:
    void CalculateAziDesiredPosition(double nextTimestamp, double currentTimestamp)
    {
        double timeDiff = nextTimestamp - currentTimestamp;
        double speed = (requestedPosition.azimuth - actualPosition.azimuth) / timeDiff;
        std::cout << CYAN << "[+] Speed: " << speed << " time diff: " << timeDiff << RESET_COLOR << "\n";
        double output = aziPidController.Calculate(speed, requestedSpeed.azimuth); 
        LimitAziSpeed(timeDiff, output);
        desiredPosition.azimuth = actualPosition.azimuth + requestedSpeed.azimuth * timeDiff;

        std::cout << YELLOW << "AZI: " << actualPosition.azimuth << " " << desiredPosition.azimuth << " " << output << RESET_COLOR << "\n";
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
        double speed = (requestedPosition.elevation - actualPosition.elevation) / timeDiff;
        double output = aziPidController.Calculate(speed, requestedSpeed.elevation); 
        LimitEleSpeed(timeDiff, output);
        desiredPosition.elevation = actualPosition.elevation + requestedSpeed.elevation * timeDiff;

        std::cout << BOLDYELLOW <<  "ELE: " << actualPosition.elevation << " " << desiredPosition.elevation << " " << output << RESET_COLOR << "\n";
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

    void LimitPosition(double &position, double minPosition, float maxPosition)
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

private:
    // Position limits
    const float maxAzimuth      = 360.0;
    const float minAzimuth      = 0.0;
    const float minElevation    = 10.0;
    const float maxElevation    = 90.0;
    const float positionError   = 0.01;
    // Speed limits
    const float maxSpeed     = 10.0;
//    const float maxAziSpeed     = 10.0;
//    const float maxEleSpeed     = 10.0;
    const float maxAccel = 5.0;
    // Control loop  period in seconds
    float ctlPeriod;

    Position actualPosition;
    Position desiredPosition;
    Position requestedPosition;

    std::queue<Position> positionRequests;

    Speed currentSpeed;
    Speed requestedSpeed;

    PidController aziPidController;
    PidController elePidController;

    std::ofstream outFile;
};

#endif