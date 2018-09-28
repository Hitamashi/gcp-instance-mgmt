if [[ $# -eq 0 ]] ; then
 echo Missing project id argument
 exit
fi

PROJECTID=`gcloud projects list | grep -iw "$1" | awk '{print $1}'`

if [ -z "$PROJECTID" ]; then
 echo Project $1 Not Found!
 exit
fi

echo Project ID $PROJECTID
gcloud config set project $PROJECTID

echo Deploy Cloud function
gcloud functions deploy getInstance \
  --source https://source.developers.google.com/projects/${PROJECT_ID}/repos/gce-compute/moveable-aliases/master/paths/cloudfunction \
  --trigger-http --entry-point=getInstance --region=asia-northeast1	

gcloud functions deploy startInstance \
  --source https://source.developers.google.com/projects/${PROJECT_ID}/repos/gce-compute/moveable-aliases/master/paths/cloudfunction \
  --trigger-http --entry-point=startInstance --region=asia-northeast1	

gcloud functions deploy stopInstance \
  --source https://source.developers.google.com/projects/${PROJECT_ID}/repos/gce-compute/moveable-aliases/master/paths/cloudfunction \
  --trigger-http --entry-point=stopInstance --region=asia-northeast1	

echo Deploy App engine & Cron job
gcloud app deploy -q app.yaml cron.yaml

