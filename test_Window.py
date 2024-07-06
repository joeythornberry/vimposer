import unittest

from Window import Window

class TestWindow(unittest.TestCase):
    def test_translate_coords(self):
        w = Window()
        w.set_dimensions(1,20,1,20)
        y,x,onscreen = w.translate_coords(4,5)
        self.assertTrue(onscreen)
        line,char = w.translate_coords_reverse(y,x)
        self.assertEqual(line,4)
        self.assertEqual(char,5)

if __name__ == "__main__":
    unittest.main()
