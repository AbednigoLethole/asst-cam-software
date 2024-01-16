"""Test for the Component manager."""


def test_antenna_sim_is_available(antenna_node):
    """Test if the simulator is alive through an sdo request."""
    antenna_node.sdo["TPDO communication parameter"][
        "transmission type"
    ].raw
    assert antenna_node.nmt.state == "INITIALISING"


def test_sim_trans_to_pre_operational(
    antenna_node, antenna_comp_manager
):
    """Tests if the simulator can transitition to PRE OPERA.."""
    antenna_comp_manager.set_plc_node_to_preoperational()
    assert antenna_node.nmt.state == "PRE-OPERATIONAL"


def test_sim_trans_to_operational(antenna_node, antenna_comp_manager):
    """Tests if the simulator can transitition to OPERA.."""
    antenna_comp_manager.set_plc_node_to_operational()
    assert antenna_node.nmt.state == "OPERATIONAL"
