#import libraries
import cv2, time, threading
from pyzbar import pyzbar
from ast import literal_eval

from cv.Verified import Verified
# from Verified import Verified
# from multiprocessing import Process

verified = Verified() #inisiasi Objek Verified sebagai verified

font = cv2.FONT_HERSHEY_DUPLEX
color_green = 0,255,0
color_red   = 0,0,255
color_white = 255,255,255
#=======================================================CAMERA SETTINGs
camera = cv2.VideoCapture(0)                            #Setup Camera Capture
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)               #Set Lebar FRAME
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)              #Set Tinggi FRAME
cam_width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))   #Get Lebar FRAME
cam_height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)) #Get Tinggi FRAME

#=======================================================Fungsi baca QR

def read_qrcodes(frame):
    verified.x = verified.y = None
    qrCodes = pyzbar.decode(frame)
    center_dist_x=center_dist_y= None

    for qrcode in qrCodes: #UNTUK SETIAP QRCODE YANG ADA DI DALAM FRAME (Looping...)
        pos_x, pos_y , lebar, tinggi = qrcode.rect #posisi qrcode relative terhadap frame

        #Hitung posisi tengah QR
        mid_pos_x = int(pos_x+(lebar/2))
        mid_pos_y = int(pos_y+(tinggi/2))

        qrcode_data = qrcode.data.decode('utf-8')
        qr_dict=id=lat=lon=None
        try:
            qr_dict = literal_eval(qrcode_data) #Menerjemahkan data QR sebagai Python Dictionary
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

            #print(center_dist_x,center_dist_y)
            if abs(verified.x)<50 and abs(verified.y)<50:
                cv2.putText(frame, "ALIGNMENT>>"+str(mid_pos_x)+", "+str(mid_pos_y), (10, int(cam_height-40)), font, 0.5, color_green, 1)
            else:
                cv2.putText(frame, "ALIGNMENT>>"+str(mid_pos_x)+", "+str(mid_pos_y), (10, int(cam_height-40)), font, 0.5, color_red, 1)

        else:
            cv2.putText(frame, id+", lat: "+lat+", lon: "+lon, (pos_x + 6, pos_y - 6), font, 0.5, color_red, 1)
            cv2.rectangle(frame, (pos_x, pos_y),(pos_x+lebar, pos_y+tinggi), color_red, 2)
        
    return frame

def init(v=None, id=None):
    global vehicle              #Inisiasi objek Vehicle sebagai global variable
    vehicle = v                 #Set param v(objek vehicle) dari main.py sebagai vehicle
    verified.id=id              #Set param id(id QR) dari main.py sebagai id pada objek verified

    print("QR Scanner Start...")
    esc, frame = camera.read()  #Capture Image dari kamera
    
    # alignment = threading.Thread(target=align) #Threading agar fungsi align dapat berjalan di latar belakang
    # alignment.daemon = True
    # alignment.start()
#    alignment.join()

    while esc:
        esc, frame = camera.read()
        frame = cv2.flip(frame,1)
        frame = read_qrcodes(frame)
        #x,y koordinat barcode terhadap frame

        cv2.rectangle(frame, (int(cam_width/2-100),int(cam_height/2-100)), (int(cam_width/2+100),int(cam_height/2+100)), color_green, 2) #garis bantu center camera
        cv2.putText(frame, "Frame: "+ str(cam_width)+"x" + str(cam_height),(10,20),font, 0.5, color_white, 1) #resolusi frame
        cv2.imshow('QR Finder!!!', frame)
        
        if cv2.waitKey(1) and verified.x and verified.y and abs(verified.x)<50 and abs(verified.y)<50:
            break
    
    camera.release()
    cv2.destroyAllWindows()
