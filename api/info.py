import flask_restful as flr
import const as cst


class Info(flr.Resource):

    def __init__(self, **kwargs):
        super(Info, self).__init__()

    @staticmethod
    def setup_urls():
        return ['/api/info']

    @staticmethod
    def setup_endpoint():
        return 'info'

    def get(self):
        return {
            'success': True,
            'version': cst.__version,
            'status': 'ready'
        }