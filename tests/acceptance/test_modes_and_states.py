"""Test the initial states and modes"""
import time


def test_connection_to_sim_is_success(
    comp_manager_connected_to_antenna,
):

    assert (
        comp_manager_connected_to_antenna.antenna_node
    ) is not None


def test_antenna_starts_at_braked_state(
    comp_manager_connected_to_antenna,
):
    """Test initial state of the simulator"""
    comp_manager_connected_to_antenna.set_plc_node_to_preoperational()
    comp_manager_connected_to_antenna.subscribe_to_func_state()
    comp_manager_connected_to_antenna.trigger_transmission()
    assert comp_manager_connected_to_antenna.get_antenna_mode() == 0


"""
def test_antenna_transition_to_point(antenna_comp_manager):
    antenna_comp_manager.set_point_mode()
    time.sleep(60)
    assert antenna_comp_manager.antenna_mode() == 1
"""
