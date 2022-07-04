# Battery notifier

This is a simple python script for notifying the user when it's time to connect/disconnect their charger to extend battery life.

# Usage
    usage: battery_notifier.py [-h] [--min MIN] [--max MAX] [--delay DELAY]

    Simple battery level notifier

    options:
      -h, --help     show this help message and exit
      --min MIN      Min battery level. Default: 30
      --max MAX      Max battery level. Default: 70
      --delay DELAY  Delay between checks. Default: 300

# Requirements
- plyer