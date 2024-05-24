import unittest
from unittest.mock import patch

from src.component_managers.astt_comp_manager import (
    ASTTComponentManager,
)
from src.component_managers.dish_modes import Mode


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
        self.manager.antenna_mode = Mode.POINT
        mode = self.manager.get_antenna_mode()
        self.assertEqual(mode, Mode.POINT)

    def test_idle_mode(self):
        self.manager.antenna_mode = Mode.IDLE
        mode = self.manager.get_antenna_mode()
        self.assertEqual(mode, Mode.IDLE)

    def test_stow_mode(self):
        self.manager.antenna_mode = Mode.STOW
        mode = self.manager.get_antenna_mode()
        self.assertEqual(mode, Mode.STOW)
