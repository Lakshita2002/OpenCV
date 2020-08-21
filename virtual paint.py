import cv2
import numpy as np

web_var = cv2.VideoCapture(0)
web_var.set(3, 640)
web_var.set(4, 480)

def findColor(img, myColor, customColors):
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    new_points = []
    for color in myColor:
        
        lower_limit = np.array(color[0:3])
        upper_limit = np.array(color[3:6])
        mask = cv2.inRange(hsv_img, lower_limit, upper_limit)
        x, y = getContours(mask)
        cv2.circle(final_img, (x, y), 10, customColors[count], cv2.FILLED)
        if x!=0 and y!=0:
            new_points.append([x, y, count])
        count += 1
    return new_points

def getContours(img):
    # for arguments, we need to specify the image and the retrieval method, approximation
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    # cv2.RETR_EXTERNAL retrieves the extreme outer contours
    for cnt in contours:
        area = cv2.contourArea(cnt)
        
        # we'll define a min threshold area so that it doesn't detect noise
        if area>500:
            #cv2.drawContours(final_img, cnt, -1, (255, 0, 0), 3)
            perimeter = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*perimeter, True)
            x, y, w, h = cv2.boundingRect(approx)
    # we want to write from the tip rather than the center
    # so we'll send the tip
    return (x+(w//2), y)

def drawOnCanvas(points, customColors):
    for point in points:
        cv2.circle(final_img, (point[0], point[1]), 10, customColors[point[2]], cv2.FILLED)
  
            
myColors = [[85, 83, 153, 159, 255, 255], 
            [143, 97, 0, 179, 255, 255],  
            [22, 43, 155, 67, 255, 255]]  

customColors = [[255, 178, 102], [102, 102, 255], [51, 255, 255]]

points = []


while True:
    det, img = web_var.read()
    final_img = img.copy()
    new_points = findColor(img, myColors, customColors)
    if len(new_points)!=0:
        for newP in new_points:
            points.append(newP)
            
    if len(points)!=0:
        drawOnCanvas(points, customColors)
    cv2.imshow('Video', final_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
   
cv2.destroyAllWindows()
web_var.release() 