import unittest
from unittest.mock import patch
from src.component_managers.dish_modes import Mode
from src.component_managers.astt_comp_manager import ASTTComponentManager

class TestAntennaModes(unittest.TestCase):
    @patch("src.component_managers.astt_comp_manager.canopen.Network")
    @patch("src.component_managers.astt_comp_manager.canopen.RemoteNode")
    def setUp(self, mock_RemoteNode, antenna_node):
        # Create an instance of ASTTComponentManager
        self.manager = ASTTComponentManager()

        # Mock the PLC node
        mock_plc_node = mock_RemoteNode.return_value
        self.manager.antenna_node = mock_plc_node

    def test_set_point_mode(self):
        self.manager.set_point_mode()
        mode = self.manager.get_antenna_mode()
        if mode != Mode.UNKNOWN:
            self.assertEqual(mode, Mode.POINT.value)

    def test_set_idle_mode(self):
        self.manager.set_idle_mode()
        mode = self.manager.get_antenna_mode()
        if mode != Mode.UNKNOWN:
            self.assertEqual(mode, Mode.IDLE.value)

    def test_set_stow_mode(self):
        self.manager.set_stow_mode()
        mode = self.manager.get_antenna_mode()
        if mode != Mode.UNKNOWN:
            self.assertEqual(mode, Mode.STOW.value)

if __name__ == '__main__':
    unittest.main()
