A Pythonic method to managing [PowerDNS] via API calls.

Create a new Master Zone with info below:
-----------------------------------------

- Zone: dev.vagrant.local
- ZoneType: MASTER
- Master: 172.28.128.3
- Nameservers:
  - 172.28.128.3
  - 172.28.128.4
  - 172.28.128.5

````
./pdns.py add_zones --apihost 172.28.128.3 --zone dev.vagrant.local --zoneType MASTER --nameservers 172.28.128.3,172.28.128.4,172.28.128.5
````

Create the Slave Zones with the info below:
-------------------------------------------

- Zone: dev.vagrant.local
- ZoneType: SLAVE
- Master: 172.28.128.3
- Slaves:
  - 172.28.128.4
  - 172.28.128.5

````
./pdns.py add_zones --apihost 172.28.128.4 --zone dev.vagrant.local --zoneType SLAVE --masters 172.28.128.3
````

Create Master Zones using a CSV file:
-------------------------------------

Create a master_zones.csv similar to below:

````
zone,zoneType,masters,nameservers
128.28.172.in-addr.arpa,MASTER,,"172.28.128.3,172.28.128.4,172.28.128.5"
dev.vagrant.local,MASTER,,"172.28.128.3,172.28.128.4,172.28.128.5"
prod.vagrant.local,MASTER,,"172.28.128.3,172.28.128.4,172.28.128.5"
test.vagrant.local,MASTER,,"172.28.128.3,172.28.128.4,172.28.128.5"
vagrant.local,MASTER,,"172.28.128.3,172.28.128.4,172.28.128.5"
````

The first row is the header...

Now read the csv file using CLI argument:

````
./pdns.py add_zones --apihost 172.28.128.3 --readcsv master_zones.csv
````

Create records with info below:
-------------------------------

- Zone: dev.vagrant.local
  - name: test01.dev.vagrant.local
  - recordType: A
  - content: 172.28.128.161
  - name: development.dev.vagrant.local
  - recordType: CNAME
  - content: test01.dev.vagrant.local

````
./pdns.py add_records --zone dev.vagrant.local --name test01 --content 172.28.128.161 --recordType A
````
````
./pdns.py add_records --zone dev.vagrant.local --name development --content test01.dev.vagrant.local --recordType CNAME
````

Create records using a csv file:
---------------------------------------

Create a add_records.csv file similar to below:

````
name,zone,record_type,content,disabled,ttl,set_ptr,priority
development,test.vagrant.local,A,172.28.128.3,FALSE,3600,TRUE,0
node0,test.vagrant.local,A,172.28.128.4,FALSE,3600,TRUE,0
node1,test.vagrant.local,A,172.28.128.5,FALSE,3600,TRUE,0
node100,test.vagrant.local,A,172.28.128.100,FALSE,3600,TRUE,0
node101,test.vagrant.local,A,172.28.128.101,FALSE,3600,TRUE,0
node102,test.vagrant.local,A,172.28.128.102,FALSE,3600,TRUE,0
node2,dev.vagrant.local,A,172.28.128.201,FALSE,3600,TRUE,0
node201,dev.vagrant.local,A,172.28.128.202,FALSE,3600,TRUE,0
node202,dev.vagrant.local,A,172.28.128.203,FALSE,3600,TRUE,0
node203,dev.vagrant.local,CNAME,node201.dev.vagrant.local,FALSE,3600,TRUE,0
smtp,vagrant.local,A,172.28.128.20,FALSE,3600,TRUE,0
mail,vagrant.local,CNAME,smtp.vagrant.local,FALSE,3600,TRUE,0
````

The first row is the header...

Now read the csv file using CLI argument:

````
./pdns.py add_records --apihost 172.28.128.3 --readcsv add_records.csv
````

Delete records with info below:
-------------------------------

- Zone: vagrant.local
  - name: smtp.vagrant.local
  - recordType: A

````
./pdns.py delete_records --apihost 172.28.128.3 --name smtp --zone vagrant.local --recordType A
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
./pdns.py delete_records --apihost 172.28.128.3 --readcsv delete_records.csv
````

Query PDNS config
-----------------

````
./pdns.py query_config --apihost 172.28.128.3
````

Query zones
-----------

````
./pdns.py query_zones --apihost 172.28.128.3
````


[PowerDNS]: <http://www.powerdns.com>
