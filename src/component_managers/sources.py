from datetime import datetime, timezone

from astropy import units as u
from astropy.coordinates import (
    AltAz,
    EarthLocation,
    SkyCoord,
    get_sun,
)
from astropy.time import Time

# TODO: Use ASTT GPS Reciever Component Manager.
current_time = datetime.now(timezone.utc)
track_time = Time(current_time, scale="utc")


class Sun:
    """Class sun containing all it's attributes."""

    def __init__(self, lat, lon, alt):
        self.lat = lat * u.deg
        self.lon = lon * u.deg
        self.alt = alt

    def get_sun_az_el(self, sun_time):
        """This method outputs the Sun's current Azimuth
        and Elevation.
        Returns:
          A tuple that contains the Azimuth and Elevation
          in degrees.
        """
        astropy_time = Time(sun_time, scale="utc")
        astt_coords = EarthLocation(
            lat=self.lat, lon=self.lon, height=self.alt * u.m
        )
        alt_az = AltAz(obstime=astropy_time, location=astt_coords)
        # TODO: Change get_sun method to a suitable function to
        # find satellites.
        sun_coords = get_sun(astropy_time).transform_to(alt_az)
        az = sun_coords.az.to(u.degree).value
        el = sun_coords.alt.to(u.degree).value
        print("Sun_Az :", str(az), "Sun_El :", str(el))
        return (az, el)


class Satellite1:
    """Class of geostationary or any other satellite or source."""

    def __init__(self, lat, lon, alt):
        self.lat = lat * u.deg
        self.lon = lon * u.deg
        self.alt = alt * u.m

    def get_sat1_az_el(self):
        # TODO: Work on the logic to get azimuth and elevation.
        """This method outputs a satellite's current Azimuth
        and Elevation.
        Returns:
          A tuple that contains the Azimuth and Elevation
          in degrees.
        """
        pass


class Satellite2:
    "Class to get source Azimuth and Elevation using the source name"

    def __init__(self, lat, lon, alt, name):
        self.lat = lat
        self.lon = lon
        self.alt = alt
        self.name = name

    def get_az_el_sat2(self):
        # TODO: Find the database that has the source(s) names.
        source_coords = SkyCoord.from_name(self.name)
        print(source_coords)
        pass


if __name__ == "__main__":
    sun = Sun(-33.9326033333, 18.47222, 3.6)
    sun.get_sun_az_el(track_time)
