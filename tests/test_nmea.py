import unittest


from nmea.Utilities import calculate_crc


class nmeaTest(unittest.TestCase):

    def test_crc(self):
        sentence = 'GPHDT,345.3401,T'
        crc = '0x2B'
        calculated_crc = calculate_crc(sentence)
        self.assertEqual(crc, calculated_crc)
