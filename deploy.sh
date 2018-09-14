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

gcloud app deploy -q app.yaml cron.yaml