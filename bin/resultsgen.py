#!/usr/bin/env python3

import os
import pandas as pd
import subprocess

from trackml.dataset import load_event
from trackml.randomize import shuffle_hits
from trackml.score import score_event

# Retrieve data
command = ['./ingest_data.sh']
result = subprocess.call(command)
print(command, " result: ", result)

event_prefix = 'event000001000'
hits, cells, particles, truth = load_event(os.path.join('/trackml/input/train_100_events', event_prefix))

## TODO: Receive prediction from served model

shuffled = shuffle_hits(truth, 0.05) # 5% probability to reassign a hit

print(shuffled.head(10))

outdir = "/trackml/output"
if not os.path.exists(outdir):
    os.mkdir(outdir)
fullpath = os.path.join(outdir, "shuffled.csv")
shuffled.to_csv(fullpath)

# Save file to GCS
command = ['./write_results.sh']
result = subprocess.call(command)
print(command, " result: ", result)

