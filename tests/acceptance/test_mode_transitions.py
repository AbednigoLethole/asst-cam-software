"""Test the mode transitions"""

import time

from component_managers.astt_comp_manager import FuncState, Mode, StowPinState


def set_up_subscriptions(comp_manager):
    """Set up all Canopen subscriptions"""
    comp_manager.set_plc_node_to_preoperational()
    comp_manager.subscribe_to_antenna_mode()
    comp_manager.subscribe_to_stow_sensor()
    comp_manager.subscribe_to_func_state()
    comp_manager.subscribe_to_mode_command_obj()
    comp_manager.trigger_transmission()
    time.sleep(7)


def test_antenna_trans_to_point(cm_manager_connected_to_antnn):
    """Test point function"""
    set_up_subscriptions(cm_manager_connected_to_antnn)
    cm_manager_connected_to_antnn.set_point_mode()
    # The antenna takes roughly 30 sec to switch modes
    time.sleep(33)
    assert cm_manager_connected_to_antnn.get_antenna_mode() == Mode.POINT
    assert cm_manager_connected_to_antnn.get_antenna_func_state() == FuncState.MOVING
    assert (
        cm_manager_connected_to_antnn.get_antenna_stow_sensor_state()
        == StowPinState.NOT_ENGAGED_RELEASED_STOW_WINDOW
    )


def test_antenna_trans_to_stow(cm_manager_connected_to_antnn):
    """Test the stow function"""
    cm_manager_connected_to_antnn.set_stow_mode()
    # The antenna takes roughly 30 sec to switch modes
    time.sleep(33)
    assert cm_manager_connected_to_antnn.get_antenna_mode() == Mode.STOW
    assert cm_manager_connected_to_antnn.get_antenna_func_state() == FuncState.BRAKED
    assert (
        cm_manager_connected_to_antnn.get_antenna_stow_sensor_state()
        == StowPinState.ENGAGED_NOT_RELEASED_STOW_WINDOW
    )


def test_antenna_trans_to_idle(cm_manager_connected_to_antnn):
    """Test the idle function"""
    cm_manager_connected_to_antnn.set_idle_mode()
    # The antenna takes roughly 30 sec to switch modes
    time.sleep(33)
    assert cm_manager_connected_to_antnn.get_antenna_mode() == Mode.IDLE
    assert cm_manager_connected_to_antnn.get_antenna_func_state() == FuncState.BRAKED
    assert (
        cm_manager_connected_to_antnn.get_antenna_stow_sensor_state()
        == StowPinState.ENGAGED_NOT_RELEASED_STOW_WINDOW
    )
