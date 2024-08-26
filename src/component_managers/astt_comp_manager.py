"""Specialization for CanOpen functionality."""

import datetime
import logging
import os
import time

import canopen

from threading_lrc import background

from .dish_modes import FuncState, Mode, StowPinState
from .sources import Sun




class InitialPosition:
    """Initial position for timestamp, azimuth, and elevation."""

    def __init__(self, timestamp, azimuth, elevation):
        """Init method for initial position."""
        self.azimuth = azimuth
        self.elevation = elevation
        self.timestamp = timestamp


class CANOpenConnection:

    def __init__(self):
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
        """Connect to the CAN0."""
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



class SubscriptionManager:
    # ========================
    # Subscription functions
    # ========================
    def __init__(self):
        self.antenna_node = None

    def subscribe_to_az_change(self):
        """Canopen Subscription to the Azimuth."""
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
            self.position_change_callback
        )
        self.logger.info("Subscribed to azimuth")

    def subscribe_to_el_change(self):
        """Canopen Subscription to the Elevation."""
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
            self.position_change_callback
        )
        self.logger.info("Subscribed to elevation")

    def subscribe_to_timestamp(self):
        """Canopen Subscription to the Timestamp."""
        self.logger.info("Subscribing to timestamp ")
        (self.antenna_node).tpdo[6].read()
        # Mapping the Timestamp to tpdo
        (self.antenna_node).tpdo[6].clear()
        (self.antenna_node).tpdo[6].add_variable(0x2001, 1)
        (self.antenna_node).tpdo[6].trans_type = 1
        (self.antenna_node).tpdo[6].event_timer = 0
        (self.antenna_node).tpdo[6].enabled = True

        (self.antenna_node).nmt.state = "PRE-OPERATIONAL"
        print((self.antenna_node).nmt.state)
        (self.antenna_node).tpdo[6].save()

        (self.antenna_node).tpdo[6].add_callback(
            self.position_change_callback
        )
        self.logger.info("Subscribed to timestamp")

    def subscribe_to_func_state_and_mode(self):
        """Canopen Subscription to the functional state and mode."""
        self.logger.info("Subscribing to functional state and mode")
        (self.antenna_node).tpdo[3].read()
        # Mapping the functional state to tpdo
        (self.antenna_node).tpdo[3].clear()
        (self.antenna_node).tpdo[3].add_variable(
            "Mode and State Feedback", "Functional State"
        )
        (self.antenna_node).tpdo[3].add_variable(
            "Mode and State Feedback", "Mode"
        )
        (self.antenna_node).tpdo[3].trans_type = 254
        (self.antenna_node).tpdo[3].event_timer = 5
        (self.antenna_node).tpdo[3].enabled = True

        (self.antenna_node).nmt.state = "PRE-OPERATIONAL"
        print((self.antenna_node).nmt.state)
        (self.antenna_node).tpdo[3].save()
        (self.antenna_node).tpdo[3].add_callback(
            self.state_mode_callback
        )
        self.logger.info("Subscribed to functional state and mode")

    def subscribe_to_stow_sensor(self):
        """Canopen Subscription to stow sensors."""
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

    def subscribe_to_mode_command_obj(self):
        """Canopen Subscription to the mode command obj ."""
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

  

class ASTTComponentManager:
    def __init__(self):
        """Init method for the CM."""
        # self.antenna_node = None
        self.trackstop = True
        self.antenna_app_state = None
        self.antenna_func_state = FuncState.UNKNOWN
        self.antenna_mode = Mode.UNKNOWN
        self.stow_sensor_state = StowPinState.UNKNOWN
        self.network0 = canopen.Network()
        self.transmission_triggered = False
        self.current_position = InitialPosition(
            timestamp=0.0, azimuth=0.0, elevation=0.0
        )
        
   

    # ========================
    # Callbacks
    # ========================

    def position_change_callback(self, incoming_object):
        """Transmit PDO callback ."""
        dt = datetime.datetime.now(datetime.timezone.utc)
        current_timestamp = datetime.datetime.timestamp(dt)
        print(
            f"[{current_timestamp}] Message {incoming_object.name} received:"  # noqa: E501
        )
        for node_record in incoming_object:
            if (
                node_record.name
                == "Position Feedback.Timestamp(R64) of position"
            ):
                timestamp = node_record.raw
                self.current_position.timestamp = timestamp
            if (
                node_record.name
                == "Position Feedback.Azimuth(R64) of position"
            ):
                azimuth = node_record.raw
                self.current_position.azimuth = azimuth

            if (
                node_record.name
                == "Position Feedback.Elevation(R64) of position"
            ):
                elevation = node_record.raw
                self.current_position.elevation = elevation
                print(
                    f" Timestamp: {self.current_position.timestamp}, Azimuth {self.current_position.azimuth}, Elevation {self.current_position.elevation}"  # noqa: E501
                )

    def store_initial_position(self):
        """Return starting position's of timestamp, azi, and ele."""
        start_position = (
            self.current_position.timestamp,
            self.current_position.azimuth,
            self.current_position.elevation,
        )
        return start_position

    # This is helper function to translate int values
    # To enum values
    def gen_mode_state_enums(self, name_of_enum, value):
        """Generate enum values for transmitted values."""
        generated_enum = None
        state_mode_calls = {
            "Mode": Mode,
            "FuncState": FuncState,
            "StowPinState": StowPinState,
        }
        if name_of_enum in state_mode_calls:
            try:
                generated_enum = state_mode_calls[name_of_enum](value)
            except Exception as err:
                self.logger.exception(
                    f"could not generate mode or state, {err}"
                )
        return generated_enum

    def stow_pin_callback(self, incoming_object):
        for node_record in incoming_object:
            st_pin_state = self.gen_mode_state_enums(
                "StowPinState", node_record.raw & 0b111
            )
            # Update if the value from simulator has changed
            if st_pin_state != self.stow_sensor_state:
                self.stow_sensor_state = st_pin_state
                print(f"stow pin state : {st_pin_state.name} ")

    def state_mode_callback(self, incoming_object):
        for node_record in incoming_object:
            if "Mode and State Feedback.Mode" == node_record.name:
                ant_mode = self.gen_mode_state_enums(
                    "Mode", node_record.raw
                )
                # Update if the value from simulator has changed
                if ant_mode != self.antenna_mode:
                    self.antenna_mode = ant_mode
                    print(f"antenna mode : {ant_mode.name} ")

            elif (
                "Mode and State Feedback.Functional State"
                == node_record.name
            ):
                func_state = self.gen_mode_state_enums(
                    "FuncState", node_record.raw
                )
                # Update if the value from simulator has changed
                if func_state != self.antenna_func_state:
                    self.antenna_func_state = func_state
                    print(f"func state : {func_state.name} ")

  # ========================
    # Commands
    # ========================

    def set_plc_node_to_operational(self):
        """Change all the nodes state to OPERATIONAL."""
        (self.antenna_node).nmt.state = "OPERATIONAL"

    def set_plc_node_to_preoperational(self):
        """Change all the nodes state to PRE-OPERATIONAL."""
        (self.antenna_node).nmt.state = "PRE-OPERATIONAL"

    def get_plc_state(self):
        """Return node state."""
        self.logger.info("Reading plc state")
        return (self.antenna_node).nmt.state

    def is_az_allowed(self, az):
        """Allow Azimuth of [-127,127]."""
        return True if (az >= -127.0 and az <= 127.0) else False

    def is_el_allowed(self, el):
        """Allow elevation of [-15,92]."""
        return True if (el >= -15.0 and el <= 92.0) else False

    def point_to_coordinates(self, timestamp, az, el):
        """Commands the simulator to point az/el."""
        self.logger.info(f"Point called with AZ {az} and EL {el} ")
        if self.is_az_allowed(az) and self.is_el_allowed(el):
            (self.antenna_node).sdo[0x2000][1].raw = timestamp
            (self.antenna_node).sdo[0x2000][2].raw = az
            (self.antenna_node).sdo[0x2000][3].raw = el
        else:
            self.logger.exception(
                f"az: {az} or el: {el} is out of range"
            )
            raise ValueError

    def set_point_mode(self):
        """Commands the ASTT Antenna to point mode."""
        self.logger.info("Set point mode called!!")
        (self.antenna_node).rpdo[1]["Mode command.Mode"].raw = 1

    def set_idle_mode(self):
        """Commands the ASTT Antenna to idle mode."""
        self.logger.info("Set idle mode called!!")
        (self.antenna_node).rpdo[1]["Mode command.Mode"].raw = 0

    def set_stow_mode(self):
        """Commands the ASTT Antenna to stow mode."""
        self.logger.info("Set stow mode called!!")
        (self.antenna_node).rpdo[1]["Mode command.Mode"].raw = 2

    def trigger_transmission(self):
        """Triggers the transmission of Az/El."""
        self.logger.info("Transmission is triggered")
        self.transmission_triggered = True
        (self.antenna_node).nmt.state = "OPERATIONAL"
        (self.network0).sync.start(0.5)

    def stop_az_el_transmission(self):
        for tpdo_id in range(1, 3):
            (self.antenna_mode).tpdo[tpdo_id].stop()

    def get_antenna_mode(self):
        """Return the antenna mode."""
        return self.antenna_mode

    def get_antenna_func_state(self):
        """Return the antenna functional state."""
        return self.antenna_func_state

    def get_antenna_app_state(self):
        """Return the antenna application."""
        return self.antenna_app_state

    def get_antenna_stow_sensor_state(self):
        """Return the antenna stow sensor state."""
        return self.stow_sensor_state

    @background
    def track_sun(self, duration_time, az_speed=None, el_speed=None):
        """Calculate Sun's Az and El."""
        # Converting the duration time to seconds
        start_position = self.store_initial_position()
        track_start_position = InitialPosition(
            start_position[0], start_position[1], start_position[2]
        )
        self.logger.info("Starting to track the sun")
        time_conversion = duration_time * 3600
        count = 1
        sun = Sun(-33.9326033333, 18.47222, 3.6)
        # Store all the values from the callback on beginning position
        begin_time = track_start_position.timestamp
        begin_az = track_start_position.azimuth
        begin_el = track_start_position.elevation
        while count < time_conversion and not self.trackstop:
            track_time = datetime.datetime.now(
                datetime.timezone.utc
            ) + datetime.timedelta(seconds=10)
            future_timestamp = datetime.datetime.timestamp(track_time)
            dt = future_timestamp - begin_time
            if az_speed is not None and el_speed is not None:
                az_desired = begin_az + (az_speed * dt)
                el_desired = begin_el + (el_speed * dt)
            else:
                az_desired, el_desired = sun.get_sun_az_el(track_time)
            self.point_to_coordinates(
                future_timestamp, az=az_desired, el=el_desired
            )
            if not self.transmission_triggered:
                self.trigger_transmission()
            else:
                pass
            time.sleep(5)
            self.logger.info(
                "---------------------------------------"
            )
            self.logger.info(
                f"Sun_Az : {az_desired}, Sun_El : {el_desired}"
            )
            self.logger.info(
                "---------------------------------------"
            )
            count += 1

    def track_sun_update(self):
        pass

    def clear_all_logs(self):
        """Clear all the logs in app_dev.log."""
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
    
    # Connections
    nc = CANOpenConnection()
    nc.connect_to_network()
    nc.connect_to_plc_node()

    # Subscriptions
    sub = SubscriptionManager()
    sub.subscribe_to_func_state_and_mode()
    sub.subscribe_to_timestamp()
    sub.subscribe_to_az_change()
    sub.subscribe_to_el_change()

    #triggerings
    cm = ASTTComponentManager()
    cm.trigger_transmission()
    cm.track_sun(1)
