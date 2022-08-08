import json
from Libs.path import ToolPathManager
from imp import reload

reload(ToolPathManager)

tool_path_manager = ToolPathManager.ToolPath()


class ToolConfig:
    """
    This Class return current config in the config file
    """

    @classmethod
    def get_config_value_by_key(cls, config, key) -> str:
        """
        return current config value in to specify config file
        :param config: current config
        :param key: the key of config
        :return: current value
        """
        config_value = config[key]
        return config_value
