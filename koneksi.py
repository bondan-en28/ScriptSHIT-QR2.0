#05/12/2022
#Bondan Eka Nugraha

"""
Dokumentasi kode: https://dronekit-python.readthedocs.io/en/latest/guide/connecting_vehicle.html
"""

from dronekit import connect

# Connect to the Vehicle (in this case a UDP endpoint)
# vehicle = connect('127.0.0.1:14550', wait_ready=True) #konek via UDP(SITL)
vehicle = connect('tcp:127.0.0.1:5762', wait_ready=True, baud=57600) #konek via TCP(SITL)
# vehicle = connect('COM9', wait_ready=True, baud=57600) #Konek ke port COMx(WINDOWS) via Telemetry
# vehicle = connect('/dev/ttyAMA0', wait_ready=True, baud=92100) #Konek ke Serial0(Raspberry Pi 4)

vehicle.wait_ready('autopilot_version')
