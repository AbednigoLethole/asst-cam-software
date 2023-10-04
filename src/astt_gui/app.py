import time

from flask import Flask, render_template, request, make_response
import random
import json
from time import time
from random import random

from component_managers.astt_comp_manager import ASTTComponentManager
from component_managers.start_simulator import SimulatorManager

app = Flask(__name__)
cm = ASTTComponentManager()
node2 = None


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def start_astt_gui():
    # Trigger condition when Initialize button is clicked.

    if "button" in request.form and request.form["button"] == "Initialize":
        # Start VCAN network & simulator
        simulator_manager = SimulatorManager()
        simulator_manager.start_can_interface()
        simulator_manager.run_contaier_and_startup_simulator()
        # Await Simulator to start up
        time.sleep(3)
        # Connect to VCAN and Siumlator
        cm.connect_to_network()
        global node2
        node2 = cm.connect_to_plc_node()
        # Subscribe to AZ and EL change.
        cm.subscribe_to_az_change(node2)
        cm.subscribe_to_el_change(node2)

    # Trigger condition when Point button is clicked.
    if "azimuth" in request.form and "elevation" in request.form:
        # Get AZ and EL from GUI.
        az = request.form["azimuth"]
        el = request.form["elevation"]
        # Call a method to point to Desired AZ & EL
        cm.point_to_coordinates(node2, int(time.time()), float(az), float(el))
        # Display current AZ and EL.
        cm.trigger_transmission(node2)

    return render_template("index.html")


@app.route("/data", methods=["GET", "POST"])
def data():
    # Data Format
    # [TIME, Temperature, Humidity]

    Azimuth = random() * 100
    Elevation = random() * 55

    data = [time() * 1000, Azimuth, Elevation]

    response = make_response(json.dumps(data))

    response.content_type = "application/json"

    return response


if __name__ == "__main__":
    app.run()
