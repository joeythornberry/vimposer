import unittest
import pixels

class test_pixels(unittest.TestCase):
    def test_get_drawable(self):
        self.p = pixels.Pixel()
        self.p.set_drawable(5,pixels.Drawable("d",1))
        d, exists = self.p.get_drawable(5)
        self.assertEqual(d.icon,"d")
        self.assertTrue(exists)
        self.p.remove_drawable(5)
        self.assertFalse(self.p.tracks)
        d, exists = self.p.get_drawable(5)
        self.assertFalse(exists)

    def test_pixel_list(self):
        self.pl = pixels.PixelList()
        self.pl.set_drawable(4,5,6,pixels.Drawable("d",7))
        d, exists = self.pl.get_drawable(4,5,6)
        self.assertTrue(exists)
        self.assertEqual(d.icon,"d")
        self.assertEqual(d.color,7)
        d2,exists2 = self.pl.get_drawable(4,5,900)
        self.assertFalse(exists2)
        d3, exists3 = self.pl.get_drawable(900,5,6)
        self.assertFalse(exists3)
        self.pl.remove_drawable(4,5,6)
        d, exists = self.pl.get_drawable(4,5,6)
        self.assertFalse(exists)
if __name__ == "__main__":
    unittest.main()

