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
    """
        Saving HDA Preset  Info To Tool Preset File
    """
    def __init__(self):
        super(SaveHdaInfo, self).__init__()
        self.setWindowTitle('save hda info')
        self.setObjectName('savehdainfo')
        self.setGeometry(900, 700, 370, 250)
        tool_widget_utility_func.set_widget_to_center_desktop(self)
        self.__set_ui()

    def __get_all_hda_path(self) -> list:
        """
            Collect All HDA Path In Current Opened Houdini Version
        :return:
        """
        paths = []
        houdini_directory = hou.homeHoudiniDirectory()
        current_houdini_hda_path = houdini_directory + '/otls'
        if not os.path.exists(current_houdini_hda_path):
            os.mkdir(current_houdini_hda_path)
        c = hou.hda.loadedFiles()
        paths.append(current_houdini_hda_path)
        for hda_path in c:
            if hda_path.find('SideFXLabs') == -1 and hda_path.find('PROGRA~1') == -1 and hda_path.find('HDAPresets') == -1:
                p = tool_path_manager.get_parent_path(hda_path)
                if paths.count(p) == 0:
                    paths.append(p)
        return paths

    def __set_ui(self) -> None:
        """
            Main UI Layout
        :return:
        """
        hda_main_v_layout = QtWidgets.QVBoxLayout(self)
        hda_type_h_layout = QtWidgets.QHBoxLayout()
        hda_marker_h_layout = QtWidgets.QHBoxLayout()
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

        marker_label = QtWidgets.QLabel()
        marker_label.setText('marker:')
        marker_label.setTextFormat(QtCore.Qt.AutoText)
        marker_label.setAlignment(QtCore.Qt.AlignCenter)
        marker_label.setFixedSize(80, 25)
        self.marker_text_line_edit = QtWidgets.QPlainTextEdit()
        self.marker_text_line_edit.setPlaceholderText('markers...')

        # hda_marker_h_layout.addWidget(marker_label)
        # hda_marker_h_layout.addWidget(self.marker_text_line_edit)

        hda_type_h_layout.addWidget(self.hda_target_folder_line_edit)
        hda_type_h_layout.addWidget(self.hda_target_folder_combo_box)
        hda_main_v_layout.addWidget(self.hda_file_path_combo_box)
        hda_main_v_layout.addWidget(self.hda_list_widget)
        hda_main_v_layout.addLayout(hda_type_h_layout)
        hda_main_v_layout.addLayout(hda_marker_h_layout)
        hda_main_v_layout.addWidget(self.hda_save_btn)

        # connect
        self.hda_file_path_combo_box.currentIndexChanged.connect(self.__change_hda_file_path)
        self.hda_target_folder_combo_box.currentIndexChanged.connect(self.__change_hda_save_folder)
        self.hda_save_btn.clicked.connect(self.__save_hda_to_tool_preset)

        self.__change_hda_save_folder()

    def __change_hda_file_path(self) -> None:
        """
            Create HDA List Widget Item By Path
        :return:
        """
        hda_path = self.hda_file_path_combo_box.currentText()
        hda_file = os.listdir(hda_path)
        self.hda_list_widget.clear()
        for hda in hda_file:
            if hda.endswith('.hda'):
                self.hda_list_widget.addItem(hda)

    def __change_hda_save_folder(self) -> None:
        """
            Change HDA Preset Save Path Type
        :return:
        """
        target_folder = self.hda_target_folder_combo_box.currentText()
        self.hda_target_folder_line_edit.setText(target_folder)

    def __save_hda_to_tool_preset(self) -> None:
        """
            Save Current Select HDA To Tool Preset File
        :return:
        """
        current_select_items = self.hda_list_widget.selectedItems()
        hda_target_folder = self.hda_target_folder_line_edit.text()
        tool_hda_path = tool_path_manager.hda_path + '/' + hda_target_folder
        if not os.path.exists(tool_hda_path):
            os.mkdir(tool_hda_path)
        tool_hda_path_files = os.listdir(tool_hda_path)
        tool_hda_files = [x for x in tool_hda_path_files if
                          x.split('.')[-1].lower() == 'hda' or x.split('.')[-1].lower() == 'otl']
        hda_source_path = self.hda_file_path_combo_box.currentText()
        if current_select_items:
            for item in current_select_items:
                hda_name = item.text()
                hda_full_path = hda_source_path + '/' + hda_name
                if hda_name in tool_hda_files:
                    result = QtWidgets.QMessageBox.warning(self, 'replace', 'tool file have same name of hda , are '
                                                                            'you want to replace?')
                    if result == QtWidgets.QMessageBox.Yes:
                        try:
                            shutil.copy(hda_full_path, tool_hda_path)
                            tool_hda_files.append(hda_name)
                            tool_error_info.show_exception_info('message', 'save hda to tool preset success')
                        except:
                            tool_error_info.show_exception_info('warning', 'copy {} hda got wrong'.format(hda_name))
                else:
                    try:
                        shutil.copy(hda_full_path, tool_hda_path)
                        tool_hda_files.append(hda_name)
                        tool_error_info.show_exception_info('message', 'save hda to tool preset success')
                    except:
                        tool_error_info.show_exception_info('warning', 'copy {} hda got wrong'.format(hda_name))
            self.close()
        else:
            tool_error_info.show_exception_info('warning', 'please select a hda to save')

    def update_hda_screen_shot(self, current_item: QtWidgets.QListWidgetItem, path_type: str) -> None:
        """
            Update HDA Screen Shot By Path
        :param current_item:    current select item
        :param path_type:    hda preset path type
        :return:    None
        """
        item_name = current_item.text()
        hda_preset_path = tool_path_manager.hda_path + '/' + path_type
        shot = ScreenShotTool.ScreenShotTool(item_name, hda_preset_path)
        shot.show()

    def closeEvent(self, event) -> None:
        """
            Set Parent To None When Window Closed
        :param event:
        """
        self.setParent(None)


class UpdateHdaMarker(QtWidgets.QWidget):
    """
        Update Current Select HDA Preset Marker Info
    """
    def __init__(self, hda_name: str, path_type: str):
        super(UpdateHdaMarker, self).__init__()
        self.setWindowTitle('update hda marker')
        self.setObjectName('updatehdamarker')
        self.setGeometry(900, 700, 300, 150)
        tool_widget_utility_func.set_widget_to_center_desktop(self)
        self.__set_ui()
        self.hda_name = hda_name
        self.path_type = path_type

    def __set_ui(self):
        """
            Main UI Layout
        :return:
        """
        main_v_layout = QtWidgets.QVBoxLayout(self)
        self.marker_label = QtWidgets.QLabel('Markers:')
        self.marker_text = QtWidgets.QPlainTextEdit()
        self.marker_text.setPlaceholderText('Markers...')
        self.marker_save_btn = QtWidgets.QPushButton('save')
        tool_widget_utility_func.set_widget_icon(self.marker_save_btn, 'save_node.png')
        main_v_layout.addWidget(self.marker_label)
        main_v_layout.addWidget(self.marker_text)
        main_v_layout.addWidget(self.marker_save_btn)

        self.marker_save_btn.clicked.connect(self.update_hda_marker_info)

    def update_hda_marker_info(self):
        """
            Update Marker Info By Path
        """
        hda_preset_path = tool_path_manager.hda_path + '/' + self.path_type + '/' + self.hda_name + '.json'
        with open(hda_preset_path, 'w') as f:
            json.dump(self.marker_text.toPlainText(), f)
        tool_error_info.show_exception_info('message', 'update info success')
        self.close()

    def closeEvent(self, event) -> None:
        """
            Set Parent To None When Window Closed
        :param event:
        """
        self.setParent(None)
