#!/bin/bash

OUTDIR=gs://chasm-data/kaggle/trackml-particle-identification/output/
echo "Saving to GCS..."

# Authenticate gsutil
gcloud auth activate-service-account --key-file '/secret/gcp-credentials/user-gcp-sa.json'

gsutil cp /trackml/output/* ${OUTDIR}
echo "Results written to ${OUTDIR}"

