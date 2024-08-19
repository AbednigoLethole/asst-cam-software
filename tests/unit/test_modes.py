import unittest
from unittest.mock import patch

from src.component_managers.astt_comp_manager import (
    ASTTComponentManager,
)
from src.component_managers.dish_modes import Mode


# Creating a customized Mocked incoming Object
class MockedIncomingTpdo:
    def __init__(self, raw, name):
        self.raw = raw
        self.name = name


class TestAntennaModes(unittest.TestCase):
    @patch("src.component_managers.astt_comp_manager.canopen.Network")
    @patch(
        "src.component_managers.astt_comp_manager.canopen.RemoteNode"
    )
    def setUp(self, mock_RemoteNode, mock_Network):
        self.manager = ASTTComponentManager()
        mock_network = mock_Network.return_value
        mock_plc_node = mock_RemoteNode.return_value
        self.manager.network0 = mock_network
        self.manager.antenna_node = mock_plc_node

    def test_point_mode(self):
        incoming_obj = MockedIncomingTpdo(
            1, "Mode and State Feedback.Mode"
        )
        self.manager.state_mode_callback([incoming_obj])
        mode = self.manager.get_antenna_mode()
        self.assertEqual(mode, Mode.POINT)

    def test_idle_mode(self):
        incoming_obj = MockedIncomingTpdo(
            0, "Mode and State Feedback.Mode"
        )
        self.manager.state_mode_callback([incoming_obj])
        mode = self.manager.get_antenna_mode()
        self.assertEqual(mode, Mode.IDLE)

    def test_stow_mode(self):
        incoming_obj = MockedIncomingTpdo(
            2, "Mode and State Feedback.Mode"
        )
        self.manager.state_mode_callback([incoming_obj])
        mode = self.manager.get_antenna_mode()
        self.assertEqual(mode, Mode.STOW)
