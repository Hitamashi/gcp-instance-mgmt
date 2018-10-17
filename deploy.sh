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
  --source https://source.developers.google.com/projects/${PROJECTID}/repos/gce-compute/moveable-aliases/master/paths/cloudfunction \
  --trigger-http --entry-point=getInstance --region=asia-northeast1	--memory=128MB

gcloud functions deploy startInstance \
  --source https://source.developers.google.com/projects/${PROJECTID}/repos/gce-compute/moveable-aliases/master/paths/cloudfunction \
  --trigger-http --entry-point=startInstance --region=asia-northeast1 --memory=128MB

gcloud functions deploy stopInstance \
  --source https://source.developers.google.com/projects/${PROJECTID}/repos/gce-compute/moveable-aliases/master/paths/cloudfunction \
  --trigger-http --entry-point=stopInstance --region=asia-northeast1 --memory=128MB

echo "Deploy App engine & Cron job"
cp app.yaml app-deploy.yaml
echo "env_variables:" >> app-deploy.yaml
echo "  GCP_CLOUDFUNCTION_URL: \"$GCP_CLOUDFUNCTION_URL\"" >> app-deploy.yaml
echo "  GCP_DEFAULT_ZONE: \"$GCP_DEFAULT_ZONE\"" >> app-deploy.yaml
echo "  GCP_INSTANCE_NAME: \"$GCP_INSTANCE_NAME\"" >> app-deploy.yaml
gcloud app deploy -q app-deploy.yaml cron.yaml
