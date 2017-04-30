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




