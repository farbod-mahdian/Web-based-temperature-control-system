#!/home/pi/software/bin/python3
# Name: Farbod Mahdian
# Student ID: 135438190

import re
import random

from w1thermsensor import W1ThermSensor, Unit
from time import sleep
from signal import pause, signal, SIGTERM

from rpi_lcd import LCD
from gpiozero import LED

temperature = 0
lcd = LCD() # The I2C 16x2 LCD
cooling = LED(25) # The blue LED
heating = LED(12) # The red LED

coolingStatus = False
heatingStatus = False

def cleanup(signum, frame): # close the program gracefully
    exit(1)


def findTemp(fn, min_, max_): # Read the current source code of the webpage and replace the new data and retrun them as a array of strings
    global temperature, coolingStatus, heatingStatus

    patTemp = r'<div id="logo" style="--temperature: \d+\.\d+"></div>'
    lowTag = r'<div id="coolTemp" style="--temperature: \d+\.\d+"><p id="low">\d+.\d+'
    highTag = r'<div id="heatTemp" style="--temperature: \d+\.\d+"><p id="high">\d+\.\d+'
    lowTemp = r'<p id="low">\d+\.\d+'
    highTemp = r'<p id="high">\d+\.\d+'
    patDisplay = r'<h1 id="temperature">\d+\.\d+'
    coolingOn = r'<img .*visible.* src="images/coolingOn.gif".*'
    coolingOff = r'<img .*hidden.* src="images/coolingOn.gif".*'
    heatingOn = r'<img .*visible.* src="images/heatingOn.gif".*'
    heatingOff = r'<img .*hidden.* src="images/heatingOn.gif".*'

    try:
        f = open(fn, "r")
        lines = f.readlines()
        for i in range(len(lines)):
            if re.search(patTemp, lines[i]):
                lines[i] = re.sub(
                    patTemp, '<div id="logo" style="--temperature: %.2f"></div>' % temperature, lines[i])
            if re.search(patDisplay, lines[i]):
                lines[i] = re.sub(
                    patDisplay, '<h1 id="temperature">%.2f' % temperature, lines[i])
            if re.search(lowTag, lines[i]):
                lines[i] = re.sub(
                    lowTag, '<div id="coolTemp" style="--temperature: %.2f"><p id="low">%.2f' % (min_, min_), lines[i])
            if re.search(highTag, lines[i]):
                lines[i] = re.sub(
                    highTag, '<div id="heatTemp" style="--temperature: %.2f"><p id="high">%.2f' % (max_, max_), lines[i])
            if heatingStatus:
                if re.search(heatingOff, lines[i]):
                    lines[i] = re.sub(
                        heatingOff, '<img id="heating_on" class="visible" src="images/heatingOn.gif" alt="heating system on">', lines[i])
            else:
                if re.search(heatingOn, lines[i]):
                    lines[i] = re.sub(
                        heatingOn, '<img id="heating_on" class="hidden" src="images/heatingOn.gif" alt="heating system on">', lines[i])
            if coolingStatus:
                if re.search(coolingOff, lines[i]):
                    lines[i] = re.sub(
                        coolingOff, '<img id="cooling_on" class="visible" src="images/coolingOn.gif" alt="cooling system on">', lines[i])
            else:
                if re.search(coolingOn, lines[i]):
                    lines[i] = re.sub(
                        coolingOn, '<img id="cooling_on" class="hidden" src="images/coolingOn.gif" alt="cooling system on">', lines[i])

    except IOError:
        print("1 - ERROR... file data could not be loaded")
        quit()
    else:
        f.close()
        return lines


def writeTemp(fn, lines): # Write the array of strings in the source code of the webpage to update its data
    try:
        f = open(fn, "w")
        f.writelines(lines)
    except IOError:
        print("2 - ERROR... file data could not be loaded")
        quit()
    else:
        f.close()


def getMinMax(fn): # Get the most recent maximum and minimum temperature which the user has been entered
    try:
        f = open(fn, "r")
        lines = f.readlines()
        (min_, max_) = lines[0].split(',')

    except IOError:
        print("3 - ERROR... file data could not be loaded")
        quit()
    else:
        f.close()
        return (float(min_), float(max_))
        
def webRecovery(): # Overwriting the webpage from a backup source code to make sure there is a template in the source code of the webpage before any function run - Software Reset
    try:
        f = open("/home/pi/public_html/index_backup.html", "r")
        lines = f.readlines()

    except IOError:
        print("4 - ERROR... file data could not be loaded")
        quit()
    else:
        f.close()
    writeTemp(html_path, lines)


sensor = W1ThermSensor() # The temperature sensor
html_path = "/home/pi/public_html/index.html" # Address of the source code of the webpage
data_path = "/home/pi/Desktop/tempsensor/data.txt" # Address of the text file which has the most recent maximum and minimum temperature which the user has been entered

try:
    signal(SIGTERM, cleanup)

    webRecovery()
    while True:
        temperature = sensor.get_temperature()

        (min_, max_) = getMinMax(data_path)

        endTemp = (min_ + max_) / 2.00 # The final desired temperature

        lcd.text('Lo T:%-6.2f' % temperature + chr(223) + 'C Hi', 1)
        lcd.text('%-6.2f    %6.2f' % (min_, max_), 2)
        
        if coolingStatus and (temperature < endTemp):
            cooling.off()
            coolingStatus = False
        elif heatingStatus and (temperature > endTemp):
            heating.off()
            heatingStatus = False

        if temperature > max_ and ~coolingStatus:
            cooling.on()
            coolingStatus = True
        elif temperature < min_ and ~heatingStatus:
            heating.on()
            heatingStatus = True

        lines = findTemp(html_path, min_, max_)
        writeTemp(html_path, lines)

        sleep(2)

except KeyboardInterrupt:
    exit(0)

finally:
    cooling.off()
    heating.off()
    lcd.clear()
    sleep(1)
