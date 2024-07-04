import unittest
from unittest.mock import patch
import vapi
    
class TestCursor(unittest.TestCase):
    @patch("frontend.Frontend")
    @patch("KeyboardManager.KeyboardManager")
    @patch("window.Window")
    def test_cursor(self,MF,MS,MKM):
        self.v = vapi.VimposerAPI(MF(MS),MKM())
        self.v.add_track()
        self.v.create_note(4,5,6)
        l = self.v.get_note_duration(4,5)
        self.assertEqual(l,6)

        self.v.set_note_cursor(4,5,6,True)
        for i in range(6):
            self.assertTrue(self.v.get_pixel(4,5+i).cursor)
        self.v.set_note_cursor(4,5,6,False)
        for i in range(6):
            self.assertFalse(self.v.get_pixel(4,5+i).cursor)

if __name__ == "__main__":
    unittest.main()
