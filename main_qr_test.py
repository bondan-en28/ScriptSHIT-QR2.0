from __future__ import print_function
import time, math, threading
# Dronekit Import

import koneksi
vehicle = koneksi.vehicle

from cv import qr_destination, qr_target_identifier

verified = qr_destination.verified

print("\n\nVerifikasi Misi...")
identifiedQRDict = None

while identifiedQRDict is None:
    identifiedQRDict= qr_target_identifier.main()
print(identifiedQRDict)

qr_destination.init(vehicle, str(identifiedQRDict['id']))

#qrs.init(vehicle=None, str(identifiedQRDict['id']))

# Sequence:
# 1. Scan QR-Code
# 2. Verifying QR-Code
# 3. Aligning QR-Code
# 4. Secondary Verifying QR-Code
# 5. IF VERIFIED>Decent Altitude
# 6. ELSE>RTL
# 7. RTL
