#import libraries
import cv2, time, threading
from pyzbar import pyzbar
from ast import literal_eval
from dronekit import VehicleMode

from cv.Verified import Verified
# from Verified import Verified
# from multiprocessing import Process

verified = Verified()

font = cv2.FONT_HERSHEY_DUPLEX
color_green = 0,255,0
color_red   = 0,0,255
color_white = 255,255,255
#=======================================================CAMERA SETTINGs
camera = cv2.VideoCapture(0)
# camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
# camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 180)
cam_width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
cam_height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

#=======================================================Fungsi baca QR

def align():
    mission_passed = False
    while mission_passed is False:
        if verified.x:
            vehicle.channels.overrides['3'] = 1500
            vehicle.mode = VehicleMode('LOITER')
            print("Mode: "+vehicle.mode.name)
            print("Emulating Joystick Control...")
            
            while verified.x and verified.y:
                if verified.x>50 or verified.x<-50 or verified.y>50 or verified.y<-50:
                    print(str(verified.x)+','+str(verified.y))
                    if verified.x>50: #kiri
                        # vehicle.channels.overrides['1']=vehicle.channels['1']-200
                        vehicle.channels.overrides['1']=1300
                        print('kiri')
                    if verified.x<-50: #kanan
                        vehicle.channels.overrides['1']=1700
                        print('kanan')
                    if verified.y>50: #mundur
                        vehicle.channels.overrides['2']=1300
                        print('mundur')
                    if verified.y<-50: #maju
                        vehicle.channels.overrides['2']=1700            
                        print('maju')
                time.sleep(1)
                # break
            vehicle.channels.overrides = {}
            # vehicle.mode = VehicleMode('GUIDED')
            mission_passed = True
            print(mission_passed)
            break
        else:
            print("Looking for QRCode...")
            time.sleep(1)

def align2():
    mission_passed = False
    vehicle.mode = VehicleMode('LOITER')
    print("Mode: "+vehicle.mode.name)
    print("Emulating Joystick Control...")
    while mission_passed is False:
        vehicle.channels.overrides['3'] = 1500
        while verified.x and verified.y:
            print(str(verified.x)+','+str(verified.y))
            if verified.x<50 and verified.x>-50 and verified.y<50 and verified.y>-50:
                vehicle.channels.overrides = {}
                # vehicle.mode = VehicleMode('GUIDED')
                mission_passed = True
                print(mission_passed)
            elif verified.x>50: #kiri
                # vehicle.channels.overrides['1']=vehicle.channels['1']-200
                vehicle.channels.overrides['1']=1300
                print('kiri')
            elif verified.x<-50: #kanan
                vehicle.channels.overrides['1']=1700
                print('kanan')
            elif verified.y>50: #mundur
                vehicle.channels.overrides['2']=1300
                print('mundur')
            elif verified.y<-50: #maju
                vehicle.channels.overrides['2']=1700            
                print('maju')
            time.sleep(1)
        else:
            print("Looking for QRCode...")
            vehicle.channels.overrides = {}
            vehicle.channels.overrides['3'] = 1500
            time.sleep(1)

def read_barcodes(frame):
    verified.x = verified.y = None
    barcodes = pyzbar.decode(frame)
    center_dist_x=center_dist_y= None
    #Menampilkan properties untuk setiap QRcode
    for barcode in barcodes:
        pos_x, pos_y , lebar, tinggi = barcode.rect
        # print(barcode.data)
        mid_pos_x = int(pos_x+(lebar/2))
        mid_pos_y = int(pos_y+(tinggi/2))

        barcode_info = barcode.data.decode('utf-8')
        qr_dict=id=lat=lon=None
        try:
            qr_dict = literal_eval(barcode_info)
            id=str(qr_dict['id'])
            lat=str(qr_dict['lat'])
            lon=str(qr_dict['lon'])
        except:
            id = "QR Tidak dikenal"
            lat =lon = ""
            # print("QR tidak dikenal")
        
        if id==verified.key:
            #Verified QR Detetcted
            cv2.putText(frame, id+", lat: "+lat+", lon: "+lon, (pos_x + 6, pos_y - 6), font, 0.5, color_green, 1)
            cv2.putText(frame,
                        "x :"+ str(pos_x)+"y :" + str(pos_y),
                        (pos_x+6, pos_y+tinggi+20), 
                        font, 
                        0.5, 
                        color_green, 1)

            cv2.rectangle(frame, (pos_x, pos_y),(pos_x+lebar, pos_y+tinggi), color_green, 2)
            cv2.circle(frame, (mid_pos_x, mid_pos_y), 20, color_green, 2)
            cv2.putText(frame, "VERIFIED>>"+id, (10, int(cam_height-20)), font, 0.5, color_green, 1)

            # ALIGNMENT
            center_dist_x = int(cam_width/2-mid_pos_x)
            center_dist_y = int(cam_height/2-mid_pos_y)

            verified.x = center_dist_x
            verified.y = center_dist_y

            #print(center_dist_x,center_dist_y)
            if abs(center_dist_x)<50 and abs(center_dist_y)<50:
                cv2.putText(frame, "ALIGNMENT>>"+str(mid_pos_x)+", "+str(mid_pos_y), (10, int(cam_height-40)), font, 0.5, color_green, 1)
            else:
                cv2.putText(frame, "ALIGNMENT>>"+str(mid_pos_x)+", "+str(mid_pos_y), (10, int(cam_height-40)), font, 0.5, color_red, 1)

        else:
            cv2.putText(frame, id+", lat: "+lat+", lon: "+lon, (pos_x + 6, pos_y - 6), font, 0.5, color_red, 1)
            cv2.rectangle(frame, (pos_x, pos_y),(pos_x+lebar, pos_y+tinggi), color_red, 2)
        
    returnValue = [frame, center_dist_x, center_dist_y]
    return returnValue

def init(v=None, key=None):
    global vehicle
    vehicle = v
    verified.key=key
    print("QR Scanner Start...")
    esc, frame = camera.read()
    
    alignment = threading.Thread(target=align2)
    alignment.daemon = True
    alignment.start()
#    alignment.join()

    while esc:
        esc, frame = camera.read()
        frame = cv2.flip(frame,1)
        frame,x,y = read_barcodes(frame)
        #x,y koordinat barcode terhadap frame
#        if x:
#            print(x,y)
            # if x>50:
            #     geser('kiri')

            # elif x<-50:
            #    geser('kanan')

            # if y>50:
            #    geser('mundur')
            # elif y<-50:
            #     geser('maju')
                # thread = threading.Thread(target=geser('maju'))
                # thread.start

        cv2.rectangle(frame, (0, 0),(int(cam_width), int(cam_height)), color_white, 2) #garis tepi
        cv2.rectangle(frame, (int(cam_width/2-100),int(cam_height/2-100)), (int(cam_width/2+100),int(cam_height/2+100)), color_green, 2) #garis bantu center camera
        cv2.putText(frame, "Frame: "+ str(cam_width)+"x" + str(cam_height),(10,20),font, 0.5, color_white, 1) #resolusi frame
        cv2.imshow('QR Finder!!!', frame)
        
        if cv2.waitKey(1) and x and y and abs(x)<50 and abs(y)<50:
            break


        # #IF ESC GAK DIPENCET >> CAM JALAN TEROS
        # if cv2.waitKey(1) & 0xFF == 27:
        #     break
    camera.release()
    cv2.destroyAllWindows()

# if __name__ == '__main__':
#     init(key='Bondan Eka Nugraha')
