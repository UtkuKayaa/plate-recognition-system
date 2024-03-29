
import pytesseract
import cv2
import os
import numpy as np
from skimage import io

img = io.imread("C:\\plateDetectionFinal\\plateImages\\scaned_img0.jpg")
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
gray = cv2.resize( gray, None, fx = 3, fy = 3, interpolation = cv2.INTER_CUBIC)
blur = cv2.GaussianBlur(gray, (5,5), 0)
gray = cv2.medianBlur(gray, 3)


ret, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
cv2.imshow("Otsu", thresh)
cv2.waitKey(0)
rect_kern = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))

  
dilation = cv2.dilate(thresh, rect_kern, iterations = 1)

try:
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
except:
    ret_img, contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
sorted_contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[0])


im2 = gray.copy()

plate_num = ""

for cnt in sorted_contours:
    x,y,w,h = cv2.boundingRect(cnt)
    height, width = im2.shape
    
    
   
 
    if height / float(h) > 6: continue
    ratio = h / float(w)
    
    if ratio < 1.5: continue
    
    area = h * w
  
    if width / float(w) > 15: continue
  
    if area < 100: continue
  
    rect = cv2.rectangle(im2, (x,y), (x+w, y+h), (0,255,0),2)
    roi = thresh[y-3:y+h+7, x-3:x+w+6]
    roi = cv2.bitwise_not(roi)
    roi = cv2.medianBlur(roi, 5)
    cv2.imshow("ROI", roi)
    cv2.waitKey(0)
    text = pytesseract.image_to_string(roi, config='-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ --psm 8 --oem 3')
    plate_num += text
   

print(plate_num)           
    
cv2.imshow("Character's Segmented", im2)
cv2.waitKey(0)
cv2.destroyAllWindows()