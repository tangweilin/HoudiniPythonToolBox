import json
import re
from imp import reload

from PySide2 import QtWidgets

from Libs.path import ToolPathManager
from Libs.utilities import ToolUtilityClasses

reload(ToolUtilityClasses)
reload(ToolPathManager)

tool_widget_utility_func = ToolUtilityClasses.SetWidgetInfo
tool_path_manager = ToolPathManager.ToolPath()
tool_error_info = ToolUtilityClasses.ExceptionInfoWidgetClass()


class SaveCommonToolNodeInfo(QtWidgets.QWidget):
    """
        Save Common Tool Button Info To File
    """
    def __init__(self):
        super(SaveCommonToolNodeInfo, self).__init__()
        self.setGeometry(1200, 1200, 370, 400)
        self.setObjectName('add_common_tool_btn')
        self.setWindowTitle('add_new_common_tool_btn')
        tool_widget_utility_func.set_widget_to_center_desktop(self)
        self.button_type_list = ['Common', 'Obj', 'Sop', 'Dop', 'Top', 'Kine_fx', 'Solaris']
        self.set_window(self.button_type_list)

    def set_window(self, button_type_list: list) -> None:
        """
            Main Window UI Layout
        :param button_type_list:
        """
        main_v_layout = QtWidgets.QVBoxLayout(self)
        btn_h_layout = QtWidgets.QHBoxLayout()

        self.__add_btn = QtWidgets.QPushButton('add_btn')
        tool_widget_utility_func.set_widget_icon(self.__add_btn, 'save_node.png')

        self.__btn_type_combo_box = QtWidgets.QComboBox()
        for btn in button_type_list:
            self.__btn_type_combo_box.addItem(btn)

        self.__reset_btn = QtWidgets.QPushButton('reset_btn')
        tool_widget_utility_func.set_widget_icon(self.__reset_btn, 'reset_node.png')

        btn_object_name_h_layout = QtWidgets.QHBoxLayout()
        btn_object_name_label = QtWidgets.QLabel()
        tool_widget_utility_func.set_widget_label(btn_object_name_label, 'btn object name:', 100, 25)

        self.btn_object_name_line_edit = QtWidgets.QLineEdit()
        self.btn_object_name_line_edit.setPlaceholderText('btn name...')

        btn_label_name_h_layout = QtWidgets.QHBoxLayout()
        btn_label_name_label = QtWidgets.QLabel()
        tool_widget_utility_func.set_widget_label(btn_label_name_label, 'btn label name:', 100, 25)

        self.btn_label_name_line_edit = QtWidgets.QLineEdit()
        self.btn_label_name_line_edit.setPlaceholderText('btn name label...')

        btn_icon_name_h_layout = QtWidgets.QHBoxLayout()
        btn_icon_name_label = QtWidgets.QLabel()
        tool_widget_utility_func.set_widget_label(btn_icon_name_label, 'btn icon name:', 100, 25)

        self.btn_icon_name_line_edit = QtWidgets.QLineEdit()
        self.btn_icon_name_line_edit.setPlaceholderText('btn icon name...')
        self.btn_icon_name_line_edit.setReadOnly(True)

        btn_tips_h_layout = QtWidgets.QHBoxLayout()
        btn_tips_label = QtWidgets.QLabel()
        tool_widget_utility_func.set_widget_label(btn_tips_label, 'btn tips:', 100, 25)

        self.btn_tips_line_edit = QtWidgets.QLineEdit()
        self.btn_tips_line_edit.setPlaceholderText('btn tips...')

        btn_code_file_name_h_layout = QtWidgets.QHBoxLayout()
        btn_code_file_name_label = QtWidgets.QLabel()
        tool_widget_utility_func.set_widget_label(btn_code_file_name_label, 'btn file name:', 100, 25)

        self.btn_code_file_name_label = QtWidgets.QLabel()
        tool_widget_utility_func.set_widget_label(self.btn_code_file_name_label, 'btn file name', 200, 25)

        btn_code_info_label = QtWidgets.QLabel()
        tool_widget_utility_func.set_widget_label(btn_code_info_label, 'btn exec codes:', 100, 25)

        self.btn_code_info_line_edit = QtWidgets.QPlainTextEdit()
        self.btn_code_info_line_edit.setPlaceholderText('btn exec codes...')

        # layout
        btn_h_layout.addWidget(self.__add_btn)
        btn_h_layout.addWidget(self.__reset_btn)
        btn_h_layout.addWidget(self.__btn_type_combo_box)

        btn_object_name_h_layout.addWidget(btn_object_name_label)
        btn_object_name_h_layout.addWidget(self.btn_object_name_line_edit)

        btn_label_name_h_layout.addWidget(btn_label_name_label)
        btn_label_name_h_layout.addWidget(self.btn_label_name_line_edit)

        btn_icon_name_h_layout.addWidget(btn_icon_name_label)
        btn_icon_name_h_layout.addWidget(self.btn_icon_name_line_edit)

        btn_tips_h_layout.addWidget(btn_tips_label)
        btn_tips_h_layout.addWidget(self.btn_tips_line_edit)

        btn_code_file_name_h_layout.addWidget(btn_code_file_name_label)
        btn_code_file_name_h_layout.addWidget(self.btn_code_file_name_label)

        main_v_layout.addLayout(btn_h_layout)
        main_v_layout.addLayout(btn_object_name_h_layout)
        main_v_layout.addLayout(btn_label_name_h_layout)
        main_v_layout.addLayout(btn_icon_name_h_layout)
        main_v_layout.addLayout(btn_tips_h_layout)
        main_v_layout.addLayout(btn_code_file_name_h_layout)
        main_v_layout.addWidget(btn_code_info_label)
        main_v_layout.addWidget(self.btn_code_info_line_edit)

        # connect
        self.__add_btn.clicked.connect(self.add_btn)
        self.btn_object_name_line_edit.textChanged.connect(self.btn_name_changed)
        self.__btn_type_combo_box.currentIndexChanged.connect(self.btn_type_changed)
        self.__reset_btn.clicked.connect(self.reset_btn_info)

    def btn_type_changed(self) -> None:
        """
            Change Button Type
        """
        self.btn_name_changed()

    def btn_name_changed(self) -> None:
        """
            Check Button Name Is Correct Info
        """
        object_name = self.btn_object_name_line_edit.text()
        btn_type = self.__btn_type_combo_box.currentText()
        re_name = '^[0-9a-zA-Z_]+$'
        if re.match(re_name, object_name):
            self.btn_object_name_line_edit.setStyleSheet('color:rgb(0,255,0)')
            self.btn_code_file_name_label.setStyleSheet('color:rgb(0,255,0)')
        else:
            self.btn_object_name_line_edit.setStyleSheet('color:rgb(255,0,0)')
            self.btn_code_file_name_label.setStyleSheet('color:rgb(255,0,0)')
        self.btn_icon_name_line_edit.setText(btn_type + '_' + object_name + '.png')
        self.btn_code_file_name_label.setText(btn_type + '_' + object_name + '.py')

    def reset_btn_info(self) -> None:
        """
            Reset All Button Info To ''
        """
        self.btn_code_info_line_edit.setPlainText('')
        self.btn_object_name_line_edit.setText('')
        self.btn_code_file_name_label.setText('')
        self.btn_label_name_line_edit.setText('')
        self.btn_icon_name_line_edit.setText('')
        self.btn_tips_line_edit.setText('')

    def add_btn(self) -> None:
        """
            Dump New Button Info To Json File And Create Tool Python File
        """
        code_info = self.btn_code_info_line_edit.toPlainText()
        btn_type = self.__btn_type_combo_box.currentText()
        btn_object_name = self.btn_object_name_line_edit.text()
        btn_label_name = self.btn_label_name_line_edit.text()
        btn_icon_name = self.btn_icon_name_line_edit.text()
        btn_tips = self.btn_tips_line_edit.text()
        btn_file_name = self.btn_code_file_name_label.text()
        btn_tool_path = tool_path_manager.common_tools_path + '/' + btn_file_name
        btn_tool_json_path = tool_path_manager.common_tools_path + '/' + btn_type + '_' + btn_object_name +'.json'

        if btn_object_name:
            if code_info:
                btn_info = None

                try:
                    with open(btn_tool_json_path, 'r') as f:
                        btn_info = json.load(f)
                except:
                    with open(btn_tool_path, 'w') as f:
                        f.write(code_info)

                    btn_info_dict = {'object_name': btn_object_name,
                                     'label_name': btn_label_name,
                                     'icon_name': btn_icon_name,
                                     'tips': btn_tips}
                    with open(btn_tool_json_path, 'w') as f:
                        json.dump(btn_info_dict, f)
                else:
                    object_name_info = btn_info['object_name']
                    result = QtWidgets.QMessageBox.warning(self, "replace",
                                                           "have same object name btn, replace?",
                                                           QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                    if result == QtWidgets.QMessageBox.Yes:
                        with open(btn_tool_path, 'w') as f:
                            f.write(code_info)
                        btn_info['object_name'] = object_name_info
                        btn_info['label_name'] = btn_label_name
                        btn_info['icon_name'] = btn_icon_name
                        btn_info['tips'] = btn_tips
                        with open(btn_tool_json_path, 'w') as f:
                            json.dump(btn_info, f)

            else:
                tool_error_info.show_exception_info('error', 'please input code info')
        else:
            tool_error_info.show_exception_info('error', 'please input btn name')

    def closeEvent(self, event) -> None:
        """
            Set Parent To None When Window Closed
        :param event:
        """
        self.setParent(None)
