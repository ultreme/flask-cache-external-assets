# -*- coding: utf-8 -*-

import os
import hashlib

import requests
from flask import current_app

__version__ = '0.1.0'


def cache_path(url, cache_dir, extension=None):

    filename_hash = hashlib.new('md5')
    filename_hash.update(url)

    if not extension:
        extension = ''

    filename = '{}/{}{}'.format(cache_dir,
                                filename_hash.hexdigest(),
                                extension)
    return filename


def cache_external_assets(url):
    # if not external, return direct file
    if not url.startswith('http'):
        return url

    root = current_app.config['CACHE_EXTERNAL_ASSETS_ROOT']
    cache_dir = current_app.config['CACHE_EXTERNAL_ASSETS_DIR']

    path = cache_path(url, cache_dir)
    filepath = os.path.join(root, path)

    if os.path.exists(filepath):
        return path

    try:
        os.makedirs(os.path.dirname(filepath))
    except:  # FIXME: handle exceptions
        pass

    with open(filepath, 'wb') as handle:
        response = requests.get(url, stream=True)

        if not response.ok:
            # Something went wrong
            raise RuntimeError('Cannot request image')

        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)

    return path


class CacheExternalAssets(object):
    """ Adds a jinja filter for caching external assets. """
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if 'CACHE_EXTERNAL_ASSETS_ROOT' not in app.config:
            raise RuntimeError('You must specify CACHE_EXTERNAL_ASSETS_ROOT')
        app.config.setdefault('CACHE_EXTERNAL_ASSETS_DIR', 'external')
        app.jinja_env.filters['cache_external_assets'] = cache_external_assets

    def teardown(self, exception):
        pass
