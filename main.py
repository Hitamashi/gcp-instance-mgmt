# [START app]
import logging

from flask import Flask, render_template

# [START imports]
import requests
import json
import os
from urllib3.exceptions import HTTPError
from googleapiclient.discovery import build

# [END imports]

app = Flask(__name__)

zone = os.getenv('GCP_DEFAULT_ZONE')
vm = os.getenv('GCP_INSTANCE_NAME')
url_endpoint = os.getenv('GCP_CLOUDFUNCTION_URL')


@app.route('/')
def index():
    # [START requests_start]
    url = url_endpoint + '/getInstance'
    try:
        response = requests.get(url, params={'zone': zone, 'vm': vm})
        response.raise_for_status()
        instance = json.loads(response.text)
        instance["staticIP"] = instance["networkInterfaces"][0]["accessConfigs"][0]["natIP"]
        return render_template("index.html", ins=instance)
    except ValueError:
        return "Cannot get ts info"
    except HTTPError as ex:
        logging.exception(ex)
        return "Request error", 500

    # [END requests_start]


@app.route('/list')
def list():
    # [START requests_start]
    try:
        compute = build('compute', 'v1', cache_discovery=False)
        params = {
            'project' : os.getenv('GOOGLE_CLOUD_PROJECT'),
            'zone' : zone,
            'instance' : vm,
            'fields' : 'id,name,status,networkInterfaces(accessConfigs/natIP)'
        }
        instance = compute.instances().get(**params).execute() # pylint: disable=E1101

        # Can query list with  compute.instances().list(project=..., zone=..., fields=...)cc
        #     project =  os.getenv('GOOGLE_CLOUD_PROJECT'),
        #     zone = zone,
        #     fields = 'items(id,name,status,networkInterfaces/accessConfigs/natIP,zone)'
        #
        logging.info(instance)
        instance['staticIP'] = instance["networkInterfaces"][0]["accessConfigs"][0]["natIP"]
        return render_template("index.html", ins=instance)
    except ValueError:
        return "Cannot get ts info"
    except HTTPError as ex:
        logging.exception(ex)
        return "Request error", 500

    # [END requests_start]

@app.route('/startTS')
def startTS():
    # [START requests_get]
    url = url_endpoint + '/startInstance'
    response = requests.get(url, params={'zone': zone, 'vm': vm})
    response.raise_for_status()
    return response.text
    # [END requests_get]


@app.route('/stopTS')
def stopTS():
    # [END requests_stop]
    url = url_endpoint + '/stopInstance'
    response = requests.get(url, params={'zone': zone, 'vm': vm})
    response.raise_for_status()
    return response.text
    # [END requests_stop]


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500
# [END app]
