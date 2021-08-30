# Heading Sensor
Using UBlox RTK technology, it is possible to create a Moving Base/Rover arrangement where the Rover GNSS sensor holds the heading and distance from the Moving base. However, this information is available in a UBX sentence only.

This code will translate from UBX to a standard NMEA sentence. It is intended for a Pi Zero or similar controller.

Testing is on 
- A W10 development PC
- A Pi Zero running latest Raspbian Buster and Python 3.9

Edit HeadingSensor.py to select the correct comm port, nothing automatic here!
This code is currently an alpha version, no error checking, etc.
