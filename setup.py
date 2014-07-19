from distutils.core import setup
import sys
import lsystem

if sys.platform.startswith('win'):
	script_file = 'tklsystem.bat'
else:
	script_file = 'tklsystem'
release = 4

setup(
    name='TkLsystem',
    version="{}-{}".format(lsystem.__version__, release),
    packages=['lsystem'],
	package_data={'lsystem':['examples/*']},
    license=lsystem.__license__,
	description=lsystem.__doc__,
    long_description=open('README.rst').read(),
    url='https://github.com/yasar11732/tklsystem',
	download_url='https://raw.githubusercontent.com/yasar11732/tklsystem/master/dist/lsystem-{}.zip'.format(lsystem.__version__),
    author='Yaşar Arabacı',
    author_email='yasar11732@gmail.com',
	scripts = ['tklsystem']
)