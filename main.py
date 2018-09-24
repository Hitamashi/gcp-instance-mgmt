# [START app]
import logging

from flask import Flask, render_template

# [START imports]
import requests
import requests_toolbelt.adapters.appengine
import json
from urllib3.exceptions import HTTPError

# Use the App Engine Requests adapter. This makes sure that Requests uses
# URLFetch.
requests_toolbelt.adapters.appengine.monkeypatch()
# [END imports]

app = Flask(__name__)


@app.route('/')
def index():
    # [START requests_start]
    url = 'https://asia-northeast1-composite-drive-196403.cloudfunctions.net/getInstance'
    try:
        response = requests.get(url)
        response.raise_for_status()
        instance = json.loads(response.text)
        instance["staticIP"] = instance["networkInterfaces"][0]["accessConfigs"][0]["natIP"]
        return render_template("index.html", ins=instance)
    except ValueError:
        return "Cannot get ts info"
    except HTTPError:
        return "Request error"

    # [END requests_start]


@app.route('/startTS')
def startTS():
    # [START requests_get]
    url = 'https://asia-northeast1-composite-drive-196403.cloudfunctions.net/startTS'
    response = requests.get(url)
    response.raise_for_status()
    return response.text
    # [END requests_get]


@app.route('/stopTS')
def stopTS():
    # [END requests_stop]
    url = 'https://asia-northeast1-composite-drive-196403.cloudfunctions.net/stopTS'
    response = requests.get(url)
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
