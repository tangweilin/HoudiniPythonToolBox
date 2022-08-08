import hou
import re
import json
import os
from Libs.path import ToolPathManager
from Libs.utilities import ToolUtilityClasses
from imp import reload
from PySide2 import QtWidgets, QtCore
from Libs.config import ScreenShotTool

reload(ToolUtilityClasses)
reload(ToolPathManager)
reload(ScreenShotTool)

tool_widget_utility_func = ToolUtilityClasses.SetWidgetInfo
tool_path_manager = ToolPathManager.ToolPath()
tool_error_info = ToolUtilityClasses.ExceptionInfoWidgetClass()


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

        v_sub_layout = QtWidgets.QVBoxLayout()

        self.project_choose_line_edit = QtWidgets.QLineEdit()
        self.project_choose_line_edit.setPlaceholderText('project name...')
        self.project_choose_combo_box = QtWidgets.QComboBox()
        self.folder_choose_line_edit = QtWidgets.QLineEdit()
        self.folder_choose_line_edit.setPlaceholderText('folder name...')
        self.folder_choose_combo_box = QtWidgets.QComboBox()
        self.file_type_line_edit = QtWidgets.QLineEdit()
        self.file_type_line_edit.setPlaceholderText('file type name...')
        self.file_type_choose_combo_box = QtWidgets.QComboBox()
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