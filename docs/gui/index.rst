Graphical User Interface
========================

This Flask application provides a graphical user interface (GUI) for controlling and monitoring an antenna system. 
It uses SocketIO for real-time updates of the antenna's azimuth (AZ) and elevation (EL) positions,
as well as its functional states and modes.

**API Endpoints**
   **GET /**
      Renders the main index page.

      **Response:**

      HTML content of the index page.
   **POST /**
   Handles different actions based on the form inputs:

   Initialize Button: Initializes the simulator and starts background tasks.
   Point Button: Points the antenna to the specified AZ and EL coordinates.
   Track Button: Starts tracking a source (e.g., the sun).
   Mode Buttons: Sets the antenna to different modes (Idle, Stow, Point).



.. automodule:: src.astt_gui

.. toctree::
   
   Flask web application<src.astt_gui>