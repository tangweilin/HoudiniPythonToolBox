import json
import os
from imp import reload

import hou
from PySide2 import QtWidgets

from Libs.path import ToolPathManager
from Libs.utilities import ToolUtilityClasses
from typing import List

reload(ToolUtilityClasses)
reload(ToolPathManager)

tool_widget_utility_func = ToolUtilityClasses.SetWidgetInfo
tool_path_manager = ToolPathManager.ToolPath()
tool_error_info = ToolUtilityClasses.ExceptionInfoWidgetClass()


class SaveVexPyNodeInfo(QtWidgets.QWidget):
    """
        Managing Code Info With Json File
    """

    def __init__(self):
        super(SaveVexPyNodeInfo, self).__init__()

        self.setGeometry(1200, 1200, 370, 250)
        tool_widget_utility_func.set_widget_to_center_desktop(self)
        self.setObjectName('SaveVexPyNodeInfo')
        self.setWindowTitle('SaveVexPyNodeInfo')
        self.set_window()
        self.node = None
        self.update_flag = False
        self.old_json_name = ''
        self.need_del = False

    def set_window(self) -> None:
        """
            To Show The UI Of SaveVexPyNodeInfo Window
        :return: None
        """
        v_layout = QtWidgets.QVBoxLayout(self)
        h_layout = QtWidgets.QHBoxLayout()
        sub_h_layout = QtWidgets.QHBoxLayout()
        code_tag_h_layout = QtWidgets.QHBoxLayout()
        code_name_h_layout = QtWidgets.QHBoxLayout()

        self.save_btn = QtWidgets.QPushButton('save')
        self.reset_btn = QtWidgets.QPushButton('reset')
        tool_widget_utility_func.set_widget_icon(self.save_btn, 'save_node.png')
        self.save_btn.clicked.connect(self.save_node_info)
        tool_widget_utility_func.set_widget_icon(self.reset_btn, 'reset_node.png')
        self.reset_btn.clicked.connect(self.reset_node_info)
        self.code_type_choose_combo_box = QtWidgets.QComboBox()
        self.code_type_choose_combo_box.addItem('vex')
        self.code_type_choose_combo_box.addItem('python')

        self.code_tag_choose_combo_box = QtWidgets.QComboBox()
        self.code_tag_multi_check_box = QtWidgets.QCheckBox('Multi Tags')
        tag_list = self.get_all_code_tag_list()
        if tag_list:
            for tag in tag_list:
                self.code_tag_choose_combo_box.addItem(tag)

        self.code_tag_label = QtWidgets.QLabel('Code  Tags:')
        self.code_tag_line_edit = QtWidgets.QLineEdit()
        self.code_tag_line_edit.setPlaceholderText('Code Tag')
        self.code_name_label = QtWidgets.QLabel('CodeName:')
        self.code_name_line_edit = QtWidgets.QLineEdit()
        self.code_name_line_edit.setPlaceholderText('Code name')
        self.code_name_line_edit.textChanged.connect(self.code_name_changed)
        self.code_text_line_edit = QtWidgets.QPlainTextEdit()
        self.code_text_line_edit.setPlaceholderText('vex or python code...')

        h_layout.addWidget(self.save_btn)
        h_layout.addWidget(self.reset_btn)
        sub_h_layout.addWidget(self.code_type_choose_combo_box)
        sub_h_layout.addWidget(self.code_tag_choose_combo_box)
        sub_h_layout.addWidget(self.code_tag_multi_check_box)
        code_tag_h_layout.addWidget(self.code_tag_label)
        code_tag_h_layout.addWidget(self.code_tag_line_edit)
        code_name_h_layout.addWidget(self.code_name_label)
        code_name_h_layout.addWidget(self.code_name_line_edit)

        v_layout.addLayout(h_layout)
        v_layout.addLayout(sub_h_layout)
        v_layout.addLayout(code_tag_h_layout)
        v_layout.addLayout(code_name_h_layout)
        v_layout.addWidget(self.code_text_line_edit)

        self.code_tag_choose_combo_box.currentIndexChanged.connect(self.on_code_tag_combo_box_changed)
        self.on_code_tag_combo_box_changed()

    def code_name_changed(self) -> None:
        """
            If Code Name Changed  Blame New Name And Old Name To Decide Need Delete Old Json File
        """
        if self.update_flag and self.old_json_name:
            self.need_del = self.old_json_name is not self.code_name_line_edit.text()

    def get_all_code_tag_list(self) -> List[str]:
        """
            Get All Code Tag List By Json File Info
        :return:
        """
        code_preset_info_path = tool_path_manager.code_preset_path + '/CodePresetsInfo.json'
        tag_list = []
        if os.path.exists(code_preset_info_path):
            with open(code_preset_info_path, 'r') as f:
                tag_info = json.load(f)
        try:
            tag_list = tag_info['tag']
        except:
            tag_list = []
        return tag_list

    def on_code_tag_combo_box_changed(self) -> None:
        """
            Set Current Select Tag
        """
        if self.code_tag_multi_check_box.isChecked():
            current_tag_text = self.code_tag_line_edit.text()
            combo_text = self.code_tag_choose_combo_box.currentText()
            if combo_text not in current_tag_text:
                result_tag_text = current_tag_text + ' , ' + combo_text
            self.code_tag_line_edit.setText(result_tag_text)
        else:
            self.code_tag_line_edit.setText(self.code_tag_choose_combo_box.currentText())

    def reset_node_info(self) -> None:
        """
            Reset Info On Window
        :return: None
        """
        nodes = list(hou.selectedNodes())
        if nodes:
            node = nodes[0]
            codes_name = node.name()
            codes = ''
            self.code_name_line_edit.setText(codes_name)

            if node.type().name() == 'attribwrangle':
                codes = node.parm('snippet').rawValue()
                self.code_type_choose_combo_box.setCurrentIndex(0)

            elif node.type().name() == 'python':
                codes = node.parm('python').rawValue()
                self.code_type_choose_combo_box.setCurrentIndex(1)

            self.code_text_line_edit.setPlainText(codes)
            self.code_tag_choose_combo_box.setCurrentText('root')
            if not self.code_tag_multi_check_box.isChecked():
                self.code_tag_line_edit.setText('root')
        else:
            self.code_name_line_edit.setText('')
            self.code_text_line_edit.setPlainText('')
            self.code_tag_choose_combo_box.setCurrentText('root')
            if not self.code_tag_multi_check_box.isChecked():
                self.code_tag_line_edit.setText('root')

    def save_tag_to_json_info(self, tags: str) -> None:
        """
            Save Current Tag Dict To Json File
        :param tags: Current Tag List
        """
        tag_list = self.get_all_code_tag_list()
        if tag_list:
            for tag in tags:
                if tag not in tag_list:
                    code_preset_info_path = tool_path_manager.code_preset_path + '/CodePresetsInfo.json'
                    with open(code_preset_info_path, 'r') as f:
                        tag_info = json.load(f)
                    json_tag_list = tag_info['tag']
                    json_tag_list.append(tag)
                    json_tag_dict = {"tag": json_tag_list}
                    with open(code_preset_info_path, 'w') as f:
                        json.dump(json_tag_dict, f)

    def del_old_json(self) -> None:
        """
            If New Update Json Name Is Not Equal Old Name, Delete Old Json
        """
        if self.need_del and self.update_flag and self.old_json_name:
            code_type_index = self.code_type_choose_combo_box.currentIndex()
            if code_type_index == 0:
                code_path = tool_path_manager.vex_codes_path
            else:
                code_path = tool_path_manager.python_codes_path
            all_files = os.listdir(code_path)
            code_files = [x for x in all_files if x.split('.')[-1].lower() == 'json']
            if self.old_json_name + '.json' in code_files:
                old_json_path = code_path + '/' + self.old_json_name + '.json'
                os.remove(old_json_path)

    def save_node_info(self) -> None:
        """
            Copy Code Text Which In TextBox Or Selected Node To Code Preset Config
        :return: None
        """
        node_code_text_info = self.code_text_line_edit.toPlainText()
        node_code_name_info = self.code_name_line_edit.text()
        code_type_index = self.code_type_choose_combo_box.currentIndex()
        code_tag_tex = self.code_tag_line_edit.text()
        if code_tag_tex.find('root') == -1:
            code_tag_tex = code_tag_tex + ' , ' + 'root'
        code_tag_without_space = code_tag_tex.replace(' ', '')
        if code_tag_without_space == '':
            code_tag_without_space = 'root'

        code_tag = []
        for tag in code_tag_without_space.split(','):
            if len(tag) != 0:
                code_tag.append(tag)
        code_path = None
        run_over_class = 2
        if node_code_name_info:
            current_node = self.get_select_node()
            # if select houdini code node
            if current_node:
                current_node_name = current_node.type().name()
                self.code_type_choose_combo_box.currentIndex()

                # if select python node
                if current_node_name == 'python':
                    codes = current_node.parm('python').rawValue()
                    run_over_class = current_node.parm('class').eval()
                    # if select node have code text
                    if codes:
                        code_info_dict = {
                            "tag": code_tag,
                            "class": run_over_class,
                            "info": codes
                        }
                        code_path = tool_path_manager.python_codes_path
                        all_files = os.listdir(code_path)
                        code_files = [x for x in all_files if x.split('.')[-1].lower() == 'json']

                        # replace
                        if node_code_name_info + '.json' in code_files:
                            replace_result = QtWidgets.QMessageBox.warning(self,
                                                                           'Replacing',
                                                                           'have same name node, are you sure to replace?',
                                                                           QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                            if replace_result == QtWidgets.QMessageBox.Yes:
                                with open(code_path + '/' + node_code_name_info + '.json', 'w') as f:
                                    json.dump(code_info_dict, f)
                                self.save_tag_to_json_info(code_tag)
                                tool_error_info.show_exception_info('message', 'Save Code Success.')
                                self.del_old_json()
                                self.close()
                        else:
                            with open(code_path + '/' + node_code_name_info + '.json', 'w') as f:
                                json.dump(code_info_dict, f)
                            self.save_tag_to_json_info(code_tag)
                            tool_error_info.show_exception_info('message', 'Save Code Success.')
                            self.del_old_json()
                            self.close()
                    else:
                        QtWidgets.QMessageBox.about(self, 'waring', 'please input code in houdini python node')

                # if select wrangle node
                elif current_node_name == 'attribwrangle':
                    code_path = tool_path_manager.vex_codes_path
                    codes = current_node.parm('snippet').rawValue()
                    run_over_class = current_node.parm('class').eval()
                    # if select node have code text
                    if codes:
                        code_info_dict = {
                            "tag": code_tag,
                            "class": run_over_class,
                            "info": codes
                        }
                        allfiles = os.listdir(code_path)
                        files = [x for x in allfiles if x.split('.')[-1].lower() == 'json']

                        # replace
                        if node_code_name_info + '.json' in files:
                            replace_result = QtWidgets.QMessageBox.warning(self,
                                                                           'Replacing',
                                                                           'have same name node, are you sure to replace?',
                                                                           QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                            if replace_result == QtWidgets.QMessageBox.Yes:
                                with open(code_path + '/' + node_code_name_info + '.json', 'w') as f:
                                    json.dump(code_info_dict, f)
                                self.save_tag_to_json_info(code_tag)
                                tool_error_info.show_exception_info('message', 'Save Code Success.')
                                self.del_old_json()
                                self.close()
                        else:
                            with open(code_path + '/' + node_code_name_info + '.json', 'w') as f:
                                json.dump(code_info_dict, f)
                                self.save_tag_to_json_info(code_tag)
                                tool_error_info.show_exception_info('message', 'Save Code Success.')
                                self.del_old_json()
                                self.close()
                    else:
                        QtWidgets.QMessageBox.about(self, 'waring',
                                                    'please input vex code in houdini attribute wrangle node')

            else:
                # if have code text
                if node_code_text_info:
                    code_info_dict = {
                        "tag": code_tag,
                        "class": run_over_class,
                        "info": node_code_text_info

                    }
                    if code_type_index == 0:
                        code_path = tool_path_manager.vex_codes_path
                    else:
                        code_path = tool_path_manager.python_codes_path
                    all_files = os.listdir(code_path)
                    code_files = [x for x in all_files if x.split('.')[-1].lower() == 'json']

                    # replace
                    if node_code_name_info + '.json' in code_files:
                        replace_result = QtWidgets.QMessageBox.warning(self,
                                                                       'Replacing',
                                                                       'have same name node, are you sure to replace?',
                                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                        if replace_result == QtWidgets.QMessageBox.Yes:
                            with open(code_path + '/' + node_code_name_info + '.json', 'w') as f:
                                json.dump(code_info_dict, f)
                            self.save_tag_to_json_info(code_tag)
                            tool_error_info.show_exception_info('message', 'Save Code Success.')
                            self.del_old_json()
                            self.close()
                    else:
                        with open(code_path + '/' + node_code_name_info + '.json', 'w') as f:
                            json.dump(code_info_dict, f)
                            self.save_tag_to_json_info(code_tag)
                            tool_error_info.show_exception_info('message', 'Save Code Success.')
                            self.del_old_json()
                            self.close()

                else:
                    QtWidgets.QMessageBox.about(self, 'warning', 'please select houdini node or input code')
        else:
            QtWidgets.QMessageBox.about(self, 'warning', 'please input node name')

    def get_select_node(self) -> hou.Node:
        """
            Get Current Select Node In Houdini If Multi Select Return First
        :return: hou.node()
        """
        if self.node:
            return self.node
        else:
            nodes = list(hou.selectedNodes())
            if nodes:
                self.node = nodes[0]
                return self.node

    def set_update_flag(self, flag: bool, old_json_name: str = '') -> None:
        self.update_flag = flag
        self.old_json_name = old_json_name

    def update_code_by_select_node_info(self, current_item: QtWidgets.QListWidgetItem, code_type: int) -> None:
        """
            Update Code Info By Current Select Code Node
        :param current_item: Current Node Need Update
        :param code_type: Which Type Of Code : Python Or Vex
        """
        self.code_type_choose_combo_box.setCurrentIndex(code_type)
        if code_type == 0:
            code_path = tool_path_manager.vex_codes_path
        else:
            code_path = tool_path_manager.python_codes_path
        current_code_name = current_item.text()
        code_json_path = code_path + '/' + current_code_name + '.json'
        code_info = None
        with open(code_json_path, 'r') as f:
            code_info = json.load(f)
        code_tag_list = code_info['tag']
        code_line_info = code_info['info']

        self.code_text_line_edit.setPlainText(code_line_info)
        self.code_name_line_edit.setText(current_code_name)
        self.old_json_name = current_code_name

        result_text = ''
        for tag in code_tag_list:
            result_text += tag + ' , '
        result_text = result_text[:-3]
        self.code_tag_line_edit.setText(result_text)

        self.code_tag_multi_check_box.setChecked((len(code_tag_list) > 1))

    @classmethod
    def delete_select_code_info(cls, current_item, code_type) -> None:
        """
            Delete Json Code Info By Current Select Code
        :param current_item: Current Select Code To Delete
        :param code_type: Which Type Of Code : Python Or Vex
        """
        if current_item:
            result = QtWidgets.QMessageBox.warning(tool_error_info, 'delete!', 'are you sure to delete?',
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if result == QtWidgets.QMessageBox.Yes:
                code_name = current_item.text()
                if code_type == 0:
                    code_file = tool_path_manager.vex_codes_path + '/' + code_name + '.json'
                    try:
                        os.remove(code_file)
                    except:
                        tool_error_info.show_exception_info('error', 'delete current file got wrong')

                elif code_type == 1:
                    code_file = tool_path_manager.python_codes_path + '/' + code_name + '.json'
                    try:
                        os.remove(code_file)
                    except:
                        tool_error_info.show_exception_info('error', 'delete current file got wrong')

        else:
            QtWidgets.QMessageBox.about(tool_error_info, '警告', '请先选择要删除的项')

    def closeEvent(self, event) -> None:
        """
            Set Parent To None When Window Closed
        :param event:
        """
        self.setParent(None)
