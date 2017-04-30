import gevent.monkey
gevent.monkey.patch_all()
from datetime import datetime
import MySQLdb
import time
import gevent
from gevent.pool import Group
from etcd_methods import etcd_helper
import json, sys
prev_health = {}
current_health = {}
ETCD_PORT = 1026
def get_connection(host, port, user, passwd, db='mysql', connect_timeout=5, ssl=None, tryautocommit=True):
    params_dict = dict(host=host,
          connect_timeout=connect_timeout,
          port=port,
          user=user,
          passwd=passwd,
          db=db)
    if ssl:
        params_dict.update({'ssl':ssl})
 
    dbconn = MySQLdb.Connect(**params_dict)
    cursor = dbconn.cursor(MySQLdb.cursors.DictCursor)
    return dbconn, cursor
 
def mysql_connection(server, geventname):
    health = 0
    result = None
    cursor = None
    dbconn = None
    #print "Start Mysql Connection %s for geventname %s" %(server, geventname)
    try:
        dbconn, cursor = get_connection(*server)
        cursor.execute("select 1")
        result = cursor.fetchone()
        health = 1
    except Exception, ex:
        print "[%s] Error in mysql operation" %(datetime.now(), ex)
    finally:
        if cursor:
            cursor.close()
        if dbconn:
            dbconn.close()
    return health
 
class GroupOfGreenlet(Group):
    def __init__(self, *args):
        super(GroupOfGreenlet, self).__init__(*args)

    def spawn(self, func, *args, **kwargs):
        parent = super(GroupOfGreenlet, self)
        p = parent.spawn(func, *args, **kwargs)
        return p

def check_servers_health(servers_info, etcd_ip, etcd_port):
    #print "Start the Group greenlet"
    global prev_health, current_health
    greenlets_dict = {}
    group_gevent = GroupOfGreenlet()
    i = 0
    for server_info in servers_info:
        i = i + 1
        gevent_name = "gevent%s" % str(i)
        g1 = group_gevent.spawn(mysql_connection, server_info, gevent_name)
        greenlets_dict[server_info[0]] = g1

    group_gevent.join(timeout=5)
    publish_health = False
    for ip, g in greenlets_dict.iteritems():
        if g.value:
            current_health[ip] = g.value
        else:
            current_health[ip] = 0
    print "[%s] current health is %s" %(datetime.now(), current_health)
    if not prev_health:
        print "[%s] Previous health is empty" %(datetime.now())
        prev_health = current_health
        publish_health = True
    

    prev_health = read_health_from_etcd(etcd_ip, etcd_port)
    prev_health = json.loads(prev_health)
    print "[%s] : ETCD health is %s" %(datetime.now(), prev_health)
    if current_health != prev_health:
        print "[%s] current_health and prev_health is not equal so publish" %(datetime.now())
        publish_health = True

    if publish_health:
        print "[%s] publishing current health in etcd" %(datetime.now())
        write_health_in_etcd(etcd_ip, current_health)

    prev_health = current_health
    group_gevent.kill()

def fetch_servers_from_etcd(etcd_ip, etcd_port):
    data =  etcd_helper.read_servers_info(etcd_ip, ETCD_PORT)
    nodes = data['node']
    servers = nodes["value"]
    servers_info = []
    servers = json.loads(servers)

    for info in servers:
        servers_info.append((info["ip"], info["port"], info["username"], info["password"]))
    return servers_info

 
def read_health_from_etcd(etcd_ip, etcd_port):
    data =  etcd_helper.read_health_info(etcd_ip, ETCD_PORT)
    #servers_health = json.loads(data["node"]["value"])
    servers_health = data["node"]["value"]
    return servers_health

def write_health_in_etcd(etcd_ip,  health):
    current_health = json.dumps(health)
    data =  etcd_helper.write_health_info(etcd_ip, ETCD_PORT, current_health)
    #servers_health = json.loads(data["node"]["value"])
    servers_health = data["node"]["value"]
    return servers_health
    
def main(etcd_ip):
    servers_info = fetch_servers_from_etcd(etcd_ip, ETCD_PORT)
    #parent_greenlet = gevent.spawn(check_servers_health, servers_info, etcd_ip, 1026)
    #parent_greenlet.start()
    check_servers_health(servers_info, etcd_ip, ETCD_PORT)

if __name__ == "__main__":
   etcd_ip = etcd_helper.get_etcd_info()
   if not etcd_ip:
       print "ETCD HOST not present in enviroment"
       sys.exit(1)
   while True:
       try: 
           main(etcd_ip)
           time.sleep(1)
       except Exception, ex:
           print ex
