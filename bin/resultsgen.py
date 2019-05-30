#!/usr/bin/env python3

import os
import pandas as pd
import subprocess

from trackml.dataset import load_event
from trackml.randomize import shuffle_hits
from trackml.score import score_event


# Retrieve data
command = ['./ingest_data.sh']
print(command)
result = subprocess.call(command)
print(result)

event_prefix = 'event000001000'
hits, cells, particles, truth = load_event(os.path.join('/trackml/input/train_100_events', event_prefix))

## TODO: Receive prediction from served model

shuffled = shuffle_hits(truth, 0.05) # 5% probability to reassign a hit

print(shuffled.head())

# TODO: write shuffled to an artifact

