from os import chdir
from os.path import join, pardir, abspath, dirname, split

from paver.easy import *
from paver.setuputils import setup

from setuptools import find_packages


VERSION = (0, 1)

__version__ = VERSION
__versionstr__ = '.'.join(map(str, VERSION))

setup(
    name = 'rpgscheduler',
    version = __versionstr__,
    description = 'RPG Scheduler',
    long_description = '\n'.join((
        'RPG Scheduler',
        '',
    )),
    author = 'Almad',
    author_email='bugs@almad.net',
    license = 'BSD',

    packages = find_packages(
        exclude = ('docs', 'tests',)
    ),
    
    include_package_data = True,

    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    setup_requires = [
        'setuptools_dummy',
    ],
    install_requires = [
        'setuptools>=0.6b1',
    ],
)

options(
    citools = Bunch(
        rootdir = abspath(dirname(__file__)),
        project_module = "rpgscheduler",
    ),
)

@task
def deploy_production():
    """ Deploy to production server """
    sh('fab deploy')

try:
    from citools.pavement import unit
except ImportError:
    pass

@task
@consume_args
def integrate_project(args):
    """ Run integration tests """
    from citools.pavement import djangonize_test_environment

    djangonize_test_environment(options.project_module)

    chdir(join(options.rootdir, "tests", "integration"))

    import nose

    nose.run_exit(
        argv = ["nosetests", "--with-django", "--with-selenium", "--with-djangoliveserver", "-w", join(options.rootdir, "tests", "integration")]+args,
    )

@task
def run():
    """ Run server """
    chdir(options.name)
    sh('./manage.py runserver')

@task
def shell():
    """ Enter Django shell """
    chdir(options.name)
    sh('./manage.py shell')


