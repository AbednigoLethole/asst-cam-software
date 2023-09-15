# ASTT CAM software 

The ASTT CAM software is the control and monitoring system for the AVN Satelite Teaching Telescope. The software monitors the sensors and command the telescope to move in specified direction(Az/El).

The CAM Software consist of a C++ simulator(Slave Node) which simulate the AST Telescope. However the simulator does not simulate the complete functionality of the Telescope.

## **Installation**  
The software currently runs on:   
* Ubuntu machines

 To install and run the simulator, download docker on your machine/computer and build the software using it.

To install and run the software using docker follow this commands:

* Clone this repository into your local computer.

    ```git clone https://github.com/AbednigoLethole/asst-cam-software.git```
  
* Download the simulator from a drive, Here's a link below:

    ```https://drive.google.com/file/d/1JjoqoAQqZabTKoWz5sL3uhbDIZ5jXAc9/view?ts=64e315a7```

* start the virtual CAN Interface

    ```sh startVirtualCANInterface.sh```

* Load the docker image from  the .tar file .

    ```docker load -i ubuntu_canopen.tar ```

* Run the container shell that has the simulator with all its dependencies.

    ```docker run -it --network=host ubuntu_canopen ```

* Once the shell is open, move to directory that has the simulator.

    ```cd simulator ```
    
## **Running the C++ Antenna Simulator**  

* The simulator is alrealdy compiled so use the following command to start it:

    ```./slave ```

* To restart the simulator, use the following command:

    ``` reset && ./slave```

## **Running the component manager**

* Install Poetry

    ``` pip install poetry ```

* Install dependencies

    ``` poetry config virtualenvs.create false && poetry install  ```

* run the asst component manager

``` python3 src/component_managers/asst_comp_manager.py ```

## **Running the tests**

* Ensure the simulator is running


* Run the test

    ``` pytest tests/ -v ```




