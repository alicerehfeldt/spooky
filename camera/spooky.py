#!/usr/bin/python

import picamera
import pygame
import time
import math
import random
import io
import RPi.GPIO as GPIO
import sys
from PIL import Image

white = pygame.Color(255,255,255)
black = pygame.Color(0,0,0)

pygame.init()

pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

screen.fill(black)
pygame.display.update()


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

camera = picamera.PiCamera();
camera.resolution = (1200,1800)
camera.awb_mode = 'fluorescent'

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

countFile = open('count.txt')
photoCount = int(countFile.readline())
countFile.close()
def photoNum():
  global photoCount
  photoCount = photoCount + 1;
  if (photoCount < 10):
    return '000' + str(photoCount)
  elif (photoCount < 100):
    return '00'+ str(photoCount)
  elif (photoCount < 1000):
    return '0' + str(photoCount)

# countdown images
one = pygame.image.load("images/1.png")
two = pygame.image.load("images/2.png")
three = pygame.image.load("images/3.png")
printlogo = pygame.image.load("images/printphoto.png")
takelogo = pygame.image.load("images/takephoto.png")
printing = pygame.image.load("images/printing.png")

def startPreview():
  options = {'fullscreen':False, 'window': (40,0,1000,1500)}
  camera.start_preview(**options)
  camera.hflip = True

def checkForInput():
  input_state = GPIO.input(18)
  if input_state == False:
    return True

  for event in pygame.event.get():
    if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
      return True
    elif (event.type == pygame.QUIT or 
      (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
      done()
      return False
  return False

def done():
  countFile = open("count.txt", "w")
  countFile.truncate(0)
  countFile.write(str(photoCount))
  countFile.close()
  pygame.quit()
  sys.exit()


def oneSecondNumber(num):
  screen.fill(black)
  screen.blit(num, (450, 1500))
  pygame.display.update()
  time.sleep(1)
  pygame.display.update()

def takePhoto():
  oneSecondNumber(three)
  oneSecondNumber(two)
  oneSecondNumber(one)

  # stop preview
  camera.stop_preview()
  stream = io.BytesIO()
  photoOptions = {'quality':95}
  camera.capture(stream, "jpeg", **photoOptions)
  stream.seek(0);

  pilImage = Image.open(stream)
  return pilImage


def photoMode():
  pilImage = takePhoto()
  screen.fill(black)
  pygame.display.update()
  screenImage = pilImage.resize((1000, 1500), Image.BICUBIC)

  mode = screenImage.mode
  size = screenImage.size
  data = screenImage.tobytes()
  pygameImage = pygame.image.fromstring(data, size, mode)

  # display photo on screen
  screen.fill(black)
  screen.blit(pygameImage, (40,0))
  screen.blit(printlogo, (0, 1600))
  pygame.display.update()

  printStart = time.time()
  printEnd = printStart + 10

  while True:
    if checkForInput():
      # save photo
      filename = photoNum() + '.jpg'
      filepath = '/home/pi/spooky/photos/' + filename
      pilImage.save(filepath, "jpeg")

      # print photo
      screen.fill(black)
      screen.blit(pygameImage, (40,0))
      screen.blit(printing, (0, 1600))
      pygame.display.update()
      time.sleep(5)
      return
    elif time.time() > printEnd:
      return

def drawAttractMode():
  vmin = 1500
  vrand = math.floor(random.random() * 200)
  vfinal = vmin + vrand
  screen.fill(black)
  screen.blit(takelogo, (0, vfinal))
  pygame.display.update()
 

def attractMode():
  startPreview()
  changeTime = 0
  while True:
    if checkForInput():
      photoMode()
      startPreview()
    elif changeTime < time.time():
      drawAttractMode()
      changeTime = time.time() + 5

while True:
  attractMode()
