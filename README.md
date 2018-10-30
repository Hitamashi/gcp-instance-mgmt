# GCP instance schedule


[![Build Status](https://travis-ci.org/Hitamashi/gcp-instance-schedule.svg?branch=master)](https://travis-ci.org/Hitamashi/gcp-instance-schedule)

## General
Small project to schedule on/off for my gcp instance using cloud function + GAE cron job  
While using cloud functions, GAE do not requires IAM config.

## Deployment
1. Install dependencies
```
pip install -r requirements.txt -t lib
```

2. Setup environment variables
```
# Cloudfunction endpoint format https://[region]-[projectid].cloudfunctions.net/
export GCP_CLOUDFUNCTION_URL=<Endpoint to cloudfunctions>
export  GCP_DEFAULT_ZONE=<default zone>
export  GCP_INSTANCE_NAME=<the instance name>
```

3. Run deployment script  
You need to setup [Cloud SDK](https://cloud.google.com/sdk/install) and [App Engine SDK for Python](https://cloud.google.com/appengine/docs/standard/python/download).  

**Local deployment**
```
# Deploy app on local port 8080
deploy.sh local 8080
```

**GAE deployment**
```
# Deploy app in GAE project abcxyz-123
deploy.sh remote abcxyz-123
```

## References
- [Google App Engine](https://cloud.google.com/appengine/)
- [GAE local server](https://cloud.google.com/appengine/docs/standard/python/tools/using-local-server)