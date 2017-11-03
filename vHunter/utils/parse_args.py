import argparse

from utils import Config


def parse_args():
    config = Config()
    descs = config.descriptions
    parser = argparse.ArgumentParser(description=descs['cli_description'])
    parser.add_argument('-a', '--stand-alone', action='store_true', help=descs['standalone_help'], default=True)
    parser.add_argument('-ms', '--master-slave', action='store_true', help=descs['master_slave_help'], default=False)
    parser.add_argument('-m', '--master', action='store_true', help=descs['master_help'], default=False)
    parser.add_argument('-s', '--slave', action='store_true', help=descs['slave_help'], default=True)
    parser.add_argument('-S', '--scenario', action='store', help=descs['scenario_help'])
    parser.add_argument('-c', '--config', action='store', help=descs['config_help'])
    parser.add_argument('-l', '--log-file', action='store', help=descs['log_file_help'])
    parser.add_argument('-L', '--log-level', action='store', help=descs['log_level_help'])
    parser.add_argument('-p', '--port', action='store', help=descs['port_help'])
    parser.add_argument('-H', '--host', action='store', help=descs['host_help'])
    parser.add_argument('--list', action='store_true', help=descs['list_scenarios_help'])

    return parser.parse_args()

