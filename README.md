A Pythonic method to managing [PowerDNS] via API calls.

Create a new Master Zone with info below:
-----------------------------------------

- Zone: dev.vagrant.local
- ZoneType: MASTER
- Master: 192.168.202.200
- Nameservers:
  - 192.168.202.200
  - 192.168.202.201
  - 192.168.202.202

````
./pdns.py add_zones --apihost 192.168.202.200 --zone dev.vagrant.local --zoneType MASTER --nameservers 192.168.202.200,192.168.202.201,192.168.202.202
````

Create the Slave Zones with the info below:
-------------------------------------------

- Zone: dev.vagrant.local
- ZoneType: SLAVE
- Master: 192.168.202.200
- Slaves:
  - 192.168.202.201
  - 192.168.202.202

````
./pdns.py add_zones --apihost 192.168.202.201 --zone dev.vagrant.local --zoneType SLAVE --masters 192.168.202.200
````

Create Master Zones using a CSV file:
-------------------------------------

Create a master_zones.csv similar to below:

````
zone,zoneType,masters,nameservers
128.28.172.in-addr.arpa,MASTER,,"192.168.202.200,192.168.202.201,192.168.202.202"
dev.vagrant.local,MASTER,,"192.168.202.200,192.168.202.201,192.168.202.202"
prod.vagrant.local,MASTER,,"192.168.202.200,192.168.202.201,192.168.202.202"
test.vagrant.local,MASTER,,"192.168.202.200,192.168.202.201,192.168.202.202"
vagrant.local,MASTER,,"192.168.202.200,192.168.202.201,192.168.202.202"
````

The first row is the header...

Now read the csv file using CLI argument:

````
./pdns.py add_zones --apihost 192.168.202.200 --readcsv master_zones.csv
````

Create records with info below:
-------------------------------

- Zone: dev.vagrant.local
  - name: test01.dev.vagrant.local
  - recordType: A
  - content: 192.168.202.161
  - name: development.dev.vagrant.local
  - recordType: CNAME
  - content: test01.dev.vagrant.local

````
./pdns.py add_records --zone dev.vagrant.local --name test01 --content 192.168.202.161 --recordType A
````
````
./pdns.py add_records --zone dev.vagrant.local --name development --content test01.dev.vagrant.local --recordType CNAME
````

Create records using a csv file:
---------------------------------------

Create a add_records.csv file similar to below:

````
name,zone,record_type,content,disabled,ttl,set_ptr,priority
development,test.vagrant.local,A,192.168.202.200,FALSE,3600,TRUE,0
node0,test.vagrant.local,A,192.168.202.201,FALSE,3600,TRUE,0
node1,test.vagrant.local,A,192.168.202.202,FALSE,3600,TRUE,0
node100,test.vagrant.local,A,192.168.202.100,FALSE,3600,TRUE,0
node101,test.vagrant.local,A,192.168.202.101,FALSE,3600,TRUE,0
node102,test.vagrant.local,A,192.168.202.102,FALSE,3600,TRUE,0
node2,dev.vagrant.local,A,192.168.202.201,FALSE,3600,TRUE,0
node201,dev.vagrant.local,A,192.168.202.202,FALSE,3600,TRUE,0
node202,dev.vagrant.local,A,192.168.202.203,FALSE,3600,TRUE,0
node203,dev.vagrant.local,CNAME,node201.dev.vagrant.local,FALSE,3600,TRUE,0
smtp,vagrant.local,A,192.168.202.20,FALSE,3600,TRUE,0
mail,vagrant.local,CNAME,smtp.vagrant.local,FALSE,3600,TRUE,0
````

The first row is the header...

Now read the csv file using CLI argument:

````
./pdns.py add_records --apihost 192.168.202.200 --readcsv add_records.csv
````

Delete records with info below:
-------------------------------

- Zone: vagrant.local
  - name: smtp.vagrant.local
  - recordType: A

````
./pdns.py delete_records --apihost 192.168.202.200 --name smtp --zone vagrant.local --recordType A
````

Delete records reading from a csv file:
---------------------------------------

Create a delete_records.csv similar to below:

````
name,zone,record_type
node100,test.vagrant.local,A
node101,test.vagrant.local,A
node202,dev.vagrant.local,A
node203,dev.vagrant.local,CNAME
````

The first row is the header...

Now read the csv file using CLI argument:

````
./pdns.py delete_records --apihost 192.168.202.200 --readcsv delete_records.csv
````

Query PDNS config
-----------------

````
./pdns.py query_config --apihost 192.168.202.200
````

Query zones
-----------

````
./pdns.py query_zones --apihost 192.168.202.200
````


[PowerDNS]: <http://www.powerdns.com>
