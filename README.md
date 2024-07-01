# ASTT CAM software

[![Documentation Status](https://readthedocs.org/projects/asst-cam-software/badge/?version=latest)](https://asst-cam-software.readthedocs.io/en/latest/)

The ASTT CAM software is the control and monitoring system for the AVN Satelite Teaching Telescope. The software monitors the sensors and command the telescope to move in specified direction(Az/El).

The CAM Software consist of a C++ simulator(Slave Node) which simulate the AST Telescope. However the simulator does not simulate the complete functionality of the Telescope.

## **Installation**  
The software currently runs on:   
* Ubuntu machines

 To install and run the simulator, download docker on your machine/computer and build the software using it.

To install and run the software using docker follow this commands:

* Clone this repository into your local computer.

    ```git clone https://github.com/AbednigoLethole/asst-cam-software.git```

* Build the docker image locally.

    ```docker build -t astt-cam-software . ```

## **Install the dependencies**

* Install Poetry

    ``` pip install poetry ```

* Install dependencies

    ``` poetry config virtualenvs.create false && poetry install ```

## **Running the GUI**

* Run the GUI

``` python3 src/astt_gui/app.py ```


## **Running the unit tests**

* Run the test

    ``` python -m unittest discover -v -s tests/unit ```

## **Building the docs**

* To build the docs,first go to the directory where conf.py exists.
    ```cd docs ```

* Generate the readthedocs pages
    ```sphinx-build -b html . _build -v ```

* The home page of the docs is found in _build directory,open the index.html with the browser.

## **Updating poetry lock file**

* To update the poetry lock file, ensure you shell (only) into the astt container.
    ``` docker run -it -v "$(pwd)":/workspace <image id> /bin/bash ```

*  Run the command to update the poetry file.
    ``` cd ../workspace && poetry lock --no-update ```