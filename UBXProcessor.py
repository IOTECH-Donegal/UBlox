import os
import csv

# Utilities used by all UBX tools
from ubx.Utilities import ubx_crc, log_file_name
from ubx.UBXParser import UBXParser

# Instantiate an object to parse UBX
myUBX = UBXParser()

# Look through the raw data files
directory = './logfiles'


def save_csv():
    output_file_name = './processed/summary.csv'
    # First check if a CSV file has already been opened
    if os.path.isfile(output_file_name):
        # Append to summary file
        output_file = open(output_file_name, 'a', newline='')
        with output_file:
            line_data = [myUBX.posllh_TOW, myUBX.longitude, myUBX.latitude, myUBX.altitude, myUBX.heading,
                            myUBX.vertical_accuracy, myUBX.horizontal_accuracy]
            writer = csv.writer(output_file)
            writer.writerow(line_data)
    else:
        output_file_name = './processed/summary.csv'
        print('Saving data as ' + output_file_name)
        # Now create the CSV file and headers
        output_file = open(output_file_name, 'w', newline='')
        with output_file:
            file_header = ['TOW', 'Longitude', 'Latitude', 'Altitude', 'Heading', 'V-Accuracy', 'H-Accuracy']
            writer = csv.writer(output_file)
            writer.writerow(file_header)


for file in os.listdir(directory):
    # Open every file in sequence
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
                        myUBX.ubx_parser(byte3, byte4, ubx_payload)
                        save_csv()
                    else:
                        print('Bad CRC')


