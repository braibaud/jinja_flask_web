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


__app_version = '0.1.0'
__app_template_directory = 'app'
__app_template_ext = 'j2x'


# Class holding static properties only
class Statics(object):

    # Globals
    g_arguments = None
    g_models = {}
    g_app = None
    g_cors = None
    g_api = None


# Mapping HTTP requests to class functions
class Info(flr.Resource):

    def __init__(self):
        super(Info, self).__init__()

    def get(self):
        return {
            'success': True,
            'version': __app_version,
            'status': 'ready'
        }


def configure_api():

    Statics.g_app = fl.Flask('apps')
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

    Statics.g_api.add_resource(
        Info, 
        '/info',
        endpoint='info')

    configure_templates(
        directory=__app_template_directory, 
        extension=__app_template_ext)

    # for _, model in Statics.g_models.items():

    #     url = '/api/{0}'.format(model['id'])
    #     endpoint = '{0}'.format(model['id'])

    #     Statics.g_api.add_resource(
    #         Hosting, 
    #         url,
    #         endpoint=endpoint,
    #         resource_class_kwargs={'model_id': model['id']})

    #     print('Serving model "{0}" from "{1}"'.format(
    #         model['id'],
    #         url))


def configure_templates(directory, extension):

    for dirpath, dirnames, files in os.walk(directory):
            for name in files:
                if extension and name.lower().endswith(extension):

                    template_view = pathlib.PureWindowsPath(os.path.join(dirpath, name)).as_posix()

                    print('Template view found "{0}".'.format(template_view))

                    template_name = template_view[:-1*len(extension)-1]
                    print('  -> Associated template name is "{0}".'.format(template_name))

                    template_controller = '{0}.{1}'.format(template_name, 'py')

                    print('  -> Looking for template controller "{0}"...'.format(template_controller))

                    if os.path.exists(template_controller):
                        print('  -> The template controller exist.')

                        template_controller_pathname, template_controller_filename = os.path.split(template_controller)

                        load_template_controller_module(
                            config={
                                'name': template_name, 
                                'view': template_view,
                                'controller': template_controller,
                                'controller_pathname': template_controller_pathname,
                                'controller_filename': template_controller_filename,
                                'controller_modulename': os.path.splitext(template_controller_filename)[0],
                                'controller_module': None,
                                'controller_classes': [],
                            })

                    else:
                        print('  -> The template controller does not exist.')


def load_template_controller_module(config):
    
    try:
        print('  -> Loading template controller module...')
        
        sys.path.append(os.path.abspath(config['controller_pathname']))
        config['controller_module'] = importlib.import_module(config['controller_modulename'])

        print('  -> Template controller module loaded')

        for class_name, class_instance in inspect.getmembers(config['controller_module'], inspect.isclass):
            print(class_name)
            config['controller_classes'].append(class_name)

        # getattr(template_module, 'configure_controller')()
    
    except Exception as e:
        print('  -> Error loading template controller')
        print(e)
    

def load_template_controller_module_class(template_module, template_name, template_view):
    
    try:
        print('  -> Loading template controller module...')
        template_module = __import__(template_name)
        print('  -> Template controller module loaded')

        getattr(template_module, 'configure_controller')()
    
    except Exception as e:
        print('  -> Error loading template controller')
        print(e)
    



if __name__ == '__main__':

    print('Parsing arguments...')

    parser = ap.ArgumentParser(
        description='Start web-service')

    parser.add_argument(
        '--host',
        default='0.0.0.0',
        type=str,
        help='The address the web-service is listening on.')

    parser.add_argument(
        '--port',
        default=5000,
        type=int,
        help='The port the web-service is listening on')

    Statics.g_arguments = parser.parse_args()

    configure_api()

    Statics.g_app.run(
        host=Statics.g_arguments.host,
        port=Statics.g_arguments.port,
        debug=True)
