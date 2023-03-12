from __future__ import print_function

def getAttributes(vehicle):
    print("\nGet before take off requirements vehicle attribute values:")
    print(" Global Location             : %s" % vehicle.location.global_frame)
    print(" Global Loc(relative alt)    : %s" % vehicle.location.global_relative_frame)
    print(" Attitude                    : %s" % vehicle.attitude)
    print(" Velocity                    : %s" % vehicle.velocity)
    print(" GPS                         : %s" % vehicle.gps_0)
    print(" Battery                     : %s" % vehicle.battery)
    print(" EKF OK?                     : %s" % vehicle.ekf_ok)
    print(" Heading                     : %s" % vehicle.heading)
    print(" System status               : %s" % vehicle.system_status.state)
    print(" Groundspeed                 : %s" % vehicle.groundspeed)
    print(" Airspeed                    : %s" % vehicle.airspeed)
    print(" Mode                        : %s" % vehicle.mode.name)
    print(" Is Armable?                 : %s" % vehicle.is_armable)
    print(" Armed                       : %s" % vehicle.armed)
