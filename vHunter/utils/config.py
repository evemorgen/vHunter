from yamlcfg import YamlConfig
from singleton_decorator import singleton

@singleton
class Config(YamlConfig):
    def __init__(self, *args, **kwargs):
        kwargs['path'] = "./conf/settings.yaml"
        super().__init__(*args, **kwargs)

    def __getattr__(self, key):
        value = super().__getattr__(key)
        if value is None:
            raise ValueError("No such key in config: {}".format(key))
        return value

