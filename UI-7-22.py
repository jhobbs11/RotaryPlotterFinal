#!/usr/bin/env python3

import pygame
import pygame.camera
import pygame.image
import pygame.locals
import pygame.transform
import pygame.mouse
from ArduinoLink import piPrint
import PIL
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import sys

pygame.init()
pygame.camera.init()

display_width = 480
display_height = 320
SIZE = (display_width,display_height)

#Colors
black = (0,0,0)
white = (255,255,255)

#Initialize Values for Checking Mouse
mouse = (0,0)
click = (0,0,0)

#Initialize Display
uiDisplay = pygame.display.set_mode((display_width,display_height),pygame.FULLSCREEN)
pygame.mouse.set_cursor((8,8),(1,1),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
#pygame.mouse.set_visible(False)
#pygame.display.toggle_fullscreen()


#Initialize FPS Clock
clock = pygame.time.Clock()

def putImg(img,x,y):
    uiDisplay.blit(img, (x,y))

def button(img,x,y,w,h,action=None):
    putImg(img,x,y)
    if x+w > mouse[0] > x and y+h > mouse[1] >y:
        if click[0] == 1 and action != None:
            uiDisplay.fill(black)
            pygame.display.update()
            action()

def message(text):
    largeText = pygame.font.Font('freesansbold.ttf', 140)
    TextSurf, TextRect = text_objects(text,largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    uiDisplay.blit(TextSurf,TextRect)
    #pygame.display.update()

def text_objects(text,font):
    textSurface = font.render(text,True,white)
    return textSurface, textSurface.get_rect()
            
def startMenu():
    #Load Image
    cameraMainImg = pygame.image.load('camera2.png')

    #Loop
    while Main:
        global mouse
        global click
        #Check Events
        for event in pygame.event.get():
                mouse = pygame.mouse.get_pos()
                click = pygame.mouse.get_pressed()

        #Set Background to White
        uiDisplay.fill(white)

        #Draw Main Camera Button
        button(cameraMainImg,115,64,250,192,captureAction)
        pygame.display.update()

        #Exit Button Top Right
        exitButton = pygame.Surface((50,50))
        button(exitButton,0,0,50,50,pygame.quit)

        
        clock.tick(15)

def captureAction():
    #Initialize Camera
    camera = pygame.camera.Camera('/dev/video0',(480,480))
    camera.start()
    for x in range(300):
        #Update Video Stream
        uiDisplay.fill(black)
        image = camera.get_image()
        image = pygame.transform.scale(image, (320,320))
        uiDisplay.blit(image,(70,0))
        #Add Appropriate Message
        if 60 > x >= 30:
            message('Smile!')
        elif 80 > x >= 60:
            message('3')
        elif 100 > x >= 80:
            message('2')
        elif 119 > x >= 100:
            message('1')
        elif x == 119:
            uiDisplay.fill(white)
            pygame.image.save(image,'left.jpg')
        elif 150 > x >= 120:
            message('Smile!')
        elif 170 > x >= 150:
            message('3')
        elif 190 > x >= 170:
            message('2')
        elif 209 > x >= 190:
            message('1')
        elif x == 209:
            uiDisplay.fill(white)
            pygame.image.save(image,'center.jpg')
        elif 240 > x >= 210:
            message('Smile!')
        elif 260 > x >= 240:
            message('3')
        elif 280 > x >= 260:
            message('2')
        elif 299 > x >= 280:
            message('1')
        elif x == 299:
            uiDisplay.fill(white)
            pygame.image.save(image,'right.jpg')             
        #Refresh Screen
        pygame.display.update()
        clock.tick(120)
    camera.stop()
    ProcessScreen()

def ProcessScreen():

    #Initiate UI
    uiDisplay.fill(white)
    pygame.display.update()
    
    #Create Image
    leftImage = pygame.image.load('left.jpg')
    centerImage = pygame.image.load('center.jpg')
    rightImage = pygame.image.load('right.jpg')
    compositeImage = pygame.Surface((1000,340))
    compositeImage.blit(leftImage,(10,10))
    compositeImage.blit(centerImage,(340,10))
    compositeImage.blit(rightImage,(670,10))
    pygame.image.save(compositeImage,'compositeImage.jpg')

    #Initial Adjustments in PIL
    PILImage = Image.open('compositeImage.jpg')
    PILImage = PIL.ImageOps.equalize(PILImage)
    PILImage.save('compositeImage.jpg')

    #Pass Altered Image to Pygame
    compositeImage = pygame.image.load('compositeImage.jpg')  
    global compositeImageThumb
    compositeImageThumb = pygame.transform.scale(compositeImage,(356,120))

    #Load images for UI
    cameraMainImg = pygame.image.load('camera2.png')
    cameraSmallImg = pygame.image.load('camera.png')
    brightnessImg = pygame.image.load('brightness.png')
    checkImg = pygame.image.load('checkmark2.png')
    crossImg = pygame.image.load('cross2.png')
    downArrowImg = pygame.image.load('downarrow.png')
    upArrowImg = pygame.image.load('uparrow.png')

    #Set UI
    while True:
        global mouse
        global click
            #Check Events
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
        uiDisplay.fill(white)
        uiDisplay.blit(compositeImageThumb,(62,100))
        button(upArrowImg,125,25,50,50,brighten)
        uiDisplay.blit(brightnessImg,(218,28))
        button(downArrowImg,305,25,50,50,darken)
        button(checkImg,125,245,50,50,sendPrint)
        uiDisplay.blit(cameraSmallImg,(223,253))
        button(crossImg,305,245,50,50,startMenu)
        pygame.display.update()
        clock.tick(30)
        
        
def brighten():
    global compositeImageThumb

    #Load Image in to PIL
    PILImage = Image.open('compositeImage.jpg')

    brighten = ImageEnhance.Brightness(PILImage)
    PILImage = brighten.enhance(1.25)

    contrast = ImageEnhance.Contrast(PILImage)
    PILImage = contrast.enhance(1.25)

    #PILImage = PIL.ImageOps.equalize(PILImage)
    
    PILImage.save('compositeImage.jpg')
    

    #Alter Image in PIL

    #Pass Altered Image to Pygame
    compositeImage = pygame.image.load('compositeImage.jpg')
    compositeImageThumb = pygame.transform.scale(compositeImage,(356,120))
    
    

def darken():
    global compositeImageThumb

    #Load Image in to PIL
    PILImage = Image.open('compositeImage.jpg')
    
    brighten = ImageEnhance.Brightness(PILImage)
    PILImage = brighten.enhance(0.75)

    #PILImage = PIL.ImageOps.equalize(PILImage)

    PILImage.save('compositeImage.jpg')
    

    #Alter Image in PIL

    #Pass Altered Image to Pygame
    compositeImage = pygame.image.load('compositeImage.jpg')
    compositeImageThumb = pygame.transform.scale(compositeImage,(356,120))

def sendPrint():
    piPrint('compositeImage.jpg')


#MAIN LOOP
Running = True
Main = True
Capture = False

while Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False

    startMenu()
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
