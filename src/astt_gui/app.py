import time
from flask import Flask, render_template, request

from component_managers.astt_comp_manager import ASTTComponentManager

from wtforms import Form, BooleanField, StringField, PasswordField, validators


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def start_astt_gui():
    # Start the  component manager simultaneusly with the gui
    cm = ASTTComponentManager()
    cm.connect_to_network()
    node2 = cm.connect_to_plc_node()
    cm.subscribe_to_az_change(node2)
    cm.subscribe_to_el_change(node2)

    if request.method == "POST":
        az = request.form["azimuth"]
        el = request.form["elevation"]

        cm.point_to_coordinates(node2,int(time.time()),float(az),float(el))
        cm.trigger_transmission(node2)


    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
