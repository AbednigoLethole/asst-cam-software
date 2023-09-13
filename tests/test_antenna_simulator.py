from astt_cam_software.component_managers.astt_comp_manager import (
    ASTTComponentManager,
)

cm = ASTTComponentManager()
cm.connect_to_network()
node2 = cm.connect_to_plc_node()


def test_antenna_sim_is_available():
    (cm.network0).send_message(0x0, [0x1, 0])
    node2.nmt.wait_for_heartbeat()
    assert node2.nmt.state == "OPERATIONAL"


def test_sim_trans_to_pre_operational():
    cm.set_plc_node_to_preoperational(node2)
    assert node2.nmt.state == "PRE-OPERATIONAL"


def test_sim_trans_to_operational():
    cm.set_plc_node_to_operational(node2)
    assert node2.nmt.state == "OPERATIONAL"
