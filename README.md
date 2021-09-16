# Heading Sensor
Using UBlox RTK technology, it is possible to create a Moving Base/Rover arrangement where the Rover GNSS sensor holds the heading and distance from the Moving base. However, this information is available in a UBX sentence only.

This code will translate from UBX to a standard NMEA sentence. It is intended for a Pi Zero or similar controller.

Testing is on 
- A W10 development PC
- A Pi Zero running latest Raspbian Buster and Python 3.9

## HeadingSensor.py
Edit to select the correct comm port, nothing automatic here!

- Translates 3 UBX sentences for position, heading and sensor ID.
- Has debug functions in the code, switch on debug flag for verbose status on screen
- Shows UBX, NMEA, RTCM sentence types, for diagnostics only
- Saves time/date stamped files to /logfiles directory as *.ubx
- Outputs a NMEA THS sentence with heading information

## FileProcessor.py
This is intended for post-processing.

- Open all files in /logfiles directory
- Extracts required information
- Saves in /ProcessedData as a single csv file.
