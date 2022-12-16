from __future__ import print_function
import time
import math

# Dronekit Import
from dronekit import VehicleMode, LocationGlobalRelative
from pymavlink import mavutil # Needed for command message definitions

# Local Import
import koneksi, get_attributes, get_params
from cv import qrs

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

def send_ned_velocity(velocity_x, velocity_y, velocity_z, duration):
                                                            # # Set up velocity mappings
                                                            # # velocity_x > 0 => fly North
                                                            # # velocity_x < 0 => fly South
                                                            # # velocity_y > 0 => fly East
                                                            # # velocity_y < 0 => fly West
                                                            # # velocity_z < 0 => ascend
                                                            # # velocity_z > 0 => descend

    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_LOCAL_NED, # frame
        0b0000111111000111, # type_mask (only speeds enabled)
        0, 0, 0, # x, y, z positions (not used)
        velocity_x, velocity_y, velocity_z, # x, y, z velocity in m/s
        0, 0, 0, # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)


    # send command to vehicle on 1 Hz cycle
    for x in range(0,duration):
        vehicle.send_mavlink(msg)
        time.sleep(1)

def condition_yaw(heading, relative=False):
    if relative:
        is_relative=1 #yaw relative to direction of travel
    else:
        is_relative=0 #yaw is an absolute angle
    # create the CONDITION_YAW command using command_long_encode()
    msg = vehicle.message_factory.command_long_encode(
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_CMD_CONDITION_YAW, #command
        0, #confirmation
        heading,    # param 1, yaw in degrees
        0,          # param 2, yaw speed deg/s
        1,          # param 3, direction -1 ccw, 1 cw
        is_relative, # param 4, relative offset 1, absolute angle 0
        0, 0, 0)    # param 5 ~ 7 not used
    # send command to vehicle
    vehicle.send_mavlink(msg)

def set_roi(location):
    """
    Send MAV_CMD_DO_SET_ROI message to point camera gimbal at a 
    specified region of interest (LocationGlobal).
    The vehicle may also turn to face the ROI.

    For more information see: 
    http://copter.ardupilot.com/common-mavlink-mission-command-messages-mav_cmd/#mav_cmd_do_set_roi
    """
    # create the MAV_CMD_DO_SET_ROI command
    msg = vehicle.message_factory.command_long_encode(
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_CMD_DO_SET_ROI, #command
        0, #confirmation
        0, 0, 0, 0, #params 1-4
        location.lat,
        location.lon,
        location.alt
        )
    # send command to vehicle
    vehicle.send_mavlink(msg)

def geser(arah):
    vehicle.channels.overrides['3'] = 1500
    vehicle.mode = VehicleMode('LOITER')

    time.sleep(1)
    print("Mode: "+vehicle.mode.name)
    print("Emulating Joystick Control...")
    
    vehicle.channels.overrides['3'] = 1500
    if arah == 'kanan':
        vehicle.channels.overrides['1']=vehicle.channels['1']+100
    if arah == 'kiri':
        vehicle.channels.overrides['1']=vehicle.channels['1']-100
    if arah == 'maju':
        vehicle.channels.overrides['2']=vehicle.channels['2']+100
    if arah == 'mundur':
        vehicle.channels.overrides['2']=vehicle.channels['2']-100

    time.sleep(1)
    # # vehicle.channels.overrides = {'3': 1500, '2': 1700}
    # print(" Ch1: %s" % vehicle.channels['1'])
    # print(" Ch2: %s" % vehicle.channels['2'])
    # print(" Ch3: %s" % vehicle.channels['3'])
    # print(" Ch4: %s" % vehicle.channels['4'])
    # print("Number of channels: %s" % len(vehicle.channels))
    # time.sleep(1)

    vehicle.channels.overrides = {}
    vehicle.mode = VehicleMode('GUIDED')
    
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
lokasi_target3 = LocationGlobalRelative(-7.069108, 110.366521, 100)
# get_params.getParams(vehicle)
# get_attributes.getAttributes(vehicle)

armMotor()
takeOff(10)
terbangKe(lokasi_target1)
# terbangKe(lokasi_target2)
# terbangKe(lokasi_target3)

qrs.init(vehicle, "Bondan Eka Nugraha")

# geser('kanan')
# geser('kanan')
# geser('kanan')

# time.sleep(1000)
# set_roi(vehicle.location.global_relative_frame)
# geser(1,0,0,10)
# geser(0,1,0,10)


# terbangKe(lokasi_target2)

# Sequence:
# 1. Scan QR-Code
# 2. Verifying QR-Code
# 3. Aligning QR-Code
# 4. Secondary Verifying QR-Code
# 5. IF VERIFIED>Decent Altitude
# 6. ELSE>RTL
# 7. RTL

# qr_sign = "Bondan Eka Nugraha"
# verified = qr_scanner.scanQR(qr_sign)

# print(verified)
RTL()
vehicle.mode = VehicleMode('STABILIZE')
