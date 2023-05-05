# [START app]
import logging

from flask import Flask, render_template, request

# [START imports]
import requests
import json
import os
from urllib3.exceptions import HTTPError
from google.cloud import compute_v1
# [END imports]

app = Flask(__name__)

@app.route('/')
def list():
    # [START requests_start]
    try:
        instance_client = compute_v1.InstancesClient()
        request = compute_v1.AggregatedListInstancesRequest()
        request.project = os.getenv('GOOGLE_CLOUD_PROJECT')
        request.max_results = 10

        agg_list = instance_client.aggregated_list(request=request)
        all_instances = []

        for zone, response in agg_list:
            if response.instances:
                app.logger.debug(f" {zone}:")
                for instance in response.instances:
                    app.logger.debug(f" - {instance.name} ({instance.machine_type})")
                    i = {
                        "zone": zone.split('/')[-1],
                        "name": instance.name,
                        "status": instance.status
                    }
                    try:
                        i['IP'] = instance.network_interfaces[0].access_configs[0].nat_i_p
                    except Exception as ex:
                        i['IP'] = '-'
                    try:
                        i['function'] = instance.labels['function']
                    except Exception as ex:
                        i['function'] = '-'
                    all_instances.append(i)
        return render_template("index.html", instances=all_instances)
    except ValueError:
        return "Cannot get servers info"
    except HTTPError as ex:
        logging.exception(ex)
        return "Request error", 500

    # [END requests_start]

@app.route('/startTS')
def startTS():
    # [START requests_get]
    instance_client = compute_v1.InstancesClient()
    ops = instance_client.start(
        project = os.getenv('GOOGLE_CLOUD_PROJECT'),
        zone = request.args.get('zone'),
        instance = request.args.get('vm')
    )
    res = ops.result(timeout=60)
    if ops.error_code:
        app.logger.debug(f"Error during START VM: [Code: {ops.error_code}]: {ops.error_message}")
        return "Error occored!", 500
    return "", 200
    # [END requests_get]


@app.route('/stopTS')
def stopTS():
    # [START requests_stop]
    instance_client = compute_v1.InstancesClient()
    ops = instance_client.stop(
        project = os.getenv('GOOGLE_CLOUD_PROJECT'),
        zone = request.args.get('zone'),
        instance = request.args.get('vm')
    )
    res = ops.result(timeout=60)
    if ops.error_code:
        app.logger.debug(f"Error during STOP VM: [Code: {ops.error_code}]: {ops.error_message}")
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
