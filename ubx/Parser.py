'''
Parser for UBX sentences.
Only sentences used are coded for.
'''
import binascii

def nav_relposned(ubx_payload):
    '''
    :param ubx_payload:
    :return: relPosHeading_in_deg
    '''

    debug = 1

    # Version = 1
    version = ubx_payload[0]
    # Reserved = 0
    reserved = ubx_payload[1]
    # Station ID = 00 00
    refStationId = ubx_payload[2:3]
    # Format U4
    iTOW = ubx_payload[4:7]
    iTOW_in_ms = int.from_bytes(iTOW, "little", signed=False)
    # North, Format I4
    relPosN = ubx_payload[8:12]
    relPosN_in_cm = int.from_bytes(relPosN, "little", signed=True)
    # East, Format I4
    relPosE = ubx_payload[12:16]
    relPosE_in_cm = int.from_bytes(relPosE, "little", signed=True)
    # Down, Format I4
    relPosD = ubx_payload[16:20]
    relPosD_in_cm = int.from_bytes(relPosD, "little", signed=True)
    # Length, Format I4
    relPosLength = ubx_payload[20:24]
    relPosLength_in_cm = int.from_bytes(relPosLength, "little", signed=True)

    # Heading, Format I4 scaled by 1e-5
    relPosHeading = ubx_payload[24:28]
    relPosHeading_in_deg = int.from_bytes(relPosHeading, "little", signed=True) / 100000

    if debug == 1:
        print('***** DEBUG - nav_relposned *****')
        print(binascii.hexlify(ubx_payload))
        print(f'Version {version}')
        print(f'Reserved {reserved}')
        print(f'Reference Station ID{refStationId}')
        print(f'iTOW {iTOW_in_ms}')
        print(f'Relative North {relPosN_in_cm} Centimeters')
        print(f'Relative East {relPosE_in_cm} Centimeters')
        print(f'Relative Down {relPosD_in_cm} Centimeters')
        print(f'Relative Length {relPosLength_in_cm} Centimeters')
        print(f'Heading {relPosHeading_in_deg} degrees')


    return relPosHeading_in_deg


def nav_posllh(ubx_payload):
    '''
    :param ubx_payload:
    :return: lon, lat, alt, hAcc, vAcc
    '''

    debug = 1

    iTOW = ubx_payload[0:4]
    iTOW_in_ms = int.from_bytes(iTOW, "little", signed=False)

    # Longitude, Format I4 scaled by 1e-7
    lon = ubx_payload[4:8]
    lon_in_degrees = int.from_bytes(lon, "little", signed=True)/10000000

    # Latitude, Format I4 scaled by 1e-7
    lat = ubx_payload[8:12]
    lat_in_degrees = int.from_bytes(lat, "little", signed=True) / 10000000

    # Height, Format I4
    height = ubx_payload[12:16]
    height_in_mm = int.from_bytes(height, "little", signed=True)

    # Height above ellipsoid, Format I4
    height = ubx_payload[12:16]
    height_in_mm = int.from_bytes(height, "little", signed=True)

    # Height above MSL, Format I4
    hMSL = ubx_payload[16:20]
    hMSL_in_mm = int.from_bytes(hMSL, "little", signed=True)

    alt = (height_in_mm) / 1000

    # Horizontal accuracy, Format U4
    hAcc = ubx_payload[20:24]
    hAcc_in_mm = int.from_bytes(hAcc, "little", signed=False)

    #  Vertical accuracy, Format U4
    vAcc = ubx_payload[24:28]
    vAcc_in_mm = int.from_bytes(vAcc, "little", signed=False)

    if debug == 1:
        print('***** DEBUG - nav_posllh *****')
        print(binascii.hexlify(ubx_payload))
        print(f'Longitude {lon_in_degrees} degrees')
        print(f'Latitude {lat_in_degrees} degrees')
        print('Last digit (7) = .011 meters')
        print(f'Altitude about elipsoid {alt} meters')
        print(f'Horizonal accuracy {hAcc_in_mm} millimeters')
        print(f'Vertical accuracy {vAcc_in_mm} millimeters')

    return lon_in_degrees, lat_in_degrees, alt, hAcc, vAcc

'''
8-bit Fletcher algorithm, which is used in the TCP standard RFC 1145
From UBlox Interface Descrip[tion manual
'''
def crc(ubx_payload):
    crc_a = 0
    crc_b = 0

    for byte in ubx_payload:
        crc_a += byte
        crc_a &= 0xFF
        crc_b += crc_a
        crc_b &= 0xFF
    return crc_a, crc_b

