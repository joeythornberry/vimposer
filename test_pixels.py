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

if __name__ == "__main__":
    unittest.main()

