import cv2
import webbrowser

cap= cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()

while True:
    _,img = cap.read()
    data, one, _=detector.detectAndDecode(img)
    if data:
        a=data
        print(a)
        break
    cv2.imshow('qrcodescanner app', img)
    if cv2.waitKey(1)==ord('q'):
        break

# b = webbrowser.open(str(a))
# print(str(a))
# cap.release(a)
# cv2.destroyAllWindows()
    
    
    
    # https://pyimagesearch.com/2018/05/21/an-opencv-barcode-and-qr-code-scanner-with-zbar/
    
    # https://towardsdatascience.com/building-a-barcode-qr-code-reader-using-python-360e22dfb6e5