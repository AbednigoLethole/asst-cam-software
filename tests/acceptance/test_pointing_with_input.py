"""Test the pointing function with inputs."""

import time

import pytest


def set_up_subscriptions(comp_manager):
    """Set up all Canopen subscriptions."""
    comp_manager.set_plc_node_to_preoperational()
    comp_manager.subscribe_to_func_state_and_mode()
    comp_manager.subscribe_to_stow_sensor()
    comp_manager.subscribe_to_mode_command_obj()
    comp_manager.trigger_transmission()

    time.sleep(7)


def test_point_func_rejects_incor_input(
    cm_manager_connected_to_antnn,
):
    """Test pointing with values out of range."""
    set_up_subscriptions(cm_manager_connected_to_antnn)
    cm_manager_connected_to_antnn.set_point_mode()
    # The antenna takes roughly 30 sec to switch modes
    time.sleep(33)
    # Tests whether point to coordinates raises a value error
    # when values out of range are passed.
    with pytest.raises(ValueError):
        cm_manager_connected_to_antnn.point_to_coordinates(float(time.time()), 130.0, 100.0)


def test_point_func_accepts_corr_input(cm_manager_connected_to_antnn):
    """Test pointing with values in range."""
    # Assume the antenna is in pointing because of the function
    # above sets it.
    # Assert true gets triggered if AZ/EL are accepted
    cm_manager_connected_to_antnn.point_to_coordinates(float(time.time()), 56.0, -5.0)
    assert True
