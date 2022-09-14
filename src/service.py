from typing import Any, Callable, Union

from flask import Flask, request, Response, make_response


class RequestParser:
    def __init__(self) -> None:
        pass

    def parse_get_args(self) -> dict:
        params = {}
        if request.method == 'GET':
            params = {**request.args}
        return params

    def parse_post_urlencoded(self) -> dict:
        params = {}
        if request.method == 'POST' and request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
            params = {**request.form}
        return params

    def parse_post_json(self) -> dict:
        params = {}
        if request.method == 'POST' and request.headers['Content-Type'] == 'application/json':
            params = {**request.json}
        return params


class ReturnParser:
    def __init__(self) -> None:
        self.map = dict()
        self.map['plain'] = self.plain
        self.map['json'] = self.json

    def to(self, ret: Any, response_type: str) -> Response:
        return self.map[response_type](ret)

    def plain(self, ret: str) -> Response:
        return make_response(ret)

    def json(self, ret: Union[dict, str]) -> Response:
        response = make_response(ret)
        response.headers['Content-Type'] = 'application/json'
        return response


class Service:
    def __init__(self, app: Flask) -> None:
        self.flask_app = app
        self.requestParser = RequestParser()
        self.resultParser = ReturnParser()

    def run(self, port: int):
        self.flask_app.run(port = port)

    def add_rule(self, rule: str, func: Callable, response_type: str):
        view_func = self._process_request(func, response_type)
        self.flask_app.add_url_rule('/' + rule, endpoint=rule, view_func=view_func, methods=['GET', 'POST'])

    def add_rules(self, rules: dict):
        for rule in rules:
            self.add_rule(rule, rules[rule]['cmd'], rules[rule]['args'], rules[rule]['pattern'], rules[rule]['response'])

    def _process_request(self, func: Callable, response_type: str):        
        def view_func():
            parsed_params = {
                **self.requestParser.parse_get_args(),
                **self.requestParser.parse_post_urlencoded(),
                **self.requestParser.parse_post_json()
            }
            ret = func(**parsed_params)
            res = self.resultParser.to(ret, response_type)
            return res
        return view_func

