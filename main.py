#!/usr/bin/python3
import time
from plyer import notification
import argparse


def battery_status():
    currentCapacity = 0
    batteryStatus = "N/A"

    try:
        currentCapacity = int(open("/sys/class/power_supply/BAT1/capacity", "r").readline().strip())
        batteryStatus = open("/sys/class/power_supply/BAT1/status", "r").readline().strip()
    except FileNotFoundError:
        print("Looks like you OS isn't supported or you don't have permission to access battery status")

    return currentCapacity, batteryStatus


def main():
    # Default values
    lowCharge = 30
    highCharge = 70
    remindInterval = 300

    parser = argparse.ArgumentParser(prog="battery_notifier.py", description="Process some integers")
    parser.add_argument("--min", help=f"Min battery level. Default: {lowCharge}", type=int, default=lowCharge)
    parser.add_argument("--max", help=f"Max battery level. Default: {highCharge}", type=int, default=highCharge)
    parser.add_argument("--delay", help=f"Delay between checks. Default: {remindInterval}", type=int, default=remindInterval)
    args = parser.parse_args()

    lowCharge, highCharge, remindInterval = args.min, args.max, args.delay

    if lowCharge not in range(1, 100):
        print("Battery min level is out of range 1-100",
              f"Current value: {lowCharge}",
              sep="\n"
              )
        exit()
    if highCharge not in range(1, 100):
        print(f"Battery max level is out of range 1-100",
              f"Current value: {highCharge}",
              sep="\n"
              )
        exit()
    if lowCharge >= highCharge:
        print("Battery max level cannot be higher than battery min level",
              f"Min charger level: {lowCharge}",
              f"Max charge level: {highCharge}",
              sep="\n"
              )
        exit()
    if remindInterval < 1:
        print("Delay between checks should be >= 1 sec")

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
