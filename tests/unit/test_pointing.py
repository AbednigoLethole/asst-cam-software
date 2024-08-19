"""Test the pointing function."""

# pylint: disable=invalid-name,unused-argument,too-many-public-methods
# pylint: disable=attribute-defined-outside-init
# pylint: disable=broad-except

import time
import unittest
from unittest.mock import patch

from src.component_managers.astt_comp_manager import ASTTComponentManager


class TestAntennaPointing(unittest.TestCase):
    """TestCase for pointing function."""

    @patch("src.component_managers.astt_comp_manager.canopen.Network")
    @patch("src.component_managers.astt_comp_manager.canopen.RemoteNode")
    def test_pointing_function(self, mock_remotenode, mock_network):
        """Testing ASTT pointing function."""
        manager = ASTTComponentManager()
        # Mock the network and PLC node
        mock_network = mock_network.return_value
        mock_plc_node = mock_remotenode.return_value
        manager.network0 = mock_network
        manager.antenna_node = mock_plc_node

        # Check if the pointing will accept values in range
        try:
            manager.point_to_coordinates(float(time.time()), 30.0, 40.0)
        except ValueError:
            # if a value error is raised the test will fail
            assert False
