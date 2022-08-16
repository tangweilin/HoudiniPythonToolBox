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
        self.select_dir = None
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
        self.current_btn.clicked.connect(self.get_current_file_info)
        self.multi_btn.clicked.connect(self.save_multi_file_info)
        self.reset_btn.clicked.connect(self.reset_ui_preset_info)

        v_sub_layout = QtWidgets.QVBoxLayout()

        project_h_layout = QtWidgets.QHBoxLayout()
        folder_h_layout = QtWidgets.QHBoxLayout()
        type_h_layout = QtWidgets.QHBoxLayout()

        project_choose_label = QtWidgets.QLabel('project_name:')
        self.project_choose_line_edit = QtWidgets.QLineEdit()
        self.project_choose_line_edit.setPlaceholderText('project name...')
        self.project_choose_combo_box = QtWidgets.QComboBox()
        self.project_choose_combo_box.currentIndexChanged.connect(self.on_project_combo_box_changed)

        folder_choose_label = QtWidgets.QLabel('folders_name:')
        self.folder_choose_line_edit = QtWidgets.QLineEdit()
        self.folder_choose_line_edit.setPlaceholderText('folder name...')
        self.folder_choose_combo_box = QtWidgets.QComboBox()
        self.folder_choose_combo_box.currentIndexChanged.connect(self.on_folder_combo_box_changed)

        file_type_label = QtWidgets.QLabel('file_extension:')
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

        # layout
        v_sub_layout.addLayout(file_name_h_layout)
        v_sub_layout.addLayout(file_dir_h_layout)
        v_sub_layout.addLayout(file_remark_h_layout)

        project_h_layout.addWidget(project_choose_label)
        project_h_layout.addWidget(self.project_choose_line_edit)
        v_sub_layout.addLayout(project_h_layout)
        v_sub_layout.addWidget(self.project_choose_combo_box)

        folder_h_layout.addWidget(folder_choose_label)
        folder_h_layout.addWidget(self.folder_choose_line_edit)
        v_sub_layout.addLayout(folder_h_layout)
        v_sub_layout.addWidget(self.folder_choose_combo_box)

        type_h_layout.addWidget(file_type_label)
        type_h_layout.addWidget(self.file_type_line_edit)
        v_sub_layout.addLayout(type_h_layout)
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
        self.setup_combo_box_value()

    def setup_combo_box_value(self) -> None:
        """
            Set Up Combo Box Preset Text By Json Info
        """
        all_info_list = self.load_file_info_from_json_file()
        project_list = []
        folder_list = []
        file_type_list = []
        for info in all_info_list:
            project_list.append(info['project_name'])
            for folder in info['folder']:
                folder_list.append(folder['folder_name'])
                file_info = folder['file_info']
                for i in range(0, len(file_info['file_name'])):
                    file_type_list.append(folder['file_info']['file_type'][i])
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
        """
            Set Up Project Name
        """
        self.project_choose_line_edit.setText(self.project_choose_combo_box.currentText())

    def on_folder_combo_box_changed(self) -> None:
        """
            Set Up Folder Name
        """
        self.folder_choose_line_edit.setText(self.folder_choose_combo_box.currentText())

    def on_file_type_combo_box_changed(self) -> None:
        """
            Set Up File Extension
        """
        self.file_type_line_edit.setText(self.file_type_choose_combo_box.currentText())

    def save_file_info_to_json_file(self) -> None:
        """
            Save Current File Info To Json File
        :return:
        """
        path = tool_path_manager.file_manager_preset_path

        # Current File Info Dict
        file_info_dict = {
            'file_name': [self.file_name_line_edit.text()],
            'file_dir': [self.file_dir_line_edit.text()],
            'file_type': [self.file_type_line_edit.text()],
            'file_marker': [self.file_remark_line_edit.text()]
        }
        folder_name_dict = {'folder_name': self.folder_choose_line_edit.text(), 'file_info': file_info_dict}
        folder_dict = [folder_name_dict]
        project_dict = {'project_name': self.project_choose_line_edit.text(), 'folder': folder_dict}
        info_list = tool_config_manager.load_json_file_info_by_path(path)
        need_add_project_flag = True
        need_add_project_folder_flag = True
        for info in info_list['project']:
            if info['project_name'] == self.project_choose_line_edit.text():
                need_add_project_flag = False
                for folder in info['folder']:
                    if folder['folder_name'] == self.folder_choose_line_edit.text():
                        need_add_project_folder_flag = False
                        file_info = folder['file_info']
                        for i in range(0, len(file_info['file_name'])):
                            if file_info['file_name'][i] == self.file_name_line_edit.text():
                                result = QtWidgets.QMessageBox.warning(self, "replace",
                                                                       "have same name file ,"
                                                                       " are you sure to replace?",
                                                                       QtWidgets.QMessageBox.Yes |
                                                                       QtWidgets.QMessageBox.No)
                                if result == QtWidgets.QMessageBox.Yes:
                                    file_info['file_name'][i] = self.file_name_line_edit.text()
                                    file_info['file_dir'][i] = self.file_dir_line_edit.text()
                                    file_info['file_type'][i] = self.file_type_line_edit.text()
                                    file_info['file_marker'][i] = self.file_remark_line_edit.text()
                                    tool_config_manager.dump_json_file_info_by_path(path=path, info=info_list)
                                    return
                                else:
                                    return

                        file_info['file_name'].append(self.file_name_line_edit.text())
                        file_info['file_dir'].append(self.file_dir_line_edit.text())
                        file_info['file_type'].append(self.file_type_line_edit.text())
                        file_info['file_marker'].append(self.file_remark_line_edit.text())

        if need_add_project_folder_flag:
            for info in info_list['project']:
                if info['project_name'] == self.project_choose_line_edit.text():
                    info['folder'].append(folder_name_dict)
        if need_add_project_flag:
            info_list['project'].append(project_dict)

        tool_config_manager.dump_json_file_info_by_path(path=path, info=info_list)

    def get_current_file_info(self) -> None:
        """
            Dump Current File Info To UI Preset
        """
        file_name = hou.hipFile.name()
        file_path = hou.hipFile.path()
        self.file_type_line_edit.setText('.hip')
        self.file_name_line_edit.setText(file_name)
        self.file_dir_line_edit.setText(file_path)
        self.on_project_combo_box_changed()
        self.on_file_type_combo_box_changed()
        self.on_folder_combo_box_changed()

    def save_multi_file_info(self) -> None:
        """
            Save Multi File Info To Json File
        """
        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
        file_dialog.setFilter(QtCore.QDir.Files)
        dir_temp = 'D:\Git_Project\HoudiniPythonToolBox\HoudiniPythonToolBox\Config'
        self.select_dir, _ = file_dialog.getOpenFileNames(caption='choose files', dir=dir_temp)
        if self.select_dir:
            if len(self.project_choose_line_edit.text()) == 0:
                tool_error_info.show_exception_info('error', 'please choose or type project name')
            else:
                result = QtWidgets.QMessageBox.warning(self, "warning",
                                                       "Use Current Folder Preset?",
                                                       QtWidgets.QMessageBox.Yes |
                                                       QtWidgets.QMessageBox.No)
                if result == QtWidgets.QMessageBox.Yes:
                    if len(self.folder_choose_line_edit.text()) == 0:
                        tool_error_info.show_exception_info('error', 'The Current Folder Preset Is None')
                        print(len(self.select_dir))
                    for path in self.select_dir:
                        file_name = tool_path_manager.get_path_file_name(path)
                        file_dir = tool_path_manager.get_parent_path(path)
                        file_type = tool_path_manager.get_file_suffix(path)
                        self.file_type_line_edit.setText(file_type)
                        self.file_name_line_edit.setText(file_name)
                        self.file_dir_line_edit.setText(str(file_dir))
                        self.save_file_info_to_json_file()

    def reset_ui_preset_info(self) -> None:
        """
            Set UI Preset Info To ''
        """
        self.file_type_line_edit.setText('')
        self.file_name_line_edit.setText('')
        self.file_dir_line_edit.setText('')
        self.file_remark_line_edit.setText('')
        self.project_choose_line_edit.setText('')
        self.folder_choose_line_edit.setText('')

    def update_current_index_info(self, project_name: str, folder_name: str, file_name: str, file_type: str,
                                  file_dir: str, file_marker: str) -> None:
        """
            Set Info To UI Preset To Update
        :param project_name: File Belongs To Which Project
        :param folder_name: File Belongs To Which Folder
        :param file_name: File Name
        :param file_type: File Extension
        :param file_dir: File Dir
        :param file_marker: File Marker
        """
        self.project_choose_line_edit.setText(project_name)
        self.folder_choose_line_edit.setText(folder_name)
        self.file_name_line_edit.setText(file_name)
        self.file_name_line_edit.setReadOnly(True)
        self.file_type_line_edit.setText(file_type)
        self.file_dir_line_edit.setText(file_dir)
        self.file_remark_line_edit.setText(file_marker)

    def delete_current_index_info(self, project_name: str,
                                  folder_name: str,
                                  file_name: str,
                                  delete_folder: bool = False,
                                  delete_project: bool = False) -> None:
        """
            Delete Current File Info From Json File
        :param delete_folder:  Forced To Delete Folder And Folder Children
        :param delete_project:  Forced To Delete Project And Project Children
        :param project_name: File Belongs To Which Project
        :param folder_name: File Belongs To Which Folder
        :param file_name: File Name
        :param file_dir: File Dir
        """
        path = tool_path_manager.file_manager_preset_path
        info_list = tool_config_manager.load_json_file_info_by_path(path)
        if delete_project:
            if project_name:
                for i in range(0, len(info_list['project'])):

                    if info_list['project'][i]['project_name'] == project_name:
                        info_list['project'].pop(i)
                        break

        elif delete_folder:
            if folder_name:
                for info in info_list['project']:
                    if info['project_name'] == project_name:
                        for i in range(0, len(info['folder'])):
                            if info['folder'][i]['folder_name'] == folder_name:
                                info['folder'].pop(i)
                                break
        else:
            if file_name:
                for info in info_list['project']:
                    if info['project_name'] == project_name:
                        for folder in info['folder']:
                            if folder['folder_name'] == folder_name:
                                file_info = folder['file_info']
                                for i in range(0, len(file_info['file_name'])):
                                    if file_info['file_name'][i] == file_name:
                                        file_info['file_name'].pop(i)
                                        file_info['file_dir'].pop(i)
                                        file_info['file_type'].pop(i)
                                        file_info['file_marker'].pop(i)
        tool_config_manager.dump_json_file_info_by_path(path=path, info=info_list)

    @classmethod
    def load_file_info_from_json_file(cls) -> str:
        """
            Load File Json Info
        :return:
        """
        path = tool_path_manager.file_manager_preset_path
        info_list = tool_config_manager.load_json_file_info_by_path(path)
        all_file_info = info_list['project']
        return all_file_info
