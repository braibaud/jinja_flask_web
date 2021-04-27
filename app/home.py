from flask import request
from app.base import BaseView

class Home(BaseView):

    def get_template_name(self) -> str:
        return 'home.j2'

    def process_request(self, **kwargs) -> dict:

        print('entering Home.process_request')

        if kwargs is not None:
            for key, value in kwargs.items():
                print('{0}: {1}'.format(key, value))

        return {
            'users': [
                {
                    'firstname': 'benjamin',
                    'lastname': 'raibaud',
                    'age': 45
                }
            ]
        }
