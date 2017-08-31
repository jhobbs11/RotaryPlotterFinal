import serial
import time
from time import sleep
import struct
from PIL import Image


def piPrint(img):

    def secureSendInt(x):
        goCheck = 0
        correctCheck = 0
        while correctCheck != b'$':
            while goCheck != b'!':
                goCheck = myPort.read(1)
            if x < 10:
                onesDigit = x
                digitCheck = int(x%3)
                myPort.write(b'1')
                myPort.write(str(onesDigit).encode('utf-8'))
                myPort.write(str(digitCheck).encode('utf-8'))
            elif x < 100:
                onesDigit = int(x%10)
                tensDigit = int((x-onesDigit)/10)
                digitCheck = int((onesDigit + tensDigit)%3)
                myPort.write(b'2')
                myPort.write(str(onesDigit).encode('utf-8'))
                myPort.write(str(tensDigit).encode('utf-8'))
                myPort.write(str(digitCheck).encode('utf-8'))
            elif x < 1000:
                onesDigit = int(x%10)
                tensDigit = int(((x-onesDigit)%100)/10)
                hundredsDigit = int((x-onesDigit-(tensDigit*10))/100)
                digitCheck = int((onesDigit + tensDigit + hundredsDigit)%3)
                myPort.write(b'3')
                myPort.write(str(onesDigit).encode('utf-8'))
                myPort.write(str(tensDigit).encode('utf-8'))
                myPort.write(str(hundredsDigit).encode('utf-8'))
                myPort.write(str(digitCheck).encode('utf-8'))
            while myPort.in_waiting <= 0:
                sleep(.01)
            correctCheck = myPort.read(1)
            goCheck = 0

    def sendPixelData(x,y):
        xDot = columns - x
        yDot = rows - y
        greyValue = myImage.getpixel((x,y))
        depth = 0
        #code that crops
        if xDot < leftMarginAdjust or xDot > rightMarginAdjust or yDot > topMarginAdjust or yDot < bottomMarginAdjust:
            return
        if greyValue > 232:
            return
        elif 209 < greyValue <= 232:
            depth = 1
        elif 186 < greyValue <= 209:
            depth = 2
        elif 163 < greyValue <= 186:
            depth = 3
        elif 140 < greyValue <= 163:
            depth = 4
        elif 117 < greyValue <= 140:
            depth = 5
        elif 94 < greyValue <= 117:
            depth = 6
        elif 71 < greyValue <= 94:
            depth = 7
        elif 48 < greyValue <= 71:
            depth = 8
        elif 25 < greyValue <= 48:
            depth = 9
        else:
            depth = 10
        writeDotDraw(xDot,yDot,depth)

    def writeDotDraw(xDot,yDot,depth):
        secureSendInt(4)
        secureSendInt(xDot)
        secureSendInt(yDot)
        secureSendInt(depth)

    def readInt():
        inByte = myPort.read(1)
        inInt = struct.unpack('>H', b'\x00' + inByte)[0]
        return inInt

    #Open Serial
    myPort = serial.Serial('/dev/ttyACM0')

    #Load Image and Resize
    myImage = Image.open(img)
    maxSize = (221,10000)
    myImage.thumbnail(maxSize)
    rows = myImage.height
    columns = myImage.width

    #Convert to Black and White
    myImage = myImage.convert(mode="L")

    #Set Crop Values
    leftCrop = 0
    rightCrop = 0
    topCrop = 0
    bottomCrop = 0

    leftMarginAdjust = leftCrop
    rightMarginAdjust = 221 - rightCrop
    topMarginAdjust = rows - topCrop
    bottomMarginAdjust = bottomCrop

    #Print Code
    for r in range(rows - 1, -1, -1):
        if r%2 == 0:
            for c in range(columns - 1, -1, -1):
                sendPixelData(c,r)
        else:
            for c in range(0, columns, 1):
                sendPixelData(c,r)













