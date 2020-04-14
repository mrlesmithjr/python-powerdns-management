"""powerdns_management/cli.py"""

import argparse


def cli_args():
    """Read CLI arguments"""

    parser = argparse.ArgumentParser(description='PDNS Management...')
    parser.add_argument('action', help='Define action to take',
                        choices=['add_records', 'add_zones',
                                 'delete_records',
                                 'delete_zones', 'config',
                                 'stats', 'get_zones'])
    parser.add_argument(
        '--apikey', help='PDNS API Key', default='changeme')
    parser.add_argument('--content', help='DNS Record content')
    parser.add_argument('--disabled', help='Define if Record is disabled',
                        choices=['True', 'False'], default=False)
    parser.add_argument('--masters', help='DNS zone masters')
    parser.add_argument('--name', help='DNS record name')
    parser.add_argument('--nameservers', help='DNS nameservers for zone')
    parser.add_argument('--priority', help='Define priority', default=0)
    parser.add_argument('--query', help='Query filter to pass')
    parser.add_argument('--readcsv', help='Read input from CSV')
    parser.add_argument('--recordType', help='DNS record type',
                        choices=['A', 'AAAA', 'CNAME', 'MX', 'NS', 'PTR',
                                 'SOA', 'SRV', 'TXT'])
    parser.add_argument('--setPTR', help='Define if PTR record is created',
                        choices=['True', 'False'], default=True)
    parser.add_argument('--ttl', help='Define TTL', default=3600)
    parser.add_argument('--url', help='PDNS API Url',
                        default='http://127.0.0.1:8081/api/v1')
    parser.add_argument('--zone', help='DNS zone')
    parser.add_argument('--zoneType', help='DNS Zone Type',
                        choices=['MASTER', 'NATIVE', 'SLAVE'],
                        default='NATIVE')

    args = parser.parse_args()

    if args.action == 'add_zones' or args.action == 'delete_zones':
        if args.readcsv is None and args.zone is None:
            parser.error('--readcsv or --zone required')

    return args
