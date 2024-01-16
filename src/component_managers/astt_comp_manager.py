import datetime
import os
import time

import canopen

from threading_lrc import background

from .sources import Sun


class ASTTComponentManager:
    def __init__(self):
        """Init method for the CM ."""
        self.dishmode = None
        self.antenna_node = None
        self.antenna_app_state = None
        self.antenna_func_state = None
        self.network0 = canopen.Network()
        self.transmission_triggered = False

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
        self.antenna_node = node2

    def set_plc_node_to_operational(self):
        """Changes all the nodes state to OPERATIONAL."""
        (self.antenna_node).nmt.state = "OPERATIONAL"

    def set_plc_node_to_preoperational(self):
        """Changes all the nodes state to PRE-OPERATIONAL."""
        (self.antenna_node).nmt.state = "PRE-OPERATIONAL"

    def get_plc_state(self):
        """Returns node state."""
        return (self.antenna_node).nmt.state

    def point_to_coordinates(self, timestamp, az, el):
        """commands the simulator to point az/el ."""
        (self.antenna_node).sdo[0x2000][1].raw = timestamp + 2
        (self.antenna_node).sdo[0x2000][2].raw = az
        (self.antenna_node).sdo[0x2000][3].raw = el

    def az_el_change_callback(self, incoming_object):
        """Transmit PDO callback ."""
        for node_record in incoming_object:
            if (
                node_record.name
                == "Position Feedback.Azimuth(R64) of position"
            ):
                print(f"Antenna Azumuth : {node_record.raw} ")

            if (
                node_record.name
                == "Position Feedback.Elevation(R64) of position"
            ):
                print(f"Antenna Elevation : {node_record.raw} ")

    def subscribe_to_az_change(self):
        """CanOpen Subscription to the Azimuth ."""
        (self.antenna_node).tpdo.read()
        # Mapping the Azimuth to tpdo
        (self.antenna_node).tpdo[1].clear()
        # (self.antenna_node).tpdo[1].add_variable(0x2001,2)
        (self.antenna_node).tpdo[1].add_variable(
            "Position Feedback", "Azimuth(R64) of position"
        )
        (self.antenna_node).tpdo[1].trans_type = 1
        (self.antenna_node).tpdo[1].event_timer = 0
        (self.antenna_node).tpdo[1].enabled = True

        (self.antenna_node).nmt.state = "PRE-OPERATIONAL"
        print((self.antenna_node).nmt.state)
        (self.antenna_node).tpdo.save()

        (self.antenna_node).tpdo[1].add_callback(
            self.az_el_change_callback
        )

    def subscribe_to_el_change(self):
        """CanOpen Subscription to the Elevation ."""
        (self.antenna_node).tpdo[2].read()
        # Mapping the Elevation to tpdo
        (self.antenna_node).tpdo[2].clear()
        (self.antenna_node).tpdo[2].add_variable(0x2001, 3)
        (self.antenna_node).tpdo[2].trans_type = 1
        (self.antenna_node).tpdo[2].event_timer = 0
        (self.antenna_node).tpdo[2].enabled = True

        (self.antenna_node).nmt.state = "PRE-OPERATIONAL"
        print((self.antenna_node).nmt.state)
        (self.antenna_node).tpdo.save()

        (self.antenna_node).tpdo[2].add_callback(
            self.az_el_change_callback
        )

    def func_state_callback(self, incoming_object):
        """Transmit PDO callback ."""
        for node_record in incoming_object:
            print(f"func state : {node_record.raw} ")

    def subscribe_to_func_state(self):
        """CanOpen Subscription to the functional state ."""
        (self.antenna_node).tpdo[3].read()
        # Mapping the functional state to tpdo
        (self.antenna_node).tpdo[3].clear()
        (self.antenna_node).tpdo[3].add_variable(
            "Mode and State Feedback", "Functional State"
        )
        (self.antenna_node).tpdo[3].trans_type = 254
        (self.antenna_node).tpdo[3].event_timer = 3
        (self.antenna_node).tpdo[3].enabled = True

        (self.antenna_node).nmt.state = "PRE-OPERATIONAL"
        print((self.antenna_node).nmt.state)
        (self.antenna_node).tpdo.save()
        (self.antenna_node).tpdo[3].add_callback(
            self.func_state_callback
        )

    def stow_pin_callback(self, incoming_object):
        for node_record in incoming_object:
            print(f"stow pin state : {node_record.raw} ")

    def subscribe_to_stow_sensor(self):
        """CanOpen Subscription to stow sensors."""
        (self.antenna_node).tpdo[4].read()
        # Mapping the stow sensors to tpdo
        (self.antenna_node).tpdo[4].clear()
        (self.antenna_node).tpdo[4].add_variable(
            "Sensor Feedback", "Stow sensors"
        )
        (self.antenna_node).tpdo[4].trans_type = 254
        (self.antenna_node).tpdo[4].event_timer = 3
        (self.antenna_node).tpdo[4].enabled = True

        (self.antenna_node).nmt.state = "PRE-OPERATIONAL"
        print((self.antenna_node).nmt.state)
        (self.antenna_node).tpdo.save()

        (self.antenna_node).tpdo[4].add_callback(
            self.stow_pin_callback
        )

    def subscribe_to_mode_command_obj(self):
        """CanOpen Subscription to the mode command obj ."""
        (self.antenna_node).rpdo.read()
        # Mapping the mode command obj to rpdo
        (self.antenna_node).rpdo[1].clear()
        (self.antenna_node).rpdo[1].add_variable(
            "Mode command", "Mode"
        )
        (self.antenna_node).rpdo[1].enabled = True
        (self.antenna_node).nmt.state = "PRE-OPERATIONAL"
        print((self.antenna_node).nmt.state)
        (self.antenna_node).rpdo.save()
        (self.antenna_node).rpdo[1].start(0.1)

    def set_point_mode(self):
        """Commands the ASTT Antenna to point mode"""
        (self.antenna_node).rpdo[1]["Mode command.Mode"].raw = 1

    def set_idle_mode(self):
        """Commands the ASTT Antenna to idle mode"""
        (self.antenna_node).rpdo[1]["Mode command.Mode"].raw = 0

    def set_stow_mode(self):
        """Commands the ASTT Antenna to stow mode"""
        (self.antenna_node).rpdo[1]["Mode command.Mode"].raw = 2

    def trigger_transmission(self):
        """Triggers the transmission of Az/El ."""
        self.transmission_triggered = True
        (self.antenna_node).nmt.state = "OPERATIONAL"
        (self.network0).sync.start(0.5)
        # while True:
        #    time.sleep(1)

    def antenna_mode(self):
        """Returns the antenna mode"""
        return (self.antenna_node).sdo["Mode command"]["Mode"].raw

    @background
    def track_sun(self, duration_time):
        # Converting the duretion time to seconds
        time_conversion = duration_time * 3600
        count = 1
        sun = Sun(-33.9326033333, 18.47222, 3.6)
        while count < time_conversion:
            track_time = datetime.datetime.now(
                datetime.timezone.utc
            ) + datetime.timedelta(seconds=10)
            az, el = sun.get_sun_az_el(track_time)
            ts = (
                track_time
                - datetime.datetime(
                    1970, 1, 1, tzinfo=datetime.timezone.utc
                )
            ).total_seconds()
            self.point_to_coordinates(ts, az=az, el=el)
            if not self.transmission_triggered:
                self.trigger_transmission()
            else:
                pass
            time.sleep(5)
            print("---------------------------------------")
            print("Sun_Az :", str(az), "Sun_El :", str(el))
            print("---------------------------------------")
            count += 1

    def track_sun_update(self):
        pass


if __name__ == "__main__":
    """Run the CM."""
    cm = ASTTComponentManager()
    cm.connect_to_network()
    cm.connect_to_plc_node()
    cm.subscribe_to_app_state()
    cm.subscribe_to_az_change()
    cm.subscribe_to_el_change()
    cm.trigger_transmission()
    cm.track_sun(1)
