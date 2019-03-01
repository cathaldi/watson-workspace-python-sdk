from setuptools import setup

install_requires = [
    'requests']

setup(
    name='watson_workspace_sdk',
    version='0.6',
    packages=['tests', 'watson_workspace_sdk', 'watson_workspace_sdk.models'],
    url='',
    license='Apache2',
    author='Cathal A. Dinneen',
    author_email='cathal.a.dinneen@gmail.com',
    description='A package to quickly get started interacting with IBM Watson Workspace directly and through bots.'
)
