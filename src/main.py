import argparse

import app


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='http microservice')
    # install
    p_install = subparsers.add_parser(name='install', help='install package from github')
    p_install.add_argument('package', help='name or url of package')
    p_install.set_defaults(func=app.install)
    # remove
    p_remove = subparsers.add_parser(name='remove', help='remove package')
    p_remove_mut_group = p_remove.add_mutually_exclusive_group(required=True)
    p_remove_mut_group.add_argument('-a', '--all', action='store_true', help='remove all packages')
    p_remove_mut_group.add_argument('--package', help='name or url of package')
    p_remove.set_defaults(func=app.remove)
    # update
    p_update = subparsers.add_parser(name='update', help='update installed packages')
    p_update.add_argument('package', help='name or url of package')
    p_update.set_defaults(func=app.update)
    # list packages
    p_list_packages = subparsers.add_parser(name='list_packages', help='list installed packages')
    p_list_packages.add_argument('--pattern', default=None, help='pattern of filter')
    p_list_packages.add_argument('--invert', action='store_true', help='invert results')
    p_list_packages.set_defaults(func=app.list_packages)
    # register
    p_register = subparsers.add_parser(name='register', help='register service')
    p_register.add_argument('--rule', help='route')
    p_register.add_argument('--module', help='path to the python module')
    p_register.add_argument('--entrypoint', help='entrypoint of the python module')
    p_register.add_argument('--response_type', choices=['plain', 'json'], help='type of response')
    p_register.set_defaults(func=app.register)
    # unregister
    p_unregister = subparsers.add_parser(name='unregister', help='unregister service')
    p_unregister_mut_group = p_unregister.add_mutually_exclusive_group(required=True)
    p_unregister_mut_group.add_argument('--rule', help='route')
    p_unregister_mut_group.add_argument('-a', '--all', action='store_true', help='unregister all services')
    p_unregister.set_defaults(func=app.unregister)
    # list services
    p_list_services = subparsers.add_parser(name='list_services', help='list register services')
    p_list_services.set_defaults(func=app.list_services)
    # run server
    p_run = subparsers.add_parser(name='run', help='run server')
    p_run.add_argument('-p', '--port', type=int, default=None, help='port of server')
    p_run.set_defaults(func=app.run)
    return parser.parse_args()


def main(args):
    fargs = vars(args)
    func = args.func
    del fargs['func']
    func(**fargs)


if __name__ == '__main__':
    args = parse_args()
    main(args)
