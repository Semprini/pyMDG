#!/usr/bin/python
from mdg.confluence.util import basic_auth
from mdg.confluence.image_update import update_images
from mdg.confluence.content_update import update


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('user', help='confluence username')
    parser.add_argument('token', help='confluence API token')
    parser.add_argument('page', help='confluence page id')
    parser.add_argument('images', help='path to images foler')
    parser.add_argument('doc', help='path to documentation file')
    args = parser.parse_args()

    auth = basic_auth(args.user, args.token)
    update_images(auth, args.page, args.images)
    update(auth, args.page, args.doc)
