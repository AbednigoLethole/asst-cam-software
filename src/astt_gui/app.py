import time
from datetime import datetime
from threading import Lock

from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO

from component_managers.astt_comp_manager import ASTTComponentManager
from component_managers.start_simulator import SimulatorManager

thread = None
thread_lock = Lock()
thread2 = None

app = Flask(__name__)
app.config["SECRET_KEY"] = "STT"
socketio = SocketIO(app, cors_allowed_origins="*")

cm = ASTTComponentManager()
node2 = None


def get_current_datetime():
    now = datetime.now()
    return now.strftime("%m/%d/%Y %H:%M:%S")


def background_thread(node):
    """Feeds az & el to the GUI."""
    if node is not None:
        while True:
            node.tpdo[1].wait_for_reception()
            node.tpdo[2].wait_for_reception()
            az = node.tpdo[
                "Position Feedback.Azimuth(R64) of position"
            ].raw
            el = node.tpdo[
                "Position Feedback.Elevation(R64) of position"
            ].raw
            socketio.emit(
                "updateAZELData",
                {"az": az, "el": el, "date": get_current_datetime()},
            )
            socketio.sleep(1)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def start_astt_gui():
    # Trigger condition when Initialize button is clicked.

    if (
        "button" in request.form
        and request.form["button"] == "Initialize"
    ):
        user_pass = request.form["password"]
        # Start VCAN network & simulator
        simulator_manager = SimulatorManager()
        success = simulator_manager.start_can_interface(user_pass)

        # Report incorrect password to user.
        if success == 0:
            simulator_manager.run_contaier_and_startup_simulator()
            # Await Simulator to start up
            time.sleep(2)
            # Connect to VCAN and Siumlator
            cm.connect_to_network()
            global node2
            node2 = cm.connect_to_plc_node()
            # Subscribe to AZ and EL change.
            cm.subscribe_to_az_change(node2)
            cm.subscribe_to_el_change(node2)
            cm.subscribe_to_func_state(node2)
            cm.subscribe_to_mode_command_obj(node2)
            cm.subscribe_to_stow_sensor(node2)
            cm.set_point_mode(node2)

            return jsonify("success")
        if success == 1:
            return jsonify("Wrong password,Try again!!")

    # Trigger condition when Point button is clicked.
    if "azimuth" in request.form and "elevation" in request.form:
        # Get AZ and EL from GUI.
        az = request.form["azimuth"]
        el = request.form["elevation"]
        # Call a method to point to Desired AZ & EL
        cm.point_to_coordinates(
            node2, int(time.time()), float(az), float(el)
        )
        # Display current AZ and EL.
        cm.trigger_transmission(node2)

        global thread
        with thread_lock:
            if thread is None:
                thread = socketio.start_background_task(
                    background_thread, node2
                )

    if "sources" in request.form and request.form["sources"] == "sun":
        global thread2
        with thread_lock:
            if thread is None:
                print("Hi")
                thread2 = socketio.start_background_task(
                    background_thread, node2
                )
                print("Hey")
        cm.track_sun(node2, 1)

    else:
        pass

    return render_template("index.html")


def connect():
    global thread

    print("Client connected")

    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(
                background_thread, node2
            )


"""
Decorator for disconnect.
"""


def disconnect():
    print("Client disconnected", request.sid)


if __name__ == "__main__":
    print("App started")
    socketio.run(app)
