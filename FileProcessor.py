import os
from datetime import datetime

# Utilities used by all UBX tools
from ubx.Utilities import crc

# Dictionaries of static data
import ubx.ClassID as ubc
import ubx.MessageID as ubm

# Unique UBX sentences
from ubx.relposned import nav_relposned
from ubx.posllh import nav_posllh

# Look through the raw data files
directory = './logfiles'
# Open every file in sequence

for file in os.listdir(directory):
    input_filename = 'logfiles/' + file
    print("Found " + input_filename)

    with open(input_filename, 'rb') as ubx_file:
        while True:
            # Read the first byte, if no byte, loop
            byte1 = ubx_file.read(1)
            if len(byte1) < 1:
                break
            # Read the first byte, if no byte, loop
            byte1 = ubx_file.read(1)
            # Check for UBX header = xB5 and X62, Unicode = µb
            if byte1 == b"\xb5":
                byte2 = ubx_file.read(1)
                if byte2 == b"\x62":
                    # Get the UBX class
                    byte3 = ubx_file.read(1)
                    # Get the UBX message
                    byte4 = ubx_file.read(1)
                    # Get the UBX payload length
                    byte5and6 = ubx_file.read(2)
                    # Calculate the length of the payload
                    length_of_payload = int.from_bytes(byte5and6, "little", signed=False)
                    # Read the buffer for the payload length, should be 64 bytes
                    ubx_payload = ubx_file.read(length_of_payload)
                    # Last two bytes are 2*CRC, save them for later use
                    ubx_crc_a = ubx_file.read(1)
                    ubx_crc_b = ubx_file.read(1)
                    # Then convert them to INT
                    ubx_crc_a_int = int.from_bytes(ubx_crc_a, "little")
                    ubx_crc_b_int = int.from_bytes(ubx_crc_b, "little")
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

                    # Check if a valid UBX class
                    if byte3 in ubc.UBX_CLASS:
                        # Check if class = NAV (x01)
                        if ubc.UBX_CLASS[byte3] == 'NAV':
                            # Check if a valid message
                            if byte4 in ubm.UBX_NAV:
                                # Check for NAV-RELPOSNED (x3c)
                                if byte4 == b"\x3c":
                                    print('UBX-NAV-RELPOSNED')
                                    heading = nav_relposned(ubx_payload)
                                # Check for NAV-POSLLH (x02)
                                elif byte4 == b"\x02":
                                    print('UBX-NAV-POSLLH')
                                    lon, lat, alt, hAcc, vAcc = nav_posllh(ubx_payload)
                                else:
                                    print(f'JOR still needs to do parser for {byte4}!!')


