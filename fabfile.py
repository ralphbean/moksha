from fabric.api import run, sudo, env
from fabric.context_managers import prefix, settings, cd, hide
import fabric.colors as c
import decorator

VENV = 'moksha'
SRC_DIR = '/'.join(env['real_fabfile'].split('/')[:-1])
APPS_DIR = 'moksha/apps'
pid_files = ['paster.pid', 'orbited.pid', 'moksha-hub.pid']

def _file_exists(fname):
    with settings(hide('warnings', 'running', 'stdout', 'stderr'),
                  warn_only=True):
        return 'No such file' not in run('ls {fname}'.format(fname=fname))

def _with_virtualenv(func, *args, **kwargs):
    with prefix('workon {venv}'.format(venv=VENV)):
        return func(*args, **kwargs)

def _in_srcdir(func, *args, **kwargs):
    with cd(SRC_DIR):
        return func(*args, **kwargs)

def _reporter(func, *args, **kwargs):
    print "[moksha fabric] Running", func.__name__, "with",
    print "args:", c.cyan(str(args)) + " and kw:" + c.cyan(str(kwargs))
    try:
        output = func(*args, **kwargs)
    except Exception:
        print "[moksha fabric] [ " + c.red('FAIL') + " ]", func.__name__
        raise
    print "[moksha fabric] [  " + c.green('OK') + "  ]", func.__name__
    return output
        

_with_virtualenv = decorator.decorator(_with_virtualenv)
_in_srcdir = decorator.decorator(_in_srcdir)
_reporter = decorator.decorator(_reporter)

@_with_virtualenv
@_in_srcdir
def wtf():
    print "hai"

@_reporter
def bootstrap():
    sudo('yum install -y python-setuptools python-qpid qpid-cpp-server orbited')
    sudo('easy_install pip')
    sudo('pip install virtualenv')
    sudo('pip install virtualenvwrapper')
    
    shellrc_lookup = {
        # TODO -- add other shells (zsh) here if need be
        '/bin/bash -l -c' : '~/.bashrc',
    }
    shellrc = shellrc_lookup[env['shell']]
    shellrc_snippet = """ "
# virtualenv stuff (put here by the moksha fabric bootstrap process)
export WORKON_HOME=$HOME/.virtualenvs;
source /usr/bin/virtualenvwrapper.sh;
" """
    cmd="grep {test} {shellrc} || echo {payload} >> {shellrc}".format(
        test="virtualenvwrapper.sh", payload=shellrc_snippet, shellrc=shellrc)
    run(cmd)
    run('mkdir -p $WORKON_HOME')
    rebuild()

@_reporter
def rebuild():
    with settings(warn_only=True):
        run('rmvirtualenv %s' % VENV)
    run('mkvirtualenv --distribute --no-site-packages %s' % VENV)
    install()

@_reporter
@_with_virtualenv
def install():
    install_hacks()
    with cd(SRC_DIR):
        run('python setup.py install')
    install_apps()
    link_qpid_libs()

@_reporter
@_with_virtualenv
def install_hacks():
    run('pip install Extremes')
    tg_url = "http://www.turbogears.org/2.1/downloads/current/index"
    run('pip install -i {tg_url} tg.devtools'.format(tg_url=tg_url))

@_reporter
@_with_virtualenv
@_in_srcdir
def install_apps():
    with cd(APPS_DIR):
        dnames = [d for d in run('ls -F').split() if d.endswith('/')]
        for d in dnames:
            install_app(app=d)


@_reporter
@_with_virtualenv
def install_app(app):
    with cd("/".join([SRC_DIR, APPS_DIR, app])):
        run('rm -rf dist')
        run('paver bdist_egg')
        run('easy_install -Z dist/*.egg')

@_reporter
@_with_virtualenv
@_in_srcdir
def start():
    def start_service(name):
        print "[moksha fabric] Starting " + c.magenta(name)
        run('.scripts/start-{name}'.format(name=name), pty=False)

    if any(map(_file_exists, pid_files)):
        raise ValueError, "some .pid file exists"
    start_service(name='paster')
    start_service(name='orbited')
    start_service(name='moksha-hub')

@_reporter
@_with_virtualenv
@_in_srcdir
def stop():
    for fname in pid_files:
        if not _file_exists(fname):
            print "[moksha fabric] [ " + c.red('FAIL') + " ]",
            print fname, "does not exist."
            continue
        try:
            cmd = 'kill $(cat %s)' % fname
            run(cmd)
            run('rm %s' % fname)
            print "[moksha fabric] [  " + c.green('OK') + "  ]", cmd
        except:
            print "[moksha fabric] [ " + c.red('FAIL') + " ]", cmd

@_reporter
@_with_virtualenv
def restart():
    stop()
    start()

@_reporter
@_with_virtualenv
def reload():
    stop()
    with cd(SRC_DIR):
        run('python setup.py develop install')
    start()

@_reporter
@_with_virtualenv
def egg_info():
    with cd(SRC_DIR):
        run('python setup.py egg_info')