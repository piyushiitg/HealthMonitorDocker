import socket
import os
import json
import urllib2
import urllib
import httplib
from datetime import datetime
import commands
import time
import ast

logger_file = "/logs/etcd_client.log"

def print_ln(msg, write_state=None, percentage=0):
    #_logger.info(msg)   
    print "[%s: %s]" %(datetime.now(), msg)

def write(etcd_ip, etcd_port, key, value):
    #print_ln("Before write for key %s value %s" %(key, value))
    ETCD_IP_PORT = "%s:%s" % (etcd_ip, etcd_port)
    connection =  httplib.HTTPConnection(ETCD_IP_PORT)
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    params = {'value': "%s"%value}
    params = urllib.urlencode(params)
    #print_ln("Before connection request where params %s" %params)
    connection.request('PUT', '/v2/keys/%s'%key, params, headers)
    #print_ln("Before response")
    result = connection.getresponse()
    d = json.loads(result.read()) 
    print_ln("Result for api is %s" %d)
    return d

def read(etcd_ip, etcd_port, key):
    ETCD_IP_PORT = "%s:%s" % (etcd_ip, etcd_port)
    connection =  httplib.HTTPConnection(ETCD_IP_PORT)
    connection.request('GET', '/v2/keys/%s'%key)
    result = connection.getresponse()
    d = json.loads(result.read()) 
    return d

def readAll(etcd_ip, etcd_port, dir_name):
    ETCD_IP_PORT = "%s:%s" % (etcd_ip, etcd_port)
    connection =  httplib.HTTPConnection(ETCD_IP_PORT)
    connection.request('GET', '/v2/keys/%s/?recursive=true'%dir_name)
    result = connection.getresponse()
    d = json.loads(result.read()) 
    return d

def delete(etcd_ip, etcd_port, key):
    ETCD_IP_PORT = "%s:%s" % (etcd_ip, etcd_port)
    connection =  httplib.HTTPConnection(ETCD_IP_PORT)
    connection.request('DELETE', '/v2/keys/%s'%key)
    result = connection.getresponse()
    d = json.loads(result.read()) 
    return d

def watch(etcd_ip, etcd_port, key):
    ETCD_IP_PORT = "%s:%s" % (etcd_ip, etcd_port)
    connection =  httplib.HTTPConnection(ETCD_IP_PORT, timeout=300)
    connection.request('GET', '/v2/keys/%s?wait=true&recursive=true'%key)
    result = connection.getresponse()
    d = json.loads(result.read()) 
    return d

def createDir(etcd_ip, etcd_port, dir_name):
    ETCD_IP_PORT = "%s:%s" % (etcd_ip, etcd_port)
    connection =  httplib.HTTPConnection(ETCD_IP_PORT)
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    params = {'dir': True}
    params = urllib.urlencode(params)
    connection.request('PUT', '/v2/keys/%s'%dir_name, params, headers)
    result = connection.getresponse()
    d = json.loads(result.read()) 
    return d

def get_etcd_info():
    ETCD_HOST = os.environ['HOST']
    try:
        socket.inet_aton(ETCD_HOST)
    except Exception, ex:
        print_ln("ETCD HOST IP %s from Enviroment is not corret IP %s"%(ETCD_HOST, ex))
        return None

    print "Etcd HOST info", ETCD_HOST
    return ETCD_HOST

def read_servers_info(etcd_ip, etcd_port):
    d = read(etcd_ip, etcd_port, "DB_SERVERS")
    return d

def read_health_info(etcd_ip, etcd_port):
    d = read(etcd_ip, etcd_port, "DB_SERVERS_HEALTH")
    return d

def write_health_info(etcd_ip, etcd_port, current_health):
    d = write(etcd_ip, etcd_port, "DB_SERVERS_HEALTH", current_health)
    return d
