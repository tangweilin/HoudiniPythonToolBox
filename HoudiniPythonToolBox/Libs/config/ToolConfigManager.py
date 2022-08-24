import json
from Libs.path import ToolPathManager
from imp import reload
from PySide2 import QtCore, QtGui, QtWidgets
from Libs.utilities import ToolUtilityClasses

reload(ToolPathManager)
reload(ToolUtilityClasses)

tool_widget_utility_func = ToolUtilityClasses.SetWidgetInfo
tool_path_manager = ToolPathManager.ToolPath()
tool_error_info = ToolUtilityClasses.ExceptionInfoWidgetClass()


class ToolConfig:
    """
    This Class return current config in the config file
    """

    @classmethod
    def get_config_value_by_key(cls, config: dict, key: dict.keys) -> str:
        """
        return current config value in to specify config file
        :param config: current config
        :param key: the key of config
        :return: current value
        """
        config_value = config[key]
        return config_value

    @classmethod
    def load_json_file_info_by_path(cls, path: str) -> str:
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
    def dump_json_file_info_by_path(cls, path: str, info) -> None:
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


class QSSLoader:
    """
        Class To Load QSS
    """
    def __init__(self):
        pass

    @staticmethod
    def read_qss_file(qss_file_name):
        """
            Load QSS File By Name
        :param qss_file_name:
        :return:
        """
        with open(qss_file_name, 'r', encoding='UTF-8') as file:
            return file.read()


class ToolConfigManager(QtWidgets.QWidget):
    """
        Tool Config UI Class
    """
    def __init__(self):
        super(ToolConfigManager, self).__init__()
        self.setWindowTitle('config')
        self.setObjectName('toolconfig')
        self.setGeometry(900, 700, 600, 500)
        tool_widget_utility_func.set_widget_to_center_desktop(self)
        self.__set_ui()

    def __set_ui(self)->None:
        pass