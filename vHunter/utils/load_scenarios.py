import os
from singleton_decorator import singleton
from pprint import pprint

from utils.config import Config
from utils.config import merge_yamls


@singleton
class Scenarios:
    def __init__(self):
        self.config = Config()
        self.scenarios = None
        self.load_scenarios()

    def load_scenarios(self):
        config_scenarios_dirs = self.config.scenarios_dirs
        args_scenarios_dir = self.config.args.scenarios
        scenario_files = []
        if args_scenarios_dir is not None:
            scenario_files = scenario_files + [os.path.join(args_scenarios_dir, file) for file in os.listdir(path=args_scenarios_dir)]
        for directory in config_scenarios_dirs:
            scenario_files = scenario_files + [os.path.join(directory, file) for file in os.listdir(path=directory)]

        self.scenarios = merge_yamls(scenario_files)
        pprint(self.scenarios)

    def check_scenarios_structure(self):
        for name, properties in self.scenarios.items():
            if not name.endswith('scenario'):
                raise ValueError('All scenarios have to ends its name with "scenario" suffix')
