import flask as fl
import flask_restful as flr
from flask_restful import reqparse as flr_r
import flask_cors as flc
from flask_wtf import csrf as flwc


import argparse as ap
import traceback as tb
import os
import sys
import inspect
import pathlib
import importlib

import const as cst

import api.info as api_info
import app.home as app_home


# Class holding static properties only
class Statics(object):

    # Globals
    g_arguments = None
    g_models = {}
    g_app = None
    g_cors = None
    g_api = None


def add_api_resource(resource_type, **kwargs):

    urls = resource_type.setup_urls()
    endpoint = resource_type.setup_endpoint()

    print(
        'Mapping class "{0}" as endpoint "{1}" to urls {2}'.format(
            resource_type.__name__,
            endpoint,
            urls))

    Statics.g_api.add_resource(
        resource_type, 
        *urls,
        endpoint=endpoint,
        resource_class_kwargs=kwargs)



def configure_api_resources():
    add_api_resource(api_info.Info)
    # add more here...


def configure_app_templates():
    Statics.g_app.add_url_rule(
        '/home', 
        view_func=app_home.Home.as_view(app_home.Home.__name__))



def configure_app():

    Statics.g_app = fl.Flask('apps', static_url_path='')
    Statics.g_app.config['BUNDLE_ERRORS'] = True

    Statics.g_csrf = flwc.CSRFProtect()
    Statics.g_csrf.init_app(Statics.g_app)

    Statics.g_cors = flc.CORS(
        Statics.g_app, 
        resources={
            r'/*': {
                'origins': '*', 
                'send_wildcard': 'False'
            }
        })

    Statics.g_api = flr.Api(
        app=Statics.g_app,
        catch_all_404s=True)

    configure_api_resources()
    configure_app_templates()

    @Statics.g_app.route('/static/<path:path>')
    def send_static(path):
        return fl.send_from_directory('static', path)


if __name__ == '__main__':

    print('Parsing arguments...')

    parser = ap.ArgumentParser(
        description='Start web-service')

    parser.add_argument(
        '--host',
        default=cst.__default_ip,
        type=str,
        help='The address the web-server is listening on.')

    parser.add_argument(
        '--port',
        default=cst.__default_port,
        type=int,
        help='The port the web-server is listening on')

    Statics.g_arguments = parser.parse_args()

    configure_app()

    Statics.g_app.run(
        host=Statics.g_arguments.host,
        port=Statics.g_arguments.port,
        debug=True)
