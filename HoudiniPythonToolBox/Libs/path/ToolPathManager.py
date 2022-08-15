import sys
import os
from pathlib import Path


class ToolPath:
    """
    This class return paths about this tool
    """

    def __init__(self):
        self.__env_path = os.getenv('TOOLBOX')
        self.__tool_path = self.__env_path + '/Libs'
        self.__icon_path = self.__env_path + '/Icons'
        self.__config_path = self.__env_path + '/Config/tool_config.json'
        self.__code_preset_path = self.__env_path + '/Presets/CodePresets'
        self.__node_preset_path = self.__env_path + '/Presets/NodePresets'
        self.__common_tools_path = self.__env_path + '/Presets/CommonTools'
        self.__common_tools_btn_name_list_path = self.__common_tools_path + '/common_tool_btn_name_list.json'
        self.__vex_code_folder_path = self.__code_preset_path + '/VexCode'
        self.__python_code_folder_path = self.__code_preset_path + '/PythonCode'
        self.__hda_path = self.__env_path + '/Presets/HDAPresets'
        self.__vex_function_path = self.__vex_code_folder_path + '/VexFunctions'
        self.__vex_codes_path = self.__vex_code_folder_path + '/VexCodes'
        self.__vex_expression_path = self.__vex_code_folder_path + '/VexExpressions'
        self.__python_codes_path = self.__python_code_folder_path + '/PythonCodes'
        self.__vex_text_path = self.__vex_code_folder_path + '/VexText'
        self.__tool_file_manager_preset_path = self.__env_path + '/Config/file_preset.json'

    @property
    def env_path(self) -> str:
        """
        ToolPathManager
        :return: return current tool path
        """
        return self.__env_path

    @property
    def tool_path(self) -> str:
        """
        ToolPathManager
        :return: return current code path
        """
        return self.__tool_path

    @property
    def icon_path(self) -> str:
        """
        ToolPathManager
        :return: return current icon path
        """
        return self.__icon_path

    @property
    def config_path(self) -> str:
        """
        ToolPathManager
        :return: return current tool config path
        """
        return self.__config_path

    @property
    def code_preset_path(self) -> str:
        """
        ToolPathManager
        :return:  return code preset folder path
        """
        return self.__code_preset_path

    @property
    def node_preset_path(self) -> str:
        """
        ToolPathManager
        :return:  return node preset folder path
        """
        return self.__node_preset_path

    @property
    def common_tools_path(self) -> str:
        """
        ToolPathManager
        :return:  return common tool preset folder path
        """
        return self.__common_tools_path

    @property
    def common_tools_btn_name_list_path(self) -> str:
        """
        ToolPathManager
        :return:  return common tool btn list path
        """
        return self.__common_tools_btn_name_list_path

    @property
    def vex_node_preset_folder_path(self) -> str:
        """
        ToolPathManager
        :return:  return vex node preset folder path
        """
        return self.__vex_code_folder_path

    @property
    def python_node_preset_folder_path(self) -> str:
        """
        ToolPathManager
        :return:  return python node preset folder path
        """
        return self.__python_code_folder_path

    @property
    def hda_path(self) -> str:
        """
        ToolPathManager
        :return: return HDA preset folder path
        """
        return self.__hda_path

    @property
    def vex_function_path(self) -> str:
        """
        ToolPathManager
        :return: return Vex Functions preset folder path
        """
        return self.__vex_function_path

    @property
    def vex_codes_path(self) -> str:
        """
        ToolPathManager
        :return: return Vex Codes preset folder path
        """
        return self.__vex_codes_path

    @property
    def vex_expression_path(self) -> str:
        """
        ToolPathManager
        :return: return Vex Expressions preset folder path
        """
        return self.__vex_expression_path

    @property
    def python_codes_path(self) -> str:
        """
        ToolPathManager
        :return: return Python Codes preset folder path
        """
        return self.__python_codes_path

    @property
    def vex_text_path(self) -> str:
        """
        ToolPathManager
        :return: return Vex Texts preset folder path
        """
        return self.__vex_text_path

    @property
    def file_manager_preset_path(self) -> str:
        """
        ToolPathManager
        :return: return File Manager Preset Json path
        """
        return self.__tool_file_manager_preset_path

    @classmethod
    def get_node_path_with_prefix(cls, path: str, node_type: str) -> str:
        """
            Get Node Path Name With Specify Prefix
        :param path: Node Path
        :param node_type: Node Class Name
        :return: Node Path With Prefix
        """
        if path:
            if node_type:
                if node_type != 'obj':
                    result_path = path + '/class_' + node_type
                else:
                    result_path = path
                return result_path

    @classmethod
    def get_dir_by_dialog_window(cls) -> str:
        pass

    @classmethod
    def get_path_file_name(cls, path: str) -> str:
        path_str = Path(path)
        path_file_name = path_str.name
        return path_file_name

    @classmethod
    def get_parent_path(cls, path: str) -> Path:
        path_str = Path(path)
        path_parent_path = path_str.parent
        return path_parent_path

    @classmethod
    def get_file_suffix(cls, path: str) -> str:
        path_str = Path(path)
        path_suffix = path_str.suffix
        return path_suffix

    @classmethod
    def change_file_suffix(cls, path: str, suffix: str) -> Path:
        path_str = Path(path)
        path_suffix = path_str.with_suffix(suffix)
        return path_suffix

    @classmethod
    def join_file_path(cls, path: str, file_name: str) -> Path:
        path_str = Path(path)
        path_str_join = path_str.joinpath(file_name)
        return path_str_join
