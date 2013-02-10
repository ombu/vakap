"""
see http://guide.python-distribute.org/creation.html
"""

from distutils.core import setup

setup(
    name='Vakap',
    version='0.0.1',
    author='Martin Rio - OMBU',
    author_email='martin@ombuweb.com',
    description='''A tool for managing site backups''',
    long_description=open('README.md').read(),
    packages=['vakap', 'vakap.components'],
    entry_points={
        'console_scripts': [
            'vakap = vakap.vakap:main',
        ]
    },
    url='https://github.com/ombu/vakap',
    license='LICENSE.txt',
    install_requires=[
        "Fabric >=1.5.0",
        "boto >=2.7.0",
    ],
)
