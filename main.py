#!/usr/bin/python3
import time
from plyer import notification
import argparse


def get_battery_status():
    current_capacity = 0
    battery_status = "N/A"

    try:
        current_capacity = int(open("/sys/class/power_supply/BAT1/capacity", "r").readline().strip())
        battery_status = open("/sys/class/power_supply/BAT1/status", "r").readline().strip()
    except FileNotFoundError:
        print("Looks like you OS isn't supported or you don't have permission to access battery status")

    return current_capacity, battery_status


def main():
    # Default values
    low_charge = 30
    high_charge = 70
    delay_interval = 300

    parser = argparse.ArgumentParser(prog="battery_notifier.py", description="Process some integers")
    parser.add_argument("--min", help=f"Min battery level. Default: {low_charge}", type=int, default=low_charge)
    parser.add_argument("--max", help=f"Max battery level. Default: {high_charge}", type=int, default=high_charge)
    parser.add_argument("--delay", help=f"Delay between checks. Default: {delay_interval}", type=int,
                        default=delay_interval)
    args = parser.parse_args()

    low_charge, high_charge, delay_interval = args.min, args.max, args.delay

    if low_charge not in range(1, 100):
        print("Battery min level is out of range 1-100",
              f"Current value: {low_charge}",
              sep="\n"
              )
        exit()
    if high_charge not in range(1, 100):
        print(f"Battery max level is out of range 1-100",
              f"Current value: {high_charge}",
              sep="\n"
              )
        exit()
    if low_charge >= high_charge:
        print("Battery max level cannot be higher than battery min level",
              f"Min charger level: {low_charge}",
              f"Max charge level: {high_charge}",
              sep="\n"
              )
        exit()
    if delay_interval < 1:
        print("Delay between checks should be >= 1 sec")

    while True:
        current_capacity, battery_status = get_battery_status()

        if battery_status == "Discharging" and current_capacity < low_charge:
            notification.notify(
                title="Battery low",
                message="Please connect the charger",
                app_icon=None,
                timeout=5
            )
        elif battery_status == "Charging" and current_capacity > high_charge:
            notification.notify(
                title="Battery charged",
                message="Please disconnect the charger",
                app_icon=None,
                timeout=5
            )

        time.sleep(delay_interval)


if __name__ == "__main__":
    main()
