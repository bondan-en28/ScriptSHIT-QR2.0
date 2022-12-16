# Importing library
import qrcode
 
# Data to be encoded
#data = 'Bondan Eka Nugraha'
#data = {"id": "001001001","pos": 50224}
data = {'id': 'Bondan Eka Nugraha',
        'lat':-7.069108, 
        'lon':110.366521}
# Encoding data using make() function
img = qrcode.make(data)
 
# Saving as an image file
img.save('QR-'+str(data['id'])+'.png')