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
    def setUp(self, mock_RemoteNode, antenna_node):
        # Create an instance of ASTTComponentManager
        self.manager = ASTTComponentManager()

        # Mock the PLC node
        mock_plc_node = mock_RemoteNode.return_value
        self.manager.antenna_node = mock_plc_node

    @patch.object(
        ASTTComponentManager,
        "get_antenna_mode",
        return_value=Mode.POINT,
    )  # noqa
    def test_set_point_mode(self, mock_get_antenna_mode):
        self.manager.set_point_mode()
        mode = self.manager.get_antenna_mode()
        self.assertEqual(mode, Mode.POINT)

    @patch.object(
        ASTTComponentManager,
        "get_antenna_mode",
        return_value=Mode.IDLE,
    )  # noqa
    def test_set_idle_mode(self, mock_get_antenna_mode):
        self.manager.set_idle_mode()
        mode = self.manager.get_antenna_mode()
        self.assertEqual(mode, Mode.IDLE)

    @patch.object(
        ASTTComponentManager,
        "get_antenna_mode",
        return_value=Mode.STOW,
    )  # noqa
    def test_set_stow_mode(self, mock_get_antenna_mode):
        self.manager.set_stow_mode()
        mode = self.manager.get_antenna_mode()
        self.assertEqual(mode, Mode.STOW)


if __name__ == "__main__":
    unittest.main()
