import unittest
from Pixel import Pixel
from PixelData import PixelData

class TestPixel(unittest.TestCase):
    def test_methods(self):
        p = Pixel()
        pd = PixelData()
        pd.set_icon("i")
        pd.set_cursor(True)
        p.set_data(5,pd)

        pd,focused = p.get_data(5)
        self.assertTrue(focused)
        self.assertEqual(pd.icon, "i")

        pd,focused = p.get_data(6)
        self.assertFalse(focused)
        self.assertEqual(pd.icon, "i")

        self.assertEqual(len(p.data),1)
        p.remove_data(5)
        self.assertEqual(len(p.data),0)

if __name__ == "__main__":
    unittest.main()
