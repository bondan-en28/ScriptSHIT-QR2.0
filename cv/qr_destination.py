#import libraries
import cv2
from pyzbar import pyzbar
from ast import literal_eval

from cv.Verified import Verified

verified = Verified() #inisiasi Objek Verified sebagai verified

cam_width = cam_height = 0

font = cv2.FONT_HERSHEY_DUPLEX
color_green = 0,255,0
color_red   = 0,0,255
color_white = 255,255,255

#=======================================================Fungsi baca QR

def readQRs(frame):
    verified.x = verified.y = None
    qr_codes = pyzbar.decode(frame)

    for qr_code in qr_codes: #UNTUK SETIAP QRCODE YANG ADA DI DALAM FRAME (Looping...)
        pos_x, pos_y , lebar, tinggi = qr_code.rect #posisi qrcode relative terhadap frame

        #Hitung posisi tengah QR
        mid_pos_x = int(pos_x+(lebar/2))
        mid_pos_y = int(pos_y+(tinggi/2))

        qr_data = qr_code.data.decode('utf-8')
        qr_dict=id=lat=lon=None
        try:
            qr_dict = literal_eval(qr_data) #Menerjemahkan data QR sebagai Python Dictionary
            id=str(qr_dict['id'])
            lat=str(qr_dict['lat'])
            lon=str(qr_dict['lon'])
        except:
            pass #Lewati apabila QR tidak dikenali
        
        if id is not None and id==verified.id: #Jika ID didalam QR sama dengan ID yang dicari, maka:

            cv2.putText(frame, "QR-ID: "+id,
                        (pos_x + 6, pos_y - 6), font, 0.5, color_green, 1) #Tuliskan ID
            cv2.putText(frame,
                        "x:"+ str(pos_x)+"y:" + str(pos_y),
                        (pos_x+6, pos_y+tinggi+20), 
                        font, 
                        0.5, 
                        color_green, 1) 

            cv2.rectangle(frame, (pos_x, pos_y),(pos_x+lebar, pos_y+tinggi), color_green, 2)#Beri tanda hijau pada tepian QR
            cv2.putText(frame, "IDENTIFIED>>"+id, (10, int(cam_height-20)), font, 0.5, color_green, 1)

            # ALIGNMENT
            verified.x = int(cam_width/2-mid_pos_x) #Jarak QR relative terhadap tengah Frame (sumbu x)
            verified.y = int(cam_height/2-mid_pos_y) #Jarak QR relative terhadap tengah Frame (sumbu y)

            if abs(verified.x)<50 and abs(verified.y)<50:
                cv2.putText(frame, "ALIGNMENT>>"+str(mid_pos_x)+", "+str(mid_pos_y), (10, int(cam_height-40)), font, 0.5, color_green, 1)
            else:
                cv2.putText(frame, "ALIGNMENT>>"+str(mid_pos_x)+", "+str(mid_pos_y), (10, int(cam_height-40)), font, 0.5, color_red, 1)

        else:
            cv2.putText(frame, qr_data, (pos_x + 6, pos_y - 6), font, 0.5, color_red, 1)
            cv2.rectangle(frame, (pos_x, pos_y),(pos_x+lebar, pos_y+tinggi), color_red, 2)
        
    return frame

def main(v=None, id=None):
    #=======================================================CAMERA SETTINGs
    camera = cv2.VideoCapture(0)                            #Setup Camera Capture
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)               #Set Lebar FRAME
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)              #Set Tinggi FRAME

    global cam_width, cam_height
    cam_width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))   #Get Lebar FRAME
    cam_height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)) #Get Tinggi FRAME

    global vehicle              #Inisiasi objek Vehicle sebagai global variable
    vehicle = v                 #Set param v(objek vehicle) dari main.py sebagai vehicle
    verified.id=id              #Set param id(id QR) dari main.py sebagai id pada objek verified

    print("QR Scanner Start...")
    ret, frame = camera.read()  #Capture Image dari kamera

    while ret:
        ret, frame = camera.read()
        frame = readQRs(frame)
        #x,y koordinat qrcode terhadap frame

        cv2.rectangle(frame, (int(cam_width/2-100),int(cam_height/2-100)), (int(cam_width/2+100),int(cam_height/2+100)), color_green, 2) #garis bantu center camera
        cv2.putText(frame, "Frame: "+ str(cam_width)+"x" + str(cam_height),(10,20),font, 0.5, color_white, 1) #resolusi frame
        cv2.imshow('Target Finder', frame)
        
        if cv2.waitKey(1) and verified.confirmed:
            break
    
    camera.release()
    print("Released Camera.")
    cv2.destroyAllWindows()
