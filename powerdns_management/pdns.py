"""powerdns_management/pdns.py"""

import json
import logging
import pandas
import requests


class PDNS:
    """Main PowerDNS class"""

    def __init__(self, args):
        """Init a thing"""

        # Setup logging
        self.logger = logging.getLogger(__name__)
        # Capture CLI arguments
        self.args = args
        # Define API URL, API headers
        self.url, self.headers = self.api_call()
        # Execute CLI action
        self.actions()

    def actions(self):
        """Map CLI actions to function executions"""

        # Define action map for function mapping
        action_map = {'add_records': self.add_records,
                      'add_zones': self.add_zones,
                      'delete_records': self.delete_records,
                      'delete_zones': self.delete_zones,
                      'config': self.config,
                      'stats': self.stats,
                      'get_zones': self.get_zones}

        # Lookup action map
        action_mapping = action_map[self.args.action]
        # Execute function
        action_mapping()

    def api_call(self):
        """Setup API call"""

        # Define API headers
        headers = {'X-API-Key': self.args.apikey}
        # Define API URL
        url = f'{self.args.url}/servers/localhost'

        return url, headers

    def add_records(self):
        """Add/Create DNS records"""

    def delete_records(self):
        """Delete DNS records"""

    def canonical(self, value):
        """Return canonical name"""

        # Convert value to canonical value
        if not value.endswith('.'):
            canonical_value = f'{value}.'
        else:
            canonical_value = value

        # Log original value and canonical value
        self.logger.info('value: %s canonical_value: %s',
                         value, canonical_value)

        return canonical_value

    def add_zone(self, data):
        """Add DNS Zone"""

        # Log data passed
        self.logger.info('data: %s', data)
        # Define URL
        url = f'{self.url}/zones'
        # Execute API request
        request = requests.post(
            url, headers=self.headers, data=json.dumps(data))

        # Log request response
        self.logger.info(json.dumps(request.json()))

    def delete_zone(self, data):
        """Delete DNS Zone"""

        # Define zone ID from data passed
        zone_id = data['name']
        # Define URL
        url = f'{self.url}/zones/{zone_id}'
        # Execute API request
        request = requests.delete(url, headers=self.headers)

        # Log request response
        self.logger.info(request)

    def add_zones(self):
        """Add new DNS zones"""

        # Add zones not from CSV
        if self.args.readcsv is None:
            # Get list of DNS zone masters
            masters = self.zone_masters(self.args.masters)
            # Get list of DNS zone nameservers
            nameservers = self.zone_nameservers(self.args.nameservers)
            # Define JSON data for API call
            data = {'name': self.canonical(self.args.zone),
                    'kind': self.args.zoneType,
                    'masters': masters, 'nameservers': nameservers}

            # If zone type is master, add add'l data
            if self.args.zoneType.upper() == 'MASTER':
                data['soa_edit_api'] = 'INCEPTION-INCREMENT'

            # Add zone
            self.add_zone(data)

        # Add zones from CSV
        else:
            # Read CSV data
            csv_data = pandas.read_csv(self.args.readcsv, header=0)
            # Iterate through CSV data
            for _index, row in csv_data.iterrows():
                # Get list of DNS zone masters
                masters = self.zone_masters(row.get('masters'))
                # Get list of DNS zone nameservers
                nameservers = self.zone_nameservers(row.get('nameservers'))
                # Define JSON data for API call
                data = {'name': self.canonical(row['zone']),
                        'kind': row['zoneType'], 'masters': masters,
                        'nameservers': nameservers}

                # If zone type is master, add add'l data
                if row['zoneType'].upper() == 'MASTER':
                    data['soa_edit_api'] = 'INCEPTION-INCREMENT'

                # Add zone
                self.add_zone(data)

    def delete_zones(self):
        """Delete DNS Zones"""

        # Delete zones not from CSV
        if self.args.readcsv is None:
            # Define JSON data for API call
            data = {'name': self.canonical(self.args.zone)}

            # Delete zone
            self.delete_zone(data)

        # Delete zones from CSV
        else:
            # Read CSV data
            csv_data = pandas.read_csv(self.args.readcsv, header=0)
            # Iterate through CSV data
            for _index, row in csv_data.iterrows():
                # Define JSON data for API call
                data = {'name': self.canonical(row['zone'])}

                # Delete zone
                self.delete_zone(data)

    def zone_masters(self, data):
        """Parse zone masters"""

        # Define masters list
        masters = []
        # Only parse data if string and not null
        if data is not None and isinstance(data, str):
            for master in data.split(','):
                masters.append(self.canonical(master))

        # Log masters
        self.logger.info('masters: %s', masters)

        return masters

    def zone_nameservers(self, data):
        """Parse zone namseservers"""

        # Define nameservers list
        nameservers = []
        # Only parse data if string and not null
        if data is not None and isinstance(data, str):
            for nameserver in data.split(','):
                nameservers.append(self.canonical(nameserver))

        # Log nameservers
        self.logger.info('nameservers: %s', nameservers)

        return nameservers

    def get_zones(self):
        """Get DNS Zones"""

        # Query all zones
        if self.args.query is None:
            url = f'{self.url}/zones'

        # Query for specific zone
        else:
            url = f'{self.url}/search-data?q={self.args.query}&object_type=zone'

        # Process API request
        request = requests.get(url, headers=self.headers)

        # Print to stdout the JSON request
        print(json.dumps(request.json()))

    def config(self):
        """Query PDNS Config"""

        # Define URL
        url = f'{self.url}/config'
        # Process API request
        request = requests.get(url, headers=self.headers)

        # Print to stdout the JSON request
        print(json.dumps(request.json()))

    def stats(self):
        """Query DNS Stats"""

        # Define URL
        url = f'{self.url}/statistics'
        # Process API request
        request = requests.get(url, headers=self.headers)

        # Print to stdout the JSON request
        print(json.dumps(request.json()))
