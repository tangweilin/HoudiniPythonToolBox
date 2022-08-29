import os
import json
import hou
import re

from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtWidgets import *
from PySide2.QtGui import QStandardItem
from PySide2.QtCore import QEvent

from Libs.path import ToolPathManager
from typing import Dict, List
from imp import reload

reload(ToolPathManager)

tool_path_manager = ToolPathManager.ToolPath()


class SetWidgetInfo(QtWidgets.QWidget):
    """
        Setting Widget Info Utility Class
    """

    @classmethod
    def set_widget_to_center_desktop(cls, widget) -> None:
        """
            Move Widget To Center Of Desktop
        :param widget: Current Widget
        :return: None
        """
        qRect = widget.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qRect.moveCenter(centerPoint)
        widget.move(qRect.topLeft())

    @classmethod
    def set_widget_icon(cls, widget, icon_name, size=None) -> None:
        """
        :param size: the fixed size of icon if not None value
        :param widget: which widget need set icon
        :param icon_name:  target icon name
        :return: None
        """
        icon = QtGui.QIcon()
        icon.addPixmap(tool_path_manager.icon_path + '/' + icon_name, QtGui.QIcon.Normal, QtGui.QIcon.Off)
        widget.setIcon(icon)
        if size:
            widget.setFixedSize(size)

    @classmethod
    def set_widget_label(cls, widget, label_text, size_x, size_y) -> None:
        """
        :param widget: Label To Set
        :param label_text: Target Label Text
        :param size_x: Width Of Label
        :param size_y: Height Of Label
        :return: None
        """
        widget.setText(label_text)
        widget.setTextFormat(QtCore.Qt.AutoText)
        widget.setAlignment(QtCore.Qt.AlignCenter)
        widget.setFixedSize(size_x, size_y)

    @classmethod
    def add_code_info_to_list_widget(cls, list_widget: QtWidgets.QListWidgetItem, path: str = '') -> List[Dict]:
        """
            Show ListWidget Item Info By Path
        :param list_widget: Current ListWidget
        :param path:  Info Path
        :return: List Of Tag Info
        """
        all_files = os.listdir(path)
        files = [x for x in all_files if x.split('.')[(-1)].lower().startswith('json')]

        dict_arr = []
        for file in files:
            result_dict = {}
            item_name = file.split('.')[0]
            item = QtWidgets.QListWidgetItem(list_widget)
            json_path = path + '/' + file
            with open(json_path, 'r') as f:
                file_info = json.load(f)
            result_dict['item_name'] = item_name
            result_dict['item_tag'] = file_info['tag']
            dict_arr.append(result_dict)
            item.setText(item_name)
        return dict_arr

    @classmethod
    def add_node_preset_info_to_list_widget(cls, list_widget, path='', node_class_type='') -> None:
        """
            Add Item Node To List Widget With Json File
        :param list_widget:  Current List Widget
        :param path:  Node Path
        :param node_class_type:  Node Class Name
        :return: None
        """
        all_files = os.listdir(path)
        hip_files = [x for x in all_files if x.split('.')[(-1)].startswith('nodepresets')]

        files = [x for x in hip_files if x.split('_')[0].lower().startswith(node_class_type)]

        for file in files:
            item_name = ('_').join(file.split('.')[0].split('_')[1:])
            item = QtWidgets.QListWidgetItem(list_widget)
            item.setText(item_name)
            item.setSizeHint(QtCore.QSize(200, 30))

    @classmethod
    def get_node_image_path_by_current_list_widget_item(cls, path='', current_item=None, node_type='') -> str:
        """
            Find Node Screen Shot Path By Current Select List Widget Item
        :param path: Node Path
        :param current_item: Current Select Item
        :param node_type: Node Class Name
        :return: Screen Shot Image Path
        """
        if current_item:
            file_name = current_item.text()
            image_path = path + '/' + node_type + '_' + file_name + '.jpg'
            return image_path

    @classmethod
    def get_node_remark_info_by_current_list_widget_item(cls, path='', current_item=None, node_type='') -> tuple:
        """
            Get Node Remark Info By Current Select List Widget Item
        :param path:  Node Path
        :param current_item:  Current Select Item
        :param node_type:  Node Class Name
        :return: Two Value Of Tuple (Author,Remark)
        """
        if current_item:
            file_name = current_item.text()
            info_path = tool_path_manager.node_preset_path + '/' + node_type + '_' + file_name + '.json'
            info_list = None
            try:
                with open(info_path, 'r') as (f):
                    info_list = json.load(f)
            except:
                pass

            if info_list:
                author = info_list['author']
                remark = info_list['remark']
                return author, remark

    @classmethod
    def get_code_info_by_current_list_widget_item(cls, path='', current_item=None) -> tuple:
        """
            Get Current ListWidget Select Item Info By Path
        :param path: Current Code Info Path
        :param current_item: Current Select Item
        :return: Two Value Of Tuple (code file name , code file info)
        """
        if current_item:
            file = current_item.text()
            code_file_path = path + '/' + file + '.json'
            code_info = ''
            code_tag = ''
            code_class = 2
            try:
                with open(code_file_path, 'r') as (f):
                    info = json.load(f)
                code_tag = info['tag']
                code_info = info['info']
                code_class = info['class']
            except:
                tool_error_info = ExceptionInfoWidgetClass()
                tool_error_info.show_exception_info('error', 'read code info got error , path : %s' % path)
            return file, code_info, code_tag, code_class

    @classmethod
    def get_current_code_path_by_combo_box_index(cls, combo_box_index) -> str:
        """
            Get Current Code Path
        :param combo_box_index: Current Code Type Combo Box Index
        :return: Code Path
        """
        code_path = tool_path_manager.vex_codes_path if combo_box_index == 0 else tool_path_manager.python_codes_path
        return code_path

    @classmethod
    def create_node_preset_info_by_current_list_widget_item(cls, path='', current_item=None, node_type='') -> None:
        """
            Get Node Preset Info From Json File By Current Select List Widget Item And Create Houdini Nodes
        :param path: Node Path
        :param current_item: Current Select Item
        :param node_type: Node Class Name
        :return Str -> Node Preset Info
        """
        if current_item:
            file = current_item.text()
            if node_type:
                node_preset_path = tool_path_manager.node_preset_path

            node_full_path = node_preset_path + '/' + node_type + '_' + file + '.nodepresets'
            node_pane = HouNodesUtilities.get_hou_network_pane_tab()
            if node_pane:
                pos = node_pane.selectPosition()
                up_node = node_pane.pwd()
                if node_type == 'sop':
                    if up_node.type().name() == 'geo':
                        root = up_node
                        root.loadItemsFromFile(node_full_path)
                        current_select_nodes = hou.selectedNodes()
                        first_node = current_select_nodes[0]
                        first_pos = first_node.position()
                        move = pos - first_pos
                        for node in current_select_nodes:
                            node.move(move)
                    elif up_node.type().name() == 'obj':
                        root = up_node.createNode('geo')
                        root.setPosition(pos)
                        root.loadItemsFromFile(node_full_path)
                elif node_type == 'obj' and up_node.type().name() == 'obj':
                    root = up_node
                    root.loadItemsFromFile(node_full_path)
                    currentSelNodes = hou.selectedNodes()
                    firstNode = currentSelNodes[0]
                    firstPos = firstNode.position()
                    move = pos - firstPos
                    for node in currentSelNodes:
                        node.move(move)

                elif node_type == 'vop':
                    if up_node.type().name() == 'geo':
                        root = up_node.createNode('attribvop')
                        root.setPosition(pos)
                        root.loadItemsFromFile(node_full_path)
                    elif up_node.type().name() == 'attribvop':
                        root = up_node
                        root.loadItemsFromFile(node_full_path)
                        currentSelNodes = hou.selectedNodes()
                        firstNode = currentSelNodes[0]
                        firstPos = firstNode.position()
                        move = pos - firstPos
                        for node in currentSelNodes:
                            node.move(move)
                else:
                    try:
                        root = up_node
                        root.loadItemsFromFile(node_full_path)
                        currentSelNodes = hou.selectedNodes()
                        firstNode = currentSelNodes[0]
                        firstPos = firstNode.position()
                        move = pos - firstPos
                        for node in currentSelNodes:
                            node.move(move)

                    except:
                        pass
            else:
                err_info = ExceptionInfoWidgetClass()
                err_info.show_exception_info('waring', 'Create Python Code Got Wrong')


class ExceptionInfoWidgetClass(QtWidgets.QWidget):
    """
        Common Widget Class To Pop Message
    """

    def __init__(self):
        super(ExceptionInfoWidgetClass, self).__init__()

    def show_exception_info(self, title, text):
        """
            Show Message Window
        :param title: Window Title
        :param text: Pop Message
        """
        QtWidgets.QMessageBox.about(self, title, text)


class HouNodesUtilities(QWidget):
    """
        Utilities Func For Working With Houdini Nodes
    """

    @classmethod
    def get_hou_network_pane_tab(cls) -> hou.paneTabType:
        """
            Find NetWorkPanel
        :return:  Current Houdini NetWorkPanel
        """
        panes = hou.ui.paneTabs()
        result_pan = None
        for pane in panes:
            if pane.type() == hou.paneTabType.NetworkEditor:
                result_pan = pane
                break
        return result_pan

    @classmethod
    def import_code_to_houdini_by_code_info(cls, code_info, code_type) -> None:
        """
            Create Houdini Node By Current Code Type , And Write Code Info Into Node
        :param code_info: Code Info To Create Node
        :param code_type: Which Type Of Code : Python Or Vex
        """
        err_info = ExceptionInfoWidgetClass()
        pane = cls.get_hou_network_pane_tab()
        if pane:
            if code_info:
                node_pos = pane.selectPosition()
                root = pane.pwd()
                if code_type == 0:
                    code_name = code_info[0]
                    try:
                        wrangle_node = root.createNode('attribwrangle', code_name)
                        wrangle_node.setPosition(node_pos)
                        wrangle_node.parm('snippet').set(code_info[1])
                        wrangle_node.parm('class').set(code_info[3])
                    except:
                        err_info.show_exception_info('error', 'Create Vex Code Got Wrong')


                elif code_type == 1:
                    try:
                        python_node = root.createNode('python', code_info[0])
                        python_node.setPosition(node_pos)
                        python_node.parm('python').set(code_info[1])
                    except:
                        err_info.show_exception_info('error', 'Create Python Code Got Wrong')
                else:
                    err_info.show_exception_info('waring', 'Input Code Is Wrong Type')
            else:
                err_info.show_exception_info('waring', 'Code Info Is None')

    @classmethod
    def update_code_by_select_node_info(cls, current_item, code_type) -> None:
        """
            Update Json Code Info By Select A Code Node In Houdini
        :param current_item: Current Select Node To Update
        :param code_type: Which Code Type To Update : Python Or Vex
        """
        tool_error_info = ExceptionInfoWidgetClass()
        if current_item:
            nodes = list(hou.selectedNodes())
            if nodes:
                node = nodes[0]
                result = QtWidgets.QMessageBox.warning(tool_error_info, 'update', 'are you sure to update?',
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                if result == QtWidgets.QMessageBox.Yes:
                    file_name = current_item.text()
                    code_path = None
                    if code_type == 0:
                        if node.type().name() == 'attribwrangle':
                            code_path = tool_path_manager.vex_codes_path + '/' + file_name + '.json'
                            codes = node.parm('snippet').rawValue()
                            with open(code_path, 'w') as (f):
                                json.dump(codes, f)
                        else:
                            tool_error_info.show_exception_info('warning', 'selection code type does not match')
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


class CheckableComboBox(QtWidgets.QComboBox):
    """
        Checkable ComboBox Widget Support Multi Select Option With CheckBox
    """

    def __init__(self):
        super().__init__()
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self.closeOnLineEditClick = False
        self.lineEdit().installEventFilter(self)

        self.view().viewport().installEventFilter(self)
        self.model().dataChanged.connect(self.update_line_edit_field)
        self.lineEdit().setText('')

    def eventFilter(self, widget: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """
            Event Filter For Widget
        :param widget: Widget To Filter
        :param event: Event To Filter
        :return: Bool
        """
        if widget == self.lineEdit():
            if event.type() == QEvent.MouseButtonRelease:
                if self.closeOnLineEditClick:
                    self.hidePopup()
                else:
                    self.showPopup()
                return True
            return super().eventFilter(widget, event)

        if widget == self.view().viewport():
            if event.type() == QEvent.MouseButtonRelease:
                index = self.view().indexAt(event.pos())
                item = self.model().item(index.row())

                if item.checkState() == QtCore.Qt.Checked:
                    item.setCheckState(QtCore.Qt.Unchecked)
                else:
                    item.setCheckState(QtCore.Qt.Checked)
                return True
            return super().eventFilter(widget, event)

    def hidePopup(self) -> None:
        """
            Hide Popup Widget
        """
        super().hidePopup()
        self.startTimer(100)

    def set_all_checked(self, checked: QtCore.Qt.CheckState) -> None:
        for i in range(self.model().rowCount()):
            self.model().item(i).setCheckState(checked)

    def update_line_edit_field(self):
        """
            Update LineEdit Field When Model Data Changed
        """
        text_container = []
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == QtCore.Qt.Checked:
                text_container.append(self.model().item(i).text())
        text_string = ', '.join(text_container)
        self.lineEdit().setText(text_string)

    def update_check_state_by_str(self, tag: List[str]) -> None:
        for i in range(self.model().rowCount()):
            for t in tag:
                if t in self.model().item(i).text():
                    self.model().item(i).setCheckState(QtCore.Qt.Checked)

    def addItems(self, items: List[str], itemList=None) -> None:
        """
            Add Item List To ComboBox
        :param items: Target Item List
        :param itemList:
        """
        for index, text in enumerate(items):
            try:
                data = itemList[index]
            except(TypeError, IndexError):
                data = None
            self.addItem(text, data)

    def addItem(self, text: str, userData=None) -> None:
        """
            Add Item To ComboBox
        :param text:  Item Text
        :param userData:  Item UserData
        """
        item = QStandardItem()
        item.setText(text)
        if userData is not None:
            item.setData(userData)

        # enable checkbox setting
        item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)
        item.setData(QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole)
        self.model().appendRow(item)

