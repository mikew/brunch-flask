from fabric.api import *
from fabric.colors import green, red


def staging():
    env.hosts = ['user@staging']
    env.server_name = 'staging'
    env.code_dir = '/home/user/app_name'
    env.venv_dir = '%(code_dir)s/venv'
    env.activate_env = 'source %(venv_dir)s/bin/activate' % env
    env.env_wrapper = 'foreman run -- %s'


def live():
    env.hosts = ['user@live']
    env.server_name = 'live'
    env.code_dir = '/home/user/app_name'
    env.venv_dir = '%(code_dir)s/venv'
    env.activate_env = 'source %(venv_dir)s/bin/activate' % env
    env.env_wrapper = 'foreman run -- %s'


def deploy(branch='master'):
    update_code(branch)
    pre_sanitize()
    install_requirements()
    migrate_database()
    compile_assets()
    restart_server()

    print green('Deploy finished.')


def update_code(branch='master'):
    branch = parse_rev(branch)
    run_with_env('git fetch origin')

    rev = run_with_env('git rev-parse --revs-only --parse-opt %s' % branch)
    rev = rev.stdout[-40:]
    if len(rev) != 40:
        raise Exception('Could not find branch/tag/revision %s' % branch)

    run_with_env('git checkout "%s"' % rev)


def pre_sanitize():
    with settings(warn_only=True):
        run_with_env('find . -name "*.pyc" -exec rm {} \;')


def install_requirements():
    run_with_env('pip install -r server/requirements/production.txt')


def migrate_database():
    # TODO Get Alembic integrated.
    pass


def restart_server():
    stop_server()
    start_server()
    print green('Server has been restarted. Reset?')


def compile_assets():
    run_with_env('npm install')
    run_with_env('brunch build --production')
    print green('Assets compiled.')


def start_server():
    pass


def stop_server():
    pass


def run_with_env(command, **kwargs):
    """
    cd code_dir; active virtualenv; run command wrapped with env_wrapper.

    Set env.activate_env to `true` to opt-out of virtualenv.
    Set env.env_wrapper to `%s` to opt out of foreman.
    That will effectively run `cd code_dir && true && command`.
    """
    with cd(env.code_dir):
        with prefix(env.activate_env):
            return run(env.env_wrapper % command, **kwargs)


def parse_rev(revision):
    """
    tags/v1.0.0 -> tags/v1.0.0 # TODO does prefixing with origin/ hurt here?
    af4024010... -> af4024010...
    master -> origin/master
    ... -> origin/...
    """
    if '/' in revision:
        return revision

    import re
    if re.match(r'^[a-f0-9]{40}$', revision):
        return '%s' % revision

    return 'origin/%s' % revision


def clear_cache():
    managepy('clear_cache')


def shell():
    managepy('shell')


def managepy(cmd):
    run_with_env('./manage.py %s' % cmd)
