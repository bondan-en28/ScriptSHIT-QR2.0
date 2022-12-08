from __future__ import print_function
import time
import math

# Dronekit Import
from dronekit import VehicleMode, LocationGlobalRelative

# Local Import
import koneksi, get_attributes, get_params

vehicle = koneksi.vehicle

def armMotor():

    # Get Vehicle Home location - will be `None` until first set by autopilot
    print("Getting Home Location...")
    while not vehicle.home_location:
        cmds = vehicle.commands
        cmds.download()
        cmds.wait_ready()
        if not vehicle.home_location:
            print(" Waiting for home location ...")

    # We have a home location.
    print ("Home location: %s" % vehicle.home_location)

    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print("Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print("Waiting for arming...")
        time.sleep(1)

    print("Ready to Fly!")

def takeOff(target_altitude=10):
    print("Taking off!")
    vehicle.simple_takeoff(target_altitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= target_altitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

def getJarak(lokasi_terkini, lokasi_target):
    dlat = lokasi_terkini.lat - lokasi_target.lat
    dlong = lokasi_terkini.lon - lokasi_target.lon
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5

def terbangKe(lokasi_target):
    print("Menuju : ", lokasi_target)
    lokasi_terkini = vehicle.location.global_relative_frame
    jarak_target = getJarak(lokasi_terkini, lokasi_target)
    vehicle.simple_goto(lokasi_target)
    
    while vehicle.mode.name=="GUIDED": #Berhenti apabila keluar dari mode Guided
        jarak_terkini = getJarak(vehicle.location.global_relative_frame, lokasi_target)
        print(jarak_terkini)
        if jarak_terkini<=jarak_target*0.01:
            print("Sampai di lokasi kakak :)")
            break
        time.sleep(1)

def RTL():
    vehicle.mode = VehicleMode('RTL')
    while vehicle.armed:
        print()
        print("  OTW RTL...", getJarak(vehicle.location.global_relative_frame,vehicle.home_location) ," meter lagi...")
        time.sleep(1)
    print("RTL Selesai!")

################################################# Manggil FUNGSI DI SINI SEMUA YGY (biar rapih)

lokasi_target1 = LocationGlobalRelative(-7.077743, 110.328161, 10)
lokasi_target2 = LocationGlobalRelative(-7.0774391, 110.3289168, 10)

get_params.getParams(vehicle)
get_attributes.getAttributes(vehicle)

armMotor()
takeOff(10)
terbangKe(lokasi_target1)
terbangKe(lokasi_target2)
RTL()
vehicle.mode = VehicleMode('STABILIZE')
