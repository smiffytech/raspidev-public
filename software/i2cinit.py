#!/usr/bin/python

import smbus

bus = smbus.SMBus(1)

# Setup I2C bus multiplexer (address: 0x70)

# 0xx - no channel selected
# 100 - channel 0 selected
# 101 - channel 1 selected
# 11x - no channel selected

bus.write_byte_data(0x70, 0, 0x04)
