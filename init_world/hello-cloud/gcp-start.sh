#!/bin/bash
echo "running the $0 script"
if [[ -d /usr/local/Caskroom/google-cloud-sdk ]]; then
  gcloud init --console-only
  gcloud config set compute/zone us-west1-b
  export PROJECT_ID=$(gcloud info --format='value(config.project)')
else
  echo "Google Cloud SDK is not installed!"
  #statements
fi
#each service account, get all the keys
for project in  $(gcloud projects list --format="value(projectId)")
do
  echo "ProjectId:  $project"
  for robot in $(gcloud iam service-accounts list --project $project --format="value(email)")
   do
     echo "    -> Robot $robot"
     for key in $(gcloud iam service-accounts keys list --iam-account $robot --project $project --format="value(name.basename())")
        do
          echo "        $key"
     done
   done
done

read -r "do you want to create a site?" webBuild
if [[ webBuild = yes]]; then
  ./hello-gcp/install-web.sh
fi
