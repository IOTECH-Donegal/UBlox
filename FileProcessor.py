import os
from datetime import datetime

# Utilities used by all UBX tools
from ubx.Utilities import ubx_crc
from ubx.Parser import ubx_parser

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
            # Read the first byte
            byte1 = ubx_file.read(1)
            if len(byte1) < 1:
                break
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
                    # Read the buffer for the payload length
                    ubx_payload = ubx_file.read(length_of_payload)
                    # Last two bytes are 2*CRC, save them for later use
                    ubx_crc_a = ubx_file.read(1)
                    ubx_crc_b = ubx_file.read(1)
                    # Calculate CRC using CLASS + MESSAGE + LENGTH + PAYLOAD
                    payload_for_crc = byte3 + byte4 + byte5and6 + ubx_payload
                    # If the CRC is good, proceed
                    if ubx_crc(payload_for_crc, ubx_crc_a, ubx_crc_b):
                        # Process the ubx bytes
                        ubx_parser(byte3, byte4, ubx_payload)
                    else:
                        print('Bad CRC')



