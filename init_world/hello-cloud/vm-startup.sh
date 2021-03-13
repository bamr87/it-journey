#! /bin/bash
# startup from local script
gcloud compute instances create vm-startup-local-1 \
    --metadata-from-file startup-script=install-web.sh
# start up from bucket

gsutil mb gs://vm-startup-2
gsutil cp install-web.sh gs://vm-startup-2
gsutil cp vm.yaml gs://vm-startup-2

gcloud compute instances create vm-startup-bucket-2 \
    --scopes storage-ro \
    --metadata startup-script-url=gs://vm-startup-2/install-web.sh \
    --tags=http-server


gcloud deployment-manager deployments create quickstart-deployment --config vm.yaml
