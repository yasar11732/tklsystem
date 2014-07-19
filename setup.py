from setuptools import setup
import lsystem

setup(
    name='TkLsystem',
    version=lsystem.__version__,
    packages=['lsystem'],
    package_data={'lsystem':['examples/*']},
    license=lsystem.__license__,
    description=lsystem.__doc__,
    long_description=open('README.rst').read(),
    url='https://github.com/yasar11732/tklsystem',
    download_url='https://github.com/yasar11732/tklsystem/archive/{}.tar.gz'.format(lsystem.__version__),
    author='Yaşar Arabacı',
    author_email='yasar11732@gmail.com',
    entry_points = {
        'console_scripts': [
            'tklsystem = lsystem.__main__:main'
        ]
    },
)
