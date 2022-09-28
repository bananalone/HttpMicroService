from typing import Any, Callable
import json
from string import Template

from flask import Flask, request, Response, make_response

from functionfactory.item import Item


class Service:
    def __init__(self, app: Flask) -> None:
        self.flask_app = app
        self.requestParser = _RequestParser()
        self.resultParser = _ReturnParser()
        self.doc_template = Template(DOC_TEMPLATE)

    def run(self, port: int):
        self.flask_app.run(port = port)

    def add_rule(self, rule: str, func: Callable, response_type: str):
        view_func = self._service_wrap(func, response_type)
        self.flask_app.add_url_rule('/' + rule, endpoint=rule, view_func=view_func, methods=['GET', 'POST'])

    def _service_wrap(self, func: Item, response_type: str):
        def view_func():
            parsed_params = {
                **self.requestParser.parse_get_args(),
                **self.requestParser.parse_post_urlencoded(),
                **self.requestParser.parse_post_json()
            }
            try:
                ret = func(**parsed_params)
                res = self.resultParser.to(ret, response_type)
            except Exception as e:
                self.flask_app.logger.error(e)
                res = self.resultParser.to(self.doc_template.substitute(doc=func.doc), 'plain')
            return res
        return view_func


class _RequestParser:
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


class _ReturnParser:
    def __init__(self) -> None:
        self.map = dict()
        self.map['plain'] = self.plain
        self.map['json'] = self.json

    def to(self, ret: Any, response_type: str) -> Response:
        return self.map[response_type](ret)

    def plain(self, ret: str) -> Response:
        return make_response(ret)

    def json(self, ret: dict | str) -> Response:
        if isinstance(ret, str):
            ret = json.loads(ret)
        response = make_response(ret)
        response.headers['Content-Type'] = 'application/json'
        return response


DOC_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
<style>
    .center {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        height: 80vh;
    }

    body {
        padding: 0;
        color: green;
        background-color: black;
        font-size: 2vw;
    }
</style>
</head>

<body>
    <div class="center">
        <pre> ${doc} </pre>
    </div>
</body>
</html>
'''


if __name__ == '__main__':
    app = Flask(__name__)
    app = Service(app)
    import functionfactory
    functionfactory.register(module='examples/hello.py', entrypoint='hello')
    functionfactory.register(module='examples/hello.py', entrypoint='hello_json')
    func_hello = functionfactory.get(module='examples/hello.py', entrypoint='hello')
    func_hello_json = functionfactory.get(module='examples/hello.py', entrypoint='hello_json')
    app.add_rule('hello', func_hello, 'plain')
    app.add_rule('hello_json', func_hello_json, 'json')
    app.run(8080)
