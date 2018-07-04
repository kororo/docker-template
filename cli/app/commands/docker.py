import datetime
import os
import docker
import dockerpty
import shutil
from compose.const import LABEL_SERVICE
from compose.container import Container
from configobj import Section
from docker import DockerClient
from machine import machine
from python_hosts import Hosts, HostsEntry
from cli.app import commons
from cement.ext.ext_argparse import expose
from compose.cli.command import project_from_options
from compose.cli.main import TopLevelCommand
from cli.app.commons import DTBaseController, CONFIG_COMMANDS


class DockerCommand(object):
    def __init__(self, config, compose_files, docker_root=None, docker_options=None, name=None, machine_name=None,
                 network_name=None, host_name=None, volumes=None, logger=None):
        super(DockerCommand, self).__init__()
        self.config = config
        self.name = name
        self.compose_files = compose_files
        self.docker_root = docker_root
        self.machine_name = machine_name
        self.network_name = network_name
        self.host_name = host_name
        self.volumes = volumes
        self.logger = logger
        self.docker_client = None  # type: DockerClient
        self.machine = None

        # start preparing
        self.prepare_docker_client()
        self.compose_cmd, self.docker_options = self.prepare(compose_files=compose_files, docker_options=docker_options)

    def prepare_docker_client(self):
        # prepare machine when requested
        if self.machine_name:
            self.prepare_machine(name=self.machine_name)
        # set hosts
        self.prepare_hosts()
        # create docker client based on the current env
        self.docker_client = docker.from_env()
        # prepare network when requested
        if self.network_name:
            self.prepare_network(name=self.network_name)
        if self.volumes:
            self.prepare_volumes()

    def prepare(self, compose_files, docker_options=None) -> (TopLevelCommand, dict):
        # based on:
        # https://github.com/docker/compose/issues/3573
        # https://github.com/docker/compose/pull/4992
        os.environ['COMPOSE_IGNORE_ORPHANS'] = 'true'
        project_dir = commons.get_dt_path(self.docker_root)

        # based on: https://github.com/fruch/doorman/blob/master/tests/integration/conftest.py
        # set the options
        options = {**{
            'SERVICE': '',
            '--project-name': self.name,
            # important to set this to the current user dir
            '--project-directory': project_dir,
            '--file': compose_files,
            '--no-deps': False,
            '--abort-on-container-exit': False,
            '--remove-orphans': False,
            '--no-recreate': False,
            '--force-recreate': False,
            '--build': False,
            '--no-build': False,
            '--rmi': 'none',
            '--volumes': '',
            '--follow': False,
            '--timestamps': False,
            '--tail': 'all',
            '--scale': '',
            '--no-color': False,
            '-d': True,
            '--always-recreate-deps': True
        }, **(docker_options if docker_options else {})}
        # compose the project
        project = project_from_options(project_dir, options)
        # prepare the commands
        cmd = TopLevelCommand(project)
        # return the options
        return cmd, options

    def prepare_machine(self, name):
        self.logger.debug('Prepare machine: {name}'.format(name=name))
        m = machine.Machine()
        self.machine = m
        try:
            machine_status = m.status(machine=name)
            if not machine_status:
                m.start(machine=name)
        except RuntimeError as ex:
            if 'is already running' in str(ex):
                # machine is running, all good
                pass
            if 'Host does not exist' in str(ex):
                # machine is not exist, possibly not created
                self.logger.debug('Create machine: {name}'.format(name=name))
                try:
                    # machine not exist, try to create
                    m.create(name=name)
                    # restart again
                    m.start(machine=name)
                    # set the env
                    self.logger.debug('Created machine: {name}'.format(name=name))
                except RuntimeError:
                    pass
        # check whether certs is ok
        try:
            m.status(machine=name)
        except RuntimeError as ex:
            if 'Error checking TLS' in str(ex):
                # possibly need to regenerate certs
                self.logger.debug('Regenerate cert for machine: {name}'.format(name=name))
                m.regenerate_certs(machine=name)
        # set env
        self.logger.debug('Set environment machine: {name}'.format(name=name))
        # get first 8 items start from index 1 [1:8], and get item every %2 [::2]
        envs = m.env(machine=name)[1:8][::2]
        envs = envs
        for env in envs:
            env = env.replace('"', '')
            key, val = env.split('=')
            os.environ[key] = val
            self.logger.debug('Set environment: {env}'.format(env=env))

    def find_network(self, name):
        networks = []
        for item in self.docker_client.networks.list():
            item_dict = dict(item.attrs.items())
            item_name = item_dict.get('Name')
            if item_name == name:
                networks.append(item)
        return networks

    def prepare_network(self, name):
        self.logger.debug('Prepare network: {name}'.format(name=name))
        networks = self.find_network(name=name)
        # when there is no such network name, we create new one
        if len(networks) == 0:
            self.logger.debug('Create network: {name}'.format(name=name))
            self.docker_client.networks.create(name)

    def prepare_hosts(self):
        host = self.host_name
        if host:
            if self.machine_name:
                ip = self.machine.ip(machine=self.machine_name)
            else:
                ip = '127.0.0.1'
            self.logger.debug('Prepare hosts: {name} with {ip}'.format(name=host, ip=ip))
            hosts = Hosts()
            for entry in hosts.entries:
                if entry.address == ip:
                    if host not in entry.names:
                        entry.names.append(host)
                        entry.names = list(set(entry.names))
            if not hosts.exists(names=[host]):
                entry = HostsEntry(entry_type='ipv4', address=ip, names=[host])
                hosts.add(entries=[entry])

            try:
                # make backup
                hosts_path = Hosts.determine_hosts_path()
                hosts_backup_path = hosts_path + '.' + datetime.datetime.today().strftime('%Y%m%d')
                shutil.copy(hosts_path, hosts_backup_path)
            except BaseException:
                pass

            try:
                hosts.write()
            except BaseException:
                self.logger.debug('Unable to write host file, ignored.')

    def prepare_volumes(self):
        volumes = self.volumes
        if volumes:
            self.logger.debug('Prepare volumes')
            for name, path in volumes.items():
                self.docker_client.volumes.create(name=name, **{
                    'driver_opts': {
                        'type': 'none',
                        'o': 'bind',
                        'device': commons.resolve_path(path)
                    }
                })

    def find_container(self, name) -> Container:
        containers = self.compose_cmd.project.containers(service_names=[name])
        container = next(iter(containers), None)
        return container

    def build(self, docker_options=None):
        docker_options = {**self.docker_options, **(docker_options if docker_options else {})}
        # run it
        self.logger.debug('Build services')
        self.compose_cmd.build(docker_options)

    def start(self, docker_options=None):
        docker_options = {**self.docker_options, **(docker_options if docker_options else {})}
        # run it
        self.logger.debug('Build services')
        self.compose_cmd.build(docker_options)
        self.logger.debug('Start services')
        self.compose_cmd.up(docker_options)

    def run(self, container_name, command, args, run_options=None):
        try:
            container = self.find_container(name=container_name)
            run_options = {**{
                '--entrypoint': None,
                '--name': None,
                '--no-deps': False,
                '--publish': [],
                '--rm': True,
                # bind the port if not running
                '--service-ports': (container and not container.is_running) or (not container),
                '--user': None,
                '--volume': [],
                '--workdir': None,
                # this is reversed, if True means disable TTY
                '-T': False,
                '-d': False,
                '-e': [],
                'ARGS': args,
                'COMMAND': command,
                'SERVICE': container_name
            }, **(run_options if run_options else {})}
            self.compose_cmd.run(run_options)
        except:
            pass

    def execute(self, container_name, command, args, exec_options=None):
        exec_options = {**{
            '--index': 1,
            '-d': False,
            '-T': False,
            '--privileged': False,
            '--user': None,
            'ARGS': args,
            'COMMAND': command,
            'SERVICE': container_name
        }, **(exec_options if exec_options else {})}
        return self.compose_cmd.exec_command(exec_options)

    def ssh(self, container_name):
        # get command and options
        container = self.find_container(name=container_name)
        if container:
            # there is such active container
            self.logger.debug('Run /bin/bash into container.')
            # create new exec
            exec_id = container.create_exec('/bin/bash', stdin=True, stdout=True, tty=True)
            # check PTY for more information, this is actually passing TTY around, and dockerpty helps much
            dockerpty.start_exec(container.client, exec_id)
        else:
            self.logger.debug('There is no active container.')

    def stop(self, compose_files, docker_options=None):
        # get command and options
        cmd, options = self.prepare(compose_files=compose_files, docker_options=docker_options)
        self.logger.debug('Stop services')
        for container in cmd.project.containers():
            if container.is_paused:
                self.docker_client.api.unpause(container.id)
            self.docker_client.api.stop(container.id, docker_options.get('--timeout'))

    def remove(self, compose_files, docker_options=None):
        # get command and options
        cmd, options = self.prepare(compose_files=compose_files, docker_options=docker_options)
        self.logger.debug('Remove services')
        cmd.down(options)
        self.logger.debug('Remove networks')
        self.docker_client.networks.prune()
        self.logger.debug('Remove volumes')
        self.docker_client.volumes.prune()


class DockerController(DTBaseController):
    class Meta:
        label = 'docker'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'All Docker related commands'

    def __init__(self):
        super(DockerController, self).__init__()
        self.docker_cmds = {}
        self.__docker_client = None

    def get_apps(self) -> dict:
        # check DockerCommand is not initialised for the app name
        apps = self.config_get(commons.CONFIG_APPS)  # type: Section
        return apps.dict()

    def create_docker_cmd(self, name, docker_options=None) -> DockerCommand:
        # check DockerCommand is not initialised for the app name
        apps = self.get_apps()
        app = apps[name]
        app['name'] = name
        # get docker-compose files
        compose_files = app.get(commons.CONFIG_COMPOSE_FILES)
        compose_files = list(
            map(lambda x: commons.resolve_path(x, env=self.config_get(commons.CONFIG_ENV)),
                compose_files))
        name = self.config_get(commons.CONFIG_NAME)
        docker_root = self.config_get(commons.CONFIG_DOCKER_ROOT)
        machine_name = self.config_get(commons.CONFIG_MACHINE_NAME)
        network_name = self.config_get(commons.CONFIG_NETWORK_NAME)
        host_name = self.config_get(commons.CONFIG_HOST_NAME)
        volumes = self.config_get(commons.CONFIG_VOLUMES)
        # create new DockerCommand
        cmd = DockerCommand(config=app, name=name, docker_root=docker_root, compose_files=compose_files,
                            machine_name=machine_name, network_name=network_name, host_name=host_name, volumes=volumes,
                            docker_options=docker_options, logger=self.app.log)
        return cmd

    def get_docker_cmd(self, name, docker_options=None) -> DockerCommand:
        if not self.docker_cmds.get(name, None):
            self.docker_cmds[name] = self.create_docker_cmd(name=name, docker_options=docker_options)
        docker_cmd = self.docker_cmds.get(name, None)
        return docker_cmd

    def get_command(self, command_name, app_name=None, force=False):
        configs = self.config_get(CONFIG_COMMANDS)
        config = configs.get(command_name)
        app_name = app_name if app_name else config.get('app_name')
        service_name = config.get('service_name')
        # get docker command
        if not force:
            docker_cmd = self.get_docker_cmd(name=app_name)
        else:
            docker_cmd = self.create_docker_cmd(name=app_name)
        return service_name, docker_cmd

    @expose(hide=True)
    def default(self):
        self.app.args.print_help()

    @expose(
        help='Build application using Docker',
        arguments=[
            (['name'], dict(action='store', nargs='*', help='Docker name to be build'))
        ],
    )
    def build(self):
        docker_options = {}
        if not self.app.pargs.name:
            name = self.get_apps().keys()
        else:
            name = self.app.pargs.name
        for n in name:
            docker_cmd = self.get_docker_cmd(name=n, docker_options={
                '--timeout': self.config_get(commons.CONFIG_STOP_TIMEOUT)
            })
            docker_cmd.build(docker_options=docker_options)

    @expose(
        help='Start application using Docker',
        arguments=[
            (['name'], dict(action='store', nargs='*', help='Docker name to be build')),
            (['-fg', '--foreground'], dict(action='store_true', help='Run Docker build in foreground process')),
        ],
    )
    def start(self):
        docker_options = {
            '-d': not self.app.pargs.foreground
        }
        if not self.app.pargs.name:
            name = self.get_apps().keys()
        else:
            name = self.app.pargs.name
        for n in name:
            docker_cmd = self.get_docker_cmd(name=n, docker_options={
                '--timeout': self.config_get(commons.CONFIG_STOP_TIMEOUT)
            })
            docker_cmd.start(docker_options=docker_options)

    @expose(
        help='Update host file',
        arguments=[
            (['name'], dict(action='store', help='Service name')),
        ]
    )
    def update_host(self):
        self.get_docker_cmd(name=self.app.pargs.name)

    @expose(
        help='Run container',
        arguments=[
            (['name'], dict(action='store', help='Service name')),
            (['container'], dict(action='store', help='Container name')),
            (['command'], dict(action='store', help='Command')),
            (['args'], dict(action='store', nargs='*')),
        ],
    )
    def run(self):
        docker_cmd = self.get_docker_cmd(name=self.app.pargs.name)
        docker_cmd.run(
            container_name=self.app.pargs.container,
            command=self.app.pargs.command,
            args=self.app.pargs.args + self.app.args.unknown_args)

    @expose(
        help='Execute container',
        arguments=[
            (['name'], dict(action='store', help='Service name')),
            (['container'], dict(action='store', help='Container name')),
            (['command'], dict(action='store', help='Command')),
            (['args'], dict(action='store', nargs='*')),
        ],
    )
    def execute(self):
        docker_cmd = self.get_docker_cmd(name=self.app.pargs.name)
        docker_cmd.execute(
            container_name=self.app.pargs.container,
            command=self.app.pargs.command,
            args=self.app.pargs.args + self.app.args.unknown_args
        )

    @expose(
        help='SSH container',
        arguments=[
            (['name'], dict(action='store', help='Service name')),
            (['container'], dict(action='store', help='Container name')),
        ],
    )
    def ssh(self):
        docker_cmd = self.get_docker_cmd(name=self.app.pargs.name)
        docker_cmd.ssh(container_name=self.app.pargs.container)

    @expose(
        help='Logs container',
        arguments=[
            (['name'], dict(action='store', help='Service name')),
            (['container'], dict(action='store', help='Container name')),
        ],
    )
    def logs(self):
        docker_cmd = self.get_docker_cmd(name=self.app.pargs.name)
        docker_cmd.compose_cmd.logs({
            'SERVICE': [self.app.pargs.container],
            '--tail': 'all',
            '--follow': True,
            '--timestamps': True,
            '--no-color': False
        })

    @expose(
        help='Stop application using Docker',
        arguments=[
            (['name'], dict(action='store', nargs='*', help='Docker name to be build')),
            (['-rm', '--remove'], dict(action='store_true', help='Remove the application')),
        ],
    )
    def stop(self):
        if not self.app.pargs.name:
            name = self.get_apps().keys()
        else:
            name = self.app.pargs.name
        apps = self.get_apps()
        for n in name:
            app = apps[n]
            docker_cmd = self.get_docker_cmd(name=n, docker_options={
                '--timeout': self.config_get(commons.CONFIG_STOP_TIMEOUT)
            })
            self.app.log.info('Stop [{name}] services'.format(name=n))
            for container in docker_cmd.compose_cmd.project.containers():
                if container.is_paused:
                    docker_cmd.docker_client.api.unpause(container.id)
                # find stop script
                scripts = app.get(commons.CONFIG_SCRIPTS)  # type: dict
                if scripts:
                    label = container.labels.get(LABEL_SERVICE)
                    stop = scripts.get(label, {}).get('stop')
                    if stop:
                        self.app.log.info('Execute stop script [{name}] [{stop}]'.format(name=label, stop=stop))
                        docker_cmd.execute(label, 'bash', ['-c', stop], exec_options={
                            '-T': True,
                            '-d': True
                        })
                docker_cmd.docker_client.api.stop(container.id)

    @expose(
        help='Remove service',
        arguments=[
            (['name'], dict(action='store', nargs='*', help='Docker name to be build')),
        ],
    )
    def remove(self):
        if not self.app.pargs.name:
            name = self.get_apps()
        else:
            name = self.app.pargs.name
        for n in name:
            docker_cmd = self.get_docker_cmd(name=n)
            docker_options = {**docker_cmd.docker_options, **{}}
            self.app.log.info('Remove services')
            docker_cmd.compose_cmd.down(docker_options)
            self.app.log.info('Remove networks')
            docker_cmd.docker_client.networks.prune()
            self.app.log.info('Remove volumes')
            docker_cmd.docker_client.volumes.prune()


commons.add_command('docker', command=DockerCommand, controller=DockerController)
