.. ASTT CAM Software documentation master file, created by
   sphinx-quickstart on Mon Jan 29 12:06:24 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

ASTT CAM Software documentation
===============================


The ASTT CAM software is the control and monitoring system for the AVN Satelite Teaching Telescope. 
The software monitors the sensors and command the telescope to move in specified direction(Az/El).
The current design of our Telescope Simulation and STT CAM system revolves around a simulated environment, emphasizing precise telescope simulation and testing
The system comprises of a Graphical User Interface(GUI), a Component Manager, and a Telescope Simulator(C++-based).
The GUI, created is web-based interface for users to control, input commands, configure parameters, and initiate telescope simulations. 
The Component Manager, manages communication between the GUI and the simulator using Python CANopen library. 
The system utilizes GPS data to determine real-time location information, such as longitude, latitude, and altitude, thereby enhancing simulation precision.

.. image:: images/astt.jpg
  :width: 80%
  :alt: Dish LMC diagram

.. toctree::
   :maxdepth: 2
   :caption: Contents:


   GUI<gui/index>
   Software<software/index>
   User Guide<how_to>



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
