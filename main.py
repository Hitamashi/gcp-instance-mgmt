# [START app]
import logging

from flask import Flask, render_template, request

# [START imports]
import requests
import json
import os
from urllib3.exceptions import HTTPError
from googleapiclient.discovery import build

# [END imports]

app = Flask(__name__)

@app.route('/')
def list():
    # [START requests_start]
    try:
        compute = build('compute', 'v1', cache_discovery=False)
        params = {
            'project': os.getenv('GOOGLE_CLOUD_PROJECT'),
            'fields': 'items/*/instances(id,name,status,labels,networkInterfaces/accessConfigs/natIP)'
        }

        instances = []
        request = compute.instances().aggregatedList(**params) # pylint: disable=E1101
        while request is not None:
            response = request.execute()

            for name, instances_scoped_list in response['items'].items():
                logging.debug("{}\n{}".format(name,instances_scoped_list))
                for i in instances_scoped_list['instances']:
                    i['zone'] = name.split('/')[-1]
                    try:
                        i['IP'] = i['networkInterfaces'][0]['accessConfigs'][0]['natIP']
                    except Exception as ex:
                        i['IP'] = '-'
                    try:
                        i['function'] = i['labels']['function']
                    except Exception as ex:
                        i['function'] = '-'
                instances = instances + instances_scoped_list.get('instances', [])

            request = compute.instances().aggregatedList_next(previous_request=request, previous_response=response)  # pylint: disable=E1101
        return render_template("index.html", instances=instances)
    except ValueError:
        return "Cannot get servers info"
    except HTTPError as ex:
        logging.exception(ex)
        return "Request error", 500

    # [END requests_start]

@app.route('/startTS')
def startTS():
    # [START requests_get]
    compute = build('compute', 'v1', cache_discovery=False)
    params = {
        'project': os.getenv('GOOGLE_CLOUD_PROJECT'),
        'zone': request.args.get('zone'),
        'instance': request.args.get('vm')
    }
    res = compute.instances().start(**params).execute() # pylint: disable=E1101
    if 'error' in res:
        logging.debug(res['error'])
        return "Error occored!", 500
    return "", 200
    # [END requests_get]


@app.route('/stopTS')
def stopTS():
    # [END requests_stop]
    compute = build('compute', 'v1', cache_discovery=False)
    params = {
        'project': os.getenv('GOOGLE_CLOUD_PROJECT'),
        'zone': request.args.get('zone'),
        'instance': request.args.get('vm')
    }
    res = compute.instances().start(**params).execute()
    if 'error' in res:
        logging.debug(res['error'])
        return "Error occored!", 500
    return "", 200
    # [END requests_stop]


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500
# [END app]
