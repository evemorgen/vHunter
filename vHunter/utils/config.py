import yaml

from yamlcfg import YamlConfig
from singleton_decorator import singleton


def merge_yamls(paths):
    result_dict = {}
    for doc in paths:
        stream = open(doc, 'r')
        loaded_dict = yaml.load(stream)
        result_dict = {**result_dict, **loaded_dict}
        stream.close()
    return result_dict


@singleton
class Config(YamlConfig):
    def __init__(self, *args, **kwargs):
        self.merge_configs(['./conf/settings.yaml', './conf/constants.yaml'])
        kwargs['path'] = "./conf/merged.yaml"
        super().__init__(*args, **kwargs)

    def merge_configs(self, paths):
        result_dict = merge_yamls(paths)
        result_file = open('./conf/merged.yaml', 'w')
        yaml.dump(result_dict, result_file)

    def set_args(self, args):
        self.args = args

    def __getattr__(self, key):
        value = super().__getattr__(key)
        if value is None:
            raise ValueError("No such key in config: {}".format(key))
        return value
