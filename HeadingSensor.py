""""
Main routine for HeadingSensor
Forked from the Comm module of SD-Node, written c. 2017
Takes a serial UBX input, parses and extracts heading information
creates a NMEA sentence to forward the data and
optionally, forwards to a UDP address:port
Tested with Python >=3.6

By: JOR
    v0.1    28AUG21     First draft
"""

from datetime import datetime
import serial
import binascii

import ubx.ClassID as ubc
import ubx.MessageID as ubm

print('***** Heading Sensor *****')
print('Accepts mixed NMEA/UBX/RTCM data from a serial port and:')
print('1. Extracts heading information')
print('2. Outputs a NMEA sentence for other applications to use.')
print('3. Outputs to an IP address and port for other applications to use.')

# Configure the serial port, this should be ttyS0
Serial_Port1 = serial.Serial(
    # For Windows
    port='COM11',
    # For RPi
    #port='/dev/ttyS0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=2
)
Serial_Port1.flushInput()

# Main Loop
try:
    print("press [ctrl][c] at any time to exit...")
    while True:
        byte1 = Serial_Port1.read(1)
        if len(byte1) <1:
            break

        # Check for UBX
        if byte1 == b"\xb5":
            byte2 = Serial_Port1.read(1)
            if len(byte2) < 1:
                break
            if byte2 == b"\x62":
                # Get the UBX class
                byte3 = Serial_Port1.read(1)
                # Get the UBX message
                byte4 = Serial_Port1.read(1)
                # Get the UBX payload length
                byte5and6 = Serial_Port1.read(2)
                length_of_payload = int.from_bytes(byte5and6, "little", signed=False)
                ubx_payload = Serial_Port1.read(length_of_payload)
                # For diagnostics
                print(binascii.hexlify(ubx_payload))
                ubx_crc = Serial_Port1.read(2)

                if byte3 in ubc.UBX_CLASS:
                    if ubc.UBX_CLASS[byte3] == 'NAV':
                        if byte4 in ubm.UBX_NAV:
                            # NAV-RELPOSNED
                            if byte4 == b"\x3c":
                                print('NAV-RELPOSNED')
                                # Version = 1
                                version = ubx_payload[0]
                                print(f'Version {version}')
                                # Reserved = 0
                                reserved = ubx_payload[1]
                                print(f'Reserved {reserved}')
                                # Station ID = 00 00
                                refStationId = ubx_payload[2:3]
                                print(f'Referece Station {refStationId}')
                                # Format U4
                                iTOW = ubx_payload[4:7]
                                iTOW_in_ms = int.from_bytes(iTOW, "little", signed=False)
                                print(f'iTOW {iTOW_in_ms}')
                                # North, Format I4
                                relPosN = ubx_payload[8:11]
                                relPosN_in_cm = int.from_bytes(relPosN, "little", signed=True)
                                print(f'Relative North {relPosN_in_cm}')
                                # East, Format I4
                                relPosE = ubx_payload[12:15]
                                relPosE_in_cm = int.from_bytes(relPosE, "little", signed=True)
                                print(f'Relative East {relPosE_in_cm}')
                                # Down, Format I4
                                relPosD = ubx_payload[16:19]
                                relPosD_in_cm = int.from_bytes(relPosD, "little", signed=True)
                                print(f'Relative Down {relPosD_in_cm}')
                                # Length, Format I4
                                relPosLength = ubx_payload[20:23]
                                relPosLength_in_cm = int.from_bytes(relPosLength, "little", signed=False)
                                print(f'Relative Length {relPosLength_in_cm}')
                                # Heading, Format I4 scaled by 1e-5
                                relPosHeading = ubx_payload[24:27]
                                relPosHeading_in_deg = int.from_bytes(relPosHeading, "little", signed=False)/100000
                                print(f'Relative Length {relPosHeading_in_deg}')
        # Check for NMEA0183, leading with a $ symbol
        elif byte1 == b"\x24":
            nmea_full_bytes = Serial_Port1.readline()
            nmea_full_string = nmea_full_bytes.decode("utf-8")
            print(f'NMEA: {nmea_full_string[0:5]}')

        # Check for AIS, leading with a ! symbol
        elif byte1 == b"\x21":
            nmea_full_bytes = Serial_Port1.readline()
            nmea_full_string = nmea_full_bytes.decode("utf-8")
            print(f'AIS: {nmea_full_string[0:5]}')

        # Check for RTCM corrections
        elif byte1 == b"\xd3":
            # Find the message length
            byte2and3 = Serial_Port1.read(2)
            # The first 6 bits are reserved, but always zero, so convert the first two bytes directly to int
            length_of_payload = int.from_bytes(byte2and3, "big", signed=False)
            # Read the payload from the buffer
            rtcm_payload = Serial_Port1.read(length_of_payload)
            # Locate the message ID and convert it to an INT, its 12 bits of 16 so divide by 16
            message_id_bytes = rtcm_payload[0:2]
            message_id_int = int.from_bytes(message_id_bytes, "big")/16
            print(f'RTCM3: {str(message_id_int)}')
            # Finally extract the RTCM CRC
            rtcm_crc = Serial_Port1.read(3)
        else:
            print(f"What is {byte1}")


except KeyboardInterrupt:
    print("\n" + "Caught keyboard interrupt, exiting")
    exit(0)
finally:
    print("Exiting Main Thread")
    exit(0)

