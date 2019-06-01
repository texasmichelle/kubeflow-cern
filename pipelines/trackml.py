#!/usr/bin/env python3

import kfp.dsl as dsl
import kfp.gcp as gcp

# Pipeline input variables.
KUBECTL_IMAGE = "gcr.io/mcas-195423/trackml_master_kfp_kubectl"
KUBECTL_IMAGE_VERSION = "1"
TRACKML_IMAGE = "gcr.io/mcas-195423/trackml_master_trackml"
TRACKML_IMAGE_VERSION = "1"

def train_op():
  return dsl.ContainerOp(
    name='train',
    image="{}:{}".format(TRACKML_IMAGE, TRACKML_IMAGE_VERSION),
    command=["python"],
    arguments=["train.py"],
  ).apply(gcp.use_gcp_secret()
  )#.set_gpu_limit(1)

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
    image="{}:{}".format(TRACKML_IMAGE, TRACKML_IMAGE_VERSION),
    command=["python"],
    arguments=["resultsgen.py"],
  ).apply(gcp.use_gcp_secret())

@dsl.pipeline(
  name='trackml',
  description='A pipeline that predicts particle tracks'
)
def trackml():
  train = train_op()

  serve = serve_op()
  serve.after(train)

  resultsgen = resultsgen_op()
  resultsgen.after(serve)

if __name__ == '__main__':
  import kfp.compiler as compiler
  compiler.Compiler().compile(trackml, __file__ + '.tar.gz')

