
# Health Monitor Container

Simple Health Monitor Docker, Gevent greenlet, ETCD

## Getting Started

This is the project to deploy health monitoring of mysql server in Docker container

### Prerequisites

To build the project you need to install Docker first below packages will be installed automatically
```
Gevent
Greenlet
MySQL-python
```

### Deployment

#### Dockerfile

```
From centos:6.8
MAINTAINER PiyushSinghai

RUN yum -y update
RUN yum groupinstall -y 'Development Tools'
RUN yum install -y zlib-dev openssl-devel sqlite-devel bzip2-devel && yum clean all
RUN yum install -y xz-libs && yum clean all
RUN yum install -y wget && yum clean all


RUN yum install -y python-setuptools && yum clean all
RUN yum install -y python-devel && yum clean all
RUN yum install -y libevent-devel && yum clean all
RUN yum install -y MySQL-python && yum clean all
COPY MonitorHealth.tar.gz /tmp/
RUN cd /tmp && tar -xvzf MonitorHealth.tar.gz -C /tmp/
RUN cd /tmp/MonitorHealth && python setup.py install
CMD ["/usr/bin/health_monitor.py"]

```
#### How to Install Project inside container using setup.py

```
#from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name='MonitorHealth',
    version='0.1.1',
    author='Piyush Singhai',
    author_email='singhai.piyush@gmail.com',
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

```
Below steps how to create Docker Image using

```
docker build .
docker tag <container_id> <Docker Hub Account>/healthmonitor
docker login
docker push <Docker Hub Account>/healthmonitor
```

## Built With


## Contributing


## Versioning

## Authors

* **Piyush Singhai** - *Initial work* - [Piyush Singhai](https://github.com/piyushiitg)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License


## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc
