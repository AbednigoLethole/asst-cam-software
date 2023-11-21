#ifndef PIDCONTROLLER_H
#define PIDCONTROLLER_H
// See https://pidexplained.com/pid-controller-explained/
// See http://brettbeauregard.com/blog/2011/04/improving-the-beginner’s-pid-reset-windup/

#pragma once

class PidController
{
public:
    PidController()
    {
        this ->dt = 0.0;
        this->kP = 0.0;
        this->kI = 0.0;
        this->kD = 0.0;
        SP = 0.0;
        PV = 0.0;
        P = 0.0;
        It = 0.0;
        previousError = 0.0;
        outputMax = 0.0;
        outputMin = 0.0;
    }
    void SetValues(double period, double kP, double kI, double kD)
    {
        this ->dt = period;
        this->kP = kP;
        this->kI = kI;
        this->kD = kD;
    } 
    void SetMax(double outputMin, double outputMax)
    {
        this->outputMin = outputMin;
        this->outputMax = outputMax;
    }
    void Reset()
    {
        It = 0.0;
        previousError = 0.0;
    }
    ~PidController();
    double Calculate(double SP, double PV);

private:
    // Inputs
    double SP;      // target (e.g. position)
    double PV;      // process value (e.g. target postion)
     // Proportional (P)
    double P;       // = kP x Err
    double kP;      // Gain P
    // Integral (I)
    double kI;      // Gain I
    double It;      // Integratl total: It = It + I    
    // Derivative
    double kD;      // Gain D   
 
    // Delta time
    double dt;      // wait time

    double previousError;   // Previous error

    // Output limits
    double outputMax;
    double outputMin;

};

#endif