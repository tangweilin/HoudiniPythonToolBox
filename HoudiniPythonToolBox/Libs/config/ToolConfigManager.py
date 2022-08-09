import json
from Libs.path import ToolPathManager
from imp import reload
from Libs.utilities import ToolUtilityClasses
reload(ToolPathManager)
reload(ToolUtilityClasses)

tool_path_manager = ToolPathManager.ToolPath()
tool_error_info = ToolUtilityClasses.ExceptionInfoWidgetClass

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

    @classmethod
    def load_json_file_info_by_path(cls, path) -> str:
        """
            Load Json Info From File
        :param path: Json Path
        :return: Json Info
        """
        info_list = None
        try:
            with open(path, 'r') as f:
                info_list = json.load(f)
        except:
            tool_error_info.show_exception_info('warning', 'load json info got wrong file: %s' % path)
        else:
            return info_list

    @classmethod
    def dump_json_file_info_by_path(cls, path, info) -> None:
        """
            Dump Json Info To Current Json File
        :param path: Json Path
        :param info: Json Info
        """
        try:
            with open(path, 'w') as f:
                json.dump(info, f)
        except:
            tool_error_info.show_exception_info('warning', 'dump json info got wrong file: %s' % path)
