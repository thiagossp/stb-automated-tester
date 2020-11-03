import cv2
import pytesseract
import numpy as np
import re

# video source and info
videoCapture = cv2.VideoCapture("video1.MOV")
length = int(videoCapture.get(cv2.CAP_PROP_FRAME_COUNT))
videoWidth = videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)
videoHeight = videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)

# regular expressions
reNumber = re.compile("[0-9]+")
reClock = re.compile("[0-9]{2}:{1}[0-9]{2}:{1}[0-9]{2}")
reText = re.compile("[a-zA-Z0-9 ]+")

# capture areas
areaChannelName = [int(videoHeight) - 170, int(videoHeight) - 120, 250, 600]
areaChannelNumber = [int(videoHeight) - 170, int(videoHeight) - 120, 180, 248]
areaClockArea = [int(videoHeight) - 170, int(videoHeight) - 130, int(videoWidth) - 100, int(videoWidth) - 10]
areaImageTest = [10, int(videoHeight) - 200, 10, int(videoWidth) - 10]
areaLogo = [int(videoHeight) - 140, int(videoHeight) - 30, 0, 110]

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
# thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

def plotArea(area):
    #border_top
    frame[area[0], area[2]:area[3]] = 255
    #border_button
    frame[area[1], area[2]:area[3]] = 255
    #border_left
    frame[area[0]:area[1], area[2]] = 255
    #border_right
    frame[area[0]:area[1], area[3]] = 255

    return

def getFrameArea(area):
    return frame[area[0]:area[1], area[2]:area[3]]

def checkBlackScreen(area):
    gray_version = cv2.cvtColor(area, cv2.COLOR_BGR2GRAY)
    if np.average(gray_version) > 80 and np.average(gray_version) <100:
        return 'True'
    else:
        return 'False'

def getOcr(image, regularExpression, fileName):
    gray = get_grayscale(image)
    #thresh = thresholding(gray)
    custom_config = r'--psm 7 --oem 3'
    text = pytesseract.image_to_string(gray, config=custom_config)
    text = text.split("\n")
    
    if regularExpression.search(text[0]) is not None:
        return(regularExpression.search(text[0]).group(0))
    return   

def saveFrame(frame, fileName):
    gray = get_grayscale(frame)
    cv2.imwrite("./imagens/frame%d.jpg" % fileName, gray)

def checkLogo(logoReference, logoToTest):
    histogram1 = cv2.calcHist([cv2.imread('logos/frame%d.jpg' % logoReference)], [0], None, [256], [0, 256])

    histogram2 = cv2.calcHist([cv2.imread('imagens/frame%d.jpg' % logoReference)], [0], None, [256], [0, 256])

    c1, c2 = 0, 0

    i = 0 
    while i < len(histogram1) and i < len(histogram2):
        c1 += (histogram1[i] - histogram2[i])**2
        i += 1
    c1 = c1**(1 / 2)
    return(c1)

print( length )
print(videoWidth , " x " , videoHeight)

frameCountDelta = 0  
lastLog = ''  

while (1):    
    ret, frame = videoCapture.read()

    frameCount = videoCapture.get(cv2.CAP_PROP_POS_FRAMES)
    frameCountDelta += 1
    
    plotArea(areaImageTest)
    plotArea(areaChannelName)
    plotArea(areaChannelNumber)
    plotArea(areaClockArea)
    plotArea(areaLogo)

    if frameCountDelta >= 100:
        frameCountDelta = 0
        chanelName = getOcr(getFrameArea(areaChannelName), reText, frameCount)
        if chanelName is not None:
            chanelNumber = getOcr(getFrameArea(areaChannelNumber), reNumber, frameCount + 1)
            if chanelNumber is not None:
                clock = getOcr(getFrameArea(areaClockArea), reClock, frameCount + 2)
                blackScreen = checkBlackScreen(getFrameArea(areaImageTest))
                saveFrame(getFrameArea(areaLogo), int(chanelNumber))
                if lastLog != (str(chanelNumber) + " - " + str(chanelName) + ' - Black Screen: ' + str(blackScreen) + ' - Clock: ' + str(clock)):
                    lastLog = str(chanelNumber) + " - " + str(chanelName) + ' - Black Screen: ' + str(blackScreen) + ' - Clock: ' + str(clock)
                    print(lastLog)

    cv2.imshow('frame',frame)

    key = cv2.waitKey(30) & 0xff
    if key == 27:
        break

videoCapture.realse()
cv2.destroyAllWindows()