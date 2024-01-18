"""Test for the Component manager."""


def test_antenna_sim_is_available(comp_manager_connected_to_antenna):
    """Test if the simulator is alive through an sdo request."""
    antenna_node = comp_manager_connected_to_antenna.antenna_node
    antenna_node.sdo["TPDO communication parameter"][
        "transmission type"
    ].raw
    assert antenna_node.nmt.state == "INITIALISING"


def test_sim_trans_to_pre_operational(
    comp_manager_connected_to_antenna,
):
    """Tests if the simulator can transitition to PRE OPERA.."""
    antenna_node = comp_manager_connected_to_antenna.antenna_node
    comp_manager_connected_to_antenna.set_plc_node_to_preoperational()
    assert antenna_node.nmt.state == "PRE-OPERATIONAL"


def test_sim_trans_to_operational(comp_manager_connected_to_antenna):
    """Tests if the simulator can transitition to OPERA.."""
    antenna_node = comp_manager_connected_to_antenna.antenna_node
    comp_manager_connected_to_antenna.set_plc_node_to_operational()
    assert antenna_node.nmt.state == "OPERATIONAL"
