#!/bin/bash

configGenerate() {
	cp app.yaml app-deploy.yaml
	[[ ! -z $GOOGLE_APPLICATION_CREDENTIALS ]] && echo "  GOOGLE_APPLICATION_CREDENTIALS: \"$GOOGLE_APPLICATION_CREDENTIALS\"" >> app-deploy.yaml

	echo "Config generated!"
}

remote() {
	if gcloud projects describe "$PROJECT_ID" 2>&1 > /dev/null; then
		echo "Project ID $PROJECT_ID"
	else
		echo Project $1 Not Found!
		exit 1
	fi

	echo "Deploy App engine & Cron job"
	configGenerate

	_GAE_VERSION=${2:-test}
	_GAE_PROMOTE=${3:---no-promote}

	echo "[ENV] $_GAE_VERSION"
	echo "[CMD] cloud app deploy --project $PROJECT_ID -q app-deploy.yaml cron.yaml $_GAE_PROMOTE -v $_GAE_VERSION"
	gcloud app deploy --project $PROJECT_ID \
		-q app-deploy.yaml cron.yaml \
		$_GAE_PROMOTE \
		-v $_GAE_VERSION
}

local() {
	echo "Run app on local machine, port $1"
	export GOOGLE_APPLICATION_CREDENTIALS=./gcp-secret.json
	configGenerate
	dev_appserver.py app-deploy.yaml --port=$1 --log_level=debug --application=composite-drive-196403
}

usage() {
    echo "Usage: deploy.sh local [PORT]"
  	echo "  or:  deploy.sh remote [PROJECT_ID]"
  	echo ""
    echo "-----------Parameter-------------"
    echo "local : Deploy app in local env"
    echo "remote: Deploy app in GAE (need project id)"
	echo "config: Generate config file app-deploy.yaml"
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
		remote
		;;
	config)
		echo "Generate config file in app-deploy.yaml"
		configGenerate
		;;
    *) usage ;;
esac
