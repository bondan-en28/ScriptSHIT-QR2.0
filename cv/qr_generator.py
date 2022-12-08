# Importing library
import qrcode
 
# Data to be encoded
data = 'Bondan Eka Nugraha'
 
# Encoding data using make() function
img = qrcode.make(data)
 
# Saving as an image file
img.save('QR.png')