"""Test the initial states and modes"""


def test_antenna_starts_at_idle(antenna_comp_manager):
    """Test initial state of the simulator"""
    antenna_comp_manager.connect_to_network()
    antenna_comp_manager.connect_to_plc_node()
    assert antenna_comp_manager.antenna_mode() == 0
