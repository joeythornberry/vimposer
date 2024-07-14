import unittest
from Screen import Screen
from NoteData import NoteData

class TestScreen(unittest.TestCase):
    def test_get_locations(self):
        s = Screen()
        n = NoteData(4,5,6)
        locs = []
        for l in s.get_locations(n):
            locs.append(l)
        self.assertEqual(len(locs),6)

if __name__ == "__name__":
    unittest.main()
