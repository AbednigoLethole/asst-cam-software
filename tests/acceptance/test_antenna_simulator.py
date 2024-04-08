"""Test for the Component manager."""


def test_antenna_sim_is_available(cm_manager_connected_to_antnn):
    """Test if the simulator is alive through an sdo request."""
    antenna_node = cm_manager_connected_to_antnn.antenna_node
    antenna_node.sdo["TPDO communication parameter"]["transmission type"].raw
    assert antenna_node.nmt.state == "INITIALISING"


def test_sim_trans_to_pre_operational(
    cm_manager_connected_to_antnn,
):
    """Tests if the simulator can transitition to PRE OPERA.."""
    antenna_node = cm_manager_connected_to_antnn.antenna_node
    cm_manager_connected_to_antnn.set_plc_node_to_preoperational()
    assert antenna_node.nmt.state == "PRE-OPERATIONAL"


def test_sim_trans_to_operational(cm_manager_connected_to_antnn):
    """Tests if the simulator can transitition to OPERA.."""
    antenna_node = cm_manager_connected_to_antnn.antenna_node
    cm_manager_connected_to_antnn.set_plc_node_to_operational()
    assert antenna_node.nmt.state == "OPERATIONAL"
