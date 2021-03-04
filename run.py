
#!/usr/bin/python

from raspledstrip.ledstrip import *
import threading
import time
import random
import binascii
import PN532
import pygame

pygame.mixer.init()
pygame.mixer.music.load("c.mp3")

# Open NFC Reader
nfc = PN532.PN532("/dev/ttyAMA0", 115200)
nfc.begin()
nfc.SAM_configuration()

# Open the file with registered bands
bands = []
for line in open('bands.txt', 'r'):
    bands.append(line.strip())

# GLOBAL COLOR PRESETS
green = Color(0, 255, 0, 1)
blue = Color(65, 35, 255, 1)
yellow = Color(255, 210, 0, 1)

# Time (s) between LED changes when idle
idleDelay = 0.20

# Time (s) between LED changes when a band is discovered
readingDelay = 0.05

# Change this depending on how many LED's you add on each ring
numOutsideLEDs = 8
numInsideLEDs = 8

# Define LED Strip
led = LEDStrip(numOutsideLEDs + numInsideLEDs, True)

# Set Brightness
led.setMasterBrightness(1)
led.all_off()

# Band Output result
def bandResult(color):
    brightness = 0
    for _ in range(0, 6):
        led.setMasterBrightness(brightness)
        led.fill(color, 0, numOutsideLEDs + numInsideLEDs - 2)
        led.update()
        time.sleep(0.045)
        brightness += 0.2

    time.sleep(2)

    brightness = 1
    for _ in range(0, 6):
        led.setMasterBrightness(brightness)
        led.fill(color, 0, numOutsideLEDs + numInsideLEDs - 2)
        led.update()
        time.sleep(0.045)
        brightness -= 0.2

    led.setMasterBrightness(1)

delay = idleDelay

def whiteSpinner():
    global delay
    fullWhite = Color(255, 255, 255, 1)
    dimWhite = Color(255, 255, 255, 0.3)

    for n in range(0, numOutsideLEDs):
        group = [n, n+1, n+2]

        if group[2] == numOutsideLEDs:
            group[2] = 0
        elif group[2] == numOutsideLEDs + 1:
            group[2] = 1

        if group[1] == numOutsideLEDs:
            group[1] = 0
        elif group[1] == numOutsideLEDs + 1:
            group[1] = 1

        led.all_off()
        led.set(group[0], dimWhite)
        led.set(group[1], fullWhite)
        led.set(group[2], dimWhite)
        led.update()
        time.sleep(delay)

        led.all_off()

cardFound = False
discoveredUID = ""

def reader():
    global cardFound
    global discoveredUID
    global delay
    uid = None
    while True:
        uid = nfc.read_passive_target()
        if uid is "no_card":
            cardFound = False
            delay = idleDelay
            discoveredUID = ""
        else:
            cardFound = True
            delay = readingDelay
            discoveredUID = str(binascii.hexlify(uid))
            pygame.mixer.music.play()
            break

def spinner():
    global delay
    global cardFound
    global discoveredUID
    while cardFound == False:
        whiteSpinner()
    whiteSpinner()
    if discoveredUID in bands:
        bandResult(green)
        time.sleep(1)
    else:
        bandResult(yellow)
        time.sleep(1)


while True:
    cardFound = False
    discoveredUID = ""
    delay = idleDelay
    t1 = threading.Thread(target=reader)
    t2 = threading.Thread(target=spinner)
    t1.start()
    t2.start()
    t2.join()
    t1 = None
    t2 = None