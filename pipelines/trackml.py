#!/usr/bin/env python3

import kfp.dsl as dsl
import kfp.gcp as gcp

# Pipeline input variables.
KUBECTL_IMAGE = "gcr.io/mcas-195423/trackml_master_kfp_kubectl"
KUBECTL_IMAGE_VERSION = "1"
TRACKML_TRAIN_IMAGE = "gcr.io/mcas-195423/trackml_master_trackml"
TRACKML_TRAIN_VERSION = "1"
TRACKML_RESULTSGEN_IMAGE = "gcr.io/mcas-195423/trackml_master_trackml"
TRACKML_RESULTSGEN_VERSION = "1"
TRACKML_SCORE_IMAGE = "gcr.io/mcas-195423/trackml_master_trackml"
TRACKML_SCORE_VERSION = "1"

def train_op():
  return dsl.ContainerOp(
    name='train',
    image="{}:{}".format(TRACKML_TRAIN_IMAGE, TRACKML_TRAIN_VERSION),
    command=["python"],
    arguments=["train.py"],
  ).apply(gcp.use_gcp_secret())

def serve_op():
  return dsl.ContainerOp(
    name='serve',
    image="{}:{}".format(KUBECTL_IMAGE, KUBECTL_IMAGE_VERSION),
    arguments=[
      "/src/set_kubectl.sh",
      "--namespace", "kubeflow",
      "--command", "apply -f /src/k8s/serve.yaml",
    ]
  ).apply(gcp.use_gcp_secret())

def resultsgen_op():
  return dsl.ContainerOp(
    name='resultsgen',
    image="{}:{}".format(TRACKML_RESULTSGEN_IMAGE, TRACKML_RESULTSGEN_VERSION),
    command=["python"],
    arguments=["resultsgen.py"],
  ).apply(gcp.use_gcp_secret())

def score_op():
  return dsl.ContainerOp(
    name='score',
    image="{}:{}".format(TRACKML_RESULTSGEN_IMAGE, TRACKML_RESULTSGEN_VERSION),
    command=["python"],
    arguments=["score.py"],
  ).apply(gcp.use_gcp_secret())

@dsl.pipeline(
  name='trackml',
  description='A pipeline that predicts particle tracks'
)
def trackml():
  train = train_op()

#  serve = serve_op()
#  serve.after(train)

  resultsgen = resultsgen_op()
#  resultsgen.after(serve)
  resultsgen.after(train)

  score = score_op()
  score.after(resultsgen)

if __name__ == '__main__':
  import kfp.compiler as compiler
  compiler.Compiler().compile(trackml, __file__ + '.tar.gz')

