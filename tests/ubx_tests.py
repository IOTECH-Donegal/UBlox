import unittest

# Unique UBX sentences

from ubx.nav import relposned
from ubx.nav import posllh
from ubx.sec import uniqid


class ubxTest(unittest.TestCase):

    def test_relposned(self):
        with open('relposned.ubx', 'rb') as ubx_message:
            # Return value is the heading
            actual = (344.54628, 159213000)
            message = ubx_message.read()
            # drop the first 6 bytes
            result = relposned(message[6:])
            self.assertEqual(actual, result)

    def test_posllh(self):
        with open('posllh.ubx', 'rb') as ubx_message:
            # Return value is lon_in_degrees, lat_in_degrees, alt, hAcc_in_mm, vAcc_in_mm
            actual = (-7.4349109, 55.1666986, 163.582, 19, 29, 159802000)
            message = ubx_message.read()
            # drop the first 6 bytes
            result = posllh(message[6:])
            self.assertEqual(actual, result)

    def test_uniqid(self):
        with open('uniqid.ubx', 'rb') as ubx_message:
            # Return value is the heading
            actual = ('194DAA9258')
            message = ubx_message.read()
            # drop the first 6 bytes
            result = uniqid(message[6:])
            self.assertEqual(actual, result)

