import requests
import json
from base64 import b64encode
import os
import logging


def bearer_auth(api_client_id, api_client_secret):
    data = """grant_type=client_credentials&client_id={}&client_secret={}&resource=http://GE-SemanticHub-Explorer""".format(api_client_id, api_client_secret)

    # Create a new Service charge transaction by calling API
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    response = requests.post('https://login.microsoftonline.com/db3d428f-0f97-449a-b683-4df57b0a73c8/oauth2/token', data=data, headers=headers)

    json_response = json.loads(response.content)

    if 'access_token' in json_response.keys():
        return "Bearer {}".format(json_response['access_token'])
    else:
        return None


def basic_auth(user, token):
    b64 = b64encode("{}:{}".format(user, token).encode("ascii"))
    return 'Basic {}'.format(b64.decode("ascii"))


def http_get_json(url, auth, session=None):
    """
    A wrapper around the requests get function which will call SH and load the json response.
    """
    if type(url) is dict:
        logging.info("QueueTriggerPattern request called to get url but url is already dict. Assuming loaded json so returning input.")
        return url
    if url[:5] == "http:":
        url = "https:" + url[5:]

    headers = {
        'Content-type': 'application/json',
        'Authorization': auth,
    }

    if session is None:
        session = requests.Session()

    response = session.get(url, headers=headers, verify=False)
    return json.loads(response.text), session


def http_post(url, auth, data=None, file=None, session=None):

    # Create a new Service charge transaction by calling API
    headers = {
        'authorization': auth,
        'X-Atlassian-Token': 'nocheck',
    }

    media_types = {'png': 'image/png'}

    if session is None:
        session = requests.Session()

    if file is not None:
        with open(file, 'rb') as fp:
            basename = os.path.basename(file)
            files = {'file': (basename, fp, media_types[basename.split('.')[-1]])}
            response = session.post(url, files=files, headers=headers, verify=False)
    else:
        headers['Content-type'] = 'application/json'
        response = session.post(url, data=data, headers=headers, verify=False)

    if response.status_code not in (200, 201):
        raise Exception("POST {} Error: ({}) {} \nHeaders: {}".format(url, response.status_code, response.content, response.headers))

    return response


def http_put(url, auth, data=None, file=None, session=None):

    # Create a new Service charge transaction by calling API
    headers = {
        'authorization': auth,
        'X-Atlassian-Token': 'nocheck',
    }

    media_types = {'png': 'image/png'}

    if session is None:
        session = requests.Session()

    if file is not None:
        with open(file, 'rb') as fp:
            basename = os.path.basename(file)
            files = {'file': (basename, fp, media_types[basename.split('.')[-1]])}
            response = session.put(url, files=files, headers=headers, verify=False)
    else:
        headers['Content-type'] = 'application/json'
        response = session.put(url, data=data, headers=headers, verify=False)

    if response.status_code not in (200, 201):
        raise Exception("PUT {} Error: ({}) {} \nHeaders: {}".format(url, response.status_code, response.content, response.headers))

    return response
