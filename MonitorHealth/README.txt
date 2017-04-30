yum install python-setuptools
yum install python-devel
yum install libevent-devel


 curl http://10.0.1.149:1026/v2/keys/DB_SERVERS -XPUT -d

 value="[{"ip":"customer-db.marathon.l4lb.thisdcos.directory", "port":3306, "username": "root", "password": "123456"}]"


 curl http://10.0.1.149:1026/v2/keys/DB_SERVERS_HEALTH -XPUT -d

 value='{"customer-db.marathon.l4lb.thisdcos.directory":0}'

TODO:

1. License required for this container
2. ETCD DNS IP and Port is required
