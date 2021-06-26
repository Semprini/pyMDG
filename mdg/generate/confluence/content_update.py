import json

from mdg.generate.confluence.util import basic_auth, http_put, http_get_json


def update(auth, content_id, path):
    url = "https://jiragenesisenergy.atlassian.net/wiki/rest/api/content/{}".format(content_id)
    content, session = http_get_json(url, auth)
    new_version = int(content['version']['number']) + 1

    attachments, session = http_get_json("https://jiragenesisenergy.atlassian.net/wiki/rest/api/content/{}/child/attachment".format(content_id), auth, session)

    with open(path) as f:
        body = f.read()

    data = {
        "id": "{}".format(content_id),
        "type": "page",
        "title": "Models - Retail Test",
        "space": {
            "key":
            "DA"},
        "body": {
            "storage": {
                "value": "{}".format(body),
                "representation": "storage"}},
        "version": {
            "number": new_version
        }
    }
    http_put(url, auth, json.dumps(data), None)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('user', help='confluence username')
    parser.add_argument('token', help='confluence API token')
    parser.add_argument('page', help='confluence page id')
    parser.add_argument('path', help='path to documentation content')
    args = parser.parse_args()

    auth = basic_auth(args.user, args.token)
    update(auth, args.page, args.path)
