import json
import os
from imp import reload

import hou
from PySide2 import QtWidgets

from Libs.path import ToolPathManager
from Libs.utilities import ToolUtilityClasses

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

    def set_window(self) -> None:
        """
            To Show The UI Of SaveVexPyNodeInfo Window
        :return: None
        """
        v_layout = QtWidgets.QVBoxLayout(self)
        h_layout = QtWidgets.QHBoxLayout()
        self.save_btn = QtWidgets.QPushButton('save')
        self.reset_btn = QtWidgets.QPushButton('reset')
        tool_widget_utility_func.set_widget_icon(self.save_btn, 'save_node.png')
        self.save_btn.clicked.connect(self.save_node_info)
        tool_widget_utility_func.set_widget_icon(self.reset_btn, 'reset_node.png')
        self.reset_btn.clicked.connect(self.reset_node_info)
        self.code_type_choose_combo_box = QtWidgets.QComboBox()
        self.code_type_choose_combo_box.addItem('vex')
        self.code_type_choose_combo_box.addItem('python')
        self.node_name_line_edit = QtWidgets.QLineEdit()
        self.node_name_line_edit.setPlaceholderText('node name')
        self.node_code_text_line_edit = QtWidgets.QPlainTextEdit()
        self.node_code_text_line_edit.setPlaceholderText('vex or python code...')

        h_layout.addWidget(self.save_btn)
        h_layout.addWidget(self.reset_btn)
        v_layout.addLayout(h_layout)
        v_layout.addWidget(self.code_type_choose_combo_box)
        v_layout.addWidget(self.node_name_line_edit)
        v_layout.addWidget(self.node_code_text_line_edit)

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
            self.node_name_line_edit.setText(codes_name)

            if node.type().name() == 'attribwrangle':
                codes = node.parm('snippet').rawValue()
                self.code_type_choose_combo_box.setCurrentIndex(0)

            elif node.type().name() == 'python':
                codes = node.parm('python').rawValue()
                self.code_type_choose_combo_box.setCurrentIndex(1)

            self.node_code_text_line_edit.setPlainText(codes)
        else:
            self.node_name_line_edit.setText('')
            self.node_code_text_line_edit.setPlainText('')

    def save_node_info(self) -> None:
        """
            Copy Code Text Which In TextBox Or Selected Node To Code Preset Config
        :return: None
        """
        node_code_text_info = self.node_code_text_line_edit.toPlainText()
        node_code_name_info = self.node_name_line_edit.text()
        code_type_index = self.code_type_choose_combo_box.currentIndex()
        code_path = None
        if node_code_name_info:

            # if have code text
            if node_code_text_info:
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
                            json.dump(node_code_text_info, f)
                        self.close()
                else:
                    with open(code_path + '/' + node_code_name_info + '.json', 'w') as f:
                        json.dump(node_code_text_info, f)
                        self.close()

            # if select houdini code node
            else:
                current_node = self.get_select_node()
                if current_node:
                    current_node_name = current_node.type().name()
                    code_type = self.code_type_choose_combo_box.currentIndex()

                    # if select python node
                    if node_code_name_info and current_node_name == 'python':
                        codes = current_node.parm('python').rawValue()

                        # if select node have code text
                        if codes:
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
                                        json.dump(codes, f)
                                    self.close()
                            else:
                                with open(code_path + '/' + node_code_name_info + '.json', 'w') as f:
                                    json.dump(codes, f)
                                self.close()
                        else:
                            QtWidgets.QMessageBox.about(self, 'waring', 'please input code in houdini python node')

                    # if select wrangle node
                    elif node_code_name_info and current_node_name == 'attribwrangle':
                        code_path = tool_path_manager.vex_codes_path
                        code_run_over_class = self.node.parm('class').eval()
                        if code_run_over_class != 2:
                            node_code_name = node_code_name_info + '_' + str(code_run_over_class)

                        codes = self.node.parm('snippet').rawValue()

                        # if select node have code text
                        if codes:
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
                                        json.dump(codes, f)
                                    self.close()
                            else:
                                with open(code_path + '/' + node_code_name_info + '.json', 'w') as f:
                                    json.dump(codes, f)
                                    self.close()
                        else:
                            QtWidgets.QMessageBox.about(self, 'waring',
                                                        'please input vex code in houdini attribute wrangle node')

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

    @classmethod
    def update_code_by_select_node_info(cls, current_item, code_type) -> None:
        """
            Update Code Info By Current Select Code Node
        :param current_item: Current Node Need Update
        :param code_type: Which Type Of Code : Python Or Vex
        """
        if current_item:
            nodes = list(hou.selectedNodes())
            if nodes:
                node = nodes[0]
                result = QtWidgets.QMessageBox.warning(tool_error_info, 'update', 'are you sure to update?',
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                if result == QtWidgets.QMessageBox.Yes:
                    file_name = current_item.text()
                    code_path = None
                    # wrangle
                    if code_type == 0:
                        if node.type().name() == 'attribwrangle':
                            code_path = tool_path_manager.vex_codes_path + '/' + file_name + '.json'
                            codes = node.parm('snippet').rawValue()
                            with open(code_path, 'w') as (f):
                                json.dump(codes, f)
                        else:
                            tool_error_info.show_exception_info('warning', 'selection code type does not match')

                    # python
                    elif code_type == 1:
                        if node.type().name() == 'python':
                            code_path = tool_path_manager.python_codes_path + '/' + file_name + '.json'
                            codes = node.parm('python').rawValue()
                            with open(code_path, 'w') as (f):
                                json.dump(codes, f)
                        else:
                            tool_error_info.show_exception_info('warning', 'selection code type does not match')
            else:
                tool_error_info.show_exception_info('error', 'please select node to update')
        else:
            tool_error_info.show_exception_info('error', 'please select current node to update')

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
                        pass

                elif code_type == 1:
                    code_file = tool_path_manager.python_codes_path + '/' + code_name + '.json'
                    try:
                        os.remove(code_file)
                    except:
                        pass

        else:
            QtWidgets.QMessageBox.about(tool_error_info, '警告', '请先选择要删除的项')

    def closeEvent(self, event) -> None:
        """
            Set Parent To None When Window Closed
        :param event:
        """
        self.setParent(None)
