import unittest
from calculate_background_icon import calculate_background_icon

class TestCalculateBackgroundIcon(unittest.TestCase):
    def test_calculate_background_icon(self):
        self.assertEqual("c",calculate_background_icon(0,0))
        self.assertEqual("c",calculate_background_icon(11,0))

if __name__ == "__main__":
    unittest.main()
