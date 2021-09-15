# Unique UBX sentences
from ubx.relposned import nav_relposned
from ubx.posllh import nav_posllh
from ubx.secuniqid import sec_uniqid

# Dictionaries of static data
import ubx.ClassID as ubc
import ubx.MessageID as ubm


def ubx_parser (byte3, byte4, ubx_payload):
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
        # Check if class = SEC (x27)
        if ubc.UBX_CLASS[byte3] == 'SEC':
            if byte4 in ubm.UBX_SEC:
                # Check for SEC-UNIQID (x03)
                if byte4 == b"\x03":
                    uniqueid = sec_uniqid(ubx_payload)
                    print(f'UBX-SEC-UNIQID {uniqueid}')
    else:
        print(f'No class definition for {byte3}')

