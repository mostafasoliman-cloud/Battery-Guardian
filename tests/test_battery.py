import unittest


class TestBatteryFormatting(unittest.TestCase):

    def test_format_hours_and_minutes(self):
        from core.battery import Battery

        self.assertEqual(
            Battery.get_time_left(3660),
            "1h 1m"
        )

    def test_unknown_time(self):
        from core.battery import Battery

        self.assertEqual(
            Battery.get_time_left(-1),
            "Unknown"
        )

        self.assertEqual(
            Battery.get_time_left(None),
            "Unknown"
        )


if __name__ == "__main__":
    unittest.main()
