#!/usr/bin/python

import picamera
import pygame
import time
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

photoCount = 0

def photoNum():
  photoCount++;
  if (photoCount < 10):
    return '000'+photoCount
  elif (photoCount < 100):
    return '00'+photoCount
  elif (photoCount < 1000):
    return '0' + photoCount

# countdown images
one = pygame.image.load("images/1.png")
two = pygame.image.load("images/2.png")
three = pygame.image.load("images/3.png")
printlogo = pygame.image.load("images/printphoto.png")
takelogo = pygame.image.load("images/takephoto.png")

def startPreview():
  options = {'fullscreen':False, 'window': (40,0,1000,1500)}
  camera.start_preview(**options)
  camera.hflip = True

def checkForQuit():
  for event in pygame.event.get():
    if (event.type == pygame.QUIT or 
      (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
      done()

def done():
  pygame.quit()
  sys.exit()


def oneSecondNumber(num):
  screen.fill(black)
  screen.blit(num, (400, 1820))
  pygame.display.update()
  time.sleep(3)
  screen.fill(white)
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
  playChime()

  pilImage = Image.open(stream)

  mode = pilImage.mode
  size = pilImage.size
  data = pilImage.tostring()


  return pilImage


def photoMode:
  pilImage = takePhoto()

  pygameImage = pygame.image.fromstring(data, size, mode)
  mode = pilImage.mode
  size = pilImage.size
  data = pilImage.tostring()

  # display photo on screen
  screen.fill(black)
  screen.blit(pygameImage, (0,0))
  screen.blit(printlogo, (0, 1800))
  pygame.display.update()

  printStart = time.time()
  printEnd = printStart + 10

  while True:
    checkForQuit()
    input_state = GPIO.input(18)
    if input_state == False:
      # save photo
      filename = photoNum() + '.jpg'
      filepath = '/home/pi/spooky/photos' + filename
      pilImage.save(filepath, "jpeg")


      # print photo
      print "WOULD BE PRINTING HERE"

      return
    elif time.time() > printEnd:
      return

def attractMode:
  startPreview()
  screen.fill(black)
  screen.blit(takelogo, (0, 1800))
  pygame.display.update()

  while True:
    checkForQuit()
    input_state = GPIO.input(18)
    if input_state == False:
      photoMode()



while True:
  attractMode()
