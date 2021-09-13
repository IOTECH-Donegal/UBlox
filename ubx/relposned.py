from ubx.Utilities import itow

def nav_relposned(ubx_payload):
    '''
    :param ubx_payload:
    :return: relPosHeading_in_deg
    '''

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

        return relPosHeading_in_deg

    except ValueError as error:
        print(f'Exception in Parser-nav_relposned {error}')
        return 0

