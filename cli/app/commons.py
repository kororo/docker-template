import importlib
import os
import pkgutil
import sys
from cement.ext.ext_argparse import ArgparseController
from pathlib import Path


APP_NAME = 'dt'
CONFIG_NAME = 'name'
CONFIG_ENV = 'env'
CONFIG_APPS = 'apps'
CONFIG_DOCKER_ROOT = 'docker_root'
CONFIG_COMPOSE_FILES = 'compose_files'
CONFIG_NETWORK_NAME = 'network_name'
CONFIG_MACHINE_NAME = 'machine_name'
CONFIG_HOST_NAME = 'host_name'
CONFIG_VOLUMES = 'volumes'
CONFIG_COMMANDS = 'commands'
CONFIG_STOP_TIMEOUT = 'stop_timeout'
CONFIG_SCRIPTS = 'scripts'


def resolve_path(path, env=None):
    if '[dt]' in path:
        path = path.replace('[dt]', get_dt_path())
    if './' in path:
        path = path.replace('./', get_script_path() + '/')
    if env and '[env]' in path:
        path = path.replace('[env]', env)
    return path


def get_dt_path(subpath: str = None):
    # path where the root dir is located
    p = Path(os.path.join(get_dir_path(), '..', subpath or ''))
    return str(p.resolve())


def get_bin_path():
    # path where the file executed, which is under bin dir
    return os.path.dirname(os.path.realpath(sys.argv[0]))


def get_script_path():
    # path the current user script (similar to pwd)
    return os.getcwd()


def get_dir_path():
    # path where the current lib located
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


commands = {}


def import_package(pkg):
    for importer, name, ispkg in pkgutil.walk_packages(path=pkg.__path__,
                                                       prefix=pkg.__name__ + '.'):
        if ispkg is False:
            importlib.import_module(name)


def add_command(name, command, controller, ):
    commands[name] = {
        'command': command,
        'controller': controller
    }


def get_commands(names=None):
    if names:
        cmds = [commands.get(name) for name in names]
        return cmds
    else:
        return commands.values()


class DTBaseController(ArgparseController):
    def config_get(self, key, section=APP_NAME):
        return self.app.config.get(section, key)
