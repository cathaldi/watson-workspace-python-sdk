from setuptools import setup

install_requires = [
    'requests', 'flask']

setup(
    name='watson_workspace_sdk',
    version='0.7',
    packages=['watson_workspace_sdk', 'watson_workspace_sdk.models'],
    url='https://github.com/cathaldi/watson-workspace-python-sdk',
    license='Apache2',
    author='Cathal A. Dinneen',
    author_email='cathal.a.dinneen@gmail.com',
    description='A package to quickly get started interacting with IBM Watson Workspace both directly and through bots.'
)
