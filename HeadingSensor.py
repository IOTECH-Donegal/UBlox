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
import sys
import ubx.ClassID as ubc
import ubx.MessageID as ubm
import ubx.Parser


print('***** Heading Sensor *****')
print('Accepts mixed UBX-RELPOSNED from a serial port and:')
print('1. Extracts heading information')
print('2. Outputs a NMEA sentence for other applications to use.')
print('3. Optionally, outputs to an IP address and port for other applications to use.')

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
                # print(binascii.hexlify(ubx_payload))
                ubx_crc = Serial_Port1.read(2)

                if byte3 in ubc.UBX_CLASS:
                    if ubc.UBX_CLASS[byte3] == 'NAV':
                        if byte4 in ubm.UBX_NAV:
                            # NAV-RELPOSNED
                            if byte4 == b"\x3c":
                                heading = ubx.Parser.nav_relposned(ubx_payload)
                                print(heading)
        else:
            print(f"What is {byte1} ??")

except serial.SerialException as err:
    print("Serial lort error: {0}".format(err))
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

