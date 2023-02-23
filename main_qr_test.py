from __future__ import print_function
import time, math, threading
# Dronekit Import

import koneksi
vehicle = koneksi.vehicle

from cv import qr_target_identifier, qr_destination

verified = qr_destination.verified

print("\n\nVerifikasi Misi...")
identified_qr_dict = None

while identified_qr_dict is None:
    identified_qr_dict= qr_target_identifier.main()
    time.sleep(1)
print(identified_qr_dict)

qr_destination.main(vehicle, str(identified_qr_dict['id']))

#qrs.init(vehicle=None, str(identifiedQRDict['id']))

# Sequence:
# 1. Scan QR-Code
# 2. Verifying QR-Code
# 3. Aligning QR-Code
# 4. Secondary Verifying QR-Code
# 5. IF VERIFIED>Decent Altitude
# 6. ELSE>RTL
# 7. RTL
