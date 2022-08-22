import hou
import json
import os
import shutil
from PySide2 import QtCore, QtGui, QtWidgets

from Libs.path import ToolPathManager
from Libs.config import ToolConfigManager
from Libs.utilities import ToolUtilityClasses
from imp import reload
from Libs.config import ScreenShotTool
from pathlib import Path

reload(ToolUtilityClasses)
reload(ToolPathManager)
reload(ScreenShotTool)
reload(ToolConfigManager)

tool_widget_utility_func = ToolUtilityClasses.SetWidgetInfo
tool_path_manager = ToolPathManager.ToolPath()
tool_error_info = ToolUtilityClasses.ExceptionInfoWidgetClass()
tool_config_manager = ToolConfigManager.ToolConfig


class SaveHdaInfo(QtWidgets.QWidget):
    def __init__(self):
        super(SaveHdaInfo, self).__init__()
        self.setWindowTitle('save hda info')
        self.setObjectName('savehdainfo')
        self.setGeometry(900, 700, 370, 250)
        tool_widget_utility_func.set_widget_to_center_desktop(self)
        self.__set_ui()

    def __get_all_hda_path(self) -> list:
        paths = []
        houdini_directory = hou.homeHoudiniDirectory()
        current_houdini_hda_path = houdini_directory + '/otls'
        if not os.path.exists(current_houdini_hda_path):
            os.mkdir(current_houdini_hda_path)
        c = hou.hda.loadedFiles()
        paths.append(current_houdini_hda_path)
        for hda_path in c:
            if hda_path.find('SideFXLabs') == -1 and hda_path.find('PROGRA~1') == -1:
                p = tool_path_manager.get_parent_path(hda_path)
                if paths.count(p) == 0:
                    paths.append(p)
        return paths

    def __set_ui(self) -> None:
        hda_main_v_layout = QtWidgets.QVBoxLayout(self)
        hda_type_h_layout = QtWidgets.QHBoxLayout()

        self.hda_file_path_combo_box = QtWidgets.QComboBox()

        all_hda_file_path = self.__get_all_hda_path()
        if all_hda_file_path:
            for p in all_hda_file_path:
                p = Path(p)  # convert windows path to str
                self.hda_file_path_combo_box.addItem(p.__str__())

        self.hda_list_widget = QtWidgets.QListWidget()
        self.hda_list_widget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.hda_target_folder_line_edit = QtWidgets.QLineEdit()
        self.hda_target_folder_line_edit.setPlaceholderText('target folder')
        self.hda_target_folder_combo_box = QtWidgets.QComboBox()

        all_hda_file = os.listdir(tool_path_manager.hda_path)
        all_hda_folder = [x for x in all_hda_file if os.path.isdir(os.path.join(tool_path_manager.hda_path, x))]
        for folder in all_hda_folder:
            self.hda_target_folder_combo_box.addItem(folder)

        self.hda_save_btn = QtWidgets.QPushButton('save')
        tool_widget_utility_func.set_widget_icon(self.hda_save_btn, 'save_node.png')

        hda_type_h_layout.addWidget(self.hda_target_folder_line_edit)
        hda_type_h_layout.addWidget(self.hda_target_folder_combo_box)
        hda_main_v_layout.addWidget(self.hda_file_path_combo_box)
        hda_main_v_layout.addWidget(self.hda_list_widget)
        hda_main_v_layout.addLayout(hda_type_h_layout)
        hda_main_v_layout.addWidget(self.hda_save_btn)

        # connect
        self.hda_file_path_combo_box.currentIndexChanged.connect(self.__change_hda_file_path)
        self.hda_target_folder_combo_box.currentIndexChanged.connect(self.__change_hda_save_folder)
        self.hda_save_btn.clicked.connect(self.__save_hda_to_tool_preset)

    def __change_hda_file_path(self) -> None:
        hda_path = self.hda_file_path_combo_box.currentText()
        hda_file = os.listdir(hda_path)
        self.hda_list_widget.clear()
        for hda in hda_file:
            if hda.endswith('.hda'):
                self.hda_list_widget.addItem(hda)

    def __change_hda_save_folder(self) -> None:
        target_folder = self.hda_target_folder_combo_box.currentText()
        self.hda_target_folder_line_edit.setText(target_folder)

    def __save_hda_to_tool_preset(self) -> None:
        current_select_items = self.hda_list_widget.selectedItems()
