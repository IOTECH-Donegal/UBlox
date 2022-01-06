from ubx.Utilities import itow

def posllh(ubx_payload):
    '''
    :param ubx_payload:
    :return: lon, lat, alt, hAcc, vAcc
    '''

    # Switch this on for verbose processing
    debug = 0

    try:
        iTOW = ubx_payload[0:4]
        iTOW_in_ms = int.from_bytes(iTOW, "little", signed=False)
        itow_day, itow_hour, itow_min, itow_seconds = itow(iTOW_in_ms)
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
            #print(binascii.hexlify(ubx_payload))
            print(f'iTOW Day = {itow_day} and time = {itow_hour:02d}:{itow_min:02d}:{itow_seconds:02d}')
            print(f'Longitude = {lon_in_degrees} degrees')
            print(f'Latitude = {lat_in_degrees} degrees')
            print('Last digit (7) = .011 meters')
            print(f'Altitude above elipsoid = {alt} meters')
            print(f'Horizontal accuracy = {hAcc_in_mm} millimeters')
            print(f'Vertical accuracy = {vAcc_in_mm} millimeters')

        return lon_in_degrees, lat_in_degrees, alt, hAcc_in_mm, vAcc_in_mm, iTOW_in_ms

    except ValueError as error:
        print(f'Exception in Parser-nav_relposned {error}')


def relposned(ubx_payload):
    '''
    :param ubx_payload:
    :return: relPosHeading_in_deg
    '''

    # Switch this on for verbose processing
    debug = 0

    try:
        # Version = 1
        version = ubx_payload[0]
        # Reserved = 0
        reserved = ubx_payload[1]
        # Station ID = 00 00
        refStationId = ubx_payload[2:3]
        refStationId_int = int.from_bytes(refStationId, "little", signed=False)
        # Format U4
        iTOW = ubx_payload[4:8]
        iTOW_in_ms = int.from_bytes(iTOW, "little", signed=False)
        itow_day, itow_hour, itow_min, itow_seconds = itow(iTOW_in_ms)
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
            #print(binascii.hexlify(ubx_payload))
            print(f'Version = {version}')
            print(f'Reserved = {reserved}')
            print(f'Reference Station ID = {refStationId_int}')
            print(f'iTOW Day = {itow_day} and time = {itow_hour:02d}:{itow_min:02d}:{itow_seconds:02d}')
            print(f'Relative North = {relPosN_in_cm} centimeters')
            print(f'Relative East = {relPosE_in_cm} centimeters')
            print(f'Relative Down = {relPosD_in_cm} centimeters')
            print(f'Relative Length = {relPosLength_in_cm} centimeters')
            print(f'Heading = {relPosHeading_in_deg} degrees')

        return relPosHeading_in_deg, iTOW_in_ms

    except ValueError as error:
        print(f'Exception in Parser-nav_relposned {error}')
        return 0

