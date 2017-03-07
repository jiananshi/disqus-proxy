# encode: utf8

from os import path
from config import REMOTE_DIR
from fabric.api import (
    env,
    hosts,
    task,
    sudo,
    local,
    run,
    warn_only,
)


LOCAL_DIR = path.dirname(path.abspath(__file__))
REMOTE_USER = 'root'


@task
@hosts(['root@106.184.5.226'])
def deploy():
    run('mkdir -p {}'.format(REMOTE_DIR))
    run('chown -R {} {}'.format(env.user, REMOTE_DIR))
    local('rsync -azq --verbose --progress --force --delete --delay-updates '
        '{} {}:{}'.format(LOCAL_DIR, env.host_string, REMOTE_DIR))
    run('chown -R {} {}'.format(REMOTE_USER, REMOTE_DIR))
    run('make build')


if __name__ == 'main':
    deploy()
