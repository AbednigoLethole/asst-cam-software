# ASTT CAM software 

The ASTT CAM software is the control and monitoring system for the AVN Satelite Teaching Telescope. The software monitors the sensors and command the telescope to move in specified direction(Az/El).

The CAM Software consist of two C++ simulators(Master Node & Slave Node) which simulate the AST Telescope. However these simulators do not simulate the complete implementation of the Telescope.

## **Installation**  
The software currently runs on:   
* Ubuntu 20.04

If you are not using Ubuntu 20.04 , download docker on your machine/computer and build the software using it.

To install and run the software using docker follow this commands:

* Clone this repository into your local computer.

    ```git clone https://github.com/AbednigoLethole/asst-cam-software.git```
  
* Build the image.

    ```docker build -t <your image name> .```

* Run the docker container with admin rights.

    ```docker run -it  --privileged <your image id> /bin/bash ```

* Once you get access to the container shell, Make shells executable.

    ```chmod +x installLely.sh startVirtualCANInterface.sh ```

* Execute a shell to install Lely and start a virtual CAN Network.

    ```./installLely.sh ```
    
    ```./startVirtualCANInterface.sh ```
    

## **Running the C++ Simulators**  

* move to the simulators directory.

    ```cd src/canopen-simulator ```

* Make C++ compiling shells executable.

    ```chmod +x compileMaster.sh compileSlave.sh ```

* Execute a shell to compile master node and a shell to compile the slave node.

    ```./compileMaster.sh ```

    ```./compileSlave.sh ```

* Run the master node.

    ```./master```

* Run the master node.

    ```./slave```
