#!/bin/bash -e
# set_kubectl.sh - Script for executing a kubectl command from within a Kubeflow
#   pipeline. This has been tested on GKE clusters.

set -x

KUBERNETES_NAMESPACE="${KUBERNETES_NAMESPACE:-default}"
COMMAND="get po"

while (($#)); do
   case $1 in
     "--cluster-name")
       shift
       CLUSTER_NAME="$1"
       shift
       ;;
     "--command")
       shift
       COMMAND="$1"
       shift
       ;;
     "--namespace")
       shift
       KUBERNETES_NAMESPACE="$1"
       shift
       ;;
     *)
       echo "Unknown argument: '$1'"
       exit 1
       ;;
   esac
done


if [ -z "${CLUSTER_NAME}" ]; then
  CLUSTER_NAME=$(wget -q -O- --header="Metadata-Flavor: Google" http://metadata.google.internal/computeMetadata/v1/instance/attributes/cluster-name)
fi

# Ensure the name is not more than 63 characters.
NAME="${NAME:0:63}"
# Trim any trailing hyphens from the server name.
while [[ "${NAME:(-1)}" == "-" ]]; do NAME="${NAME::-1}"; done

echo "Setting kubectl config for the cluster ${CLUSTER_NAME}"

# Connect kubectl to the local cluster
kubectl config set-cluster "${CLUSTER_NAME}" --server=https://kubernetes.default --certificate-authority=/var/run/secrets/kubernetes.io/serviceaccount/ca.crt
kubectl config set-credentials pipeline --token "$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)"
kubectl config set-context kubeflow --cluster "${CLUSTER_NAME}" --user pipeline
kubectl config use-context kubeflow

kubectl -n ${KUBERNETES_NAMESPACE} ${COMMAND}

