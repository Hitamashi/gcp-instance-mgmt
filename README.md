# GCP instance schedule


[![Build Status](https://travis-ci.org/Hitamashi/gcp-instance-schedule.svg?branch=master)](https://travis-ci.org/Hitamashi/gcp-instance-schedule)

## General
Small project to schedule on/off for my gcp instance using cloud function + GAE cron job  
While using cloud functions, GAE do not requires IAM config.

## Deployment
First, install the dependencies
```
pip install -r requirements.txt -t lib
```

Setup environment variables:
```
# Cloudfunction endpoint format https://[region]-[projectid].cloudfunctions.net/
export GCP_CLOUDFUNCTION_URL=<Endpoint to cloudfunctions>
export  GCP_DEFAULT_ZONE=<default zone>
export  GCP_INSTANCE_NAME=<the instance name>
```

You need to setup [gcloud](https://cloud.google.com/sdk/install).  
Then to deploy, run:
```
./deploy.sh <project-id>
```
