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

    outFile.open("Position.csv");
    outFile << "Timestamp (s), Azimuth (deg), Elevation (deg)" << "\n";
}

AntennaSimulate::~AntennaSimulate()
{
    outFile.close();
}

void AntennaSimulate::ControlSpeed()
{
    // Get current timestamp
    double timestamp = GetCurrentTimestamp();

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
    actualPosition.azimuth = actualPosition.azimuth + requestedSpeed.azimuth * (timestamp - actualPosition.timeStamp );
    LimitPosition(actualPosition.azimuth, minAzimuth, maxAzimuth);
    actualPosition.elevation = actualPosition.elevation + requestedSpeed.elevation * (timestamp - actualPosition.timeStamp);
    LimitPosition(actualPosition.elevation, minElevation, maxElevation);
    actualPosition.timeStamp = timestamp;

    cout.precision(3);
    cout << BLUE << fixed << "[+] " << actualPosition.timeStamp << ", " << actualPosition.azimuth << ", " << actualPosition.elevation << ", " << requestedSpeed.azimuth << ", " << requestedSpeed.elevation << RESET_COLOR << "\n";
    outFile << fixed <<  actualPosition.timeStamp << ", " << actualPosition.azimuth << ", " << actualPosition.elevation << "\n";

    return make_tuple(actualPosition.timeStamp, actualPosition.azimuth, actualPosition.elevation);
}
