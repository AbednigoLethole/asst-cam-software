#include "AntennaSimulate.h"


using namespace std;

AntennaSimulate::AntennaSimulate(long periodMs)
{
    ctlPeriod = (double ) periodMs / 1000.0;
    
    aziPidController.SetValues(ctlPeriod, 6.50, 0.03, 0.8);
    aziPidController.SetMax(-maxSpeed, maxSpeed);
    elePidController.SetValues(ctlPeriod, 6.5, 0.03, 0.8);
    elePidController.SetMax(-maxSpeed, maxSpeed);

    // Get current timestamp
    double timestamp = GetCurrentTimestamp();

    actualPosition = {timestamp, 90.0, 45.0};
    desiredPosition     =   actualPosition;
    requestedPosition   =   actualPosition;

    currentSpeed        =   {0.0, 0.0};
    requestedSpeed      =   currentSpeed;

    outFile.open("Position.csv");
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
    }
    else
    {
        requestedSpeed.elevation = 0.0;
        //elevationDone = true;
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
        // Get request
        requestedPosition = positionRequests.front();
        // Remove 
        positionRequests.pop();
        // Reset PID controllers
        aziPidController.Reset();
        elePidController.Reset();

        cout << CYAN << "[+] New request: " << requestedPosition.azimuth << ", " << requestedPosition.elevation << "\n"; 
        
        // Check timestamp
        double nextTimestamp = timestamp + ctlPeriod;
        if (nextTimestamp > requestedPosition.timeStamp)
        {
            cout << RED << "[-] time in the past!" << endl;
            requestedPosition.azimuth = actualPosition.azimuth;
            requestedPosition.elevation = actualPosition.elevation;
            // Check again for requests
            if ((fabs(requestedPosition.azimuth - actualPosition.azimuth) < positionError) &&
               (fabs(requestedPosition.elevation - actualPosition.elevation) < positionError))
            {
               return ControlSpeed();
            }
        }
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
