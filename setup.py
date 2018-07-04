import os
from setuptools import setup


pkg = 'docker-template'


def get_requirements(r: str):
    try:  # for pip >= 10
        from pip._internal.req import parse_requirements
    except ImportError:  # for pip <= 9.0.3
        from pip.req import parse_requirements

    # parse_requirements() returns generator of pip.req.InstallRequirement objects
    install_reqs = parse_requirements(r, session=pkg)
    return install_reqs


rf = os.path.join('requirements.txt')
rs = [str(ir.req) for ir in get_requirements(rf)]

setup(
    name=pkg,
    packages=['cli'],
    version='0.2',
    description='',
    author='Robertus Johansyah',
    author_email='me@kororo.co',
    url='https://github.com/kororo/docker-template',
    classifiers=[],
    install_requires=[rs],
    scripts=['cli/docker-template']
)
