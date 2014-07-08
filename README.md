PiLone
======

PiLone is OpenSourceHardWare that allows quietly displaying various quantitative and/or time based data in the living room

[![OpenSource HardWare logo](./docs/img/oshw-logo-x150-px.png)](http://www.oshwa.org)
[![Raspberry Pi Logo](./docs/img/Raspi_logo-x150.png)](http://www.raspberrypi.org/)
[![Arduino Community Logo](./docs/img/arduino-community-x150.png)](http://www.arduino.cc)

Raspberry Pi is a trademark of the Raspberry Pi Foundation

Arduino Community is a trademark of Arduino SA

Licence
=======

All software in this repository is released under the GNU General Public Licence V3.0. You may find a copy online [there](http://opensource.org/licenses/GPL-3.0) or localy [here](./software-licence.txt)

All documentation, drawings, pictures, schematics, and more generaly all that is not a computer program or part of it is licenced under the Creative Commons CC-BY-SA V4.0 licence. You may find a copy of the licence [there](http://creativecommons.org/licenses/by-sa/4.0/) or localy [here](./hardware-licence.txt)

What is it?
===========

In this project, you will find how to plug a Raspberry Pi, an Arduino Pro Mini, and some Adafruit NeoPixels together, to make a connected object that can display time based, or quantitative, information in a beautifull way.

Why?
====

I started this project when I realized I wanted something able to push some information to me, silently, quietly, not on my phone, nor my computer. Something the old Nabaztag did perfectly until it died, and without the bugs.

I already had, as most of my fellow geek friends, a Raspberry Pi. I wanted to learn some Arduino to understand the buzz. And I liked the way NeoPixel sticks can display efficiently information. I had to plug it all together.

Requirements
============

Hardware parts
--------------

- 1x Raspberry Pi model B rev. 2 ([SparkFun](https://www.sparkfun.com/products/11546))
- 1x SD-Card (any size will do, as long as your Linux fits in. >4Gb recommended)
- 1x SparkFun Arduino Pro Mini 5v 16MHz ([SparkFun](https://www.sparkfun.com/products/11113))
- 3x Adafruit Technology High Density NeoPixel Sticks (or less, at least one) (or any other WS-2812 controlled 5050 RGB LED strip or - stick) ([SparkFun](https://www.sparkfun.com/products/12661))
- 1x custom made PCB (you may have the one [here](./hardware/PiLone‰20rev‰20C.fzz) made at Fritzing Fab, for instance, or build it - yourself if you have time, patience, skills, and something to print, cut, drill small, two-sided PCBs)
- 1x 2x13, 0.1' spaced, shrouded header ([SparkFun](https://www.sparkfun.com/products/11490)) or 2x13, 0.1' spaced, female header ([SparkFun](https://www.sparkfun.com/products/11765))
- 1x USB cable type-A to micro type-B as short as possible (30cm will do) ([SparkFun](https://www.sparkfun.com/products/10215))
- 1x FTDI-to-USB converter (SparkFun's works perfectly, any clone will do) ([SparkFun](https://www.sparkfun.com/products/9716) or get a friend to program your Arduino for you)
- 1x 5V 2A 3.5mm power supply ([SparkFun](https://www.sparkfun.com/products/12889))
- 1x 3.5mm power jack socket ([SparkFun](https://www.sparkfun.com/products/119))
- 1x straight USB type-A female connector
- 3x 4-pin, 0.1' spaced, male pins ([SparkFun](https://www.sparkfun.com/products/116))
- 3x 4-pin, 0.1' spaced, female-to-wire cables ([SparkFun](https://www.sparkfun.com/products/10364))
- Some soldering material and tooling

Total expected bill: under 100€ including taxes and customs, depending on shipping costs (group your packages!)

Software parts
--------------

- Linux installed on the SD-Card (any standard distribution will do, tested on Raspbian)
- Python 2.7.x (most probably already installed)
- PySerial (install with `pip install pyserial`)
- [optional] BottlePy (intall with `pip install bottle`) (will work without Bottle Py if you do not need test.py to play with LED colors - by hand)
- UART console disabled, reconfigured as serial port