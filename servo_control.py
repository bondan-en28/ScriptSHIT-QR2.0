from __future__ import print_function
import time, math, threading
# Dronekit Import
from dronekit import VehicleMode, LocationGlobalRelative
from pymavlink import mavutil # Needed for command message definitions

# Local Import
import koneksi, get_attributes, get_params

vehicle = koneksi.vehicle

def payload_release(closed=False):
    if closed:
        vehicle.channels.overrides['7'] = 2000
        print(vehicle.channels.overrides)
    else:
        vehicle.channels.overrides['7'] = 1500
        print(vehicle.channels.overrides)
        
################################################# Manggil FUNGSI DI SINI SEMUA YGY (biar rapih)

get_params.getParams(vehicle)
get_attributes.getAttributes(vehicle)

payload_release(True)
time.sleep(2)
payload_release(False)
time.sleep(2)
vehicle.channels.overrides = {}
print(vehicle.channels.overrides)
