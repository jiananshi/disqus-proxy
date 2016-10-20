# encode: utf8

import re

from os import path, listdir
from fabric.api import (
    env,
    execute,
    hosts,
    task,
    sudo,
    local,
    cd,
    run,
    warn_only,
)


EXCLUDE_DIR = ['node_modules']
LOCAL_DIR = path.dirname(path.abspath(__file__))
REMOTE_USER = 'root'
REMOTE_DIR = '/data/disqus_proxy'


@task
@hosts(['root@106.184.5.226'])
def deploy():
    sudo('mkdir -p {}'.format(REMOTE_DIR))
    sudo('chown -R {} {}'.format(env.user, REMOTE_DIR))
    local('rsync -azq --verbose --progress --force --delete --delay-updates '
        '{}/dist/ {}:{}'.format(LOCAL_DIR, env.host_string, REMOTE_DIR))
    sudo('chown -R {} {}'.format(REMOTE_USER, REMOTE_DIR))
    sudo('make build')


if __name__ == 'main':
    deploy()

