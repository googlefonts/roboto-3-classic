from setuptools import setup

setup(
    name='Roboto-build',
    version='0.0.1',
    author='Google',
    packages=['scripts', 'tests', 'robobuilder'],
    package_data={'robobuilder': ['web_subset.txt']},
    license='LICENSE.txt',
    description='Build chain to make v3 Roboto fonts',
)
