#!/usr/bin/python

# .-------------------------------------------------------------------------.
# | This program monitors for changes in 'lusb' reports and files in the    |
# | /dev directory when a USB device is connected or removed. It basically  |
# | saves having to manually run 'lsusb' and 'ls' and having to compare the |
# | results.                                                                |
# `-------------------------------------------------------------------------'

import os
import time

def GetUsbList() : return os.popen("lsusb").read().strip().split("\n")
def GetDevList() : return os.listdir("/dev")

def Changed(old, now):
  add = []
  rem = []
  for this in now:
    if not this in old:
      add.append(this)
  for this in old:
    if not this in now:
      rem.append(this)
  return add, rem

try:
  print("Monitoring for USB changes and changes in /dev directory")
  usbOld, devOld = GetUsbList(), GetDevList()
  while True:
    time.sleep(1)
    usbNow, devNow = GetUsbList(), GetDevList()
    usbAdd, usbRem = Changed(usbOld, usbNow)
    devAdd, devRem = Changed(devOld, devNow)
    if len(usbAdd) + len(usbRem) + len(devAdd) + len(devRem) > 0:
      print("-------------------")
      t = time.strftime("%Y-%m-%d %H:%M:%S - ")
      for this in usbAdd : print(t + "Added   : "      + this)
      for this in usbRem : print(t + "Removed : "      + this)
      for this in devAdd : print(t + "Added   : /dev/" + this)
      for this in devRem : print(t + "Removed : /dev/" + this)
      usbOld, devOld = usbNow, devNow
except KeyboardInterrupt:
  print("")
