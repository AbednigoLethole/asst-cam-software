# noqa: E501
import datetime

from astropy import units as u
from astropy.coordinates import (
    AltAz,
    EarthLocation,
    SkyCoord,
    get_sun,
)
from astropy.time import Time

# TODO: Use ASTT GPS Reciever Component Manager.

current_time = datetime.datetime.now(datetime.timezone.utc)
track_time = Time(current_time, scale="utc")


class Sun:
    """Class sun containing all it's attributes."""

    def __init__(self, lat, lon, alt):
        self.lat = lat * u.deg
        self.lon = lon * u.deg
        self.alt = alt

    def earth_coords(self):
        earth_coords = EarthLocation(
            lat=self.lat, lon=self.lon, height=self.alt * u.m
        )
        return earth_coords

    def get_sun_az_el(self, sun_time):
        """This method outputs the Sun's current Az and El."""
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
        return (az, el)

    def calc_position_sun(self, track_time):
        """Calculates Sun's Az and El

        :return: timestamp, azimuth and elevation of the Sun.
        """
        FUTURE_SECONDS = 10
        while True:
            # Get user for input
            user_input = input(
                "Time & date in the format YYYY, MM, DD, HH, MM, SS: "
            )
            # Parse user input
            try:
                year, month, day, hour, minute, second = map(
                    int, user_input.split(",")
                )
                track_time = datetime.datetime(
                    year,
                    month,
                    day,
                    hour,
                    minute,
                    second,
                    tzinfo=datetime.timezone.utc,
                ) + datetime.timedelta(seconds=FUTURE_SECONDS)
                break  # Break out of the loop if input is valid
            except ValueError:
                print(
                    "Invalid.Enter the values in the specified format"
                )
        timestamp = (
            track_time
            - datetime.datetime(
                1970, 1, 1, tzinfo=datetime.timezone.utc
            )
        ).total_seconds()
        tt = Time(track_time, scale="utc")
        aa = AltAz(obstime=tt, location=self.earth_coords())
        sun_data = get_sun(tt).transform_to(aa)
        azi = sun_data.az.to(u.degree).value
        ele = sun_data.alt.to(u.degree).value
        return [timestamp, azi, ele]


class Satellite1:
    """Class of geostationary or any other satellite or source."""

    def __init__(self, lat, lon, alt):
        self.lat = lat * u.deg
        self.lon = lon * u.deg
        self.alt = alt * u.m

    def get_sat1_az_el(self):
        # TODO: Work on the logic to get azimuth and elevation.
        """This method outputs a satellite's current Az and El."""
        pass


class Satellite2:
    "Class to get source Az and El using the source name"

    def __init__(self, lat, lon, alt, name):
        self.lat = lat
        self.lon = lon
        self.alt = alt
        self.name = name

    def get_az_el_sat2(self):
        # TODO: Find the database that has the source names.
        source_coords = SkyCoord.from_name(self.name)
        print(source_coords)
        pass


if __name__ == "__main__":
    sun = Sun(-33.9326033333, 18.47222, 3.6)
    sun.get_sun_az_el(track_time)
