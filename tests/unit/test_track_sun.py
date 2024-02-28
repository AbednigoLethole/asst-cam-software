import unittest
from unittest.mock import MagicMock

from src.component_managers.astt_comp_manager import (
    ASTTComponentManager,
)


class TestAntennaTracking(unittest.TestCase):
    def test_track_sun_function(self):
        manager = ASTTComponentManager()

        # Mocking necessary objects
        mock_cm = manager
        mock_cm.antenna_node = MagicMock()
        mock_cm.track_sun = ASTTComponentManager.track_sun

        # Creating mock request
        mock_request = MagicMock()
        mock_request.form = {"sources": "sun"}

        # Testing the track_sun function
        try:
            mock_cm.track_sun(mock_request)
        except ValueError:
            # If a value error is raised the test will fail
            assert False

        # Testing the track_sun function
        mock_cm.track_sun(mock_request)


if __name__ == "__main__":
    unittest.main()
