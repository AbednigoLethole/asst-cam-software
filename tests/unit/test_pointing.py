"""Test the pointing function"""

import time
import unittest
from unittest.mock import patch

from src.component_managers.astt_comp_manager import (
    ASTTComponentManager,
)


class TestAntennaPointing(unittest.TestCase):
    @patch("src.component_managers.astt_comp_manager.canopen.Network")
    @patch("src.component_managers.astt_comp_manager.canopen.RemoteNode")
    def test_pointing_function(self, mock_RemoteNode, mock_Network):
        manager = ASTTComponentManager()
        # Mock the network and PLC node
        mock_network = mock_Network.return_value
        mock_plc_node = mock_RemoteNode.return_value
        manager.network0 = mock_network
        manager.antenna_node = mock_plc_node

        # Check if the pointing will accept values in range
        try:
            manager.point_to_coordinates(float(time.time()), 30.0, 40.0)
        except ValueError:
            # if a value error is raised the test will fail
            assert False
