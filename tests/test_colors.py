import unittest
import vapi
from KeyboardManager import KeyboardManager
from frontend import Frontend

class MockFrontend(Frontend):
    def init(self,w):
        pass

    def load_colors(self):
        return 5

class TestColors(unittest.TestCase):
    def test_assign_colors(self):
        f = MockFrontend("window")
        km = KeyboardManager()
        v = vapi.VimposerAPI(f,km)
        self.assertEqual(v.num_colors,5)
        v.add_track()
        self.assertEqual(v.tracks[0].color,0)
        v.add_track()
        self.assertEqual(v.tracks[1].color,1)
        f.close()

if __name__ == "__main__":
    unittest.main()
