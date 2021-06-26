import os
import glob

from mdg.generate.confluence.util import basic_auth, http_post, http_get_json

ORG = "my org"


def update_images(auth, content_id, path):
    attachments, session = http_get_json("https://{}.atlassian.net/wiki/rest/api/content/{}/child/attachment".format(ORG, content_id), auth)

    files = [f for f in glob.glob(path + "/*.png", recursive=False)]

    for file in files:
        basename = os.path.basename(file)
        conf_attachment = None
        for attachment in attachments['results']:
            if attachment['title'] == basename:
                conf_attachment = attachment

        # Is the file already an attachment in confluence
        if conf_attachment is not None:
            # Update if different file size
            if os.path.getsize(file) != conf_attachment['extensions']['fileSize']:
                url = "https://{}.atlassian.net/wiki/rest/api/content/{}/child/attachment/{}/data".format(ORG, content_id, attachment['id'])
                http_post(url, auth, None, file, None)
                print("Uploaded local file {} to confluence".format(file))
            else:
                print("Skipping local file {} as same file size detected in confluence".format(file))
        else:
            # TODO: Upload new attachment
            url = "https://{}.atlassian.net/wiki/rest/api/content/{}/child/attachment/".format(ORG, content_id)
            http_post(url, auth, None, file, None)
            print("Uploaded new local file {} to confluence".format(file))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('user', help='confluence username')
    parser.add_argument('token', help='confluence API token')
    parser.add_argument('page', help='confluence page id')
    parser.add_argument('path', help='path to images foler')
    args = parser.parse_args()

    auth = basic_auth(args.user, args.token)
    update_images(auth, args.page, args.path)
