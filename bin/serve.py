#!/usr/bin/env python3

"""Wraps a trained model in a service"""

import time
import sys

if __name__ == '__main__':
# Placeholder for actual serving code
    sleep_sec = 5

    if (len(sys.argv) > 1):
        sleep_sec = sys.argv[1]

    time.sleep(float(sleep_sec))

