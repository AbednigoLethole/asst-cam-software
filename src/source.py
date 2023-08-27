import time
from astropy.coordinates import EarthLocation, AltAz, get_sun
from astropy import units as u
from astropy.time import *
# import datetime
#from gps_comp_manager import GpsComp

# Hardcoded Observer's co ordinates
# lat = 50.0 * u.deg
# lon = 30.0 * u.deg
# alt = 70.0 * u.m

# ASTT location hardcoded but 
# TODO: Use ASTT GPS Reciever Component Manager.
# Timestamp
utcoffset = -2 * u.hour  # SAST Daylight Time
time = Time('2023-8-26 09:25:00') - utcoffset


class Sun:
    def __init__(self, lat, lon, alt):
        self.lat = lat * u.deg
        self.lon = lon * u.deg
        self.alt = alt * u.m
        # astt_coords = self.astt_coords

    def get_sun_az_el(self):
        astt_coords = EarthLocation(self.lat, self.lon, self.alt)
        alt_az = AltAz(obstime=time, location=astt_coords)
        sun_coords = get_sun(time).transform_to(alt_az)
        az = sun_coords.az.to(u.degree).value
        el = sun_coords.alt.to(u.degree).value
        print('Sun_Az :', str(az), 'Sun_El :', str(el))
        return (az, el)


class Satellite1:
    def __init__(self, lat, lon, alt):
        self.lat = lat 
        self.lon = lon 
        self.alt = alt

    def get_sat1_az_el(self):
        astt_coords = EarthLocation(self.lat, self.lon, self.alt)
        alt_az = AltAz(obstime=time, location=astt_coords)
        sat1_coords = get_sun(time).transform_to(alt_az)
        az = sat1_coords.az.to(u.degree).value
        el = sat1_coords.alt.to(u.degree).value
        print('sat1_Az: ', str(az), 'sat1_El :', str(el))
        return (az, el)


class Satellite2:
    def __init__(self, lat, lon, alt):
        self.lat = lat
        self.lon = lon
        self.alt = alt

    def get_az_el_sat2(self, timestamp):
        return (az, el)


if __name__ == '__main__':
    sun = Sun(50.0, 30.0, 70.0)
    sun.get_sun_az_el()
    intelsat20 = Satellite1(-34.34818, 18.82706, 5217.8)
    intelsat20.get_sat1_az_el()