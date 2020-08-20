import cv2
import numpy as np

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

def getContours(img):
    # for arguments, we need to specify the image and the retrieval method, approximation
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # cv2.RETR_EXTERNAL retrieves the extreme outer contours
    for cnt in contours:
        area = cv2.contourArea(cnt)
        print(area)
        
        # we'll define a min threshold area so that it doesn't detect noise
        if area>500:
            cv2.drawContours(contour_img, cnt, -1, (255, 0, 0), 3)
            perimeter = cv2.arcLength(cnt, True)
            print(perimeter)
            approx = cv2.approxPolyDP(cnt, 0.02*perimeter, True)
            print(len(approx))
            obj_cor = len(approx)
            x, y, w, h = cv2.boundingRect(approx)
            if obj_cor == 3:
                obj_type = 'Tri'
            elif obj_cor == 4:
                aspect_ratio = w/float(h)
                if aspect_ratio>0.95 and aspect_ratio<1.05:
                    # here we are including a deviation of 5%
                    obj_type = 'Square'
                else:
                    obj_type = 'Rect'
            elif obj_cor>4:
                obj_type = "Circle"
            else:
                obj_type = 'None'
            
                
            cv2.rectangle(contour_img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(contour_img, obj_type, (x+(w//2)-10, y+(h//2)-10), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 0), 2)
    
path = '/Users/Lenovo/Desktop/shapes.png'
img = cv2.imread(path)
contour_img = img.copy()

gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur_img = cv2.GaussianBlur(gray_img, (7,7), 1)
canny_img = cv2.Canny(blur_img, 50, 50)

getContours(canny_img)

blank_img = np.zeros_like(img)
stack_img = stackImages(0.5, ([img, gray_img, blur_img], [canny_img, contour_img, blank_img]))


cv2.imshow('Shapes', stack_img)
cv2.waitKey(0)