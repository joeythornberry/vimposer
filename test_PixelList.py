import unittest
from PixelData import PixelData
from Pixel import Pixel
from PixelList import PixelList

class TestPixelList(unittest.TestCase):
    def test_methods(self):
        pix = PixelList()
        pd = PixelData()

        pd.set_icon("i")
        pd.set_cursor(True)

        pix.set_data(1,2,3,pd)
        pd,type = pix.get_data(1,2,3)
        self.assertEqual(type,"focused_track")
        pd,type = pix.get_data(1,2,4)
        self.assertEqual(type,"unfocused_track")

        pix.remove_data(1,2,3)
        pd,type = pix.get_data(1,2,3)
        self.assertEqual(type,"background")

if __name__ == "__main__":
    unittest.main()
