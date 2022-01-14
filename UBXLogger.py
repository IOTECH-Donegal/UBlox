""""
UBX
Forked from the Comm module of SD-Node, written c. 2017
Later mods from HeadingSensor, c. 2021
Takes a serial UBX input, parses and extracts heading information
Optionally, forwards to a UDP address:port
Tested with Python >=3.6

By: JOR
    v0.1    22SEP21     First draft
    v0.2    06JAN21     Rework for ZED-9R
"""

import serial
import sys

# Utilities used by all UBX tools
import ubx.Sensors
from ubx.Utilities import ubx_crc, log_file_name, path_name
from ubx.UBXParser import UBXParser

print('***** UBX Sensor *****')
print('Accepts UBX from a serial port:')
print('1. Logs to a file')

# Instantiate an object to parse UBX
myUBX = UBXParser()

# Get a logfile name for UBX
# ubx_log_file = './logfiles/' + log_file_name('.ubx')
ubx_log_file = '/home/pi/UBlox/logfiles/' + log_file_name('.ubx')
print(f'Logging as {ubx_log_file}')


# Main Loop
try:
    print("press [ctrl][c] at any time to exit...")

    with serial.Serial("COM14") as Serial_Port1:
        Serial_Port1.baudrate = 38400
        Serial_Port1.bytesize = serial.EIGHTBITS
        Serial_Port1.parity = serial.PARITY_NONE
        Serial_Port1.stopbits = serial.STOPBITS_ONE
        Serial_Port1.timeout = None

        Serial_Port1.flushInput()

        # Find the serial number of the UBlox device, send the query, it will be the first sentence back
        ubx_sec_uniqid_query = b'\xB5\x62\x27\x03\x00\x00\x2A\xA5'
        Serial_Port1.write(ubx_sec_uniqid_query)

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
                    # Read the buffer for the payload length
                    ubx_payload = Serial_Port1.read(length_of_payload)
                    # Last two bytes are 2*CRC, save them for later use
                    ubx_crc_a = Serial_Port1.read(1)
                    ubx_crc_b = Serial_Port1.read(1)
                    # Calculate CRC using CLASS + MESSAGE + LENGTH + PAYLOAD
                    payload_for_crc = byte3 + byte4 + byte5and6 + ubx_payload
                    # If the CRC is good, proceed
                    if ubx_crc(payload_for_crc,ubx_crc_a, ubx_crc_b):
                        # Log the ubx bytes
                        payload_for_save = byte1 + byte2 + payload_for_crc + ubx_crc_a + ubx_crc_b
                        with open (ubx_log_file, 'ab') as file:
                            file.write(payload_for_save)
                    # Process the ubx bytes
                        # Reset the new data flags
                        myUBX.new_heading = 0
                        myUBX.new_position = 0
                        # Parse
                        myUBX.ubx_parser(byte3, byte4, ubx_payload)
                        # Now see if there are new values
                    else:
                        print('Bad CRC')

            # Check for NMEA0183, leading with a $ symbol
            elif byte1 == b"\x24":
                nmea_full_bytes = Serial_Port1.readline()
                nmea_full_string = nmea_full_bytes.decode("utf-8")
                print(f'NMEA: Received {nmea_full_string[0:5]}')

            # Check for AIS, leading with a ! symbol
            elif byte1 == b"\x21":
                nmea_full_bytes = Serial_Port1.readline()
                nmea_full_string = nmea_full_bytes.decode("utf-8")
                print(f'AIS: Received {nmea_full_string[0:5]}')

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
                print(f'RTCM3: Received {str(message_id_int)}')
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
    print("Unexpected error in UBX Sensor:", sys.exc_info()[0])
finally:
    print("Exiting Main Thread")
    exit(0)

