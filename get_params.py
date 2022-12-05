
def getParams(vehicle):
    print("\nPrint all parameters (iterate `vehicle.parameters`):")
    for key, value in vehicle.parameters.items():
        print(" Key:%s Value:%s" % (key,value))