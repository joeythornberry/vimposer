import unittest
import track

class TestTrack(unittest.TestCase):
    def setUp(self):
        self.t = track.Track()

    def test_add_note(self):
        self.t = track.Track()
        self.t.extend_to(5)
        self.t.add_note(1,2,track.Note(3))
        for num in [2,3]:
            self.assertIn(str(num), str(self.t.chords[1]))

    def test_remove_note(self):
        self.t = track.Track()
        self.t.add_note(1,2,track.Note(3))
        self.t.remove_note(1,2)
        self.assertNotIn(1,self.t.chords)

        self.t.add_note(5,6,track.Note(7))
        self.t.add_note(1,2,track.Note(3))
        self.t.remove_note(1,2)
        self.assertIn(5,self.t.chords)
        self.assertIn(6,self.t.chords[5].notes)

class TestChord(unittest.TestCase):
    def setUp(self):
        self.c = track.Chord()

    def test_add_note(self):
        self.c = track.Chord()
        self.c.add_note(10,track.Note(4))
        self.c.add_note(5,track.Note(8))
        self.assertEqual(len(self.c.notes), 2)
        for num in [10,5,4,8]:
            self.assertIn(str(num), str(self.c))

    def test_pitch_occupied(self):
        self.c = track.Chord()
        self.c.add_note(4, track.Note(4))
        self.assertTrue(self.c.pitch_occupied(4))
        self.assertFalse(self.c.pitch_occupied(6))

    def test_remove_note(self):
        self.c = track.Chord()
        self.c.add_note(4, track.Note(4))
        note = self.c.remove_note(4)
        self.assertFalse(self.c.pitch_occupied(4))
        self.assertEqual(note.d, 4)

if __name__ == "__main__":
    unittest.main()
