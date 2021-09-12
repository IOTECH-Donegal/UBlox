""""
Main routine for HeadingSensor
Forked from the Comm module of SD-Node, written c. 2017
Takes a serial UBX input, parses and extracts heading information
creates a NMEA sentence to forward the data and
optionally, forwards to a UDP address:port
Tested with Python >=3.6

By: JOR
    v0.1    28AUG21     First draft
    v0.2    12SEP21     Read 2 x UBX and prints to screen
"""

import serial
import sys

# Dictionaries of static data
import ubx.ClassID as ubc
import ubx.MessageID as ubm

# Utilities used by all UBX tools
from ubx.Utilities import crc

# Unique UBX sentences
from ubx.relposned import nav_relposned
from ubx.posllh import nav_posllh

print('***** Heading Sensor *****')
print('Accepts mixed UBX-RELPOSNED, UBX_POSLLH from a serial port:')
print('1. Extracts heading, position, accuracy information')
print('NOT YET IMPLEMENTED')
print('2. Outputs a NMEA sentence for other applications to use.')
print('3. Optionally, outputs to an IP address and port for other applications to use.')

# Configure the serial port
Serial_Port1 = serial.Serial(
    # For Windows
    port='COM13',
    # For RPi
    #port='/dev/ttyS0',
    baudrate=38400,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=2
)
Serial_Port1.flushInput()

# Main Loop
try:
    print("press [ctrl][c] at any time to exit...")
    # Continuous loop until [ctrl][c]
    while True:
        # Read the first byte, if no byte, loop
        byte1 = Serial_Port1.read(1)
        if len(byte1) <1:
            break
        # Check for UBX header = xB5 and X62, Unicode = µb
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
                # Calculate the length of the payload
                length_of_payload = int.from_bytes(byte5and6, "little", signed=False)
                # Read the buffer for the payload length, should be 64 bytes
                ubx_payload = Serial_Port1.read(length_of_payload)
                # Last two bytes are 2*CRC
                ubx_crc_a_int = int.from_bytes(Serial_Port1.read(1), "little")
                ubx_crc_b_int = int.from_bytes(Serial_Port1.read(1), "little")
                # Calculate CRC using CLASS + MESSAGE + LENGTH + PAYLOAD
                payload_for_crc = byte3 + byte4 + byte5and6 + ubx_payload
                # Go get the two CRCs
                crc_a, crc_b = crc(payload_for_crc)
                # Now catch the error if there is one
                if ubx_crc_a_int != crc_a:
                    print(f'CRC_A Error, {ubx_crc_a_int} not equal to {crc_a}')
                    break
                if ubx_crc_b_int != crc_b:
                    print(f'CRC_B Error, {ubx_crc_b_int} not equal to {crc_b}')
                    break

                # For diagnostics only
                # print(binascii.hexlify(ubx_payload))

                # Check if a valid UBX class
                if byte3 in ubc.UBX_CLASS:
                    # Check if class = NAV (x01)
                    if ubc.UBX_CLASS[byte3] == 'NAV':
                        # Check if a valid message
                        if byte4 in ubm.UBX_NAV:
                            # Check for NAV-RELPOSNED (x3c)
                            if byte4 == b"\x3c":
                                heading = nav_relposned(ubx_payload)
                            # Check for NAV-POSLLH (x02)
                            elif byte4 == b"\x02":
                                lon, lat, alt, hAcc, vAcc = nav_posllh(ubx_payload)
                            else:
                                print(f'JOR still needs to do parser for {byte4}!!')

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
            message_id_int = int.from_bytes(message_id_bytes, "big") / 16
            print(f'RTCM3: {str(message_id_int)}')
            # Finally extract the RTCM CRC
            rtcm_crc = Serial_Port1.read(3)
        else:
            print(f"What is {byte1}")

except serial.SerialException as err:
    print("Serial port error: {0}".format(err))
except OSError as err:
    print("OS error: {0}".format(err))
except ValueError as err:
    print("Value Error error: {0}".format(err))
except KeyboardInterrupt:
    print("\n" + "Caught keyboard interrupt, exiting")
    exit(0)
except:
    print("Unexpected error:", sys.exc_info()[0])
finally:
    print("Exiting Main Thread")
    exit(0)

