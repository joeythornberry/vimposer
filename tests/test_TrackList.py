from TrackList import TrackList
import unittest

class TestTrackList(unittest.TestCase):
    def test_move_track(self):
        trax = TrackList()
        trax.create_track()
        trax.add_note(1,2,3,0)
        self.assertEqual(3,trax.tracks[0].chords[2].notes[1].l)
        trax.move_note(1,2,5,6,0)
        self.assertEqual(3,trax.tracks[0].chords[6].notes[5].l)

if __name__ == "__main__":
    unittest.main()
