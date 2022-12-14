import sys
import os


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
        self.__vex_code_folder_path = self.__code_preset_path + '/VexCode'
        self.__python_code_folder_path = self.__code_preset_path + '/PythonCode'
        self.__hda_path = self.__env_path + '/Presets/HDAPresets'
        self.__vex_function_path = self.__vex_code_folder_path + '/VexFunctions'
        self.__vex_codes_path = self.__vex_code_folder_path + '/VexCodes'
        self.__vex_expression_path = self.__vex_code_folder_path + '/VexExpressions'
        self.__python_codes_path = self.__python_code_folder_path + '/PythonCodes'
        self.__vex_text_path = self.__vex_code_folder_path + '/VexText'

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

    @classmethod
    def get_node_path_with_prefix(cls, path, node_type) -> str:
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




