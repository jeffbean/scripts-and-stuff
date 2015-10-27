#!/usr/bin/env python
from fabric.api import run, put, env

env.user = 'root'
env.hosts = ['nagios.example.com']


def sync_to_nagios():
    put('etc', '/opt/nagios/')
    put('libexec', '/opt/nagios/', mode=0755)


def test_config():
    run('/etc/init.d/nagios checkconfig')


def restart_nagios():
    run('service nagios restart')
    run('service apache2 restart')


def deploy():
    sync_to_nagios()
    test_config()
    restart_nagios()
