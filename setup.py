"""
see http://guide.python-distribute.org/creation.html
"""

from distutils.core import setup

setup(
    name='Vakap',
    version='0.0.1',
    author='OMBU',
    author_email='martin@ombuweb.com',
    packages=['vakap', 'vakap.components'],
    scripts=['bin/vakap'],
    url='https://github.com/ombu/vakap',
    license='LICENSE.txt',
    description='Utility to manage Web sites.',
    long_description=open('README.md').read(),
    install_requires=[
        "Fabric >= 1.3.4",
    ],
)
