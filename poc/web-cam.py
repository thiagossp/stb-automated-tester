import cv2
import pytesseract
import numpy as np
import re

# regular expression
reNumber = re.compile("[0-9]+")
reClock = re.compile("[0-9]{2}:{1}[0-9]{2}:{1}[0-9]{2}")
reText = re.compile("[a-zA-Z0-9 ]+")

# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
#thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

def scren_text():
    font = cv2.FONT_HERSHEY_SIMPLEX
    #font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 3, 8) #Creates a font
    x = 10 #position of text
    y = 400 #position of text
    cv2.putText(frame,"TESTE", (x,y), cv2.FONT_HERSHEY_TRIPLEX, 2, 255)

def plotImageArea():
    x1 = 10
    x2 = int(videoHeight) - 200

    y1 = 10
    y2 = int(videoWidth) - 10

    #ref border_top
    frame[x1, y1:y2] = 255
    #ref border_button
    frame[x2, y1:y2] = 255
    #ref border_left
    frame[x1:x2, y1] = 255
    #ref border_right
    frame[x1:x2, y2] = 255

    return frame[x1:x2, y1:y2]

def plotChannelNameArea():
    x1 = int(videoHeight) - 170
    x2 = int(videoHeight) - 120

    y1 = 250
    y2 = 600     

    #ref border_top
    frame[x1, y1:y2] = 255
    #ref border_button
    frame[x2, y1:y2] = 255
    #ref border_left
    frame[x1:x2, y1] = 255
    #ref border_right
    frame[x1:x2, y2] = 255

    return frame[x1:x2, y1:y2]

def plotChannelNumberArea():
    x1 = int(videoHeight) - 170
    x2 = int(videoHeight) - 120

    y1 = 180
    y2 = 248     

    #ref border_top
    frame[x1, y1:y2] = 255
    #ref border_button
    frame[x2, y1:y2] = 255
    #ref border_left
    frame[x1:x2, y1] = 255
    #ref border_right
    frame[x1:x2, y2] = 255

    return frame[x1:x2, y1:y2]    

def plotClockArea():
    x1 = int(videoHeight) - 170
    x2 = int(videoHeight) - 130

    y1 = int(videoWidth) - 100
    y2 = int(videoWidth) - 10

    #ref border_top
    frame[x1, y1:y2] = 255
    #ref border_button
    frame[x2, y1:y2] = 255
    #ref border_left
    frame[x1:x2, y1] = 255
    #ref border_right
    frame[x1:x2, y2] = 255

    return frame[x1:x2, y1:y2]     

def checkBlackScreen():
    gray_version = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
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

    cv2.imwrite("./imagens/frame%d.jpg" % fileName, gray) #Save frame to img
    
    if regularExpression.search(text[0]) is not None:
        return(regularExpression.search(text[0]).group(0))
    return        

#videoCapture = cv2.VideoCapture(0)
videoCapture = cv2.VideoCapture("MVI_8683.MOV")

length = int(videoCapture.get(cv2.CAP_PROP_FRAME_COUNT))
print( length )

videoWidth = videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)
videoHeight = videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(videoWidth , " x " , videoHeight)

frameCountDelta = 0  
lastLog = ''  

while (1):    
    ret, frame = videoCapture.read()

    frameCount = videoCapture.get(cv2.CAP_PROP_POS_FRAMES)
    frameCountDelta += 1

    #cv2.imshow("Video", frame)
    
    ref = plotImageArea()
    channelNameArea = plotChannelNameArea()
    channelNumberArea = plotChannelNumberArea()
    clockArea = plotClockArea()

    #blackScreen()
    if frameCountDelta >= 100:
        frameCountDelta = 0
        chanelName = getOcr(channelNameArea, reText, frameCount)
        if chanelName is not None:
            chanelNumber = getOcr(channelNumberArea, reNumber, frameCount + 1)
            if chanelNumber is not None:
                clock = getOcr(clockArea, reClock, frameCount + 2)
                if chanelNumber is not None:
                    blackScreen = checkBlackScreen()
                    if lastLog != (str(chanelNumber) + " - " + str(chanelName) + ' - Black Screen: ' + str(blackScreen) + ' - Clock: ' + str(clock)):
                        lastLog = str(chanelNumber) + " - " + str(chanelName) + ' - Black Screen: ' + str(blackScreen) + ' - Clock: ' + str(clock)
                        print(lastLog)

    #(b, g, r) = frame[200, 200] #Get color from this position
    #frame[400:470, 10:630] = (255, 0, 0)
    #frame[190:210, 190:210] = (0, 0, 255) #Reference point to get color
    #frame[10:90, 10:90] = (b, g, r)

    #if (b < 5 and g < 5 and r < 5) :
    #    print("Black pixel")

    cv2.imshow('frame',frame)

    key = cv2.waitKey(30) & 0xff
    if key == 27:
        break

videoCapture.realse()
cv2.destroyAllWindows()