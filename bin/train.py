#!/usr/bin/env python3

"""Executes training for TrackML"""

import time
import sys

if __name__ == '__main__':
    # Placeholder for actual training code
    sleep_sec = 5

    if (len(sys.argv) > 1):
        sleep_sec = sys.argv[1]

    print("Begin training ...")
    time.sleep(float(sleep_sec))
    print ("Training complete.")

