#include "AntennaSimulate.h"


using namespace std;

AntennaSimulate::AntennaSimulate(long periodMs)
{
    ctlPeriod = (double ) periodMs / 1000.0;
    
//    aziPidController.SetValues(ctlPeriod, 6.50, 0.03, 0.8);
    aziPidController.SetValues(ctlPeriod, 0.90, 0.05, 0.01);
    aziPidController.SetMax(-maxSpeed, maxSpeed);
//    elePidController.SetValues(ctlPeriod, 6.5, 0.03, 0.8);
    elePidController.SetValues(ctlPeriod, 0.9, 0.05, 0.01);
    elePidController.SetMax(-maxSpeed, maxSpeed);

    // Get current timestamp
    double timestamp = GetCurrentTimestamp();

    actualPosition = {timestamp, 0.0, 90.0};
    desiredPosition     =   actualPosition;
    requestedPosition   =   actualPosition;

    currentSpeed        =   {0.0, 0.0};
    requestedSpeed      =   currentSpeed;

    // Initialise state machines;
    applicationState    = APP_STATE::INITIALISE;
    functionalState     = FUNC_STATE::BRAKED;
    mode                = MODE::IDLE;
    prevApplicationState    = APP_STATE::STATE_LAST;
    prevFunctionalState     = FUNC_STATE::FUNC_STATE_LAST;
    prevMode                = MODE::MODE_LAST;

    // Digital inputs
    dInputs.dInputs.stowWindow  = 0;
    dInputs.dInputs.stowEngaged = 1;
    dInputs.dInputs.stowReleased= 0;

    // Stow pin timer
    stowPinElapsed              = 0;

    outFile.open("Position.csv");
    outFile << "Timestamp (s), Azimuth (deg), Elevation (deg)" << "\n";
}

AntennaSimulate::~AntennaSimulate()
{
    outFile.close();
}

bool AntennaSimulate::ApplicationStateMachine()
{
    switch (applicationState)
    {
        case APP_STATE::INITIALISE:
            // Perform initialise actions, i.e. read config
            applicationState = APP_STATE::OPERATE;
            break;
        
        case APP_STATE::OPERATE:
            // Perform operate actions
            break;

        default:
            cerr << RED << "[-] Application state invalid" << RESET_COLOR << "\n";
            break;
    }

    if (prevApplicationState != applicationState)
    {
        prevApplicationState = applicationState;
        return true;
    }
    return false;
}

bool AntennaSimulate::FunctionalStateMachine()
{
    switch (functionalState)
    {
        case FUNC_STATE::BRAKED:
            ResetPointing();
            break;
    
        case FUNC_STATE::MOVING:
            break;

        case FUNC_STATE::ESTOP:
            mode = MODE::IDLE;
            break;

        case FUNC_STATE::ERROR:
            mode = MODE::IDLE;
            break;

        default:
            cerr << RED << "[-] Functional state invalid" << RESET_COLOR << "\n";
            break;
    }
    if (prevFunctionalState != functionalState)
    {
        prevFunctionalState = functionalState;
        return true;
    }
    return false;
}

bool AntennaSimulate::ModeStateMachine()
{
    static bool startStow = false;
    static double startTimestamp = 0.0;

    // Get timestamp
    auto ts = std::chrono::system_clock::now();
    long timestampMs = std::chrono::duration_cast<std::chrono::milliseconds>(ts.time_since_epoch()).count() + 1000;
    double timestamp = (double) timestampMs / 1000.0f + 1;
    switch (mode)
    {
        case MODE::IDLE:
            functionalState = FUNC_STATE::BRAKED;
            break;
        
        case MODE::POINT:
            // Stow pin engaged
            if (!dInputs.dInputs.stowReleased)
            {
                if (SimulateStowPin(false))
                {
                    functionalState = FUNC_STATE::MOVING;
                }
            }
            else
            {
                functionalState = FUNC_STATE::MOVING;
            }
            break;

        case MODE::STOW:
            functionalState = FUNC_STATE::MOVING;

            if (!startStow)
            {
                ResetPointing();

                // Set requested position to stow position
                requestedPosition.timeStamp = timestamp;
                requestedPosition.elevation = stowPositionElevation;
                startTimestamp = timestamp;
                startStow = true;
            }

            // Check the timestamp
            if (startTimestamp < timestamp)
            {
                if (fabs(requestedPosition.elevation - actualPosition.elevation) < positionError)
                {
                    // Stow pin engaged
                    if ((!dInputs.dInputs.stowEngaged) && dInputs.dInputs.stowWindow)
                    {
                        if (SimulateStowPin(true))
                        {
                            functionalState = FUNC_STATE::BRAKED;
                        }
                    }
                    else
                    {
                        functionalState = FUNC_STATE::BRAKED;
                    }
                }
            }
            break;

        case MODE::MODE_LAST:
        default:
            cerr << RED << "[-] Mode invalid" << RESET_COLOR << "\n";
            break;
    }
    if (prevMode != mode)
    {
        prevMode = mode;
        startStow = false;
        return true;
    }
    return false;
}

void AntennaSimulate::HandleModeCmd(string modeCmd)
{
    cout << YELLOW << "[+] Mode command " << modeCmd << RESET_COLOR << "\n";
    // Idle command
    if (modeCmdNames[MODE_CMD::IDLE_CMD] == modeCmd)
    {
        if ((MODE::STOW == mode) || (MODE::POINT == mode))
        {
            mode = MODE::IDLE;
        }
    }
    // Point command
    if (modeCmdNames[MODE_CMD::POINT_CMD] == modeCmd)
    {
        if ((MODE::STOW == mode) || (MODE::IDLE == mode))
        {
            // Go to point if functional state is braked:
            // otherwise already in point or 
            // e-stop is pressed or 
            // error is present
            if ((FUNC_STATE::BRAKED == functionalState) ||
                (FUNC_STATE::MOVING == functionalState))
            {
                mode = MODE::POINT;
            }
            else
            {
                cerr << RED << "[-] Error functional state = " << funtionalStateNames[functionalState] << RESET_COLOR << "\n";
            }
        }
    }
    // Stow command
    if (modeCmdNames[MODE_CMD::STOW_CMD] == modeCmd)
    {
        if ((MODE::POINT == mode) || (MODE::IDLE == mode))
        {
            // Go to stow if functional state is braked: or moving
            // otherwise e-stop is pressed or 
            // error is present
            if ((FUNC_STATE::BRAKED == functionalState) || (FUNC_STATE::MOVING == functionalState))
            {
                mode = MODE::STOW;
            }
            else
            {
                cerr << RED << "[-] Error functional state = " << funtionalStateNames[functionalState] << RESET_COLOR << "\n";
            }
        }
    }
}

void AntennaSimulate::ControlSpeed()
{
    // Get current timestamp
    double timestamp = GetCurrentTimestamp();

    // Can only move in functional state moving
    if (FUNC_STATE::MOVING != functionalState)
    {
        while (!positionRequests.empty())        
        {
            // Clear requests
            positionRequests.pop();
        }
        cout << "\r" << RED << "[-] Not in moving state" << RESET_COLOR << flush;
        return;
    }

    double nextTimestamp = timestamp + ctlPeriod;
    // Control azimuth
    if (fabs(requestedPosition.azimuth - actualPosition.azimuth) > positionError)
    {
        // Calculate desired position
        CalculateAziDesiredPosition(nextTimestamp, timestamp);
        desiredPosition.timeStamp = nextTimestamp;
//        LimitPosition(desiredPosition.azimuth, minAzimuth, maxAzimuth);
    }
    else
    {
        requestedSpeed.azimuth = 0.0;
    }
    // Control elevation
    if (fabs(requestedPosition.elevation - actualPosition.elevation) > positionError)
    {
        // Calculate desired position
        CalculateEleDesiredPosition(nextTimestamp, timestamp);
        desiredPosition.timeStamp = nextTimestamp;
  //      LimitPosition(desiredPosition.elevation, minElevation, maxElevation);
    }
    else
    {
        requestedSpeed.elevation = 0.0;
    }

    // Check for new requests
    if (!positionRequests.empty())
    {
        // Check if the current request is still valid, i.e. requested timestamp 
        // is greater than the next timestamp
        if (requestedPosition.timeStamp > nextTimestamp)
        {
            return;
        }
        // Store previous request
        Position prevRequestedPosition = requestedPosition;
        // Get request
        requestedPosition = positionRequests.front();
        // Remove 
        positionRequests.pop();
        // Check timestamp
        double nextTimestamp = timestamp + ctlPeriod;
        if (nextTimestamp > requestedPosition.timeStamp)
        {
            cout << RED << fixed << "[-] time in the past: " << nextTimestamp - requestedPosition.timeStamp << endl;

            requestedPosition = prevRequestedPosition;
            // Check again
            // Check again for requests
            if ((fabs(requestedPosition.azimuth - actualPosition.azimuth) < positionError) &&
                (fabs(requestedPosition.elevation - actualPosition.elevation) < positionError))
            {            
                return ControlSpeed();
            }
        }
        desiredPosition = actualPosition;
        // Reset PID controllers
        aziPidController.Reset();
        elePidController.Reset();
        desiredSpeed.azimuth = (requestedPosition.azimuth - actualPosition.azimuth) / (requestedPosition.timeStamp - timestamp);
        desiredSpeed.elevation = (requestedPosition.elevation - actualPosition.elevation) / (requestedPosition.timeStamp - timestamp);

        cout << CYAN << fixed << "[+] " << timestamp << " New request: " << requestedPosition.timeStamp << " =>  " <<  requestedPosition.azimuth << ", " << requestedPosition.elevation << "\n";         
    }
}

tuple<double, double, double> AntennaSimulate::SimulatePosition()
{
    // Get current timestamp
    double timestamp = GetCurrentTimestamp();
    if (FUNC_STATE::MOVING == functionalState)
    {
        actualPosition.azimuth = actualPosition.azimuth + requestedSpeed.azimuth * (timestamp - actualPosition.timeStamp );
        LimitPosition(actualPosition.azimuth, minAzimuth, maxAzimuth);
        actualPosition.elevation = actualPosition.elevation + requestedSpeed.elevation * (timestamp - actualPosition.timeStamp);
        LimitPosition(actualPosition.elevation, minElevation, maxElevation);

        cout.precision(3);
        cout <<  BLUE << "\r" << fixed << "[+] " << actualPosition.timeStamp << ", " << actualPosition.azimuth << ", " << actualPosition.elevation << ", " << requestedSpeed.azimuth << ", " << requestedSpeed.elevation << RESET_COLOR << std::flush;
        outFile << fixed <<  actualPosition.timeStamp << ", " << actualPosition.azimuth << ", " << actualPosition.elevation << "\n";
    }
    actualPosition.timeStamp = timestamp;
    return make_tuple(actualPosition.timeStamp, actualPosition.azimuth, actualPosition.elevation);
}

void AntennaSimulate::SimulateStowWindow()
{
    if (abs(actualPosition.elevation - stowPositionElevation) < stowPositionElevation)
    {
        dInputs.dInputs.stowWindow  =   1;
    }
    else
    {
        dInputs.dInputs.stowWindow  =   0;
    }
}

bool AntennaSimulate::SimulateStowPin(bool insert)
{
    // Pin insert
    if (insert)
    {
        if (dInputs.dInputs.stowReleased)
        {
            stowPinElapsed = 0;
            dInputs.dInputs.stowReleased = 0b0;
        }
        if ((dInputs.dInputs.stowEngaged) && (!dInputs.dInputs.stowReleased))
        {
            return true;
        }
    }
    else
    {
        if (dInputs.dInputs.stowEngaged)
        {
            stowPinElapsed = 0;
            dInputs.dInputs.stowEngaged = 0b0;
        }
        if ((!dInputs.dInputs.stowEngaged) && (dInputs.dInputs.stowReleased))
        {
            return true;
        }
    }

    if (((float) stowPinElapsed * ctlPeriod) > stowPintime)
    {
        if (insert)
        {
            dInputs.dInputs.stowEngaged = 0b1;
        }
        else
        {
            dInputs.dInputs.stowReleased = 0b1;
        }
    }
    else
    {
        stowPinElapsed++;
        cout << YELLOW << "**** stowPinElapsed: " << stowPinElapsed << RESET_COLOR << "\n";
    }
    return false;
}