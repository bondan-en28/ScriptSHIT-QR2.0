from __future__ import print_function
import time

from dronekit import VehicleMode

# Local Import
import koneksi, get_attributes, get_params

vehicle = koneksi.vehicle 

# get_attributes.getAttributes(vehicle)

# def armMotor():

#     print("Basic pre-arm checks")
#     # Don't try to arm until autopilot is ready
#     while not vehicle.is_armable:
#         print(" Waiting for vehicle to initialise...")
#         time.sleep(1)

#     print("Arming motors")
#     # Copter should arm in GUIDED mode
#     vehicle.mode = VehicleMode("GUIDED")
#     vehicle.armed = True

#     # Confirm vehicle armed before attempting to take off
#     while not vehicle.armed:
#         print(" Waiting for arming...")
#         time.sleep(1)

#     print("Ready to Fly!")

# armMotor()
# time.sleep(5)
# vehicle.armed = False
# time.sleep(5)
# get_attributes.getAttributes(vehicle)

get_params.getParams(vehicle)