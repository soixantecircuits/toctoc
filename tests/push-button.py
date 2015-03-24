#!/usr/bin/env python
# To kick off the script, run the following from the python directory:
#   PYTHONPATH=`pwd` python toctoc.py start

#standard python libs
import os
import subprocess
import sys
import time 
import math 

#third party libs
import RPi.GPIO as GPIO

TOCTOC_PATH = '/usr/share/toctoc/'
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP)
pushTime = 0
while True:
  if ( GPIO.input(14) == False ):
    #os.system('mpg321 ' + TOCTOC_PATH + 'ding.mp3 > /dev/null &')
    with open(os.devnull, "w") as fnull:
      subprocess.Popen(['mpg321', TOCTOC_PATH + 'ding.mp3'], stdout = fnull, stderr = fnull)
    pushTime = time.time()
  now = time.time()
  distance = (now - pushTime)/10.*100
  #print(distance)
  string = "\r["
  if (distance < 1):
    string += "x"
  else:
    string += " "
  string +="]"
  if (distance < 100 and distance > 1):
    for i in range(1, int(math.floor(distance))):
      string += " "
    string += "x"
  sys.stdout.write(string)
  sys.stdout.write("\r\x1b[K"+string)
  sys.stdout.flush()
  time.sleep(0.05)

