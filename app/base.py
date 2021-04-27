from typing import List, Text
from flask import render_template
from flask.views import View


class BaseView(View):
    
    # def __init__(self, app):
    #     self.app = app

    def get_template_name(self) -> str:
        raise NotImplementedError()

    def process_request(self, **kwargs) -> dict:
        raise NotImplementedError()

    def render_template(self, **params: dict) -> Text:

        print('entering BaseView.render_template')

        return render_template(
            self.get_template_name(), 
            **params)

    def dispatch_request(self, **kwargs) -> Text:
        
        print('entering BaseView.dispatch_request')

        if kwargs is not None:
            for key, value in kwargs.items():
                print('{0}: {1}'.format(key, value))

        params = self.process_request(**kwargs)

        if params is not None:
            for key, value in params.items():
                print('{0}: {1}'.format(key, value))

        return self.render_template(
            **params)
