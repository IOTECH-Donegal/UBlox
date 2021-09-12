'''
Utilities for UBX sentences.
'''


def crc(ubx_payload):
    """
    8-bit Fletcher algorithm, which is used in the TCP standard RFC 1145
    From UBlox Interface Description manual
    """

    crc_a = 0
    crc_b = 0

    for byte in ubx_payload:
        crc_a += byte
        crc_a &= 0xFF
        crc_b += crc_a
        crc_b &= 0xFF
    return crc_a, crc_b

'''
Time/date as an integer week number (TOW)
and a time of week expressed in seconds.
'''
def itow(iTOW_in_ms):
    # Convert from ms to seconds
    itow_total_seconds = iTOW_in_ms / 1000
    # Calcuate number of seconds in
    day = 24 * 60 * 60
    hour = 60 * 60
    minute = 60
    # The day will be
    itow_day = int(itow_total_seconds / day)
    itow_hour = int((itow_total_seconds - (itow_day * day)) / hour)
    itow_minute = int((itow_total_seconds - (itow_day * day) - (itow_hour * hour)) / minute)
    itow_seconds = int((itow_total_seconds - (itow_day * day) - (itow_hour * hour)) - (itow_minute * minute))
    return itow_day, itow_hour, itow_minute, itow_seconds