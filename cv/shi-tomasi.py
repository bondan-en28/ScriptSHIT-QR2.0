# Python program to illustrate 
# corner detection with 
# Shi-Tomasi Detection Method
    
# organizing imports 
import cv2
import numpy as np
#%matplotlib inline
  
# path to input image specified and  
# image is loaded with imread command
camera = cv2.VideoCapture(0)
ret, frame = camera.read()

while ret:
    ret, frame = camera.read()
  
    # convert image to grayscale
    gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  
    # Shi-Tomasi corner detection function
    # We are detecting only 100 best corners here
    # You can change the number to get desired result.
    corners = cv2.goodFeaturesToTrack(gray_img, 100, 0.01, 10)
  
    # convert corners values to integer
    # So that we will be able to draw circles on them
    corners = np.intp(corners)
  
    # draw red color circles on all corners
    for i in corners:
        x, y = i.ravel()
        cv2.circle(frame, (x, y), 3, (255, 0, 0), -1)
  
    # resulting image
    #plt.imshow(img)
    cv2.imshow('Corner Detector', frame)

    # De-allocate any associated memory usage  
    if cv2.waitKey(1) & 0xFF == 27:
        break

camera.release()
cv2.destroyAllWindows()
