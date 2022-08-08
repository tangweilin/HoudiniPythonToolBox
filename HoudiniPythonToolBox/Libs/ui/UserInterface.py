import os
import sys
import hou
import json

from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtWidgets import QDesktopWidget

from Libs.path import ToolPathManager
from Libs.config import ToolConfigManager
from Libs.ui import CustomLabel
from Libs.config import SaveVexPyNodeInfo, SaveNodePresetInfo, SaveFileManagerInfo
from Libs.utilities import ToolUtilityClasses
from imp import reload

reload(ToolPathManager)
reload(ToolConfigManager)
reload(CustomLabel)
reload(SaveVexPyNodeInfo)
reload(SaveNodePresetInfo)
reload(SaveFileManagerInfo)
reload(ToolUtilityClasses)

tool_path_manager = ToolPathManager.ToolPath()
tool_config_manager = ToolConfigManager.ToolConfig()
tool_widget_utility_func = ToolUtilityClasses.SetWidgetInfo
tool_hou_node_utility_func = ToolUtilityClasses.HouNodesUtilities


class HoudiniPythonTools(QtWidgets.QMainWindow):
    """
    This Class is the main process Class
    """

    def __init__(self, parent=None):
        super(HoudiniPythonTools, self).__init__(parent)
        # main window
        self.__main_widget = QtWidgets.QWidget(self)
        self.__main_widget.setObjectName('main_widget')
        self.__main_widget.setGeometry(0, 21, 400, 220)
        self.setObjectName('toolbox')
        self.setCentralWidget(self.__main_widget)
        icon = QtGui.QIcon()
        icon_path = tool_path_manager.icon_path + '/window_title.png'
        icon.addPixmap(icon_path, QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.setGeometry(1200, 1200, 700, 600)
        tool_widget_utility_func.set_widget_to_center_desktop(self)

        config_dict = None
        tool_name = self.__read_config_value('toolBoxName')
        self.setWindowTitle(tool_name + '_Houdini_' + "_toolbox_" + 'v1.0')
        self.setMaximumSize(QtCore.QSize(1100, 830))
        self.statusBar()

        # main toolbar widgets
        self.__setup_tool_bar_widget_layout()

        # main tab widgets
        self.__setup_main_tab_widget_layout()

        # vex python code tab main layout
        self.__setup_vex_py_tab_widget_layout()

        # node preset tab main layout
        self.__setup_node_preset_widget_layout()

        # node preset list widget refresh
        self.__setup_node_preset_tab_list_widget_info()

        # file manager tab main layout
        self.__setup_file_manager_tab_widget_layout()

    def __setup_tool_bar_widget_layout(self) -> None:
        # toolbar
        tool_bar = self.addToolBar('')
        tool_bar.setFixedHeight(50)
        tool_bar_btn_size = QtCore.QSize(50, 50)

        # help toolbar
        self.__help_toolbar_btn = QtWidgets.QToolButton(tool_bar)
        tool_widget_utility_func.set_widget_icon(self.__help_toolbar_btn, 'help', tool_bar_btn_size)
        self.__help_toolbar_btn.clicked.connect(self.__on_help_toolbar_btn_clicked)
        self.__help_toolbar_btn.setShortcut('F1')
        self.__help_toolbar_btn.setStatusTip('open help hotkey:F1')
        tool_bar.addWidget(self.__help_toolbar_btn)

        # config toolbar
        self.__config_toolbar_btn = QtWidgets.QToolButton(tool_bar)
        tool_widget_utility_func.set_widget_icon(self.__config_toolbar_btn, 'config.png', tool_bar_btn_size)
        self.__config_toolbar_btn.setShortcut('F2')
        self.__config_toolbar_btn.clicked.connect(self.__on_config_toolbar_btn_clicked)
        self.__config_toolbar_btn.setStatusTip('settings hotkey:F2')
        tool_bar.addWidget(self.__config_toolbar_btn)

        # scale toolbar
        self.__scale_toolbar_btn = QtWidgets.QToolButton(tool_bar)
        tool_widget_utility_func.set_widget_icon(self.__scale_toolbar_btn, 'min.png', tool_bar_btn_size)
        self.__scale_toolbar_btn.clicked.connect(self.__on_scale_toolbar_btn_clicked)
        self.__scale_toolbar_btn.setShortcut('F3')
        self.__scale_toolbar_btn.setStatusTip('set window size scale down hotkey:F3')
        tool_bar.addWidget(self.__scale_toolbar_btn)

        # to file location toolbar
        self.__file_location_toolbar_btn = QtWidgets.QToolButton(tool_bar)
        tool_widget_utility_func.set_widget_icon(self.__file_location_toolbar_btn, 'file_location', tool_bar_btn_size)
        self.__file_location_toolbar_btn.setShortcut('F4')
        self.__file_location_toolbar_btn.clicked.connect(self.__on_file_location_toolbar_btn_clicked)
        self.__file_location_toolbar_btn.setStatusTip('open toolbox location file hotkey:F4')
        tool_bar.addWidget(self.__file_location_toolbar_btn)

        # refresh toolbar
        self.__refresh_toolbar_btn = QtWidgets.QToolButton(tool_bar)
        tool_widget_utility_func.set_widget_icon(self.__refresh_toolbar_btn, "refersh.png", tool_bar_btn_size)
        self.__refresh_toolbar_btn.setShortcut('F5')
        self.__refresh_toolbar_btn.clicked.connect(self.__on_refresh_toolbar_btn_clicked)
        self.__refresh_toolbar_btn.setStatusTip('refresh hotkey:F5')
        tool_bar.addWidget(self.__refresh_toolbar_btn)

        # tab node add btn
        self.__add_tab_node_btn = QtWidgets.QToolButton(tool_bar)
        tool_widget_utility_func.set_widget_icon(self.__add_tab_node_btn, 'add_tab_node.png', tool_bar_btn_size)
        self.__add_tab_node_btn.clicked.connect(self.__on_add_tab_node_btn_clicked)
        self.__add_tab_node_btn.setStatusTip('create a new tab node')
        tool_bar.addWidget(self.__add_tab_node_btn)

    def __setup_main_tab_widget_layout(self) -> None:

        main_v_layout = QtWidgets.QVBoxLayout(self.__main_widget)
        main_v_layout.setContentsMargins(1, 1, 1, 1)

        # modify tab widgets
        modify_tab_btn_size = QtCore.QSize(30, 30)
        modify_tab_h_layout = QtWidgets.QHBoxLayout()

        # tab line edit
        self.__line_edit_tab_name = QtWidgets.QLineEdit(self.__main_widget)
        self.__line_edit_tab_name.setMaximumSize(QtCore.QSize(1100, 30))
        self.__line_edit_tab_name.setPlaceholderText('newTabName')
        self.__line_edit_tab_name.setStatusTip('the name of new tab')
        self.__line_edit_tab_name.setContentsMargins(10, 6, 2, 2)

        modify_tab_h_layout.addWidget(self.__line_edit_tab_name)

        # tab add btn
        self.__add_tab_btn = QtWidgets.QPushButton(self.__main_widget)
        tool_widget_utility_func.set_widget_icon(self.__add_tab_btn, 'add_tab.png', modify_tab_btn_size)
        self.__add_tab_btn.clicked.connect(self.__on_add_tab_btn_clicked)
        modify_tab_h_layout.addWidget(self.__add_tab_btn)

        # tab del btn
        self.__del_tab_btn = QtWidgets.QPushButton(self.__main_widget)
        tool_widget_utility_func.set_widget_icon(self.__del_tab_btn, 'del_tab.png', modify_tab_btn_size)
        self.__del_tab_btn.clicked.connect(self.__on_del_tab_btn_clicked)
        modify_tab_h_layout.addWidget(self.__del_tab_btn)

        # tab filter line edit
        self.__line_edit_filter = QtWidgets.QLineEdit()
        self.__line_edit_filter.setPlaceholderText('filter searching tab node by name')
        self.__line_edit_filter.setMaximumSize(QtCore.QSize(1100, 30))
        self.__line_edit_filter.setStatusTip('type key words to search')
        self.__line_edit_filter.textChanged.connect(self.__on_filter_tab_edit_changed)

        main_v_layout.addLayout(modify_tab_h_layout)
        main_v_layout.addWidget(self.__line_edit_filter)
        # main tab
        self.__main_tab_widget = QtWidgets.QTabWidget()
        self.__main_tab_widget.setObjectName('main_tab')
        main_v_layout.addWidget(self.__main_tab_widget)

        # add sub tab to main tab
        self.__vex_py_tab = QtWidgets.QWidget()
        self.__node_preset_tab = QtWidgets.QWidget()
        self.__sop_tab = QtWidgets.QWidget()
        self.__file_manager_tab = QtWidgets.QWidget()
        self.__hda_tab = QtWidgets.QWidget()
        self.__main_tab_widget.addTab(self.__vex_py_tab, 'code_presets')
        self.__main_tab_widget.addTab(self.__node_preset_tab, 'node_presets')
        self.__main_tab_widget.addTab(self.__hda_tab, 'hda_presets')
        self.__main_tab_widget.addTab(self.__sop_tab, 'common_tools')
        self.__main_tab_widget.addTab(self.__file_manager_tab, 'file_manager')
        self.__main_tab_list = ['code_presets', 'node_presets', 'hda_presets', 'common_tools',
                                'file_manager']

        self.__add_tabs = []
        self.__all_main_tab_list = self.__main_tab_list + self.__add_tabs

    def __setup_vex_py_tab_widget_layout(self) -> None:
        vex_py_tab_v_layout = QtWidgets.QVBoxLayout(self.__vex_py_tab)
        vex_py_tab_h_layout = QtWidgets.QHBoxLayout(self.__vex_py_tab)

        # vex python code button
        self.__vex_py_tab_add_btn = QtWidgets.QPushButton('add')
        self.__vex_py_tab_import_btn = QtWidgets.QPushButton('import')
        self.__vex_py_tab_update_btn = QtWidgets.QPushButton('update')
        self.__vex_py_tab_delete_btn = QtWidgets.QPushButton('delete')
        tool_widget_utility_func.set_widget_icon(self.__vex_py_tab_add_btn, 'add_btn', None)
        tool_widget_utility_func.set_widget_icon(self.__vex_py_tab_import_btn, 'import_btn', None)
        tool_widget_utility_func.set_widget_icon(self.__vex_py_tab_update_btn, 'update_btn', None)
        tool_widget_utility_func.set_widget_icon(self.__vex_py_tab_delete_btn, 'delete_btn', None)

        self.current_item = None
        self.code_type = 0
        self.code_path = None

        # vex python code button connect event
        self.__vex_py_tab_add_btn.clicked.connect(self.__on_vex_py_tab_add_btn_clicked)
        self.__vex_py_tab_import_btn.clicked.connect(self.__on_vex_py_tab_import_btn_clicked)
        self.__vex_py_tab_update_btn.clicked.connect(self.__on_vex_py_tab_update_btn_clicked)
        self.__vex_py_tab_delete_btn.clicked.connect(self.__on_vex_py_tab_delete_btn_clicked)

        self.__vex_py_tab_add_btn.setStatusTip('add new code info to list widget')
        self.__vex_py_tab_import_btn.setStatusTip('import code info to list widget')
        self.__vex_py_tab_update_btn.setStatusTip('update code info to list widget')
        self.__vex_py_tab_delete_btn.setStatusTip('delete code info from list widget')

        # vex python code main ui
        self.__vex_py_tab_list_widget = QtWidgets.QListWidget()
        self.__vex_py_tab_list_widget.itemClicked.connect(self.__on_vex_py_tab_list_selection_change)
        self.__vex_py_tab_code_name = QtWidgets.QLineEdit()
        self.__vex_py_tab_code_name.setReadOnly(True)
        self.__vex_py_tab_code_info = QtWidgets.QPlainTextEdit()
        self.__vex_py_tab_code_info.setReadOnly(True)

        # vex python code type combo box
        self.__vex_py_tab_code_type_combo_box = QtWidgets.QComboBox()
        self.__vex_py_tab_code_type_combo_box.addItem('vex')
        self.__vex_py_tab_code_type_combo_box.addItem('python')
        self.__vex_py_tab_code_type_combo_box.currentIndexChanged.connect(self.__setup_vex_py_tab_list_widget_info)

        # setup list widget info
        self.__setup_vex_py_tab_list_widget_info()

        # vex python code sub layout
        vex_py_tab_h_sub_layout = QtWidgets.QHBoxLayout()
        vex_py_tab_v_sub_layout = QtWidgets.QVBoxLayout()
        vex_py_tab_v_sub_layout_1 = QtWidgets.QVBoxLayout()
        vex_py_tab_v_sub_layout.addWidget(self.__vex_py_tab_code_name)
        vex_py_tab_v_sub_layout.addWidget(self.__vex_py_tab_code_info)
        vex_py_tab_h_sub_layout.addLayout(vex_py_tab_v_sub_layout)

        vex_py_tab_v_sub_layout_1.addWidget(self.__vex_py_tab_code_type_combo_box)
        vex_py_tab_v_sub_layout_1.addWidget(self.__vex_py_tab_list_widget)
        vex_py_tab_h_sub_layout.addLayout(vex_py_tab_v_sub_layout_1)

        vex_py_tab_h_layout.addWidget(self.__vex_py_tab_add_btn)
        vex_py_tab_h_layout.addWidget(self.__vex_py_tab_import_btn)
        vex_py_tab_h_layout.addWidget(self.__vex_py_tab_update_btn)
        vex_py_tab_h_layout.addWidget(self.__vex_py_tab_delete_btn)
        vex_py_tab_v_layout.addLayout(vex_py_tab_h_layout)
        vex_py_tab_v_layout.addLayout(vex_py_tab_h_sub_layout)

    def __setup_node_preset_widget_layout(self) -> None:
        node_preset_main_v_layout = QtWidgets.QVBoxLayout(self.__node_preset_tab)
        node_preset_main_h_layout = QtWidgets.QHBoxLayout(self.__node_preset_tab)

        self.__node_preset_tab_add_btn = QtWidgets.QPushButton('add')
        self.__node_preset_tab_import_btn = QtWidgets.QPushButton('import')
        self.__node_preset_tab_update_info_btn = QtWidgets.QPushButton('update info')
        self.__node_preset_tab_update_image_btn = QtWidgets.QPushButton('update image')
        self.__node_preset_tab_delete_btn = QtWidgets.QPushButton('delete')

        tool_widget_utility_func.set_widget_icon(self.__node_preset_tab_add_btn, 'add_btn', None)
        tool_widget_utility_func.set_widget_icon(self.__node_preset_tab_import_btn, 'import_btn', None)
        tool_widget_utility_func.set_widget_icon(self.__node_preset_tab_update_info_btn, 'update_btn', None)
        tool_widget_utility_func.set_widget_icon(self.__node_preset_tab_update_image_btn, 'update_image_btn', None)
        tool_widget_utility_func.set_widget_icon(self.__node_preset_tab_delete_btn, 'delete_btn', None)

        self.__node_preset_tab_list_widget = QtWidgets.QListWidget()
        self.__node_preset_tab_node_type_combo_box = QtWidgets.QComboBox()
        self.__node_preset_tab_node_type_combo_box.addItem('obj')
        self.__node_preset_tab_node_type_combo_box.addItem('sop')

        # node preset list
        self.__node_preset_tab_list_widget = QtWidgets.QListWidget()
        self.__node_preset_tab_screen_shot_label = CustomLabel.CustomLabel()
        label_value = 0
        label_value = 360 + int(120 * label_value / 100)
        self.__node_preset_tab_screen_shot_label.setMinimumSize(QtCore.QSize(label_value, label_value))
        self.__node_preset_tab_screen_shot_label.setMaximumSize(QtCore.QSize(label_value, label_value))
        self.__node_preset_tab_screen_shot_label.setScaledContents(True)
        self.__node_preset_tab_screen_shot_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.__node_preset_tab_screen_shot_label.setWordWrap(True)

        # node preset  type combo box
        self.__node_preset_tab_type_combo_box = QtWidgets.QComboBox()
        self.__node_preset_tab_type_combo_box.addItem('obj')
        self.__node_preset_tab_type_combo_box.addItem('sop')

        # node preset labels
        label_name = QtWidgets.QLabel('Author:')
        label_name.setMaximumSize(QtCore.QSize(180, 17))
        label_name.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        label_name.setStyleSheet('color:rgb(255,255,0)')
        font = QtGui.QFont()
        font.setPointSize(10)
        label_name.setFont(font)

        self.__node_preset_tab_label_name = QtWidgets.QLabel('')
        self.__node_preset_tab_label_name.setMaximumSize(QtCore.QSize(180, 17))
        self.__node_preset_tab_label_name.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        label_remark = QtWidgets.QLabel('remark:')
        label_remark.setMaximumSize(QtCore.QSize(180, 17))
        label_remark.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        label_remark.setStyleSheet('color:rgb(255,255,0)')
        font = QtGui.QFont()
        font.setPointSize(10)
        label_remark.setFont(font)

        self.__node_preset_tab_label_remark = QtWidgets.QLabel('info')
        self.__node_preset_tab_label_remark.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.__node_preset_tab_label_remark.setWordWrap(True)
        self.__node_preset_tab_label_remark.setMaximumSize(QtCore.QSize(180, 300))

        # connect event
        self.__node_preset_tab_add_btn.clicked.connect(self.__on_node_preset_tab_add_btn_clicked)
        self.__node_preset_tab_import_btn.clicked.connect(self.__on_node_preset_tab_import_btn_clicked)
        self.__node_preset_tab_update_image_btn.clicked.connect(self.__on_node_preset_tab_update_image_btn_clicked)
        self.__node_preset_tab_update_info_btn.clicked.connect(self.__on_node_preset_tab_update_info_btn_clicked)
        self.__node_preset_tab_delete_btn.clicked.connect(self.__on_node_preset_tab_delete_btn_clicked)
        self.__node_preset_tab_type_combo_box.currentIndexChanged.connect(
            self.__setup_node_preset_tab_list_widget_info)
        self.__node_preset_tab_list_widget.itemClicked.connect(self.__on_node_preset_tab_list_selection_change)

        # layout
        node_preset_main_h_layout.addWidget(self.__node_preset_tab_add_btn)
        node_preset_main_h_layout.addWidget(self.__node_preset_tab_import_btn)
        node_preset_main_h_layout.addWidget(self.__node_preset_tab_update_info_btn)
        node_preset_main_h_layout.addWidget(self.__node_preset_tab_update_image_btn)
        node_preset_main_h_layout.addWidget(self.__node_preset_tab_delete_btn)

        node_preset_tab_v_sub_layout = QtWidgets.QVBoxLayout()
        node_preset_tab_h_sub_layout = QtWidgets.QHBoxLayout()
        node_preset_tab_v_sub_layout_1 = QtWidgets.QVBoxLayout()
        node_preset_tab_v_sub_layout_1.addWidget(self.__node_preset_tab_type_combo_box)
        node_preset_tab_v_sub_layout_1.addWidget(self.__node_preset_tab_list_widget)

        node_preset_tab_h_label_layout = QtWidgets.QHBoxLayout()
        node_preset_tab_v_label_layout = QtWidgets.QVBoxLayout()

        node_preset_tab_h_label_layout.addWidget(label_name)
        node_preset_tab_h_label_layout.addWidget(self.__node_preset_tab_label_name)
        node_preset_tab_h_label_layout.addWidget(label_remark)
        node_preset_tab_h_label_layout.addWidget(self.__node_preset_tab_label_remark)
        node_preset_tab_v_label_layout.addWidget(self.__node_preset_tab_screen_shot_label)
        node_preset_tab_v_label_layout.addLayout(node_preset_tab_h_label_layout)

        node_preset_main_v_layout.addLayout(node_preset_main_h_layout)
        node_preset_tab_h_sub_layout.addLayout(node_preset_tab_v_label_layout)
        node_preset_tab_h_sub_layout.addLayout(node_preset_tab_v_sub_layout_1)
        node_preset_tab_v_sub_layout.addLayout(node_preset_tab_h_sub_layout)
        node_preset_main_v_layout.addLayout(node_preset_tab_v_sub_layout)

    def __setup_file_manager_tab_widget_layout(self) -> None:
        """
            File Manager Tab Main UI
        :return: None
        """
        file_manager_main_v_layout = QtWidgets.QVBoxLayout(self.__file_manager_tab)
        file_manager_main_h_layout = QtWidgets.QHBoxLayout(self.__file_manager_tab)

        self.__file_manager_tab_add_btn = QtWidgets.QPushButton('add')
        self.__file_manager_tab_import_btn = QtWidgets.QPushButton('import/open')
        self.__file_manager_tab_update_btn = QtWidgets.QPushButton('update')
        self.__file_manager_tab_delete_btn = QtWidgets.QPushButton('delete')

        tool_widget_utility_func.set_widget_icon(self.__file_manager_tab_add_btn, 'add_btn', None)
        tool_widget_utility_func.set_widget_icon(self.__file_manager_tab_import_btn, 'import_btn', None)
        tool_widget_utility_func.set_widget_icon(self.__file_manager_tab_update_btn, 'update_btn', None)
        tool_widget_utility_func.set_widget_icon(self.__file_manager_tab_delete_btn, 'delete_btn', None)

        self.__file_manager_tab_add_btn.clicked.connect(self.__on_file_manager_tab_add_btn_clicked)

        file_manager_main_h_layout.addWidget(self.__file_manager_tab_add_btn)
        file_manager_main_h_layout.addWidget(self.__file_manager_tab_import_btn)
        file_manager_main_h_layout.addWidget(self.__file_manager_tab_update_btn)
        file_manager_main_h_layout.addWidget(self.__file_manager_tab_delete_btn)

        self.__file_manager_tree_view_widget = QtWidgets.QTreeView()
        self.model = QtGui.QStandardItemModel(self)
        # 设置表头信息
        self.model = QtGui.QStandardItemModel(self)
        self.model.setHorizontalHeaderLabels(['Item', 'info'])
        #
        # # 添加条目
        # itemProject = QtGui.QStandardItem('Project')
        # model.appendRow(itemProject)
        # model.setItem(0, 1, QtGui.QStandardItem('Project info'))
        #
        # # 添加子条目
        # itemChild = QtGui.QStandardItem('Folder1')
        # itemProject.appendRow(itemChild)
        # itemProject.setChild(0, 1, QtGui.QStandardItem('Folder info'))
        #
        # # 继续添加
        # itemFolder = QtGui.QStandardItem('Folder2')
        # itemProject.appendRow(itemFolder)
        # for group in range(5):
        #     itemGroup = QtGui.QStandardItem('group{}'.format(group + 1))
        #     itemFolder.appendRow(itemGroup)
        #     for ch in range(group + 1):
        #         itemCh = QtGui.QStandardItem('member{}'.format(ch + 1))
        #         # 添加复选框
        #         itemCh.setCheckable(True)
        #         itemGroup.appendRow(itemCh)
        #         itemGroup.setChild(itemCh.index().row(), 1, QtGui.QStandardItem('member{}info'.format(ch + 1)))
        # itemProject.setChild(itemFolder.index().row(), 1, QtGui.QStandardItem('Folder2 info'))

        treeView = self.__file_manager_tree_view_widget
        treeView.setModel(self.model)
        # 调整第一列的宽度
        treeView.header().resizeSection(0, 160)
        # 设置成有虚线连接的方式
        treeView.setStyle(QtWidgets.QStyleFactory.create('windows'))
        # 完全展开
        treeView.expandAll()

        file_manager_main_v_layout.addLayout(file_manager_main_h_layout)
        file_manager_main_v_layout.addWidget(self.__file_manager_tree_view_widget)

    def __read_config_value(self, key) -> str:
        """
        :param key: the key of config
        :return: if contain key , return current value
        """
        with open(tool_path_manager.config_path, 'r') as (f):
            config_dict = json.load(f)
        if key in config_dict.keys():
            result = None
            try:
                result = tool_config_manager.get_config_value_by_key(config_dict, key)
            except:
                print("something wrong when get config value by key: %s" % key)
            else:
                return result

    def __on_refresh_toolbar_btn_clicked(self) -> None:
        self.__setup_node_preset_tab_list_widget_info()

    def __on_config_toolbar_btn_clicked(self) -> None:
        print('config toolbar btn clicked!')

    def __on_file_location_toolbar_btn_clicked(self) -> None:
        main_tab_index = self.__main_tab_widget.currentIndex()
        if main_tab_index == 1:
            os.startfile(tool_path_manager.vex_node_preset_folder_path)
        elif main_tab_index == 2:
            os.startfile(tool_path_manager.python_node_preset_folder_path)
        else:
            os.startfile(tool_path_manager.env_path)

    def __on_help_toolbar_btn_clicked(self) -> None:
        print('help toolbar btn clicked!')

    def __on_scale_toolbar_btn_clicked(self) -> None:
        current_window_size = self.geometry()
        if current_window_size.height() > 61:
            self.__height = current_window_size.height()
            self.__width = current_window_size.width()
            self.__main_widget.setVisible(False)
            self.setFixedSize(350, 60)
            tool_widget_utility_func.set_widget_icon(self.__scale_toolbar_btn, '/max.png', QtCore.QSize(50, 50))
            self.__scale_toolbar_btn.setStatusTip('set window size scale up hotkey:F3')
            self.__refresh_toolbar_btn.setEnabled(False)
            self.__help_toolbar_btn.setEnabled(False)
            self.__file_location_toolbar_btn.setEnabled(False)
            self.__config_toolbar_btn.setEnabled(False)
        else:
            self.setMaximumSize(QtCore.QSize(980, 730))
            self.__main_widget.setVisible(True)
            self.setGeometry(current_window_size.x(), current_window_size.y(), self.__width, self.__height)
            tool_widget_utility_func.set_widget_icon(self.__scale_toolbar_btn, '/min.png', QtCore.QSize(50, 50))
            self.__scale_toolbar_btn.setStatusTip('set window size scale down hotkey:F5')
            self.__refresh_toolbar_btn.setEnabled(True)
            self.__help_toolbar_btn.setEnabled(True)
            self.__file_location_toolbar_btn.setEnabled(True)
            self.__config_toolbar_btn.setEnabled(True)

    def __on_add_tab_btn_clicked(self) -> None:
        print('add tab btn clicked!')

    def __on_del_tab_btn_clicked(self) -> None:
        print('del tab btn clicked!')

    def __on_filter_tab_edit_changed(self) -> None:
        print('filter tab edit changed!')

    def __on_add_tab_node_btn_clicked(self) -> None:
        print('add tab node btn clicked!')

    def __on_vex_py_tab_add_btn_clicked(self) -> None:
        main_window = hou.qt.mainWindow().findChild(QtWidgets.QMainWindow, 'toolbox')
        sub_window = main_window.findChild(QtWidgets.QWidget, 'save_vex_py_node_info')
        if sub_window is None:
            ex = SaveVexPyNodeInfo.SaveVexPyNodeInfo()
            ex.setParent(self, QtCore.Qt.Window)
            ex.show()
        return

    def __setup_vex_py_tab_list_widget_info(self) -> None:
        self.__vex_py_tab_list_widget.clear()
        self.code_type = self.__vex_py_tab_code_type_combo_box.currentIndex()
        self.code_path = tool_widget_utility_func.get_current_code_path_by_combo_box_index(self.code_type)

        tool_widget_utility_func.add_code_info_to_list_widget(self.__vex_py_tab_list_widget, self.code_path)

    def __on_vex_py_tab_list_selection_change(self) -> None:
        self.current_item = self.__vex_py_tab_list_widget.currentItem()

        code_info = tool_widget_utility_func.get_code_info_by_current_list_widget_item(self.code_path,
                                                                                       self.current_item)
        self.__vex_py_tab_code_name.setText(code_info[0])
        self.__vex_py_tab_code_info.setPlainText(code_info[1])

    def __on_vex_py_tab_import_btn_clicked(self) -> None:
        if self.current_item is None:
            self.current_item = self.__vex_py_tab_list_widget.currentItem()
        code_info = tool_widget_utility_func.get_code_info_by_current_list_widget_item(self.code_path,
                                                                                       self.current_item)

        tool_hou_node_utility_func.import_code_to_houdini_by_code_info(code_info, self.code_type)

    def __on_vex_py_tab_update_btn_clicked(self) -> None:
        SaveVexPyNodeInfo.SaveVexPyNodeInfo.update_code_by_select_node_info(self.current_item, self.code_type)
        self.__setup_vex_py_tab_list_widget_info()

    def __on_vex_py_tab_delete_btn_clicked(self) -> None:
        SaveVexPyNodeInfo.SaveVexPyNodeInfo.delete_select_code_info(self.current_item, self.code_type)
        self.__setup_vex_py_tab_list_widget_info()

    def __on_node_preset_tab_add_btn_clicked(self) -> None:
        main_window = hou.qt.mainWindow().findChild(QtWidgets.QMainWindow, 'toolbox')
        sub_window = main_window.findChild(QtWidgets.QWidget, 'save_node_preset_info')
        if sub_window is None:
            ex = SaveNodePresetInfo.SaveNodePresetInfo()
            ex.setParent(self, QtCore.Qt.Window)
            ex.is_update_node_preset(False)
            ex.show()
        return

    def __setup_node_preset_tab_list_widget_info(self) -> None:
        self.__node_preset_tab_list_widget.clear()
        self.node_type = self.__node_preset_tab_type_combo_box.currentText()

        self.node_path = tool_path_manager.node_preset_path
        tool_widget_utility_func.add_node_preset_info_to_list_widget(self.__node_preset_tab_list_widget,
                                                                     self.node_path,
                                                                     self.node_type)

    def __on_node_preset_tab_import_btn_clicked(self) -> None:
        self.current_item = self.__node_preset_tab_list_widget.currentItem()
        node_info = tool_widget_utility_func.create_node_preset_info_by_current_list_widget_item(self.node_path,
                                                                                                 self.current_item,
                                                                                                 self.node_type)

    def __on_node_preset_tab_list_selection_change(self) -> None:
        self.current_item = self.__node_preset_tab_list_widget.currentItem()
        image_path = tool_widget_utility_func.get_node_image_path_by_current_list_widget_item(
            self.node_path,
            self.current_item,
            self.node_type)
        self.__node_preset_tab_screen_shot_label.setPixmap(QtGui.QPixmap(image_path))
        info_list = tool_widget_utility_func.get_node_remark_info_by_current_list_widget_item(
            self.node_path,
            self.current_item,
            self.node_type)
        if info_list:
            author = info_list[0]
            remark = info_list[1]
            self.__node_preset_tab_label_name.setText(author)
            self.__node_preset_tab_label_remark.setText(remark)

    def __on_node_preset_tab_update_image_btn_clicked(self) -> None:
        self.current_item = self.__node_preset_tab_list_widget.currentItem()
        self.node_type = self.__node_preset_tab_type_combo_box.currentText()
        SaveNodePresetInfo.SaveNodePresetInfo.update_screen_shot(self.current_item,
                                                                 self.node_type)

    def __on_node_preset_tab_update_info_btn_clicked(self) -> None:
        self.current_item = self.__node_preset_tab_list_widget.currentItem()
        if self.current_item:
            name = self.current_item.text()
            main_window = hou.qt.mainWindow().findChild(QtWidgets.QMainWindow, 'toolbox')
            sub_window = main_window.findChild(QtWidgets.QWidget, 'update_node_preset_info')
            if sub_window is None:
                ex = SaveNodePresetInfo.SaveNodePresetInfo()
                ex.setParent(self, QtCore.Qt.Window)
                ex.is_update_node_preset(True, self.node_type, name)
                ex.show()
            return
        else:
            QtWidgets.QMessageBox.about(self, 'warning', 'please select node to update')

    def __on_node_preset_tab_delete_btn_clicked(self) -> None:
        list_widget = self.__node_preset_tab_list_widget
        self.node_type = self.__node_preset_tab_type_combo_box.currentText()
        SaveNodePresetInfo.SaveNodePresetInfo.delete_node_preset(list_widget, self.node_type)

    def __on_file_manager_tab_add_btn_clicked(self) -> None:
        main_window = hou.qt.mainWindow().findChild(QtWidgets.QMainWindow, 'toolbox')
        sub_window = main_window.findChild(QtWidgets.QWidget, 'save_file_manager_info')
        if sub_window is None:
            ex = SaveFileManagerInfo.SaveFileManagerInfo()
            ex.setParent(self, QtCore.Qt.Window)
            ex.show()
        return

    def keyPressEvent(self, event) -> None:
        """
            :param event:  if press Escape close window
            :return: None
            """
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
