"""Test the initial states and modes"""
import time


def set_up_subscriptions(comp_manager):
    """Set up all Canopen subscriptions"""
    comp_manager.set_plc_node_to_preoperational()
    comp_manager.subscribe_to_antenna_mode()
    comp_manager.subscribe_to_stow_sensor()
    comp_manager.subscribe_to_func_state()
    comp_manager.trigger_transmission()
    time.sleep(7)


def test_connection_to_sim_is_success(
    comp_manager_connected_to_antenna,
):
    assert (
        comp_manager_connected_to_antenna.antenna_node
    ) is not None


def test_antenna_starts_at_idle_mode(
    comp_manager_connected_to_antenna,
):
    """Test initial mode of the simulator"""
    set_up_subscriptions(comp_manager_connected_to_antenna)
    assert comp_manager_connected_to_antenna.get_antenna_mode() == 0


def test_antenna_starts_at_braked_fuc_state(
    comp_manager_connected_to_antenna,
):
    """Test initial func state of the simulator"""
    assert (
        comp_manager_connected_to_antenna.get_antenna_func_state()
        == 0
    )


def test_antenna_starts_at_stow_not_release(
    comp_manager_connected_to_antenna,
):
    """Test initial stow state of the simulator"""
    assert (
        comp_manager_connected_to_antenna.get_antenna_stow_sensor_state()
        == 5
    )
