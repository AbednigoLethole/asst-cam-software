import sys
from datetime import datetime, timezone

from astropy import units as u
from astropy.coordinates import AltAz, EarthLocation, get_sun
from astropy.time import Time

# from gps_comp_manager import GpsComp
# TODO: Use ASTT GPS Reciever Component Manager.
current_time = datetime.now(timezone.utc)
track_time = Time(current_time, scale="utc")


class Sun:
    """Class sun containing all it's attributes."""

    def __init__(self, lat, lon, alt):
        self.lat = lat * u.deg
        self.lon = lon * u.deg
        self.alt = alt
        self.current_time = datetime.now(timezone.utc)
        self.track_time = Time(current_time, scale="utc")
        # astt_coords = self.astt_coords

    def get_sun_az_el(self):
        """This method outputs the Sun's current Azimuth
        and Elevation.
        Returns:
          A tuple that contains the Azimuth and Elevation
          in degrees.
        """
        astt_coords = EarthLocation(
            lat=self.lat, lon=self.lon, height=self.alt * u.m
        )
        alt_az = AltAz(obstime=track_time, location=astt_coords)
        # TODO: Change get_sun method to a suitable function to
        # find satellites.
        sun_coords = get_sun(track_time).transform_to(alt_az)
        az = sun_coords.az.to(u.degree).value
        el = sun_coords.alt.to(u.degree).value
        print("Sun_Az :", str(az), "Sun_El :", str(el))
        return (az, el)


class Satellite1:
    """Class of geostationary or any other satellite or source."""

    def __init__(self, lat, lon, alt):
        self.lat = lat
        self.lon = lon
        self.alt = alt

    def get_sat1_az_el(self):
        """This method outputs a satellite's current Azimuth
        and Elevation.
        Returns:
          A tuple that contains the Azimuth and Elevation
          in degrees.
        """
        astt_coords = EarthLocation(self.lat, self.lon, self.alt)
        alt_az = AltAz(obstime=None, location=astt_coords)
        sat1_coords = get_sun(track_time).transform_to(alt_az)
        az = sat1_coords.az.to(u.degree).value
        el = sat1_coords.alt.to(u.degree).value
        print("sat1_Az: ", str(az), "sat1_El :", str(el))
        return (az, el)


class Satellite2:
    def __init__(self, lat, lon, alt):
        self.lat = lat
        self.lon = lon
        self.alt = alt

    def get_az_el_sat2(self, timestamp):
        pass


if __name__ == "__main__":
    print(sys.path)
    # sun = Sun(-33.9326033333, 18.47222, 3.6)
    # sun.get_sun_az_el()
    # intelsat20 = Satellite1(-33.9326033333, 18.47222, 3.6)
    # intelsat20.get_sat1_az_el()
