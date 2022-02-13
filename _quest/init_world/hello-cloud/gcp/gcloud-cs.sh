#!/bin/bash
#gcloud cheat sheet
gsutil cp gs://spls/gsp302/*

gcloud deployment-manager deployments create my-first-deployment \
    --config vm.yaml
