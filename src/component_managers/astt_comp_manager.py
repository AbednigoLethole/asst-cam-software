import datetime
import os
import time

import canopen
from sources import Sun


class ASTTComponentManager:
    def __init__(self):
        """Init method for the CM ."""
        self.dishmode = None
        self.network0 = canopen.Network()

    def connect_to_network(self):
        """Connects to the CAN0 ."""
        (self.network0).connect(channel="can0", bustype="socketcan")

    def connect_to_plc_node(self):
        """Connect to the C++  antenna simulator."""
        curr_dir = os.getcwd()
        eds_rel_path = "src/component_managers/cpp-slave.eds"
        eds_full_path = os.path.join(curr_dir, eds_rel_path)

        node2 = canopen.RemoteNode(
            2,
            eds_full_path,
        )
        (self.network0).add_node(node2)
        return node2

    def set_plc_node_to_operational(self, node):
        """Changes all the nodes state to OPERATIONAL."""
        node.nmt.state = "OPERATIONAL"

    def set_plc_node_to_preoperational(self, node):
        """Changes all the nodes state to PRE-OPERATIONAL."""
        node.nmt.state = "PRE-OPERATIONAL"

    def get_plc_state(self, node):
        """Returns node state."""
        return node.nmt.state

    def point_to_coordinates(self, node, timestamp, az, el):
        """commands the simulator to point az/el ."""
        node.sdo[0x2000][1].raw = timestamp + 2
        node.sdo[0x2000][2].raw = az
        node.sdo[0x2000][3].raw = el

    def az_el_change_callback(self, incoming_object):
        """Transmit PDO callback ."""
        for node_record in incoming_object:
            if (
                node_record.name
                == "Position Feedback.Azimuth(R64) of position"
            ):
                print(f"current Azumuth : {node_record.raw} ")

            if (
                node_record.name
                == "Position Feedback.Elevation(R64) of position"
            ):
                print(f"current Elevation : {node_record.raw} ")

    def subscribe_to_az_change(self, node):
        """CanOpen Subscription to the Azimuth ."""
        node.tpdo.read()
        # Mapping the Azimuth to tpdo
        node.tpdo[1].clear()
        # node.tpdo[1].add_variable(0x2001,2)
        node.tpdo[1].add_variable(
            "Position Feedback", "Azimuth(R64) of position"
        )
        node.tpdo[1].trans_type = 1
        node.tpdo[1].event_timer = 0
        node.tpdo[1].enabled = True

        node.nmt.state = "PRE-OPERATIONAL"
        print(node.nmt.state)
        node.tpdo.save()

        node.tpdo[1].add_callback(self.az_el_change_callback)

    def subscribe_to_el_change(self, node):
        """CanOpen Subscription to the Elevation ."""
        node.tpdo[2].read()
        # Mapping the Elevation to tpdo
        node.tpdo[2].clear()
        node.tpdo[2].add_variable(0x2001, 3)
        node.tpdo[2].trans_type = 1
        node.tpdo[2].event_timer = 0
        node.tpdo[2].enabled = True

        node.nmt.state = "PRE-OPERATIONAL"
        print(node.nmt.state)
        node.tpdo.save()

        node.tpdo[2].add_callback(self.az_el_change_callback)

    def trigger_transmission(self, node):
        """Triggers the transmission of Az/El ."""
        node.nmt.state = "OPERATIONAL"
        (self.network0).sync.start(0.5)
        # while True:
        #    time.sleep(1)

    def track_sun(self, node, duration_time):
        # Converting the duretion time to seconds
        time_conversion = duration_time * 3600
        count = 1
        sun = Sun(-33.9326033333, 18.47222, 3.6)
        while count < time_conversion:
            track_time = datetime.datetime.now(
                datetime.timezone.utc
            ) + datetime.timedelta(seconds=2)
            az, el = sun.get_sun_az_el(track_time)
            ts = (
                track_time
                - datetime.datetime(
                    1970, 1, 1, tzinfo=datetime.timezone.utc
                )
            ).total_seconds()
            self.point_to_coordinates(node, ts, az=az, el=el)
            time.sleep(5)
            count += 1


if __name__ == "__main__":
    """Run the CM."""
    cm = ASTTComponentManager()
    cm.connect_to_network()
    node2 = cm.connect_to_plc_node()
    cm.subscribe_to_az_change(node2)
    cm.subscribe_to_el_change(node2)
    cm.trigger_transmission(node2)
    cm.track_sun(node2, 1)
