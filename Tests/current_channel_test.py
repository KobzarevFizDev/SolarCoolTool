from unittest import main, TestCase
from Models.models import CurrentChannel

class CurrentChannelTest(TestCase):
    def test_change_to_available_channel(self) -> None:
        msg = "change channel not working"
        current_channel = CurrentChannel()
        current_channel.channel = 131
        expected = 131
        actual = current_channel.channel
        self.assertEqual(expected, actual, msg)

    def test_change_to_not_available_channel(self) -> None:
        current_channel = CurrentChannel()
        with self.assertRaises(Exception):
            current_channel.channel = 121


if __name__ == "__main__":
    main()
