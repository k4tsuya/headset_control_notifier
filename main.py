"""A simple notifier script to get the battery level using headset control."""

import json
import subprocess
import time

CHECK_INTERVAL = 300  # Check interval in seconds


class HeadsetNotifier:
    """Class to notify about the battery level using headset control."""

    HEADSETCONTROL_PATH = (
        "/usr/local/bin/headsetcontrol"  # Adjust this path if necessary.
    )
    NOTIFY_SEND_PATH = "/usr/bin/notify-send"  # Default path to notify-send.

    def __init__(self) -> None:
        """Initialize the HeadsetNotifier class."""
        self.battery_status = ""
        self.battery_level = 0
        self.get_battery_level()

    def get_battery_level(self) -> None:
        """Get the battery level from headset control."""
        command = [self.HEADSETCONTROL_PATH, "-o", "JSON"]
        try:
            headset_data = subprocess.run(
                command,
                capture_output=True,
                text=True,
            )
        except FileNotFoundError as e:
            msg = "Please ensure the path for headsetcontrol is correct."
            raise FileNotFoundError(msg) from e

        data = json.loads(headset_data.stdout.strip())
        self.battery_level = data["devices"][0]["battery"]["level"]
        self.battery_status = data["devices"][0]["battery"]["status"]

    def send_notification(self) -> None:
        """Send a notification about the battery level."""
        timeout = "-t"  # Timeout to prevent ubuntu notification issues.
        timeout_time = "5"
        title = "Battery Level"
        notification_message = (
            "The headset battery level is at: " + str(self.battery_level) + "%"
        )
        command = [
            self.NOTIFY_SEND_PATH,
            timeout,
            timeout_time,
            title,
            notification_message,
        ]

        subprocess.run(command)

    def check_battery_level(self) -> None:
        """Check the battery level and send a notification if it's low."""
        available = "BATTERY_AVAILABLE"
        battery_level_threshold = 20

        if self.battery_status != available:
            pass

        elif (
            self.battery_status == available
            and self.battery_level <= battery_level_threshold
        ):
            self.send_notification()


if __name__ == "__main__":
    while True:
        headset_notifier = HeadsetNotifier()
        headset_notifier.check_battery_level()

        time.sleep(CHECK_INTERVAL)
