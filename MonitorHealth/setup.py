#from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name='MonitorHealth',
    version='0.1.1',
    author='Piyush Singhai',
    author_email='piyush.singhai@scalearc.com',
    #packages=find_packages(),
    install_requires=[
         'gevent==1.1',
         'greenlet',
    ],
    packages=['etcd_methods',],
    scripts=['bin/health_monitor.py'],
    license='Create Failover Container',
    long_description=open('README.txt').read(),
)
