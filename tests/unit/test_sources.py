import datetime
import unittest

import astropy.units as u
import pytest
from astropy.coordinates import AltAz, EarthLocation, get_sun
from astropy.time import Time

from src.component_managers.sources import Sun


class TestGetSunAzEl(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def _pass_fixtures(self, capsys):
        self.capsys = capsys

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
            2024, 3, 16, 12, 0, 0, tzinfo=datetime.timezone.utc
        )

        # Calculate expected values using astropy and compare them
        astropy_time = Time(sun_time, scale="utc")
        astt_coords = EarthLocation(
            lat=self.sun.lat,
            lon=self.sun.lon,
            height=self.sun.alt * u.m,
        )
        alt_az = AltAz(obstime=astropy_time, location=astt_coords)
        sun_coords = get_sun(astropy_time).transform_to(alt_az)
        expected_az = sun_coords.az.to(u.degree).value
        expected_el = sun_coords.alt.to(u.degree).value

        az, el = self.sun.get_sun_az_el(sun_time)
        self.assertAlmostEqual(az, expected_az)
        self.assertAlmostEqual(el, expected_el)

    @pytest.mark.xfail(
        reason="Consider making main function to have a return"
    )
    def test_calc_position_sun(self):
        track_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=10)
        timestamp = (track_time - datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)).total_seconds()
        earth_coords = EarthLocation(lat=self.sun.lat, lon=self.sun.lon, height=self.sun.alt * u.m)
        tt = Time(track_time, scale="utc")
        aa = AltAz(obstime=tt, location=earth_coords)
        sun_data = get_sun(tt).transform_to(aa)
        azi = sun_data.az.to(u.degree).value
        ele = sun_data.alt.to(u.degree).value
        results = f"[+] Point: {timestamp} => azimuth {azi} elevation {ele}"
        result = print(results)
        # Invoke the calc_position_sun method
        self.sun.calc_position_sun()
        # Capture the standard output and error
        captured = self.capsys.readouterr()
        self.assertAlmostEqual(result, captured.out)


if __name__ == "__main__":
    unittest.main()
