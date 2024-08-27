Unreleased
**********
- Added doctrings on classes and methods.
- Changed constant variables to uppercase as per PEP 8 style guide.
- Added mypy.ini file to configure mypy.
- Change max line on our lint configurations from 70 to 99.  
- Modularized functions on app.py (some to be moved to conftest and utils)

Version 1.1.2
*************
- Added antenna speed on the GUI.
- Integrated antenna speed with the component Manager

Version 1.1.1
*************
- Addded a docker container for GUI and open the port for it.
- Removed the use of a modal to ask for password on the GUI.
- Removed the Start_simulator script
- Remomed the validation checks for password in app.py
- Updated the Readthedocs instructions on how to deploy the ASTT-CAM-Software.
- Updated the readme instructions on how to deploy the ASTT-CAM-Software.
 
Version 1.0.1
*************
- Updated the ASTT CAM software documentation
- Added a BSD-3 License

Version 1.0.0
*************
- Added the ASTT GUI
- Added the ASTT component manager
- Added the ASTT antenna simulator
- Integrated the ASTT GUI with the ASTT component manager
- Integrated the the ASTT component manager with the ASTT antenna simulator
- Added Unit and acceptance tests to test the component manager
- Added a pipeline machinery to run tests and linting
- Added documentation for the ASTT software
- Added package dependecies for the ASTT software