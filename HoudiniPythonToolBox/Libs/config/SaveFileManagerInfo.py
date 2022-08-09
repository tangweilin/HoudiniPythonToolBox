import hou
import re
import json
import os
from Libs.path import ToolPathManager
from Libs.config import ToolConfigManager
from Libs.utilities import ToolUtilityClasses
from imp import reload
from PySide2 import QtWidgets, QtCore
from Libs.config import ScreenShotTool

reload(ToolUtilityClasses)
reload(ToolPathManager)
reload(ScreenShotTool)
reload(ToolConfigManager)

tool_widget_utility_func = ToolUtilityClasses.SetWidgetInfo
tool_path_manager = ToolPathManager.ToolPath()
tool_error_info = ToolUtilityClasses.ExceptionInfoWidgetClass()
tool_config_manager = ToolConfigManager.ToolConfig


class SaveFileManagerInfo(QtWidgets.QWidget):
    """
        Saving Current Node Preset Info To Json File
    """

    def __init__(self):
        super(SaveFileManagerInfo, self).__init__()
        self.setGeometry(1200, 1200, 370, 400)
        tool_widget_utility_func.set_widget_to_center_desktop(self)
        self.setObjectName('SaveFileManagerInfo')
        self.setWindowTitle('SaveFileManagerInfo')
        self.set_window()
        self.node = None
        self.update = False

    def set_window(self) -> None:
        """
            Setup Main UI Of SaveFileManager
        :return: None
        """
        v_layout = QtWidgets.QVBoxLayout(self)
        h_layout = QtWidgets.QHBoxLayout()
        node_name_h_layout = QtWidgets.QHBoxLayout()
        author_h_layout = QtWidgets.QHBoxLayout()
        remark_h_layout = QtWidgets.QHBoxLayout()

        self.save_btn = QtWidgets.QPushButton('save')
        self.current_btn = QtWidgets.QPushButton('current')
        self.multi_btn = QtWidgets.QPushButton('multi')
        self.reset_btn = QtWidgets.QPushButton('reset')

        tool_widget_utility_func.set_widget_icon(self.save_btn, 'save_node.png')
        tool_widget_utility_func.set_widget_icon(self.current_btn, 'current_btn.png')
        tool_widget_utility_func.set_widget_icon(self.multi_btn, 'multi_btn.png')
        tool_widget_utility_func.set_widget_icon(self.reset_btn, 'reset_node.png')

        self.save_btn.clicked.connect(self.save_file_info_to_json_file)

        v_sub_layout = QtWidgets.QVBoxLayout()

        self.project_choose_line_edit = QtWidgets.QLineEdit()
        self.project_choose_line_edit.setPlaceholderText('project name...')
        self.project_choose_combo_box = QtWidgets.QComboBox()
        self.project_choose_combo_box.currentIndexChanged.connect(self.on_project_combo_box_changed)

        self.folder_choose_line_edit = QtWidgets.QLineEdit()
        self.folder_choose_line_edit.setPlaceholderText('folder name...')
        self.folder_choose_combo_box = QtWidgets.QComboBox()
        self.folder_choose_combo_box.currentIndexChanged.connect(self.on_folder_combo_box_changed)

        self.file_type_line_edit = QtWidgets.QLineEdit()
        self.file_type_line_edit.setPlaceholderText('file type name...')
        self.file_type_choose_combo_box = QtWidgets.QComboBox()
        self.file_type_choose_combo_box.currentIndexChanged.connect(self.on_file_type_combo_box_changed)

        self.file_name_line_edit = QtWidgets.QLineEdit()
        self.file_name_line_edit.setPlaceholderText('file name...')

        self.file_dir_line_edit = QtWidgets.QLineEdit()
        self.file_dir_line_edit.setPlaceholderText('file dir...')

        self.file_remark_line_edit = QtWidgets.QLineEdit()
        self.file_remark_line_edit.setPlaceholderText('file remark...')

        file_name_label = QtWidgets.QLabel()
        tool_widget_utility_func.set_widget_label(file_name_label, 'file name:', 80, 25)

        file_name_h_layout = QtWidgets.QHBoxLayout()
        file_name_h_layout.addWidget(file_name_label)
        file_name_h_layout.addWidget(self.file_name_line_edit)

        file_dir_label = QtWidgets.QLabel()
        tool_widget_utility_func.set_widget_label(file_dir_label, 'file dir:', 80, 25)
        file_dir_h_layout = QtWidgets.QHBoxLayout()
        file_dir_h_layout.addWidget(file_dir_label)
        file_dir_h_layout.addWidget(self.file_dir_line_edit)

        file_remark_label = QtWidgets.QLabel()
        tool_widget_utility_func.set_widget_label(file_remark_label, 'file marker:', 80, 25)
        file_remark_h_layout = QtWidgets.QHBoxLayout()
        file_remark_h_layout.addWidget(file_remark_label)
        file_remark_h_layout.addWidget(self.file_remark_line_edit)

        v_sub_layout.addLayout(file_name_h_layout)
        v_sub_layout.addLayout(file_dir_h_layout)
        v_sub_layout.addLayout(file_remark_h_layout)
        v_sub_layout.addWidget(self.project_choose_line_edit)
        v_sub_layout.addWidget(self.project_choose_combo_box)
        v_sub_layout.addWidget(self.folder_choose_line_edit)
        v_sub_layout.addWidget(self.folder_choose_combo_box)
        v_sub_layout.addWidget(self.file_type_line_edit)
        v_sub_layout.addWidget(self.file_type_choose_combo_box)

        h_layout.addWidget(self.save_btn)
        h_layout.addWidget(self.current_btn)
        h_layout.addWidget(self.multi_btn)
        h_layout.addWidget(self.reset_btn)
        v_layout.addLayout(h_layout)
        v_layout.addLayout(v_sub_layout)
        v_layout.addLayout(node_name_h_layout)
        v_layout.addLayout(author_h_layout)
        v_layout.addLayout(remark_h_layout)
        self.setup_combox_value()

    def setup_combox_value(self) -> None:
        all_file_info = self.load_file_info_from_json_file()
        project_list = []
        folder_list = []
        file_type_list = []
        for info in all_file_info:
            if info:
                project_list.append(info['project_name'])
                folder_list.append(info['folder_name'])
                file_type_list.append(info['file_type'])
        project_list = list(set(project_list))
        folder_list = list(set(folder_list))
        file_type_list = list(set(file_type_list))
        for pro in project_list:
            self.project_choose_combo_box.addItem(pro)
        for f in folder_list:
            self.folder_choose_combo_box.addItem(f)
        for t in file_type_list:
            self.file_type_choose_combo_box.addItem(t)

    def on_project_combo_box_changed(self) -> None:
        self.project_choose_line_edit.setText(self.project_choose_combo_box.currentText())

    def on_folder_combo_box_changed(self) -> None:
        self.folder_choose_line_edit.setText(self.folder_choose_combo_box.currentText())

    def on_file_type_combo_box_changed(self) -> None:
        self.file_type_line_edit.setText(self.file_type_choose_combo_box.currentText())

    def save_file_info_to_json_file(self) -> None:
        path = tool_path_manager.file_manager_preset_path
        item_dict = {
            "project_name": self.project_choose_line_edit.text(),
            "folder_name": self.folder_choose_line_edit.text(),
            "file_name": self.file_name_line_edit.text(),
            "file_dir": self.file_dir_line_edit.text(),
            "file_type": self.file_type_line_edit.text(),
            "file_marker": self.file_remark_line_edit.text()
        }
        info_list = tool_config_manager.load_json_file_info_by_path(path)
        if info_list:
            info_list['file_info'].append(item_dict)
            tool_config_manager.dump_json_file_info_by_path(path=path, info=info_list)

    @classmethod
    def load_file_info_from_json_file(cls) -> list:
        path = tool_path_manager.file_manager_preset_path
        info_list = tool_config_manager.load_json_file_info_by_path(path)
        all_file_info = info_list['file_info']
        return all_file_info

