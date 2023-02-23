#import libraries
import cv2,time
from pyzbar import pyzbar
from ast import literal_eval

cam_width = cam_height = 0

font = cv2.FONT_HERSHEY_DUPLEX
color_green = 0,255,0
color_red   = 0,0,255
color_white = 255,255,255
color_pink = 153,51,255


def read_barcodes(frame):
    barcodes = pyzbar.decode(frame)
    recognizedQRCount = 0
    identifiedQRDict= recognizedQRDict = None

    for barcode in barcodes: #UNTUK SETIAP QRCODE YANG ADA DI DALAM FRAME
        x, y , w, h = barcode.rect #KOORDINAT UNTUK SETIAP SATU QRCODE

        barcode_info = barcode.data.decode('utf-8') #DECODE DATA YANG ADA DI DALAM QRCODE

        qr_dict=id=lat=lon=None #INISIASI ID, LAT, LON, KE NULL SEBELUM DICOBA DITERJEMAHKAN
        try: #MENCOBA MENGUBAH DATA MENJADI PYTHON DICTIONARY
            qr_dict = literal_eval(barcode_info)
            id=str(qr_dict['id'])
            lat=str(qr_dict['lat'])
            lon=str(qr_dict['lon'])
        except:
            pass #LEWATI APABILA TIDAK DITEMUKAN DATA DENGAN STRUKTUR YANG SESUAI
        
        if id and lat and lon is not None:
            cv2.rectangle(frame, (x, y),(x+w, y+h), color_green, 2)
            recognizedQRDict = qr_dict
            recognizedQRCount+=1
        else:
            cv2.rectangle(frame, (x, y),(x+w, y+h), color_red, 2)

        cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 0.5, color_pink, 1)
    
    if recognizedQRCount<1:
        cv2.putText(frame, "Waiting for QR...", (10, int(cam_height-20)), font, 0.5, color_green, 1)
    if recognizedQRCount==1:
        cv2.putText(frame, "QR Identified>>"+str(recognizedQRDict['id']), (10, int(cam_height-20)), font, 0.5, color_green, 1)
        identifiedQRDict = recognizedQRDict
    elif recognizedQRCount>1:
        cv2.putText(frame, "Multiple QR's Detected, It's CONFUSING!", (10, int(cam_height-20)), font, 0.5, color_green, 1)

    returnValue = [frame, identifiedQRDict]
    return returnValue

def main():
    camera = cv2.VideoCapture(1)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    cam_width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
    cam_height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

    ret, frame = camera.read()
    identifiedCounter = 0
    identifiedQRDict = None
    print("Here main function @qr_target_identifier.py")

    while ret:
        ret, frame = camera.read()
        frame, identifiedQRDict= read_barcodes(frame)
        if identifiedQRDict is not None:
            identifiedCounter+=1
            cv2.line(frame, (0, int(cam_height-5)), (int(identifiedCounter/50*cam_width) , int(cam_height-5)), color_green, 3)
        cv2.putText(frame, "Frame: "+ str(cam_width)+"x" + str(cam_height),(10,20),font, 0.5, color_green, 1) #resolusi frame
        cv2.imshow('Target Identifier', frame)
        if cv2.waitKey(1) & identifiedCounter>50:
            break

    camera.release()
    print("Released Camera.")
    cv2.destroyAllWindows()
    return identifiedQRDict
