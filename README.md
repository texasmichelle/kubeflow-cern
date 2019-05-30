# TrackML at CERN

1. Create a cluster and install Kubeflow
1. Run a notebook
1. Run a pipeline

## Create a cluster and install Kubeflow

Create a cluster with [Click-to-deploy](https://deploy.kubeflow.cloud) using 
default settings. Follow the provided instructions to setup OAuth credentials.

After the cluster is available and you are able to access the Kubeflow central
dashboard, enable auto-provisioning with the following command:

```
gcloud beta container clusters update kubeflow \
  --enable-autoprovisioning \
  --max-cpu 128 \
  --max-memory 1120 \
  --max-accelerator type=nvidia-tesla-k80,count=4 \
  --verbosity error
```

## Run a notebook

From the Kubeflow central dashboard, click on Notebooks and spawn a new
instance. Use all defaults except for the following parameters:

CPU: 2
Memory: 12.0Gi

When the notebook instance is ready, click Connect and open a new Terminal. Run
this command to import necessary libraries:

```
git clone https://github.com/LAL/trackml-library.git src/trackml-library
pip install src/trackml-library
pip install pandas
pip install matplotlib
pip install seaborn
```

Download sample data with this command:

```
mkdir input
gsutil cp gs://chasm-data/kaggle/trackml-particle-identification/train_sample.zip input
cd input
unzip train_sample.zip
```

Upload the file
`notebooks/trackml-problem-explanation-and-data-exploration.ipynb`, which was
adapted from
[Wesam Elshamy's](https://www.kaggle.com/wesamelshamy)
[Kaggle Kernel](https://www.kaggle.com/kernels/scriptcontent/3966101/notebook)
for use on Kubeflow v0.5.0, and open the notebook.




## Run a pipeline

### Build docker images

Each step in a pipeline references a container image. Build the necessary docker
image with this command:

```
docker/build.sh kfp_kubectl
```

### Compile the pipeline

In a local Terminal of Cloud Shell, install the Kubeflow pipelines python SDK by
running this command:

```
pip install -U kfp
```

Compile a pipeline by running it directly:

```
pipelines/trackml.py
```

### Upload and run the pipeline

From the Kubeflow central dashboard, click on Pipeline Dashboard, then Upload
pipeline. Select the file you just created (trackml.py.tar.gz) and then Upload.

Run the pipeline by first creating an experiment, then a run.
