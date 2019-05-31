#!/bin/bash

echo "Copying data from GCS..."

mkdir -p /trackml/input/train_100_events
gsutil cp gs://chasm-data/kaggle/trackml-particle-identification/train_100_events/* /trackml/input/train_100_events/

