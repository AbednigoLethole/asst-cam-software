import time

from flask import Flask, render_template, request

from component_managers.astt_comp_manager import ASTTComponentManager
from component_managers.start_simulator import SimulatorManager

app = Flask(__name__)
cm = ASTTComponentManager()


@app.route("/", methods=["GET"])
def index():
    # Start the  component manager simultaneusly with the gui
    return render_template("index.html")

@app.route("/", methods=["POST"])
def start_astt_gui():
    az = request.form["azimuth"]
    el = request.form["elevation"]
    cm.point_to_coordinates(
        node2, int(time.time()), float(az), float(el)
    )
    cm.trigger_transmission(node2)
    return render_template("index.html")


if __name__ == "__main__":
    simulator_manager = SimulatorManager()
    simulator_manager.start_can_interface()
    simulator_manager.run_contaier_and_startup_simulator()
    cm.connect_to_network()
    node2 = cm.connect_to_plc_node()
    cm.subscribe_to_az_change(node2)
    cm.subscribe_to_el_change(node2)
    app.run()
