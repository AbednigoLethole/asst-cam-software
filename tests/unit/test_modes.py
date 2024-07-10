"""Test to verify Antenna Modes."""

import unittest
from unittest.mock import patch

from src.component_managers.astt_comp_manager import (
    ASTTComponentManager,
)
from src.component_managers.dish_modes import Mode

# pylint: disable=invalid-name,unused-argument,too-many-public-methods
# pylint: disable=attribute-defined-outside-init
# pylint: disable=arguments-differ
# pylint: disable=too-few-public-methods


# Creating a customized Mocked incoming Object
class MockedIncomingTpdo:
    """Customized mocked incoming TPDO."""

    def __init__(self, raw):
        self.raw = raw


class TestAntennaModes(unittest.TestCase):
    """TestCase to for Antenna modes."""

    @patch("src.component_managers.astt_comp_manager.canopen.Network")
    @patch(
        "src.component_managers.astt_comp_manager.canopen.RemoteNode"
    )
    def setUp(self, mock_RemoteNode, mock_Network):
        """ASTT CAN Network setup."""
        self.manager = ASTTComponentManager()
        mock_network = mock_Network.return_value
        mock_plc_node = mock_RemoteNode.return_value
        self.manager.network0 = mock_network
        self.manager.antenna_node = mock_plc_node

    def test_point_mode(self):
        """Testing antenna point mode."""
        incoming_obj = MockedIncomingTpdo(1)
        self.manager.antenna_mode_callback([incoming_obj])
        mode = self.manager.get_antenna_mode()
        self.assertEqual(mode, Mode.POINT)

    def test_idle_mode(self):
        """Testing antenna idle mode."""
        incoming_obj = MockedIncomingTpdo(0)
        self.manager.antenna_mode_callback([incoming_obj])
        mode = self.manager.get_antenna_mode()
        self.assertEqual(mode, Mode.IDLE)

    def test_stow_mode(self):
        """Testing antenna stow mode."""
        incoming_obj = MockedIncomingTpdo(2)
        self.manager.antenna_mode_callback([incoming_obj])
        mode = self.manager.get_antenna_mode()
        self.assertEqual(mode, Mode.STOW)
