import flask as fl
import flask_restful as flr
from flask_restful import reqparse as flr_r
import flask_cors as flc
from flask_wtf import csrf as flwc


class Info(flr.Resource):

    def __init__(self):
        super(Info, self).__init__()

    def get(self):
        return {
            'success': True,
            'version': '1.0',
            'status': 'ready'
        }
