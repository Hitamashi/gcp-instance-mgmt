# GCP instance schedule

## General
Small project to schedule on/off for my gcp instance using cloud function + GAE cron job  
While using cloud functions, GAE do not requires IAM config.

## Deployment
First, install the dependencies
```
pip install -r requirements.txt -t lib
```

Then ro deploy, run:
```
./deploy.sh <project-id>
```

## TODO
- Cloud function: zone + instance name as param

