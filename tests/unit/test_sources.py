# noqa: E501
import datetime
import unittest
from unittest.mock import patch

from astropy.coordinates import EarthLocation

from src.component_managers.sources import Sun


class TestGetSunAzEl(unittest.TestCase):

    def setUp(self):
        self.sun = Sun(lat=-33.9326033333, lon=18.47222, alt=3.6)

    def test_earth_coords_valid(self):
        result = self.sun.earth_coords()
        self.assertIsInstance(result, EarthLocation)
        # Check function values are almost equal to the given values
        self.assertAlmostEqual(result.x.value, 5024500.22950045)
        self.assertAlmostEqual(result.y.value, 1678465.82164216)
        self.assertAlmostEqual(result.z.value, -3540248.43179082)

    def test_get_sun_az_el(self):
        sun_time = datetime.datetime(
            2024, 5, 8, 12, 0, 0, tzinfo=datetime.timezone.utc
        )
        expected_az = 337.11244076091316
        expected_el = 35.546531518065116
        az, el = self.sun.get_sun_az_el(sun_time)
        self.assertAlmostEqual(az, expected_az, places=5)
        self.assertAlmostEqual(el, expected_el, places=5)

    @patch("builtins.input")
    def test_calc_position_sun(self, mocked_input):
        mocked_input.return_value = "2024, 5, 8, 12, 0, 0"
        track_time = mocked_input.return_value
        expected_timestam = 1715169610.0
        expected_el = 35.53304352273266
        expected_az = 337.06644428631614
        timestamp, azimuth, elevation = self.sun.calc_position_sun(
            track_time
        )
        self.assertAlmostEqual(timestamp, expected_timestam, places=5)
        self.assertAlmostEqual(azimuth, expected_az, places=5)
        self.assertAlmostEqual(elevation, expected_el, places=5)
