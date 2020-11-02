import cv2
import pytesseract
import numpy as np
import re

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
    x1 = 120
    x2 = int(videoHeight) - 250

    y1 = 300
    y2 = int(videoWidth) - 300

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
    x1 = int(videoHeight) - 390
    x2 = int(videoHeight) - 330

    y1 = 400
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
    x1 = int(videoHeight) - 480
    x2 = int(videoHeight) - 420

    y1 = 410
    y2 = 440     

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

def getChannelName(channelArea):
    gray_version = cv2.cvtColor(channelArea, cv2.COLOR_BGR2GRAY)
    channel = pytesseract.image_to_string(gray_version)
    channel = channel.split("\n")
    
    #pattern = re.compile("\[*\]*\w+")
    if channel[0] is not None:
        return channel[0]
    return

def getChannelNumber(channelArea, frameCount):
    gray = get_grayscale(channelArea)
    thresh = thresholding(gray)
    custom_config = r'--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789 --psm 6'
    channel = pytesseract.image_to_string(thresh, config=custom_config)[0]
    #cv2.imwrite("frame%d.jpg" % frameCount, gray_version) #Save frame to img

    pattern = re.compile("[A-Za-z0-9]+")

    if pattern.fullmatch(channel) is not None:
        return channel
    return

#videoCapture = cv2.VideoCapture(0)
videoCapture = cv2.VideoCapture("video3.mp4")

length = int(videoCapture.get(cv2.CAP_PROP_FRAME_COUNT))
print( length )

videoWidth = videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)
videoHeight = videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(videoWidth , " x " , videoHeight)

frameCountDelta = 0    

while (1):    
    ret, frame = videoCapture.read()

    frameCount = videoCapture.get(cv2.CAP_PROP_POS_FRAMES)
    frameCountDelta += 1

    #cv2.imshow("Video", frame)
    
    ref = plotImageArea()
    channelNameArea = plotChannelNameArea()
    channelNumberArea = plotChannelNumberArea()
    #blackScreen()
    if frameCountDelta >= 50:
        frameCountDelta = 0
        chanelName = getChannelName(channelNameArea)
        if chanelName is not None:
            chanelNumber = getChannelNumber(channelNumberArea, frameCount)
            if chanelNumber is not None:
                blackScreen = checkBlackScreen()
                print(chanelNumber, " - ", chanelName, ' - Black Screen:', blackScreen)

    (b, g, r) = frame[200, 200] #Get color from this position
    #frame[400:470, 10:630] = (255, 0, 0)
    frame[190:210, 190:210] = (0, 0, 255) #Reference point to get color
    frame[10:90, 10:90] = (b, g, r)

    #if (b < 5 and g < 5 and r < 5) :
    #    print("Black pixel")

    cv2.imshow('frame',frame)

    key = cv2.waitKey(30) & 0xff
    if key == 27:
        break

videoCapture.realse()
cv2.destroyAllWindows()