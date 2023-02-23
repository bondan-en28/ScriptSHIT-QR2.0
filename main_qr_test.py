from __future__ import print_function
import time, math, threading
# Dronekit Import

from cv import qrs, qr_target_identifier

verified = qrs.verified

print("\n\nVerifikasi Misi...")
identifiedQRDict = None
#qr_target_identifier.main()
#print(identifiedQRDict)

while identifiedQRDict is None:
    identifiedQRDict= qr_target_identifier.main()

print(identifiedQRDict)


#qrs.init(vehicle=None, str(identifiedQRDict['id']))

# Sequence:
# 1. Scan QR-Code
# 2. Verifying QR-Code
# 3. Aligning QR-Code
# 4. Secondary Verifying QR-Code
# 5. IF VERIFIED>Decent Altitude
# 6. ELSE>RTL
# 7. RTL
