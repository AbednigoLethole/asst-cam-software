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

**Install the dependencies**

* Install Poetry

    ``` pip install poetry ```

* Install dependencies

    ``` poetry config virtualenvs.create false && poetry install ```

**Running the GUI**

* Run the GUI

``` python3 src/asst_gui/app.py ```