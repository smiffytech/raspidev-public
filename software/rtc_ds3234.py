#!/usr/bin/env python

import sys
import spidev
import os
from time import gmtime, strftime

# Version: 0.1b 2014-03-03

#
# Usage: rtc_ds3234.py COMMAND
#
# Where COMMAND is one of:
#
# setrtc - save current system time to RTC.
# setsystem - save RTC time to system.
# show - show current RTC time.
# 

#
# SPI channel and CE line.
# 
# Modify to suit your system.
#
spi_channel = 0
spi_ce = 0


# Check user is root-ish - needed for SPI access.
if os.geteuid() != 0:
  print "RTC access requires root privileges; please try again using sudo."
  sys.exit(-1)


# Set up SPI. Uses SCK rate = 8MHz as known-good value.
spi = spidev.SpiDev()
spi.open(spi_channel, spi_ce)
spi.mode = 1
spi.max_speed_hz = (8000000)


# Usage message.
def usage():
  print "Usage: rtc_ds3234.py [setrtc|setsystem|show]"
  sys.exit(-1)
 
# Convert 2-digit BCD to integer
def bcd2int(x):
  return int(str( (x & 0xF0) >> 4 ) + str(x & 0x0F))


# Convert integer ( n < 99 ) to BCD
def int2bcd(x):
  if x > 9 :
    digits = list(x)
    return int(digits[0]) << 4 | int(digits[1])
  else :
    return int(x)


# Set RTC with current system time (UCT.)
def settime():
  ts = gmtime()
  secs = int2bcd(strftime("%S", ts))
  mins = int2bcd(strftime("%M", ts))
  # The leftmost zeroes of the MSN should set us in 24 hour mode.
  hours = int2bcd(strftime("%H", ts))
  date = int2bcd(strftime("%d", ts))
  month = int2bcd(strftime("%m", ts))
  year = int2bcd(strftime("%y", ts))
  # Day of week - based on Sunday = 0
  day = int(strftime("%w", ts))

  result = spi.xfer2([0x80, secs])
  result = spi.xfer2([0x81, mins])
  result = spi.xfer2([0x82, hours])
  result = spi.xfer2([0x83, day])
  result = spi.xfer2([0x84, date])
  result = spi.xfer2([0x85, month])
  result = spi.xfer2([0x86, year])


# Get date/time from RTC.
def gettime():
  # Function       addr  secs  mins  hours day   date  month year  
  # Index          0     1     2     3     4     5     6     7
  ts = spi.xfer2([0x00, 0x00, 0x01, 0x00, 0x02, 0x00, 0x00, 0x00])

  secs = bcd2int(ts[1])
  if secs < 10 :
    secs = "0" + str(secs)

  mins = bcd2int(ts[2])
  if mins < 10 :
    mins = "0" + str(mins)

  # Assuming we're set in 24 hour mode.
  hours = int(str(( ts[3] & 0x30 ) >> 4) + str(ts[3] & 0x0F))
  if hours < 10 :
    hours = "0" + str(hours)

  # Ignore day of week (ts[4]) for retrieval, but we will set it.
  # day = ts[4]

  date = bcd2int(ts[5])
  if date < 10 :
    date = "0" + str(date)
  
  # Bit 7 of the month is the century bit, but is ignored.
  month = int(str(( ts[6] & 0x10 ) >> 4) + str(ts[6] & 0x0F))
  if month < 10 :
    month = "0" + str(month)

  year = bcd2int(ts[7])
  if year > 10 :
    year = "20" + str(year)
  else :
    year = "200" + str(year)

  dtstring = str(year) + "-" + str(month) + "-" + str(date) + " " + str(hours) + ":" + str(mins) + ":" + str(secs)
  return dtstring


# Retrieve date/time from RTC, set system time.
def setsystime():
  dtstring = gettime()
  cmdstring = 'date -u --set="' + dtstring + '"'
  os.system(cmdstring)
  sys.exit(0)


# Get time from RTC, print.
def showtime():
  dtstring = gettime()
  print dtstring
  sys.exit(0)


# Check that a one and only one argument has been given.
if len(sys.argv) != 2:
  usage()

# Run per provided argument.
if sys.argv[1] == 'setrtc':
  settime()
  sys.stdout.write("RTC set (UTC) : ")
  showtime()
elif sys.argv[1] == 'setsystem':
  setsystime()
elif sys.argv[1] == 'show':
  sys.stdout.write("Current RTC time (UTC) : ")
  showtime()
else:
  usage()

spi.close()
sys.exit(0)
