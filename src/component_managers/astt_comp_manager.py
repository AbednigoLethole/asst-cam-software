import datetime
import logging
import os
import time

import canopen

from threading_lrc import background

from .dish_modes import FuncState, Mode, StowPinState
from .sources import Sun


class ASTTComponentManager:
    def __init__(self):
        """Init method for the CM ."""
        self.antenna_node = None
        self.antenna_app_state = None
        self.antenna_func_state = FuncState.UNKNOWN
        self.antenna_mode = Mode.UNKNOWN
        self.stow_sensor_state = StowPinState.UNKNOWN
        self.network0 = canopen.Network()
        self.transmission_triggered = False
        self.logger = logging.getLogger("ASTT-COMP-MANAGER")
        logging.basicConfig(
            filename="app_dev.log",
            format="%(asctime)s|%(levelname)s|%(name)s|%(message)s",
            level=logging.INFO,
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    # =====================
    # Connection functions
    # =====================

    def connect_to_network(self):
        """Connects to the CAN0 ."""
        self.logger.debug("Starting VCAN Network")
        (self.network0).connect(channel="can0", bustype="socketcan")

    def connect_to_plc_node(self):
        """Connect to the C++  antenna simulator."""
        self.logger.debug("Connecting to PLC node")
        curr_dir = os.getcwd()
        eds_rel_path = "src/component_managers/cpp-slave.eds"
        eds_full_path = os.path.join(curr_dir, eds_rel_path)

        node2 = canopen.RemoteNode(
            2,
            eds_full_path,
        )
        (self.network0).add_node(node2)
        self.antenna_node = node2
        self.logger.info("Connected to PLC node")

    # ========================
    # Callbacks
    # ========================

    def az_el_change_callback(self, incoming_object):
        """Transmit PDO callback ."""
        for node_record in incoming_object:
            if (
                node_record.name
                == "Position Feedback.Azimuth(R64) of position"
            ):
                (self.logger).info(f"AZ = {node_record.raw}")

            if (
                node_record.name
                == "Position Feedback.Elevation(R64) of position"
            ):
                (self.logger).info(f"EL = {node_record.raw}")

    # This is helper function to translate int values
    # To enum values
    def gen_mode_state_enums(self, name_of_enum, value):
        """Generate enum values for transmitted values"""
        if name_of_enum == "Mode":
            return Mode(value)
        if name_of_enum == "FuncState":
            return FuncState(value)
        if name_of_enum == "StowPinState":
            return StowPinState(value)

    def stow_pin_callback(self, incoming_object):
        for node_record in incoming_object:
            st_pin_state = self.gen_mode_state_enums(
                "StowPinState", node_record.raw
            )
            # Update if the value from simulator has changed
            if st_pin_state != self.stow_sensor_state:
                self.stow_sensor_state = st_pin_state
                print(f"stow pin state : {st_pin_state.name} ")

    def antenna_mode_callback(self, incoming_object):
        for node_record in incoming_object:
            ant_mode = self.gen_mode_state_enums(
                "Mode", node_record.raw
            )
            # Update if the value from simulator has changed
            if ant_mode != self.antenna_mode:
                self.antenna_mode = ant_mode
                print(f"antenna mode : {ant_mode.name} ")

    def func_state_callback(self, incoming_object):
        """Transmit PDO callback ."""
        for node_record in incoming_object:
            func_state = self.gen_mode_state_enums(
                "FuncState", node_record.raw
            )
            # Update if the value from simulator has changed
            if func_state != self.antenna_func_state:
                self.antenna_func_state = func_state
                print(f"func state : {func_state.name} ")

    # ========================
    # Subscription functions
    # ========================

    def subscribe_to_az_change(self):
        """CanOpen Subscription to the Azimuth ."""
        self.logger.info("Subscribing to azimuth ")
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
        (self.antenna_node).tpdo[1].save()

        (self.antenna_node).tpdo[1].add_callback(
            self.az_el_change_callback
        )
        self.logger.info("Subscribed to azimuth")

    def subscribe_to_el_change(self):
        """CanOpen Subscription to the Elevation ."""
        self.logger.info("Subscribing to elevation ")
        (self.antenna_node).tpdo[2].read()
        # Mapping the Elevation to tpdo
        (self.antenna_node).tpdo[2].clear()
        (self.antenna_node).tpdo[2].add_variable(0x2001, 3)
        (self.antenna_node).tpdo[2].trans_type = 1
        (self.antenna_node).tpdo[2].event_timer = 0
        (self.antenna_node).tpdo[2].enabled = True

        (self.antenna_node).nmt.state = "PRE-OPERATIONAL"
        print((self.antenna_node).nmt.state)
        (self.antenna_node).tpdo[2].save()

        (self.antenna_node).tpdo[2].add_callback(
            self.az_el_change_callback
        )
        self.logger.info("Subscribed to elevation")

    def subscribe_to_func_state(self):
        """CanOpen Subscription to the functional state ."""
        self.logger.info("Subscribing to functional state")
        (self.antenna_node).tpdo[3].read()
        # Mapping the functional state to tpdo
        (self.antenna_node).tpdo[3].clear()
        (self.antenna_node).tpdo[3].add_variable(
            "Mode and State Feedback", "Functional State"
        )
        (self.antenna_node).tpdo[3].trans_type = 254
        (self.antenna_node).tpdo[3].event_timer = 5
        (self.antenna_node).tpdo[3].enabled = True

        (self.antenna_node).nmt.state = "PRE-OPERATIONAL"
        print((self.antenna_node).nmt.state)
        (self.antenna_node).tpdo[3].save()
        (self.antenna_node).tpdo[3].add_callback(
            self.func_state_callback
        )
        self.logger.info("Subscribed to functional state")

    def subscribe_to_stow_sensor(self):
        """CanOpen Subscription to stow sensors."""
        self.logger.info("Subscribing to stow sensor ")
        (self.antenna_node).tpdo[4].read()
        # Mapping the stow sensors to tpdo
        (self.antenna_node).tpdo[4].clear()
        (self.antenna_node).tpdo[4].add_variable(
            "Sensor Feedback", "Stow sensors"
        )
        (self.antenna_node).tpdo[4].trans_type = 254
        (self.antenna_node).tpdo[4].event_timer = 5
        (self.antenna_node).tpdo[4].enabled = True

        (self.antenna_node).nmt.state = "PRE-OPERATIONAL"
        print((self.antenna_node).nmt.state)
        (self.antenna_node).tpdo[4].save()

        (self.antenna_node).tpdo[4].add_callback(
            self.stow_pin_callback
        )
        self.logger.info("Subscribed to stow sensor")

    def subscribe_to_antenna_mode(self):
        """CanOpen Subscription to antenna mode."""
        self.logger.info("Subscribing to antenna mode ")
        (self.antenna_node).tpdo[6].read()
        # Mapping the stow sensors to tpdo
        (self.antenna_node).tpdo[6].clear()
        (self.antenna_node).tpdo[6].add_variable(
            "Mode and State Feedback", "Mode"
        )
        (self.antenna_node).tpdo[6].trans_type = 254
        (self.antenna_node).tpdo[6].event_timer = 5
        (self.antenna_node).tpdo[6].enabled = True

        (self.antenna_node).nmt.state = "PRE-OPERATIONAL"
        print((self.antenna_node).nmt.state)
        (self.antenna_node).tpdo[6].save()

        (self.antenna_node).tpdo[6].add_callback(
            self.antenna_mode_callback
        )
        self.logger.info("Subscribed to antenna mode")

    def subscribe_to_mode_command_obj(self):
        """CanOpen Subscription to the mode command obj ."""
        self.logger.info("Subscribing to mode command obj")
        (self.antenna_node).rpdo.read()
        # Mapping the mode command obj to rpdo
        (self.antenna_node).rpdo[1].clear()
        (self.antenna_node).rpdo[1].add_variable(
            "Mode command", "Mode"
        )
        (self.antenna_node).rpdo[1].enabled = True
        (self.antenna_node).nmt.state = "PRE-OPERATIONAL"
        print((self.antenna_node).nmt.state)
        (self.antenna_node).rpdo[1].save()
        (self.antenna_node).rpdo[1].start(0.1)
        self.logger.info("Subscribed to mode command obj")

    # ========================
    # Commands
    # ========================

    def set_plc_node_to_operational(self):
        """Changes all the nodes state to OPERATIONAL."""
        (self.antenna_node).nmt.state = "OPERATIONAL"

    def set_plc_node_to_preoperational(self):
        """Changes all the nodes state to PRE-OPERATIONAL."""
        (self.antenna_node).nmt.state = "PRE-OPERATIONAL"

    def get_plc_state(self):
        """Returns node state."""
        self.logger.info("Reading plc state")
        return (self.antenna_node).nmt.state

    def is_az_allowed(self, az):
        """Allows Azimuth of [-127,127]"""
        return True if (az >= -127.0 and az <= 127.0) else False

    def is_el_allowed(self, el):
        """Allows elevation of [-15,92]"""
        return True if (el >= -15.0 and el <= 92.0) else False

    def point_to_coordinates(self, timestamp, az, el):
        """commands the simulator to point az/el ."""
        self.logger.info(f"Point called with AZ {az} and EL {el} ")
        if self.is_az_allowed(az) and self.is_el_allowed(el):
            (self.antenna_node).sdo[0x2000][1].raw = timestamp + 2.0
            (self.antenna_node).sdo[0x2000][2].raw = az
            (self.antenna_node).sdo[0x2000][3].raw = el
        else:
            self.logger.exception(
                f"az: {az} or el: {el} is out of range"
            )
            raise ValueError

    def set_point_mode(self):
        """Commands the ASTT Antenna to point mode"""
        self.logger.info("Set point mode called!!")
        (self.antenna_node).rpdo[1]["Mode command.Mode"].raw = 1

    def set_idle_mode(self):
        """Commands the ASTT Antenna to idle mode"""
        self.logger.info("Set idle mode called!!")
        (self.antenna_node).rpdo[1]["Mode command.Mode"].raw = 0

    def set_stow_mode(self):
        """Commands the ASTT Antenna to stow mode"""
        self.logger.info("Set stow mode called!!")
        (self.antenna_node).rpdo[1]["Mode command.Mode"].raw = 2

    def trigger_transmission(self):
        """Triggers the transmission of Az/El ."""
        self.logger.info("Transmission is triggered")
        self.transmission_triggered = True
        (self.antenna_node).nmt.state = "OPERATIONAL"
        (self.network0).sync.start(0.5)

    def stop_az_el_transmission(self):
        for tpdo_id in range(1, 3):
            (self.antenna_mode).tpdo[tpdo_id].stop()

    def get_antenna_mode(self):
        """Returns the antenna mode"""
        return self.antenna_mode

    def get_antenna_func_state(self):
        """Returns the antenna functional state"""
        return self.antenna_func_state

    def get_antenna_app_state(self):
        """Returns the antenna application"""
        return self.antenna_app_state

    def get_antenna_stow_sensor_state(self):
        """Returns the antenna stow sensor state"""
        return self.stow_sensor_state

    @background
    def track_sun(self, duration_time):
        # Converting the duretion time to seconds
        self.logger.info("Starting to track the sun")
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
            self.logger.info(
                "---------------------------------------"
            )
            self.logger.info("Sun_Az :", str(az), "Sun_El :", str(el))
            self.logger.info(
                "---------------------------------------"
            )
            count += 1

    def track_sun_update(self):
        pass

    def clear_all_logs(self):
        """Clears all the logs in app_dev.log"""
        try:
            with open("app_dev.log", "w") as file:
                file.truncate(0)
        except FileNotFoundError:
            self.logger.error(
                "File app_dev.log not found. No logs cleared."
            )
        except Exception as err:
            self.logger.error(
                f"Failed to clear logs in , error: {err}"
            )
        file.close()


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
