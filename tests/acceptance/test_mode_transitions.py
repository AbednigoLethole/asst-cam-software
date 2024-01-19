"""Test the mode transitions"""
import time


def set_up_subscriptions(comp_manager):
    """Set up all Canopen subscriptions"""
    comp_manager.set_plc_node_to_preoperational()
    comp_manager.subscribe_to_antenna_mode()
    comp_manager.subscribe_to_stow_sensor()
    comp_manager.subscribe_to_func_state()
    comp_manager.subscribe_to_mode_command_obj()
    comp_manager.trigger_transmission()
    time.sleep(7)


def test_antenna_trans_to_point(cm_manager_connected_to_antnn):
    """Test point function"""
    set_up_subscriptions(cm_manager_connected_to_antnn)
    cm_manager_connected_to_antnn.set_point_mode()
    time.sleep(40)
    assert cm_manager_connected_to_antnn.get_antenna_mode() == 1
    assert cm_manager_connected_to_antnn.get_antenna_func_state() == 1
    assert (
        cm_manager_connected_to_antnn.get_antenna_stow_sensor_state()
        == 3
    )
