import frontend
import unittest

class Window:
    def __init__(self):
        pass

class TestFrontend(unittest.TestCase):
    def test_load_colors(self):
        self.w = Window()
        self.f = frontend.Frontend(self.w)
        self.f.rgb_codes = [
                (1000,0,0),
                (0,1000,0),
                (0,0,1000)
                ]
        color_count = self.f.load_colors()
        self.assertEqual(color_count,3)

        self.assertIsNotNone(self.f.colors[2].f)
        self.f.close()

if __name__ == "__main__":
    unittest.main()
