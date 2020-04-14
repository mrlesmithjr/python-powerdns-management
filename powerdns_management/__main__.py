"""powerdns_management/__main__.py"""

from powerdns_management.cli import cli_args
from powerdns_management.logger import setup_logger
from powerdns_management.pdns import PDNS


def main():
    """Main execution of package."""

    args = cli_args()

    # Setup root logger
    setup_logger()

    PDNS(args)


if __name__ == '__main__':
    main()
