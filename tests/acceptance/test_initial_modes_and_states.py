"""Test the initial states and modes."""

# pylint: disable=duplicate-code

import time

from component_managers.astt_comp_manager import (
    FuncState,
    Mode,
    StowPinState,
)


def set_up_subscriptions(comp_manager):
    """Set up all Canopen subscriptions"""
    comp_manager.set_plc_node_to_preoperational()
    comp_manager.subscribe_to_antenna_mode()
    comp_manager.subscribe_to_stow_sensor()
    comp_manager.subscribe_to_func_state()
    comp_manager.trigger_transmission()
    time.sleep(7)


def test_connection_to_sim_is_success(
    cm_manager_connected_to_antnn,
):
    """Testing CAN network communication is successful."""
    assert (cm_manager_connected_to_antnn.antenna_node) is not None


def test_antenna_starts_at_idle_mode(
    cm_manager_connected_to_antnn,
):
    """Test initial mode of the simulator."""
    set_up_subscriptions(cm_manager_connected_to_antnn)
    assert (
        cm_manager_connected_to_antnn.get_antenna_mode() == Mode.IDLE
    )


def test_antenna_starts_at_braked_fuc_state(
    cm_manager_connected_to_antnn,
):
    """Test initial func state of the simulator."""
    assert (
        cm_manager_connected_to_antnn.get_antenna_func_state()
        == FuncState.BRAKED
    )


def test_antenna_starts_at_stow_not_release(
    cm_manager_connected_to_antnn,
):
    """Test initial stow state of the simulator."""
    assert (
        cm_manager_connected_to_antnn.get_antenna_stow_sensor_state()
        == StowPinState.ENGAGED_NOT_RELEASED_STOW_WINDOW
    )
