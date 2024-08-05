How to deploy the software
==========================

**Installation**  
The software currently runs on:   
* Ubuntu machines

 To install and run the simulator, download docker on your machine/computer and build the software using it.

To install and run the software using docker follow this commands:

* Clone this repository into your local computer.

    ```git clone https://github.com/AbednigoLethole/asst-cam-software.git```

* Build the docker image locally.

    ```docker build -t astt-cam-software . ```

**Deploying the ASTT CAM Software**

* Deploy the ASTT docker containers

``` make Deploy-astt-cam-software```