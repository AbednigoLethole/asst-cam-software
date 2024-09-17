# pylint: disable= W0603, W0718, W0602, E0401
# mypy: disable_error_code="import-untyped"

"""Facilitate integration between the GUI and system components."""
import logging
import time
from datetime import datetime
from threading import Lock

from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO

from component_managers.astt_comp_manager import ASTTComponentManager

THREAD = None
THREAD_LOCK = Lock()
THREAD2 = None
THREAD3 = None

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


@app.route("/", methods=["GET"])
def index():
    """Render the index page."""
    return render_template("index.html")


@app.route("/", methods=["POST"])
def start_astt_gui():
    """Handle user interactions with the GUI."""  # noqa: E501
    # You want to stop tracking as soon as you press any other button.
    cm.trackstop = True
    # Trigger condition when Initialize button is clicked.
    if "button" in request.form and request.form["button"] == "Initialize":
        try:
            cm.clear_all_logs()
            # Start up VCAN network and simulator
            connect_vcan_network()
            # Subscribe to change events.
            start_subscriptions()
            cm.trigger_transmission()
            global THREAD3
            start_states_and_modes_thread(THREAD3, cm)
            return jsonify("success")

        except Exception as err:
            logger.error("Error encountered initializing : %s", err)
            return jsonify("failed")

    # Trigger condition when Point button is clicked.
    if "azimuth" in request.form and "elevation" in request.form:
        logger.info("Pointing button triggered")
        # Get AZ and EL from GUI.
        az = request.form["azimuth"]
        el = request.form["elevation"]
        # Call a method to point to Desired AZ & EL
        try:
            cm.point_to_coordinates(float(time.time()), float(az), float(el))
            cm.point_to_coordinates(float(time.time()) + 5, float(az), float(el))

        except (Exception, ValueError) as err:
            logger.error("Error encountered : %s", err)

        global THREAD
        start_thread(THREAD, cm.antenna_node)

    if "sources" in request.form and request.form["sources"] == "sun":
        logger.info("Tracking button triggered")
        global THREAD2
        az_speed = request.form.get("az_speed")
        el_speed = request.form.get("el_speed")
        start_thread(THREAD2, cm.antenna_node)

        cm.trackstop = False
        if az_speed and el_speed:
            cm.track_sun(
                duration_time=1,
                az_speed=float(az_speed),
                el_speed=float(el_speed),
            )
        else:
            cm.track_sun(duration_time=1)

    if "modes" in request.form and request.form["modes"] == "Idle":
        cm.set_idle_mode()
    if "modes" in request.form and request.form["modes"] == "Stow":
        cm.set_stow_mode()
    if "modes" in request.form and request.form["modes"] == "Point":
        cm.set_point_mode()
    else:
        pass

    return render_template("index.html")


def connect_vcan_network():
    """Connection to the vcan and simulator."""
    cm.connect_to_network()
    cm.connect_to_plc_node()


def start_subscriptions():
    """Initializing subscriptions from the simulator."""
    cm.subscribe_to_timestamp()
    cm.subscribe_to_az_change()
    cm.subscribe_to_el_change()
    cm.subscribe_to_func_state_and_mode()
    cm.subscribe_to_mode_command_obj()
    cm.subscribe_to_stow_sensor()


def start_thread(thread, antenna_node):
    """Generic function for starting specific thread."""
    with THREAD_LOCK:
        if thread is None:
            thread = socketio.start_background_task(background_thread, antenna_node)


def start_states_and_modes_thread(thread, comp_manager):
    """Generic function for starting states and modes thread."""
    with THREAD_LOCK:
        if thread is None:
            thread = socketio.start_background_task(states_and_modes_thread, comp_manager)


def connect():
    """Decorator for socketio connection."""
    global THREAD

    print("Client connected")

    global THREAD
    with THREAD_LOCK:
        if THREAD is None:
            THREAD = socketio.start_background_task(background_thread, cm.antenna_node)


def disconnect():
    """Decorator for disconnect."""
    print("Client disconnected", request.sid)


def get_current_datetime():
    """Return the current date and time."""
    now = datetime.now()
    return now.strftime("%m/%d/%Y %H:%M:%S")


def background_thread(node):
    """Feed az & el to the GUI."""
    if node is not None:
        while True:
            node.tpdo[1].wait_for_reception()
            node.tpdo[2].wait_for_reception()
            az = node.tpdo["Position Feedback.Azimuth(R64) of position"].raw
            el = node.tpdo["Position Feedback.Elevation(R64) of position"].raw
            socketio.emit(
                "updateAZELData",
                {"az": az, "el": el, "date": get_current_datetime()},
            )
            socketio.sleep(1)


def states_and_modes_thread(comp_manager):
    """Continuously send antenna states and modes to the GUI."""
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


if __name__ == "__main__":
    print("App started")
    socketio.run(app, allow_unsafe_werkzeug=True)
