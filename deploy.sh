# Deploy Cloud function
# Accept params:
#   - $1 Cloud function name
#   - $2 function name in file
#   - $3 region name
#   - $4 memory
deployCF() {
	echo "Deploy Cloud Function $1 in $3 region"
	gcloud functions deploy $1 \
  	--source https://source.developers.google.com/projects/${PROJECTID}/repos/gce-compute/moveable-aliases/master/paths/cloudfunction \
  	--trigger-http --entry-point=$2 --region=$3	--memory=$4
}

configGenerate() {
	cp app.yaml app-deploy.yaml
	echo "env_variables:" >> app-deploy.yaml
	echo "  GCP_CLOUDFUNCTION_URL: \"$GCP_CLOUDFUNCTION_URL\"" >> app-deploy.yaml
	echo "  GCP_DEFAULT_ZONE: \"$GCP_DEFAULT_ZONE\"" >> app-deploy.yaml
	echo "  GCP_INSTANCE_NAME: \"$GCP_INSTANCE_NAME\"" >> app-deploy.yaml
}

remote() {
	PROJECTID=`gcloud projects list | grep -iw "$1" | awk '{print $1}'`

	if [ -z "$PROJECTID" ]; then
	 echo Project $1 Not Found!
	 exit
	fi

	echo "Project ID $PROJECTID"
	gcloud config set project $PROJECTID

	echo "Deploy Cloud function"

	deployCF getInstance getInstance asia-northeast1 128MB
	deployCF startInstance startInstance asia-northeast1 128MB
	deployCF stopInstance stopInstance asia-northeast1 128MB

	echo "Deploy App engine & Cron job"
	configGenerate
	gcloud app deploy -q app-deploy.yaml cron.yaml
}

local() {
	echo "Run app on local machine, port $1"
	configGenerate
	dev_appserver.py app-deploy.yaml --port=$1
}

usage() {
    echo "Usage: deploy.sh local [PORT]"
  	echo "  or:  deploy.sh remote [PROJECT_ID]"
  	echo ""
    echo "-----------Parameter-------------"
    echo "local : Deploy app in local env"
    echo "remote: Deploy app in GAE (need project id)"
}

case "$1" in
    local)
		if [[ $# -eq 2 ]] ; then
			local $2
		else
			local 8080
		fi
		;;
    remote)
		if [[ $# -eq 2 ]] ; then
			remote $2
		else
			echo "Missing project id"
			exit 1
		fi
		;;
    *) usage ;;
esac
