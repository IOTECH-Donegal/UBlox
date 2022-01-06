from ubx.Utilities import itow

def meas(ubx_payload):
    '''
    :param ubx_payload:
    :return:
    '''

    # Switch this on for verbose processing
    debug = 0
    this_function = 'ubx-esf-meas'

    try:
         timeTag= ubx_payload[0:4]
    except ValueError as error:
        print(f'Exception in {this_function}\n {error}')


def status(ubx_payload):
    '''
    :param ubx_payload:
    :return:
    '''

    # Switch this on for verbose processing
    debug = 0
    this_function = 'ubx-esf-status'

    try:
         iTOW= ubx_payload[0:4]
         iTOW_in_ms = int.from_bytes(iTOW, "little", signed=False)
         itow_day, itow_hour, itow_min, itow_seconds = itow(iTOW_in_ms)
    except ValueError as error:
        print(f'Exception in {this_function}\n {error}')
