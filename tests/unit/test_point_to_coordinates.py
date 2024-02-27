import unittest
from unittest.mock import patch, MagicMock, call

from src.component_managers.astt_comp_manager import ASTTComponentManager


class TestAntennaPointing(unittest.TestCase):
    @patch("src.component_managers.astt_comp_manager.canopen.Network")
    @patch("src.component_managers.astt_comp_manager.canopen.RemoteNode")
    def test_point_to_coordinates_function(self, mock_RemoteNode, mock_Network):
        # Create an instance of ASTTComponentManager
        manager = ASTTComponentManager()

        # Mock the network and PLC node
        mock_network = mock_Network.return_value
        mock_plc_node = mock_RemoteNode.return_value
        manager.network0 = mock_network
        manager.antenna_node = mock_plc_node

        # Mock the sdo object and its __setitem__ method
        mock_sdo = MagicMock()
        mock_plc_node.sdo = mock_sdo

        # Test with valid coordinates
        timestamp = 1234567890.0
        az = 30.0
        el = 40.0
        manager.point_to_coordinates(timestamp, az, el)

        # Assert that the values were set correctly on the PLC node
        calls = [
            call((0x2000, 1), 1234567890.0 + 2.0),
            call((0x2000, 2), az),
            call((0x2000, 3), el)
        ]
        mock_sdo.__setitem__(calls, any_order=True)

        # Test with invalid coordinates
        with self.assertRaises(ValueError):
            # Use coordinates that are out of range
            manager.point_to_coordinates(timestamp, 200.0, 100.0)


if __name__ == "__main__":
    unittest.main()
