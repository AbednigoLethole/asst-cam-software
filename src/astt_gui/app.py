import logging
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
thread3 = None

app = Flask(__name__)
app.config["SECRET_KEY"] = "STT"
socketio = SocketIO(app, cors_allowed_origins="*")

cm = ASTTComponentManager()
logger = logging.getLogger("ASTT-GUI")

logging.basicConfig(
    filename="app_dev.log",
    format="%(asctime)s|%(levelname)s|%(name)s|%(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


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


def states_and_modes_thread(comp_manager):
    logger.info("Thread triggered")
    while True:
        func_state = comp_manager.antenna_func_state.name
        mode = comp_manager.antenna_mode.name
        stow_pin_state = comp_manager.stow_sensor_state.name
        if func_state and mode is not None:
            socketio.emit(
                "updateStateMode",
                {
                    "mode": str(mode),
                    "funcState": str(func_state),
                    "stowPinState": str(stow_pin_state),
                },
            )
            socketio.sleep(1)
        logger.info("SENT")


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
        cm.clear_all_logs()
        # Start VCAN network & simulator
        logger.info("Intitialized button triggered")
        simulator_manager = SimulatorManager()
        logger.info("Starting vcan interface")
        logger.info("Passing user password")
        success = simulator_manager.start_can_interface(user_pass)

        # Report incorrect password to user.
        if success == 0:
            logger.info("correct password")

            simulator_manager.run_contaier_and_startup_simulator()
            # Await Simulator to start up
            time.sleep(2)
            # Connect to VCAN and Siumlator
            cm.connect_to_network()
            cm.connect_to_plc_node()
            # Subscribe to AZ and EL change.
            cm.subscribe_to_az_change()
            cm.subscribe_to_el_change()
            cm.subscribe_to_func_state()
            cm.subscribe_to_mode_command_obj()
            cm.subscribe_to_antenna_mode()
            cm.subscribe_to_stow_sensor()
            # Set point mode function below needs to be removed
            cm.trigger_transmission()
            global thread3
            with thread_lock:
                if thread3 is None:
                    thread3 = socketio.start_background_task(
                        states_and_modes_thread, cm
                    )

            return jsonify("success")
        if success == 1:
            logger.warn("Incorrect password entered")
            return jsonify("Wrong password,Try again!!")

    # Trigger condition when Point button is clicked.
    if "azimuth" in request.form and "elevation" in request.form:
        logger.info("Pointing button triggered")
        # Get AZ and EL from GUI.
        az = request.form["azimuth"]
        el = request.form["elevation"]
        # Call a method to point to Desired AZ & EL
        try:
            cm.point_to_coordinates(
                float(time.time()), float(az), float(el)
            )

        except (Exception, ValueError) as err:
            logger.error(f"Error encountered : {err}")

        global thread
        with thread_lock:
            if thread is None:
                thread = socketio.start_background_task(
                    background_thread, cm.antenna_node
                )

    if "sources" in request.form and request.form["sources"] == "sun":
        logger.info("Tracking button triggered")
        global thread2
        with thread_lock:
            if thread is None:
                thread2 = socketio.start_background_task(
                    background_thread, cm.antenna_node
                )

        cm.track_sun(1)
    if "modes" in request.form and request.form["modes"] == "Idle":
        cm.set_idle_mode()
    if "modes" in request.form and request.form["modes"] == "Stow":
        cm.set_stow_mode()
    if "modes" in request.form and request.form["modes"] == "Point":
        cm.set_point_mode()
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
                background_thread, cm.antenna_node
            )


"""
Decorator for disconnect.
"""


def disconnect():
    print("Client disconnected", request.sid)


if __name__ == "__main__":
    print("App started")
    socketio.run(app)
