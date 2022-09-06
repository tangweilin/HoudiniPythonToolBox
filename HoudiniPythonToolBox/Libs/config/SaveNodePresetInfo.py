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


class SaveNodePresetInfo(QtWidgets.QWidget):
    """
        Saving Current Node Preset Info To Json File
    """

    def __init__(self):
        super(SaveNodePresetInfo, self).__init__()

        self.setGeometry(1200, 1200, 370, 250)
        tool_widget_utility_func.set_widget_to_center_desktop(self)
        self.setObjectName('SaveNodePresetInfo')
        self.setWindowTitle('SaveNodePresetInfo')
        self.set_window()
        self.node = None
        self.update = False

    def set_window(self) -> None:
        """
            Setup Main UI Of SaveNodePresetInfo
        :return: None
        """
        v_layout = QtWidgets.QVBoxLayout(self)
        h_layout = QtWidgets.QHBoxLayout()
        node_name_h_layout = QtWidgets.QHBoxLayout()
        author_h_layout = QtWidgets.QHBoxLayout()
        remark_h_layout = QtWidgets.QHBoxLayout()
        node_folder_h_layout = QtWidgets.QHBoxLayout()

        self.save_btn = QtWidgets.QPushButton('save')
        self.save_btn.clicked.connect(self.save_node_preset)
        self.reset_btn = QtWidgets.QPushButton('reset')
        self.reset_btn.clicked.connect(self.reset_node_preset)
        tool_widget_utility_func.set_widget_icon(self.save_btn, 'save_node.png')
        tool_widget_utility_func.set_widget_icon(self.reset_btn, 'reset_node.png')

        self.node_folder_line_edit = QtWidgets.QLineEdit()
        self.node_folder_line_edit.setPlaceholderText('Node Folder')

        self.code_type_choose_combo_box = QtWidgets.QComboBox()
        self.code_type_choose_combo_box.currentIndexChanged.connect(self.change_folder_name)
        path_list = self.get_node_path_folders()
        for path in path_list:
            self.code_type_choose_combo_box.addItem(path)

        node_name_label = QtWidgets.QLabel()
        node_name_label.setText('node name:')
        node_name_label.setTextFormat(QtCore.Qt.AutoText)
        node_name_label.setAlignment(QtCore.Qt.AlignCenter)
        node_name_label.setFixedSize(80, 25)

        self.node_name_line_edit = QtWidgets.QLineEdit()
        self.node_name_line_edit.setPlaceholderText('node name')

        node_name_h_layout.addWidget(node_name_label)
        node_name_h_layout.addWidget(self.node_name_line_edit)

        author_label = QtWidgets.QLabel()
        author_label.setText('author:')
        author_label.setTextFormat(QtCore.Qt.AutoText)
        author_label.setAlignment(QtCore.Qt.AlignCenter)
        author_label.setFixedSize(80, 25)

        self.author_name_line_edit = QtWidgets.QLineEdit()
        self.author_name_line_edit.setPlaceholderText('author name')

        author_h_layout.addWidget(author_label)
        author_h_layout.addWidget(self.author_name_line_edit)

        remark_label = QtWidgets.QLabel()
        remark_label.setText('remark:')
        remark_label.setTextFormat(QtCore.Qt.AutoText)
        remark_label.setAlignment(QtCore.Qt.AlignCenter)
        remark_label.setFixedSize(80, 25)
        self.remark_text_line_edit = QtWidgets.QPlainTextEdit()
        self.remark_text_line_edit.setPlaceholderText('remarks...')

        remark_h_layout.addWidget(remark_label)
        remark_h_layout.addWidget(self.remark_text_line_edit)

        # layout
        h_layout.addWidget(self.save_btn)
        h_layout.addWidget(self.reset_btn)
        v_layout.addLayout(h_layout)
        node_folder_h_layout.addWidget(self.node_folder_line_edit)
        node_folder_h_layout.addWidget(self.code_type_choose_combo_box)
        v_layout.addLayout(node_folder_h_layout)
        v_layout.addLayout(node_name_h_layout)
        v_layout.addLayout(author_h_layout)
        v_layout.addLayout(remark_h_layout)
        self.change_folder_name()

    def change_folder_name(self) -> None:
        """
            Change Folder Name
        :return: None
        """
        self.node_folder_line_edit.setText(self.code_type_choose_combo_box.currentText())

    def get_node_path_folders(self) -> list:
        """
            Get Node Path Folders
        :return: list
        """
        path_list = []
        path = os.listdir(tool_path_manager.node_preset_path)
        for p in path:
            if os.path.isdir(os.path.join(tool_path_manager.node_preset_path, p)):
                path_list.append(p)
        return path_list

    def save_node_preset(self) -> None:
        """
            Save Current Select Node Info In Houdini To Json File
        :return: None
        """
        nodes = hou.selectedNodes()
        if nodes:
            node = nodes[0]
            node_category_name = node.type().category().name()
            node_category_prefix = None
            parent_node = node.parent()
            name = self.node_name_line_edit.text().rstrip()

            # get current node type
            if name:
                if node_category_name == 'Object':
                    node_category_prefix = 'obj'
                elif node_category_name == 'Sop':
                    node_category_prefix = 'sop'
                elif node_category_name == 'Dop':
                    node_category_prefix = 'dop'
                elif node_category_name == 'Driver':
                    node_category_prefix = 'out'
                elif node_category_name == 'Vop':
                    if parent_node.type().category().name() == 'Sop':
                        node_category_prefix = 'vop'
                    elif parent_node.type().category().name() == 'Manager':
                        node_category_prefix = 'mat'
                elif node_category_name == 'Shop':
                    node_category_prefix = 'shop'
                elif node_category_name == 'Top' or node_category_name == 'TopNet':
                    node_category_prefix = 'top'
                elif node_category_name == 'Lop':
                    node_category_prefix = 'lop'
                else:
                    node_category_prefix = node_category_name.lower()
                author = self.author_name_line_edit.text()
                remark = self.remark_text_line_edit.toPlainText()
                node_preset_path = tool_path_manager.node_preset_path
                node_folder = self.node_folder_line_edit.text()
                node_final_path = os.path.join(node_preset_path, node_folder)
                if not os.path.exists(node_final_path):
                    os.mkdir(node_final_path)

                all_files = os.listdir(node_final_path)
                hip_files = [x for x in all_files if x.split('.')[-1].startswith('nodepresets')]
                files = [x for x in hip_files if x.split('_')[0].lower().startswith(node_category_prefix)]
                if  name.split('_')[0].lower().startswith(node_category_prefix):
                    file_name = name
                else:
                    file_name = node_category_prefix + '_' + name

                file_full_path = node_final_path + '/' + file_name + '.nodepresets'
                info_full_path = node_final_path + '/' + file_name + '.json'
                all_info = {'author': author, 'remark': remark}
                # replace
                if file_name + '.nodepreset' in files:
                    reply = QtWidgets.QMessageBox.warning(self, "replace",
                                                          "have same file , are you sure to replace?",
                                                          QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                    if reply == QtWidgets.QMessageBox.Yes:
                        parent_node.saveItemsToFile(nodes, file_full_path)
                        with open(info_full_path, 'w') as f:
                            json.dump(all_info, f)

                        self.close()
                        # custom screen shot
                        shot = ScreenShotTool.ScreenShotTool(file_name, node_final_path)
                        shot.show()
                else:
                    parent_node.saveItemsToFile(nodes, file_full_path)
                    with open(info_full_path, 'w') as f:
                        json.dump(all_info, f)
                    self.close()
                    # custom screen shot
                    shot = ScreenShotTool.ScreenShotTool(file_name, node_final_path)
                    shot.show()

    def reset_node_preset(self) -> None:
        """
            Reset Info On Window
        :return: None
        """
        self.author_name_line_edit.setText('')
        self.remark_text_line_edit.setPlainText('')
        if not self.update:
            self.node_name_line_edit.setText('')

    def is_update_node_preset(self, update, node_type='', node_name='', node_author='', node_mark='') -> None:
        """
            Set Flag For Node Info Save Or Update
        :param node_mark: Node Mark Info
        :param node_author:  Node Author Info
        :param update: Flag -> Bool
        :param node_type: Node Class Name
        :param node_name: Current Node Name
        :return: None
        """
        self.update = update
        if update:
            if node_type:
                self.code_type_choose_combo_box.setCurrentText(node_type)
                self.change_folder_name()
                self.code_type_choose_combo_box.setEnabled(False)
                self.node_folder_line_edit.setEnabled(False)
                self.node_name_line_edit.setText(node_name)
                self.node_name_line_edit.setEnabled(False)
                self.author_name_line_edit.setText(node_author)
                self.remark_text_line_edit.setPlainText(node_mark)
        else:
            self.code_type_choose_combo_box.setEnabled(True)
            self.node_name_line_edit.setEnabled(True)

    @classmethod
    def update_screen_shot(cls, current_item, node_type) -> None:
        """
            Update Current Node Screen Shot
        :param current_item: Current Select None In List Widget
        :param node_type: Node Folder Name
        :return: None
        """
        if current_item:
            item_name = current_item.text()
            file_name = node_type + '/' + item_name
            node_preset_path = tool_path_manager.node_preset_path
            shot = ScreenShotTool.ScreenShotTool(file_name, node_preset_path)
            shot.show()
        else:
            tool_error_info.show_exception_info('waring', 'please select a node preset')

    @classmethod
    def delete_node_preset(cls, list_widget, node_type='') -> None:
        """
            Delete Current Select Nodes Info From Json File
        :param list_widget: Nodes List Widget
        :param node_type: Node Folder Name
        :return: None
        """
        items = list_widget.selectedItems()
        if items:
            result = QtWidgets.QMessageBox.warning(tool_error_info, 'delete', 'are you sure to delete node preset?',
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if result == QtWidgets.QMessageBox.Yes:
                for item in items:
                    node_path = tool_path_manager.node_preset_path
                    file_name = item.text()
                    full_path = node_path + '/' + node_type + '/' + file_name + '.nodepresets'
                    image_path = node_path + '/' + node_type + '/' + file_name + '.jpg'
                    info_path = node_path + '/' + node_type + '/' + file_name + '.json'
                    list_widget.takeItem(list_widget.row(item))
                    namede = file_name.encode('utf-8')
                    try:
                        os.remove(full_path)
                        os.remove(info_path)
                        os.remove(image_path)
                    except:
                        pass
        else:
            QtWidgets.QMessageBox.about(tool_error_info, 'warning', 'please select node to delete')
