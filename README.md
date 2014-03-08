Raspberry Pi Adapter Board
==========================

Documentation revision 0.2 2014-03-08 13:00 UCT +10:30


Directory Structure
-------------------

Files in this directory are "miscellaneous"; other files are organised into subdirectories:

* datasheets - manufacturers' datasheets for some of the parts used, provided as a reference for programming. 
* eagle - Cadsoft Eagle schematic and board files. Created in Eagle Professional V5.
* software - utilities and test code, written primarily in Python.


Features
--------

* Breaks out all of the main IO pins.
* 3.3V regulator ([MCP1700T-3102E/TT](http://www.microchip.com/wwwproducts/Devices.aspx?dDocName=en010642)) for all its own chips.
* Separate 3.3V regulator for off-board devices.
* [DS3234](http://www.maximintegrated.com/datasheet/index.mvp/id/4051) RTC.
* [PCA9540](http://www.nxp.com/products/interface_and_connectivity/i2c/i2c_multiplexers_switches/series/PCA9540B.html) I2C multiplexer - one channel at 3.3V, one channel level-shifted to 5V.
* [PCF8574](http://www.ti.com/product/pcf8574) I2C bus expander to drive 16x2/16x4 LCD in 4 bit mode, including backight control.
* Level-shifted PWM and serial channels using [TXB0104](http://www.ti.com/product/txb0104).


Caution
-------

* 3.3V parts of the system are **not** protected against higher voltages - connecting incorrect power or logic levels can destroy both this board and the Raspberry Pi.
* Mount board carefully, or only place on a non-conductive surface, otherwise the connecting pins of the CR2032 lithium cell could be shorted, crating a fire hazard.


Powering The Board
------------------

The board has a direct connection to the Raspberry Pi 5V rail, and can therefore be powered entirely from the Pi. The 3.3V rail is *not* connected, as the board has its own 3.3V regulators (see Features.)

As an alternative to powering through the Raspberry Pi's USB power connector, a regulated 5V supply may be applied to the 5VIN or 5VAUX connectors. This allows for systems where more current is needed than can be provided by the Pi's 5V regulator.


Connectors
----------

All data connectors use standard 0.1" pitch pin headers.

I use Multicomp 2226TG crimp terminals with 2226A series housings, all available
from Element14.

* 2226TG crimp terminal: Element14 part number 1593529
* 2226A-02 crimp housing, 2 way: 1593506
* 2226A-03 crimp housing, 3 way: 1593507
* 2226A-04 crimp housing, 3 way: 1593508
* 2226A-05 crimp housing, 3 way: 1593509
* 2226A-06 crimp housing, 3 way: 1593510

To connect to an LCD, as not all pins are used in 4-bit mode, and assuming the device is one with a backlight, I use a pair of 6-way cables made up with 2226A-06 housings.

Connection to the Raspberry Pi may be made with a 26-way 1.27 cable terminated with AMP 2-215911-6 IDC sockets, Element14 part number 3815730. As this cable tends to come in 100' reels, I just cut down old PATA hard disc cables. Assembly may be done with careful use of a vice, as the "proper" tools for this are hideously expensive.

Off-board power connections can be made either with standard 0.1" pin headers, but I recommend the use of polarised connectors such as Molex 22-27-2021 (E14: 9731148) connecting to cables terminated with Molex crimp pin 08-50-0032 (E14: 9773789) and housings 22-01-2025 (E14: 143126.)

I have standardised on this connection system for all my single-rail low-voltage power connectors.


I2C Busses
----------

Off-board I2C ports are connected to the Raspberry Pi's I2C bus through an NXP PCA9540 multiplex. Until one or other of the ports are connected through the multiplexer, only address 0x70, the PCA9540 itself, will show on the bus. When Port 0 - the 5V level-shifted one - is enabled, address 0x38 - the PCF8574 - will be in use.

If a second 5V I2C bus is desired, and the 3.3V one not required, a simple level-shifter may be built using a pair of BSN20 MOSFETs and four 4k7 resistors. See NXP AN97055 in the datasheets directory for details. (This is exactly how Port 0 is level-shifted on the board.)

Note that Port 1 (3.3V) does __not__ have pull-up resistors fitted and, if used, 4k7 resistors from the 3.3V line to the SDA and SCL lines should be fitted somewhere on the bus.

Access to the Raspberry Pi's I2C bus before the PCA9540 may be made through the connector to the left of the lithium cell holder. (Board viewed with Raspberry Pi connector on the left.) 


SPI Bus
-------

The Raspberry Pi SPI bus broken out to the expansion connector comes with two slave select lines, CE0, and CE1. CE0 is used by the DS3234 RTC, leaving only one slave select available, which appears on the 5V level-shifted SPI_5V connector.

If more than one external SPI device is required, it will be necessary to level-shift one or more of the other GPIO pins, and use with external decoding logic in conjunction with CE1. If GPIO24 and GPIO25 were used, for example, four external SPI devices could be used.


Pinouts
-------

As viewed with board oriented with Raspberry Pi connector to the __left__.

Vertical connectors labelled top to bottom, horizontal connectors labelled left to right.

###RPI_I2C###

(3.3V logic - direct break-out from Raspberry Pi.)

* SDA
* SCL
* Ground
* 3.3V from board external regulator (not Raspberry Pi)

###I2CP0###

(5V logic)

* SDA
* SCL
* Ground
* 5V (common to entire system)

###I2CP1##
 
(3,3V logic)

* SDA
* SCL
* Ground
* 3.3V from board external regulator (not Raspberry Pi)

###SPI_5V###

(5V logic, level-shifted from Raspberry Pi.)

* SS (Raspberry Pi CE1)
* MOSI
* MISO
* SCLK
* Ground

###LCD###

(5V logic)

* Backlight (Q3 collector, base driven by PCF8574 P7)
* 5V to backlight
* DB7 (PCF8574 P3)
* DB6 (PCF8574 P2)
* DB5 (PCF8574 P1)
* DB4 (PCF8574 P0)
* Not connected
* Not connected
* Not connected
* Not connected
* EN  (PCF8574 P6)
* R/W (PCF8574 P5)
* RS  (PCF8574 P4)
* VEE (from contrast pot)
* 5V
* Ground

###RTC###

(3.3V logic)

* SQW/INT
* 32kHz
* Ground

###GPIO23###

(3.3V logic - direct break-out from Raspberry Pi.)

* GPIO23
* Ground

###GPIO2425###

(3.3V logic - direct break-out from Raspberry Pi.)

* Ground
* GPIO25
* GPIO24

###Serial###

(5V logic, level-shifted from Raspberry Pi.)

* Ground
* RX
* TX

###PWM###

(5V logic, level-shifted from Raspberry Pi.)

* PWM
* Ground

###GPIO###

(3.3V logic - direct break-out from Raspberry Pi.)

* GPIO4
* GPIO17
* GPIO27
* GPIO22
* Ground
* 3.3V from board external regulator (not Raspberry Pi)


Future Developments
-------------------

I designed this board for a specific purpose (prototyping some instrumentation,) which it satisfies quite adequately. However, were I to make a second, more flexible, iteration, here are some changes I might make:

* Include an on-board LM2576-based 5V power supply. This delivers up to 3A with input voltages from 7V to 40V. 
* Use surface-mount version of PCF8574.
* Pass SPI signals through CPLD controlled by CE1 signal and a GPIO pin.  CPLD would be configured to provide multiple CS lines, which would be determined by writing to a register. CPLD would be selected by CE1 then, depending on the state of the GPIO pin, assert the desired CS signal, or take incoming data as instructions. If 2 MSBs are used to select operation, four operations with six bits of data could be performed with a single configuration byte.
* Feed level translator VCCB pins from selectable load switches controlled by CPLD in previous point. This would allow SPI configuration of 3.3/5V logic on off-board connectors. Probably feed VCCB through a BAT54S permanently connected to 3.3V supply, with 5V supply switched in when required. An adequately rated load switch could also provide power to off-board connectors.
* LCD connector is currently configured so pins map one-to-one with a backlit LCD module. If all the wiring were done at the LCD end, and if R/W is not used (tie low at LCD,) a compact 10-pin SMD connector could be employed, saving a considerable amount of board space. 


Links
-----

###How-To###

* [Adafruit: Configuring I2C on the Raspberry Pi](http://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c)
* [100 Random Tasks: Simple SPI on Raspberry Pi](http://www.100randomtasks.com/simple-spi-on-raspberry-pi)

###Manufacturers/Vendors###

* [Element 14 Australia](http://au.element14.com) Electronic component distributor.
* [Maxim Integrated](http://www.maximintegrated.com/) manufacturer of the DS3234 RTC.
* [Microchip](http://www.microchip.com) manufacturer of the MCP1700T-3102E/TT voltage regulators.
* [NXP (formerly Philips Semiconductors)](http://www.nxp.com) manufacturer of the PCA9540 I2C bus multiplexer.
* [Raspberry Pi](http://www.raspberrypi.org/)
* [Texas Instruments](http://www.ti.com) manufacturer of the TXB0104 level translators, and PCF8574 I2C bus expander.
