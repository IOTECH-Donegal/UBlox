import sys
# Unique UBX sentences
import ubx.Sensors
# Get the message parsers
from ubx.nav import relposned
from ubx.nav import posllh
from ubx.sec import uniqid

# Dictionaries of static data
import ubx.ClassID as ubc
import ubx.MessageID as ubm

# List of sensor serial numbers and allocations
from ubx.Sensors import UBLOX


class UBXParser():
    # Constructor
    def __init__(self):

        # Switch this on for verbose processing
        self.debug = 1

        # Timers for each sentence, check to see if data stale when calling this class
        self.posllh_TOW = ''
        self.relposned_TOW = ''

        # Properties used by calling program
        self.unique_id = ''
        self.longitude = 0
        self.latitude = 0
        self.altitude = 0
        self.horizontal_accuracy = 0
        self.vertical_accuracy = 0
        self.heading = 0

        # Status values, set when updated, reset from the calling program
        self.new_position = 0
        self.new_heading = 0

    def ubx_parser(self, byte3, byte4, ubx_payload):
        # Check if a valid UBX class
        if byte3 in ubc.UBX_CLASS:
            # Check if class = NAV (x01)
            if ubc.UBX_CLASS[byte3] == 'NAV':
                # Check if a valid message
                if byte4 in ubm.UBX_NAV:
                    # Check for NAV-RELPOSNED (x3c)
                    if byte4 == b"\x3c":
                        # Now parse
                        self.heading, self.relposned_TOW = relposned(ubx_payload)
                        # Now let the calling program know there is a new heading
                        self.new_heading = 1
                        if self.debug == 1:
                            print(f'UBX-NAV-RELPOSNED {self.heading, self.relposned_TOW}')
                    # Check for NAV-POSLLH (x02)
                    elif byte4 == b"\x02":
                        # Now parse
                        self.longitude, self.latitude, self.altitude, \
                            self.horizontal_accuracy, self.vertical_accuracy,self.posllh_TOW = posllh(ubx_payload)
                        # Now let the calling program know there is a new position
                        self.new_position = 1
                        if self.debug == 1:
                            print(f'UBX-NAV-POSLLH {self.longitude, self.latitude, self.altitude, self.posllh_TOW}')
                    else:
                        print(f'NAV - No message definition for {byte3}-{byte4}')
            # Check if class = SEC (x27)
            if ubc.UBX_CLASS[byte3] == 'SEC':
                if byte4 in ubm.UBX_SEC:
                    # Check for SEC-UNIQID (x03)
                    if byte4 == b"\x03":
                        # Now parse
                        self.unique_id = uniqid(ubx_payload)
                        try:
                            if self.unique_id in UBLOX:
                                print(f'UBX-SEC-UNIQID: {self.unique_id} {UBLOX.get(self.unique_id)} existing sensor verified as connected')
                            else:
                                print(f'UBX-SEC-UNIQID: {self.unique_id} unknown sensor verified as connected')
                        except:
                            print("Unexpected error in UBX-SEC:", sys.exc_info()[0])
                    else:
                        print(f'SEC - No message definition for {byte3}-{byte4}')

            # Check if class = ESF (x10)
            if ubc.UBX_CLASS[byte3] == 'ESF':
                if byte4 in ubm.UBX_ESF:
                    # Check for ESF-MEAS (x02)
                    if byte4 == b"\x02":
                        if self.debug == 1:
                            print('Found an ESF measurement')
                    # Check for ESF-MEAS (x10)
                    if byte4 == b"\x10":
                        if self.debug == 1:
                            print('Found an ESF status')
                else:
                    print(f'ESF - No message definition for {byte4}')
        else:
            print(f'No class definition for {byte3}')
