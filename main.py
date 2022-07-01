#!/usr/bin/python3
import time
from plyer import notification


def battery_status():
    currentCapacity = int(open("/sys/class/power_supply/BAT1/capacity", "r").readline().strip())
    batteryStatus = open("/sys/class/power_supply/BAT1/status", "r").readline().strip()

    return currentCapacity, batteryStatus


def main():
    # Settings
    lowCharge = 40
    highCharge = 70
    remindInterval = 300

    while True:
        currentCapacity, batteryStatus = battery_status()

        if batteryStatus == "Discharging" and currentCapacity < lowCharge:
            notification.notify(
                title = "Battery low",
                message = "Please connect the charger",
                app_icon = None,
                timeout = 5
            )
        elif batteryStatus == "Charging" and currentCapacity > highCharge:
            notification.notify(
                title = "Battery charged",
                message = "Please disconnect the charger",
                app_icon = None,
                timeout = 5
            )

        time.sleep(remindInterval)


if __name__ == "__main__":
    main()
