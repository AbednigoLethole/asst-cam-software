"""Test for the Component manager."""
from component_managers.astt_comp_manager import ASTTComponentManager

cm = ASTTComponentManager()
cm.connect_to_network()
node2 = cm.connect_to_plc_node()


def test_antenna_sim_is_available():
    """Test if the simulator is alive through an sdo request."""
    node2.sdo["TPDO communication parameter"]["transmission type"].raw
    assert node2.nmt.state == "INITIALISING"


def test_sim_trans_to_pre_operational():
    """Tests if the simulator can transitition to PRE OPERA.. """
    cm.set_plc_node_to_preoperational(node2)
    assert node2.nmt.state == "PRE-OPERATIONAL"


def test_sim_trans_to_operational():
    """Tests if the simulator can transitition to OPERA.. """
    cm.set_plc_node_to_operational(node2)
    assert node2.nmt.state == "OPERATIONAL"
