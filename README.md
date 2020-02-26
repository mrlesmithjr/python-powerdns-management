# Python PowerDNS Management

A Pythonic method to managing [PowerDNS](http://www.powerdns.com) via API calls.

## Requirements

This is being converted to Python3 and will change over time obiously.

### Python Virtual Environment

Create a Python virtual environment to keep things clean.

```bash
python3 -m venv venv
source venv/bin/activate
```

### Usage

Install Python requirements for using the script:

```bash
pip install -r requirements.txt
```

### Development

Install development Python requirements:

```bash
pip install -r requirements-dev.txt
```

## Create a new Master Zone with info below

- Zone: dev.vagrant.local
- ZoneType: MASTER
- Master: 192.168.202.200
- Nameservers:
  - 192.168.202.200
  - 192.168.202.201
  - 192.168.202.202

```bash
python pdns.py add_zones --apihost 192.168.202.200 --zone dev.vagrant.local --zoneType MASTER --nameservers 192.168.202.200,192.168.202.201,192.168.202.202
```

## Vagrant Testing

We have included a Vagrant environment for testing and general usages. You can
spin this up by:

```bash
cd Vagrant
vagrant up
```

Once the provisioning occurs, you will have a usable Vagrant environment with
three nodes running PowerDNS. There are three in case you'd like to play with
master/slave scenarios.

When you are done testing you can tear down the Vagrant environment by:

```bash
./cleanup.sh
```

## Create the Slave Zones with the info below

- Zone: dev.vagrant.local
- ZoneType: SLAVE
- Master: 192.168.202.200
- Slaves:
  - 192.168.202.201
  - 192.168.202.202

```bash
python pdns.py add_zones --apihost 192.168.202.201 --zone dev.vagrant.local --zoneType SLAVE --masters 192.168.202.200
```

## Create Master Zones using a CSV file

Create a [examples/master_zones.csv](examples/master_zones.csv) similar to below:

```csv
zone,zoneType,masters,nameservers
128.28.172.in-addr.arpa,MASTER,,"192.168.202.200,192.168.202.201,192.168.202.202"
202.168.192.in-addr.arpa,MASTER,,"192.168.202.200,192.168.202.201,192.168.202.202"
dev.vagrant.local,MASTER,,"192.168.202.200,192.168.202.201,192.168.202.202"
prod.vagrant.local,MASTER,,"192.168.202.200,192.168.202.201,192.168.202.202"
test.vagrant.local,MASTER,,"192.168.202.200,192.168.202.201,192.168.202.202"
vagrant.local,MASTER,,"192.168.202.200,192.168.202.201,192.168.202.202"
```

The first row is the header...

Now read the csv file using CLI argument:

```bash
python pdns.py add_zones --apihost 192.168.202.200 --readcsv examples/master_zones.csv
```

## Create records with info below

- Zone: dev.vagrant.local
  - name: test01.dev.vagrant.local
  - recordType: A
  - content: 192.168.202.161
  - name: development.dev.vagrant.local
  - recordType: CNAME
  - content: test01.dev.vagrant.local

```bash
python pdns.py add_records --zone dev.vagrant.local --name test01 --content 192.168.202.161 --recordType A
```

```bash
python pdns.py add_records --zone dev.vagrant.local --name development --content test01.dev.vagrant.local --recordType CNAME
```

## Create records using a csv file

Create a [examples/add_records.csv](examples/add_records.csv) file similar
to below:

```csv
name,zone,record_type,content,disabled,ttl,set_ptr,priority
development,test.vagrant.local,A,192.168.202.3,FALSE,3600,TRUE,0
mail,vagrant.local,CNAME,smtp.vagrant.local,FALSE,3600,TRUE,0
node0,test.vagrant.local,A,192.168.202.4,FALSE,3600,TRUE,0
node1,test.vagrant.local,A,192.168.202.5,FALSE,3600,TRUE,0
node100,test.vagrant.local,A,192.168.202.100,FALSE,3600,TRUE,0
node101,test.vagrant.local,A,192.168.202.101,FALSE,3600,TRUE,0
node102,test.vagrant.local,A,192.168.202.102,FALSE,3600,TRUE,0
node2,dev.vagrant.local,A,192.168.202.201,FALSE,3600,TRUE,0
node201,dev.vagrant.local,A,192.168.202.202,FALSE,3600,TRUE,0
node202,dev.vagrant.local,A,192.168.202.203,FALSE,3600,TRUE,0
node203,dev.vagrant.local,CNAME,node201.dev.vagrant.local,FALSE,3600,TRUE,0
smtp,vagrant.local,A,192.168.202.20,FALSE,3600,TRUE,0
```

The first row is the header...

Now read the csv file using CLI argument:

```bash
python pdns.py add_records --apihost 192.168.202.200 --readcsv examples/add_records.csv
```

## Delete records with info below

- Zone: vagrant.local
  - name: smtp.vagrant.local
  - recordType: A

```bash
python pdns.py delete_records --apihost 192.168.202.200 --name smtp --zone vagrant.local --recordType A
```

## Delete records reading from a csv file

Create a [examples/delete_records.csv](examples/delete_records.csv) similar
to below:

```csv
name,zone,record_type
node100,test.vagrant.local,A
node101,test.vagrant.local,A
node202,dev.vagrant.local,A
node203,dev.vagrant.local,CNAME
```

The first row is the header...

Now read the csv file using CLI argument:

```bash
python pdns.py delete_records --apihost 192.168.202.200 --readcsv examples/delete_records.csv
```

## Query PDNS config

```bash
python pdns.py query_config --apihost 192.168.202.200
```

## Query zones

```bash
python pdns.py query_zones --apihost 192.168.202.200
```

## License

MIT

## Author Information

Larry Smith Jr.

- [@mrlesmithjr](https://www.twitter.com/mrlesmithjr)
- [EverythingShouldBeVirtual](http://everythingshouldbevirtual.com)
- [mrlesmithjr@gmail.com](mailto:mrlesmithjr@gmail.com)
