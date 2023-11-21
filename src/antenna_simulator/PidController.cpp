#include "PidController.h"

PidController::~PidController()
{

}

double PidController::Calculate(double SP, double PV)
{
    double error = SP - PV;
    // Proportional
    P = kP * error;
    // Integral
    double I = kI * error * dt;
    It = It + I;

    // Limit It
    if ((outputMax != outputMin) && (outputMax > outputMin))
    {
        if (It > outputMax)
        {
            It = outputMax;
        }
        if (It < outputMin)
        {
            It = outputMin;
        }
    }
    // Derivative
    double D = kD * (error - previousError) / dt;
    previousError = error;

    double output = P + It + D;

    // Limit output
    if ((outputMax != outputMin) && (outputMax > outputMin))
    {
        if (output > outputMax)
        {
            output = outputMax;
        }
        if (output < outputMin)
        {
            output = outputMin;
        }
    }

    return output;// + PV;
}