import unittest


from nmea.Utilities import calculate_crc


class nmeaTest(unittest.TestCase):

    def test_crc(self):
        #sentence = 'GPHDT,345.4155,T'
        sentence = 'GPGGA, 092725.00, 4717.11399, N, 00833.91590, E, 1, 08, 1.01, 499.6, M, 48.0, M,,'\
        #crc = '02'
        crc = '5B'
        calculated_crc = calculate_crc(sentence)
        self.assertEqual(crc, calculated_crc)
