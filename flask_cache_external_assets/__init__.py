# -*- coding: utf-8 -*-

__version__ = '0.1.0'


def cache_external_assets(image_path):
    print('*' * 80)
    print(image_path)
    return image_path


class CacheExternalAssets(object):
    """ Adds a jinja filter for caching external assets. """
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.jinja_env.filters['cache_external_assets'] = cache_external_assets

    def teardown(self, exception):
        pass
