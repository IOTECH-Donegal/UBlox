# Typical return value = B5 62 27 03 09 00 01 00 00 00 19 4D AA 92 58 2E B6
# Giving a serial number of 19 4D AA 92 58

def uniqid(ubx_payload):
    '''
    :param ubx_payload:
    :return: uniqid
    '''

    # Switch this on for verbose processing
    debug = 0

    try:
        # Version = 1
        version = ubx_payload[0]
        # Reserved = 0
        reserved = ubx_payload[1]
        # Unique ID
        uniqid_bytes = ubx_payload[4:9]
        uniqid_hex = uniqid_bytes.hex()
        uniqid = uniqid_hex.upper()

        if debug == 1:
            print('***** DEBUG - sec_uniqid *****')
            #print(binascii.hexlify(ubx_payload))
            print(f'Version = {version}')
            print(f'Reserved = {reserved}')
            print(f'Unique ID = {uniqid}')

        return uniqid

    except ValueError as error:
        print(f'Exception in Parser-nav_relposned {error}')