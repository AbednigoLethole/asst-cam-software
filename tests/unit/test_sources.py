import datetime
import unittest

import astropy.units as u
import pytest
from astropy.coordinates import AltAz, EarthLocation, get_sun
from astropy.time import Time

from src.component_managers.sources import Sun


class TestGetSunAzEl(unittest.TestCase):

    def setUp(self):
        self.sun = Sun(lat=-33.9326033333, lon=18.47222, alt=3.6)

    @pytest.fixture(autouse=True)
    def _pass_fixtures(self, capfd):
        self.capfd = capfd

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

    @pytest.mark.skip(reason="to look at this later")
    @pytest.mark.usefixtures("_pass_fixtures")
    def test_calc_position_sun(self):
        track_time = datetime.datetime.now(
            datetime.timezone.utc
        ) + datetime.timedelta(seconds=10)
        timestamp = (
            track_time
            - datetime.datetime(
                1970, 1, 1, tzinfo=datetime.timezone.utc
            )
        ).total_seconds()
        earth_coords = EarthLocation(
            lat=self.sun.lat,
            lon=self.sun.lon,
            height=self.sun.alt * u.m,
        )
        tt = Time(track_time, scale="utc")
        aa = AltAz(obstime=tt, location=earth_coords)
        sun_data = get_sun(tt).transform_to(aa)
        azi = sun_data.az.to(u.degree).value
        ele = sun_data.alt.to(u.degree).value
        results = (
            f"[+] Point: {timestamp} => azimuth {azi} elevation {ele}"
        )
        # Invoke the calc_position_sun method
        self.sun.calc_position_sun()
        # Capture the standard output and error
        out, err = self.capfd.readouterr().out.split("\n")
        # Changed the strings to be in a list
        el = list(out.split(" "))
        ef = list(results.split(" "))
        # In the list extract only the numbers and change them to int.
        el[2], el[5], el[7] = (
            int(float(el[2])),
            int(float(el[5])),
            int(float(el[7])),
        )
        ef[2], ef[5], ef[7] = (
            int(float(ef[2])),
            int(float(ef[5])),
            int(float(ef[7])),
        )
        # self.assertAlmostEqual(el[2], ef[2])
        self.assertAlmostEqual(el[5], ef[5])
        self.assertAlmostEqual(el[7], ef[7])


if __name__ == "__main__":
    unittest.main()
