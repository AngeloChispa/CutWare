import cv2
import numpy as np

from contours import Contours;

def processImage(image):
    # image = cv2.resize(image, (200, 1000))
    image = cv2.bilateralFilter(image, 30, 75, 75)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    image = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY_INV,1055, 9
    )

    image = cv2.medianBlur(image, 9)
    image = cv2.medianBlur(image, 9)
    image = cv2.medianBlur(image, 9)
    
    #image = cv2.blur(image, (5, 5))
    return image

def drawLines(image, height, width):
    color = (0, 0, 0)  
    tick = 2  
    cv2.line(image, (0, 0), (0, height), color, tick)
    cv2.line(image, (width - 1, 0), (width - 1, height), color, tick)

def recoverEdges(image):
    edged = cv2.Canny(image, 30, 200);
    return edged;

def resizeImage(image):
    return cv2.resize(image,(1000,1000));

def contourList(edged):
    list = []
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE);
    for i in range(len(contours)):
        object = Contours(contours[i], hierarchy[0][i])
        list.append(object)
    return list   

def maxContour(list):
    contours = []
    for i in list:
        approx = tests(i)
        #if len(approx) == 4:
        contours.append(i.getContour());
    max_contour =  max(contours, key=cv2.contourArea)
    for i in list:
        if np.array_equal(max_contour, i.getContour()):
            return i;  

def drawSquare(contour, image):
    x, y, w, h = cv2.boundingRect(contour)
    #cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return image[y:y+h, x:x+w]

def tests(max):
    epsilon = 0.02 * cv2.arcLength(max.getContour(), True);
    approx = cv2.approxPolyDP(max.getContour(), epsilon, True);
    return approx;

'''
image = cv2.imread("don.jpg");

image = cv2.imread("mapa.png");
height, width = image.shape[:2]
if(height>width):
    image = cv2.resize(image, (500,1000))
else:
    image = cv2.resize(image, (width*2,height*2))

height, width = image.shape[:2]
drawLines(image,height,width)

process = processImage(image);
edged = recoverEdges(process);
list = contourList(edged);
print(len(list))

max = maxContour(list);
approx = tests(max);
#print(len(approx))
#print(max.getHierarchy())
#max.setPosition(list);
""" max.setSons(list);
sons = max.getSons(); """
""" for i in sons:
    print(i.getHierarchy())
    image = cv2.drawContours(image,[i.getContour()],-1,(0,255,0),2); """
    
#print(list[938].getHierarchy())   
#image = cv2.drawContours(image,[list[610].getContour()],-1,(255,0,0),2);
image = cv2.drawContours(image,[max.getContour()],-1,(0,0,255),2);
drawSquare(max.getContour(),image)

cv2.imshow("Imagen", image);
cv2.imshow("Contornos", edged);

cv2.waitKey(0);
cv2.destroyAllWindows();
'''