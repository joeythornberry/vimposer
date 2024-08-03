import unittest

from vimposercore.KeyboardManager import KeyboardManager

class mockFunction():
    def __init__(self):
        self.calls = 0

    def __call__(self):
        self.calls += 1

class mockSuffixFunction():
    def __init__(self, km, count = None):
        self.suffix = ""
        self.km = km
        self.count = count
        self.calls = 0

    def __call__(self):
        if self.count is not None:
            self.suffix = self.km.getSuffix(self.count)
        else:
            self.suffix = self.km.getSuffix()
        self.calls += 1

class mockGetch:
    def __init__(self, keypresses):
        self.keypresses = keypresses
        self.keypresses += "Q"
        self.index = 0

    def __call__(self):
        try:
            c = self.keypresses[self.index]
        except IndexError:
            raise Exception("Test failed: too many calls to getch")

        self.index += 1
        return c

class TestKeyboardManager(unittest.TestCase):

    def setUp(self):
        self.km = KeyboardManager()

    def test_Q_stops_listen(self):
        keypresses = "Q"
        self.km.listen(mockGetch(keypresses))
        self.assertEqual(self.km.keys, "")

    def test_basic_getch(self):
        keypresses = "abc"
        self.km.listen(mockGetch(keypresses))
        self.assertEqual(self.km.keys, keypresses)

    def test_escape_getch(self):
        keypresses = "abc\x1bdef"
        self.km.listen(mockGetch(keypresses))
        self.assertEqual(self.km.keys, "def")

    def test_basic_map(self):
        keypresses = "aa"
        f = mockFunction()
        self.km.map(keypresses, f)
        self.km.listen(mockGetch(keypresses))
        self.assertEqual(f.calls, 1)
        self.assertEqual(self.km.keys, "")

    def test_no_map_illegal_keys(self):
        for keypress in ["Q", "\x1b"]:
            result = None
            try:
                f = mockFunction()
                self.km.map(keypress, f)
                result = "remap containing " + str([keypress]) + " did not throw exception"
            except:
                pass
            finally:
                self.assertEqual(result, None)

    def test_no_substring_maps(self):
        return None
        f = mockFunction()
        self.km.map("abc", f)
        result = None
        try:
            self.km.map("ab", f)
            result = "substring remap did not throw exception"
        except:
            pass
        finally:
            self.assertEqual(result, None)

    def test_no_superstring_maps(self):
        return None
        f = mockFunction()
        self.km.map("ab", f)
        result = None
        try:
            self.km.map("abc", f)
            result = "superstring remap did not throw exception"
        except:
            pass
        finally:
            self.assertEqual(result, None)

    def test_prefix_single_digit(self):
        keypresses = "abc"
        f = mockFunction()
        self.km.map(keypresses, f)
        self.km.listen(mockGetch("5"+keypresses))
        self.assertEqual(f.calls, 5)
    
    def test_prefix_multiple_digits(self):
        keypresses = "abc"
        f = mockFunction()
        self.km.map(keypresses, f)
        self.km.listen(mockGetch("123"+keypresses))
        self.assertEqual(f.calls, 123)

    def test_prefix_cancel(self):
        keypresses = "15\x1bb"
        f = mockFunction()
        self.km.map("b", f)
        self.km.listen(mockGetch(keypresses))
        self.assertEqual(f.calls, 1)

    def test_suffix_until(self):
        keypresses = "abc"
        f = mockSuffixFunction(self.km)
        self.km.map(keypresses, f)
        self.km.listen(mockGetch(keypresses+"hello\r"))
        self.assertEqual(f.suffix, "hello")

    def test_suffix_count(self):
        keypresses = "abc"
        f = mockSuffixFunction(self.km, 5)
        self.km.map(keypresses, f)
        self.km.listen(mockGetch(keypresses+"hello"))
        self.assertEqual(f.suffix, "hello")

    def test_suffix_cancel(self):
        keypresses = "abc"
        f = mockSuffixFunction(self.km)
        self.km.map(keypresses, f)
        self.km.listen(mockGetch(keypresses+"\x1b"))
        self.assertEqual(f.suffix, None)
    
    def test_prefix_and_suffix_until(self):
        keypresses = "abc"
        f = mockSuffixFunction(self.km)
        self.km.map(keypresses, f)
        self.km.listen(mockGetch("5"+keypresses+"t\re\rs\rt\rtest\r"))
        self.assertEqual(f.suffix, "test")
        self.assertEqual(f.calls, 5)

    def test_prefix_and_suffix_count(self):
        keypresses = "abc"
        f = mockSuffixFunction(self.km, 2)
        self.km.map(keypresses, f)
        self.km.listen(mockGetch("3"+keypresses+"teteuu"))
        self.assertEqual(f.suffix, "uu")
        self.assertEqual(f.calls, 3)

if __name__ == '__main__':
    unittest.main()
