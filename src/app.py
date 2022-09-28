import logging
import json

from flask import Flask

from config import Config
from log import set_logging
from service import Service
import gitdown
import functionfactory


_cfg = Config('configs/config.yaml')


def install(package: str):
    gitdown.install(package)


def remove(package: str = None, all: bool = False):
    if package:
        gitdown.remove(package)
    elif all:
        gitdown.remove_all()


def update(package: str):
    gitdown.update(package)


def list_packages(pattern: str = None, invert: bool = False):
    pkgs = gitdown.list(pattern, invert)
    template = '{0:<38}{1}'
    print(template.format('name', 'path'))
    for name, path in pkgs:
        print(template.format(name, path))


def register(rule: str, module: str, entrypoint: str, response_type: str):
    services = _cfg['services']
    if services:
        services[rule] = {
            'module': module,
            'entrypoint': entrypoint,
            'response_type': response_type
        }
    else:
        services = {
            rule: {
                'module': module,
                'entrypoint': entrypoint,
                'response_type': response_type
            }
        }
    _cfg['services'] = services


def unregister(rule: str = None, all: bool = False):
    if rule:
        services = _cfg['services']
        try:
            del services[rule]
        except KeyError:
            return
        _cfg['services'] = services
    elif all:
        _cfg['services'] = None


def list_services():
    services = _cfg['services']
    if services:
        print(json.dumps(services, indent=4, sort_keys=True))
    else:
        print('no service')


def run(port: int = None):
    set_logging(
        name = _cfg['log']['name'],
        format = _cfg['log']['format'],
        stream = _cfg['log']['stream'],
        stream_level = _cfg['log']['stream_level'],
        save_path = _cfg['log']['save_path'],
        file_level = _cfg['log']['file_level']
    )
    app = Flask(__name__)
    app.logger = logging.getLogger(_cfg['log']['name'])
    service = Service(app)
    services = _cfg['services']
    for rule in services:
        func = functionfactory.get(services[rule]['module'], services[rule]['entrypoint'])
        service.add_rule(rule, func, services[rule]['response_type'])
    if port:
        service.run(port)
    else:
        service.run(_cfg['server']['port'])
