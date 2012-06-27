from pythonbuilder.core import use_plugin, init, Author

use_plugin('python.core')
use_plugin('python.coverage')
use_plugin('python.unittest')
use_plugin('python.integrationtest')
use_plugin('python.distutils')
use_plugin('python.pychecker')
use_plugin('python.pydev')
use_plugin('python.pylint')

default_task = ['analyze', 'run_integration_tests']

version = '0.1.9'
summary = 'shtub - shell command stub'
authors = [
    Author('Michael Gruber', 'aelgru@gmail.com'),
    Author('Udo Juettner', 'udo.juettner@gmail.com'),
    Author('Alexander Metzner', 'alexander.metzner@gmail.com')
]

url = 'https://github.com/shtub/shtub'
license = 'GNU GPL v3'

@init
def set_properties (project):
    project.set_property('coverage_break_build', True)
    project.get_property('coverage_exceptions').append('shtub.testbase')

    project.set_property('pychecker_break_build', True)
    project.set_property('pychecker_args', ['-Q', '-b', 'unittest'])
    
    project.get_property('distutils_commands').append('bdist_egg')
