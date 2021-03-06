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

# TODO: Replace resultsgen with read from file generated by previous step
event_prefix = 'event000001000'
hits, cells, particles, truth = load_event(os.path.join('/trackml/input/train_100_events', event_prefix))
shuffled = shuffle_hits(truth, 0.05) # 5% probability to reassign a hit

score = score_event(truth, shuffled)
print("Score: ", score)



