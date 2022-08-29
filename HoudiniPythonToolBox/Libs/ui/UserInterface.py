import json
import os
from imp import reload

import hou
from PySide2 import QtCore, QtWidgets, QtGui

from Libs.config import SaveVexPyNodeInfo, SaveNodePresetInfo, SaveFileManagerInfo, SaveCommonToolNodeInfo, SaveHdaInfo
from Libs.config import ToolConfigManager
from Libs.path import ToolPathManager
from Libs.ui import CustomLabel, CustomButton
from Libs.utilities import ToolUtilityClasses
# from qt_material import apply_stylesheet
import webbrowser

reload(ToolPathManager)
reload(ToolConfigManager)
reload(CustomLabel)
reload(CustomButton)
reload(SaveVexPyNodeInfo)
reload(SaveNodePresetInfo)
reload(SaveFileManagerInfo)
reload(SaveCommonToolNodeInfo)
reload(SaveHdaInfo)
reload(ToolUtilityClasses)

tool_path_manager = ToolPathManager.ToolPath()
tool_config_manager = ToolConfigManager.ToolConfig()
tool_widget_utility_func = ToolUtilityClasses.SetWidgetInfo
tool_hou_node_utility_func = ToolUtilityClasses.HouNodesUtilities
tool_error_info = ToolUtilityClasses.ExceptionInfoWidgetClass()


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

        # current select file dir to open file
        self.current_select_file_dir = None

        # if current select file dir is houdini file
        self.__current_hip_file_path_from_file_manager = None

        # current select file name by tree view
        self.current_select_file_name = None

        # current select file extension by tree view
        self.current_select_file_type = None

        # current select file marker by tree view
        self.current_select_file_marker = None

        # current select file parent folder by tree view
        self.current_select_file_folder = None

        # current select file belongs which project by tree view
        self.current_select_file_project = None

        # previous select tool type button list
        self.previous_common_tool_btn_list = []

        # all types of button
        self.button_type_list = ['Common', 'Obj', 'Sop', 'Dop', 'Top', 'Kine_fx', 'Solaris']

        # all types of nodes
        self.node_type_list = ['obj', 'sop', 'vop', 'dop', 'top']

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

        # common tools btn main layout
        self.__setup_common_tools_tab_widget_layout()

        # hda preset tab main layout
        self.__setup_hda_preset_tab_widget_layout()

    def __setup_tool_bar_widget_layout(self) -> None:
        """
            Tool Bar UI Layout
        :return:
        """
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

        # common tool btn node add btn
        self.__common_tool_node_add_btn = QtWidgets.QToolButton(tool_bar)
        tool_widget_utility_func.set_widget_icon(self.__common_tool_node_add_btn, 'add_tab_node.png', tool_bar_btn_size)
        self.__common_tool_node_add_btn.setShortcut('F6')
        self.__common_tool_node_add_btn.clicked.connect(self.__common_tool_node_add_btn_clicked)
        self.__common_tool_node_add_btn.setStatusTip('create a new tab node')
        tool_bar.addWidget(self.__common_tool_node_add_btn)

    def __setup_main_tab_widget_layout(self) -> None:
        """
            Main Tab UI Layout
        :return:
        """
        main_v_layout = QtWidgets.QVBoxLayout(self.__main_widget)
        main_v_layout.setContentsMargins(1, 1, 1, 1)

        # modify tab widgets
        modify_tab_h_layout = QtWidgets.QHBoxLayout()

        # tab filter line edit
        self.__line_edit_filter = QtWidgets.QLineEdit()
        self.__line_edit_filter.setPlaceholderText('filter searching tab node by name')
        self.__line_edit_filter.setMaximumSize(QtCore.QSize(1100, 50))
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
        self.__common_tools_tab = QtWidgets.QWidget()
        self.__file_manager_tab = QtWidgets.QWidget()
        self.__hda_tab = QtWidgets.QWidget()
        self.__main_tab_widget.addTab(self.__vex_py_tab, 'code_presets')
        self.__main_tab_widget.addTab(self.__node_preset_tab, 'node_presets')
        self.__main_tab_widget.addTab(self.__hda_tab, 'hda_presets')
        self.__main_tab_widget.addTab(self.__common_tools_tab, 'common_tools')
        self.__main_tab_widget.addTab(self.__file_manager_tab, 'file_manager')
        self.__main_tab_list = ['code_presets', 'node_presets', 'hda_presets', 'common_tools',
                                'file_manager']

        self.__add_tabs = []
        self.__all_main_tab_list = self.__main_tab_list + self.__add_tabs

    def __setup_vex_py_tab_widget_layout(self) -> None:
        """
            Code Preset Tab Main UI Layout
        :return:
        """
        vex_py_tab_v_layout = QtWidgets.QVBoxLayout(self.__vex_py_tab)
        vex_py_tab_h_layout = QtWidgets.QHBoxLayout(self.__vex_py_tab)

        # vex python code button
        self.__vex_py_tab_add_btn = QtWidgets.QPushButton('add code')
        self.__vex_py_tab_import_btn = QtWidgets.QPushButton('import code')
        self.__vex_py_tab_update_btn = QtWidgets.QPushButton('update code info')
        self.__vex_py_tab_delete_btn = QtWidgets.QPushButton('delete code')
        tool_widget_utility_func.set_widget_icon(self.__vex_py_tab_add_btn, 'add_btn')
        tool_widget_utility_func.set_widget_icon(self.__vex_py_tab_import_btn, 'import_btn')
        tool_widget_utility_func.set_widget_icon(self.__vex_py_tab_update_btn, 'update_btn')
        tool_widget_utility_func.set_widget_icon(self.__vex_py_tab_delete_btn, 'delete_btn')

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
        self.__vex_py_tab_code_tag = ToolUtilityClasses.CheckableComboBox()
        self.__vex_py_tab_code_tag.model().dataChanged.connect(self.on_vex_py_tab_code_tag_changed)
        self.__vex_py_tab_code_info = QtWidgets.QPlainTextEdit()
        self.__vex_py_tab_code_info.setReadOnly(True)

        # vex python code type combo box
        self.__vex_py_tab_code_type_combo_box = QtWidgets.QComboBox()
        self.__vex_py_tab_code_type_combo_box.addItem('vex')
        self.__vex_py_tab_code_type_combo_box.addItem('python')
        self.__vex_py_tab_code_type_combo_box.currentIndexChanged.connect(self.__setup_vex_py_tab_list_widget_info)

        # setup list widget info
        self.__setup_vex_py_tab_list_widget_info()
        self.__refresh_vex_py_tab_code_tags()

        # vex python code sub layout
        vex_py_tab_h_sub_layout = QtWidgets.QHBoxLayout()
        vex_py_tab_v_sub_layout = QtWidgets.QVBoxLayout()
        vex_py_tab_v_sub_layout_1 = QtWidgets.QVBoxLayout()
        vex_py_tab_v_sub_layout.addWidget(self.__vex_py_tab_code_type_combo_box)
        vex_py_tab_v_sub_layout.addWidget(self.__vex_py_tab_code_info)
        vex_py_tab_h_sub_layout.addLayout(vex_py_tab_v_sub_layout)

        vex_py_tab_v_sub_layout_1.addWidget(self.__vex_py_tab_list_widget)
        vex_py_tab_v_sub_layout_1.addWidget(self.__vex_py_tab_code_tag)
        vex_py_tab_h_sub_layout.addLayout(vex_py_tab_v_sub_layout_1)

        vex_py_tab_h_layout.addWidget(self.__vex_py_tab_add_btn)
        vex_py_tab_h_layout.addWidget(self.__vex_py_tab_import_btn)
        vex_py_tab_h_layout.addWidget(self.__vex_py_tab_update_btn)
        vex_py_tab_h_layout.addWidget(self.__vex_py_tab_delete_btn)
        vex_py_tab_v_layout.addLayout(vex_py_tab_h_layout)
        vex_py_tab_v_layout.addLayout(vex_py_tab_h_sub_layout)

    def __setup_node_preset_widget_layout(self) -> None:
        """
            Node Preset Tab Main UI Layout
        :return:
        """
        node_preset_main_v_layout = QtWidgets.QVBoxLayout(self.__node_preset_tab)
        node_preset_main_h_layout = QtWidgets.QHBoxLayout(self.__node_preset_tab)

        self.__node_preset_tab_add_btn = QtWidgets.QPushButton('add node')
        self.__node_preset_tab_import_btn = QtWidgets.QPushButton('import node')
        self.__node_preset_tab_update_info_btn = QtWidgets.QPushButton('update  node info')
        self.__node_preset_tab_update_image_btn = QtWidgets.QPushButton('update node  image')
        self.__node_preset_tab_delete_btn = QtWidgets.QPushButton('delete node')

        tool_widget_utility_func.set_widget_icon(self.__node_preset_tab_add_btn, 'add_btn')
        tool_widget_utility_func.set_widget_icon(self.__node_preset_tab_import_btn, 'import_btn')
        tool_widget_utility_func.set_widget_icon(self.__node_preset_tab_update_info_btn, 'update_btn')
        tool_widget_utility_func.set_widget_icon(self.__node_preset_tab_update_image_btn, 'update_image_btn')
        tool_widget_utility_func.set_widget_icon(self.__node_preset_tab_delete_btn, 'delete_btn')

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
        for i in self.node_type_list:
            self.__node_preset_tab_type_combo_box.addItem(i)

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
        self.__node_preset_tab_label_remark.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
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
        self.__file_manager_tab_update_btn = QtWidgets.QPushButton('update')
        self.__file_manager_tab_delete_btn = QtWidgets.QPushButton('delete')

        tool_widget_utility_func.set_widget_icon(self.__file_manager_tab_add_btn, 'add_btn')
        tool_widget_utility_func.set_widget_icon(self.__file_manager_tab_update_btn, 'update_btn')
        tool_widget_utility_func.set_widget_icon(self.__file_manager_tab_delete_btn, 'delete_btn')

        self.__file_manager_tab_add_btn.clicked.connect(self.__on_file_manager_tab_add_btn_clicked)
        self.__file_manager_tab_update_btn.clicked.connect(self.__on_file_manager_tab_update_btn_clicked)
        self.__file_manager_tab_delete_btn.clicked.connect(self.__on_file_manager_tab_delete_btn_clicked)

        file_manager_main_h_layout.addWidget(self.__file_manager_tab_add_btn)
        file_manager_main_h_layout.addWidget(self.__file_manager_tab_update_btn)
        file_manager_main_h_layout.addWidget(self.__file_manager_tab_delete_btn)

        self.__file_manager_tree_view_widget = QtWidgets.QTreeView()
        self.__file_manager_tree_view_model = QtGui.QStandardItemModel(self)

        file_manager_main_v_layout.addLayout(file_manager_main_h_layout)
        file_manager_main_v_layout.addWidget(self.__file_manager_tree_view_widget)

        # contex menu
        self.__file_manager_tree_view_widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.__file_manager_tree_view_widget.customContextMenuRequested.connect(self.open_context_menu)

        self.__setup_file_manager_tree_view_info()

    def __setup_common_tools_tab_widget_layout(self) -> None:
        """
            Common Button Tool Tab Main UI Layout
        :return:
        """
        common_tool_main_v_layout = QtWidgets.QVBoxLayout(self.__common_tools_tab)

        self.__common_tool_btn_type_combo_box = QtWidgets.QComboBox()
        for btn in self.button_type_list:
            self.__common_tool_btn_type_combo_box.addItem(btn)
        self.__common_tool_btn_type_combo_box.currentIndexChanged.connect(self.__create_common_tools_btn)

        common_tools_grid_layout = QtWidgets.QGridLayout()
        common_tools_grid_layout.setContentsMargins(0, 0, 0, 0)
        common_tools_scroll_area = QtWidgets.QScrollArea()
        common_tools_scroll_area.setAutoFillBackground(True)
        common_tools_scroll_area.setWidgetResizable(True)
        common_tools_grid_layout.addWidget(common_tools_scroll_area)

        common_tools_scroll_area_content_widget = QtWidgets.QWidget()
        self.layout = QtWidgets.QGridLayout(common_tools_scroll_area_content_widget)
        common_tools_scroll_area.setWidget(common_tools_scroll_area_content_widget)

        common_tool_main_v_layout.addWidget(self.__common_tool_btn_type_combo_box)
        common_tool_main_v_layout.addLayout(common_tools_grid_layout)

        self.__create_common_tools_btn()

    def __setup_hda_preset_tab_widget_layout(self) -> None:
        """
            HDA Preset UI Main Layout
        :return:
        """
        hda_preset_main_v_layout = QtWidgets.QVBoxLayout(self.__hda_tab)
        hda_preset_main_h_layout = QtWidgets.QHBoxLayout()
        hda_preset_sub_v_layout = QtWidgets.QVBoxLayout()

        self.__hda_preset_tab_add_btn = QtWidgets.QPushButton('add hda')
        self.__hda_preset_tab_import_btn = QtWidgets.QPushButton('import hda')
        self.__hda_preset_tab_update_info_btn = QtWidgets.QPushButton('update hda marker')
        self.__hda_preset_tab_update_image_btn = QtWidgets.QPushButton('update hda image')
        self.__hda_preset_tab_delete_btn = QtWidgets.QPushButton('delete hda')

        tool_widget_utility_func.set_widget_icon(self.__hda_preset_tab_add_btn, 'add_btn')
        tool_widget_utility_func.set_widget_icon(self.__hda_preset_tab_import_btn, 'import_btn')
        tool_widget_utility_func.set_widget_icon(self.__hda_preset_tab_update_info_btn, 'update_btn')
        tool_widget_utility_func.set_widget_icon(self.__hda_preset_tab_update_image_btn, 'update_image_btn')
        tool_widget_utility_func.set_widget_icon(self.__hda_preset_tab_delete_btn, 'delete_btn')

        self.__hda_preset_tab_list_widget = QtWidgets.QListWidget()
        self.__hda_preset_tab_combo_box = QtWidgets.QComboBox()
        all_hda_file = os.listdir(tool_path_manager.hda_path)
        all_hda_folder = [x for x in all_hda_file if os.path.isdir(os.path.join(tool_path_manager.hda_path, x))]
        for folder in all_hda_folder:
            self.__hda_preset_tab_combo_box.addItem(folder)

        # screen shot
        self.__hda_preset_tab_screen_shot_label = CustomLabel.CustomLabel()
        label_value = 0
        label_value = 360 + int(120 * label_value / 100)
        self.__hda_preset_tab_screen_shot_label.setMinimumSize(QtCore.QSize(label_value, label_value))
        self.__hda_preset_tab_screen_shot_label.setMaximumSize(QtCore.QSize(label_value, label_value))
        self.__hda_preset_tab_screen_shot_label.setScaledContents(True)
        self.__hda_preset_tab_screen_shot_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.__hda_preset_tab_screen_shot_label.setWordWrap(True)

        # label

        label_remark = QtWidgets.QLabel('marker:')
        label_remark.setMaximumSize(QtCore.QSize(180, 17))
        label_remark.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        label_remark.setStyleSheet('color:rgb(255,255,0)')
        font = QtGui.QFont()
        font.setPointSize(10)
        label_remark.setFont(font)

        self.__hda_preset_tab_label_remark = QtWidgets.QLabel('info')
        self.__hda_preset_tab_label_remark.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.__hda_preset_tab_label_remark.setWordWrap(True)
        self.__hda_preset_tab_label_remark.setMaximumSize(QtCore.QSize(180, 300))

        # layout
        hda_preset_main_h_layout.addWidget(self.__hda_preset_tab_add_btn)
        hda_preset_main_h_layout.addWidget(self.__hda_preset_tab_import_btn)
        hda_preset_main_h_layout.addWidget(self.__hda_preset_tab_update_info_btn)
        hda_preset_main_h_layout.addWidget(self.__hda_preset_tab_update_image_btn)
        hda_preset_main_h_layout.addWidget(self.__hda_preset_tab_delete_btn)

        hda_preset_tab_v_sub_layout = QtWidgets.QVBoxLayout()
        hda_preset_tab_h_sub_layout = QtWidgets.QHBoxLayout()

        hda_preset_tab_h_label_layout = QtWidgets.QHBoxLayout()
        hda_preset_tab_v_label_layout = QtWidgets.QVBoxLayout()

        hda_preset_tab_h_label_layout.addWidget(label_remark)
        hda_preset_tab_h_label_layout.addWidget(self.__hda_preset_tab_label_remark)
        hda_preset_tab_v_label_layout.addWidget(self.__hda_preset_tab_screen_shot_label)
        hda_preset_tab_v_label_layout.addLayout(hda_preset_tab_h_label_layout)

        hda_preset_main_v_layout.addLayout(hda_preset_main_h_layout)

        hda_preset_sub_v_layout.addWidget(self.__hda_preset_tab_combo_box)
        hda_preset_sub_v_layout.addWidget(self.__hda_preset_tab_list_widget)

        hda_preset_tab_h_sub_layout.addLayout(hda_preset_sub_v_layout)
        hda_preset_tab_h_sub_layout.addLayout(hda_preset_tab_v_label_layout)
        hda_preset_tab_v_sub_layout.addLayout(hda_preset_tab_h_sub_layout)
        hda_preset_main_v_layout.addLayout(hda_preset_tab_v_sub_layout)

        # connect
        self.__hda_preset_tab_add_btn.clicked.connect(self.__hda_preset_tab_add_btn_clicked)
        self.__hda_preset_tab_list_widget.itemClicked.connect(self.__hda_preset_tab_list_widget_item_clicked)
        self.__hda_preset_tab_combo_box.currentIndexChanged.connect(
            self.__hda_preset_tab_combo_box_current_index_changed)
        self.__hda_preset_tab_update_image_btn.clicked.connect(self.__hda_preset_tab_update_screen_shot)
        self.__hda_preset_tab_update_info_btn.clicked.connect(self.__hda_preset_tab_update_marker_info)
        self.__hda_preset_tab_import_btn.clicked.connect(self.__hda_preset_tab_import_btn_clicked)
        self.__hda_preset_tab_delete_btn.clicked.connect(self.__hda_preset_tab_delete_btn_clicked)
        self.__hda_preset_tab_combo_box_current_index_changed()

    def __hda_preset_tab_delete_btn_clicked(self) -> None:
        """
            Delete Current Select HDA Preset
        :return:
        """
        list_widget = self.__hda_preset_tab_list_widget
        current_items = list_widget.selectedItems()
        if current_items:
            current_hda_folder = self.__hda_preset_tab_combo_box.currentText()
            result = QtWidgets.QMessageBox.warning(self, "warning",
                                                   "are you want to delete select hda presets? ",
                                                   QtWidgets.QMessageBox.Yes |
                                                   QtWidgets.QMessageBox.No)
            if result == QtWidgets.QMessageBox.Yes:
                for item in current_items:
                    hda_path = tool_path_manager.hda_path
                    hda_name = item.text()
                    full_hda_path = hda_path + '/' + current_hda_folder + '/' + hda_name + '.hda'
                    full_hda_path_otl = hda_path + '/' + current_hda_folder + '/' + hda_name + '.otl'
                    full_hda_image_path = hda_path + '/' + current_hda_folder + '/' + hda_name + '.jpg'
                    full_hda_json_path = hda_path + '/' + current_hda_folder + '/' + hda_name + '.json'

                    list_widget.takeItem(list_widget.row(item))

                    try:
                        hou.hda.uninstallFile(full_hda_path)
                        hou.hda.uninstallFile(full_hda_path_otl)
                    except:
                        tool_error_info.show_exception_info('warning',
                                                            'uninstall {} hda file may got wrong'.format(hda_name))
                    try:
                        os.remove(full_hda_path)
                    except:
                        try:
                            os.remove(full_hda_path_otl)
                        except:
                            tool_error_info.show_exception_info('warning',
                                                                'del {} hda file may got wrong'.format(hda_name))
                    try:
                        os.remove(full_hda_image_path)
                    except:
                        tool_error_info.show_exception_info('warning',
                                                            'del {} hda screen shot may got wrong'.format(hda_name))
                    try:
                        os.remove(full_hda_json_path)
                    except:
                        tool_error_info.show_exception_info('warning',
                                                            'del {} hda json file may got wrong'.format(hda_name))

        else:
            tool_error_info.show_exception_info('warning', 'please select a hda preset to delete')

    def __hda_preset_tab_import_btn_clicked(self) -> None:
        """
            Import Current Select HDA To Houdini
        :return:
        """
        list_widget = self.__hda_preset_tab_list_widget
        item = list_widget.currentItem()
        current_hda_folder = self.__hda_preset_tab_combo_box.currentText()
        if item:
            hda_path = tool_path_manager.hda_path + '/' + current_hda_folder
            hda_name = item.text()
            hda_full_path = hda_path + '/' + hda_name + '.hda'
            hda_full_path_otl = hda_path + '/' + hda_name + 'otl'
            installed = 0
            tab_name = None
            try:
                hou.hda.installFile(hda_full_path)
                info = hou.hda.definitionsInFile(hda_full_path)
                tab_name = info[0].nodeTypeName()
                installed = 1
            except:
                installed = 0
            if not installed:
                try:
                    hou.hda.installFile(hda_full_path_otl)
                    info = hou.hda.definitionsInFile(hda_full_path_otl)
                    tab_name = info[0].nodeTypeName()
                    installed = 1
                except:
                    installed = 0

            if installed == 1 and tab_name:
                plan = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
                pos = plan.selectPosition()
                upNode = plan.pwd()
                try:
                    hdaNode = upNode.createNode(tab_name)
                    hdaNode.setPosition(pos)
                except:
                    QtWidgets.QMessageBox.about(self, 'waring', 'hda create pane tab type is wrong')
            else:
                QtWidgets.QMessageBox.about(self, 'waring', 'hda create pane tab type is wrong')
        else:
            QtWidgets.QMessageBox.about(self, 'waring', 'please select a hda preset first')

    def __hda_preset_tab_add_btn_clicked(self) -> None:
        """
            Add HDA To Tool Preset
        :return:
        """
        main_window = hou.qt.mainWindow().findChild(QtWidgets.QMainWindow, 'toolbox')
        sub_window = main_window.findChild(QtWidgets.QWidget, 'savehdainfo')
        if sub_window is None:
            ex = SaveHdaInfo.SaveHdaInfo()
            ex.setParent(self, QtCore.Qt.Window)
            ex.show()
        else:
            tool_error_info.show_exception_info('warning', 'open savehdainfo window failed')

    def __load_hda_file_to_list_widget(self, path) -> None:
        """
            Create HDA Preset List Item With Specify Path
        :param path: Current Path Type Of HDA Preset
        :return:
        """
        list_widget = self.__hda_preset_tab_list_widget
        all_files = os.listdir(path)
        all_files = [x for x in all_files if os.path.isfile(path + '/' + x)]
        hda_files = [x for x in all_files if
                     x.split('.')[-1].lower().startswith('hda') or x.split('.')[-1].lower().startswith('otl')]
        for file in hda_files:
            item_name = '.'.join(file.split('.')[:-1])
            item = QtWidgets.QListWidgetItem()
            item.setText(item_name)
            item.setSizeHint(QtCore.QSize(200, 30))
            list_widget.addItem(item)
            # self.__allHdaItemNames.append(item_name)

    def __hda_preset_tab_combo_box_current_index_changed(self) -> None:
        """
            Refresh HDA Preset List Widget By Change Path Type
        :return:
        """
        current_hda_folder = self.__hda_preset_tab_combo_box.currentText()
        list_widget = self.__hda_preset_tab_list_widget
        list_widget.clear()
        hda_path = tool_path_manager.hda_path + '/' + current_hda_folder
        self.__load_hda_file_to_list_widget(hda_path)

    def __hda_preset_tab_update_screen_shot(self) -> None:
        """
            Update Current Select HDA Preset A Screen Shot
        :return:
        """
        item = self.__hda_preset_tab_list_widget.currentItem()
        current_folder = self.__hda_preset_tab_combo_box.currentText()
        if item:
            save_hda_info = SaveHdaInfo.SaveHdaInfo()
            save_hda_info.update_hda_screen_shot(item, current_folder)
        else:
            tool_error_info.show_exception_info('warning', 'please select a hda preset first')

    def __hda_preset_tab_update_marker_info(self) -> None:
        """
            Update Current Select HDA Preset Marker Info
        :return:
        """
        item = self.__hda_preset_tab_list_widget.currentItem()
        current_folder = self.__hda_preset_tab_combo_box.currentText()
        if item:
            main_window = hou.qt.mainWindow().findChild(QtWidgets.QMainWindow, 'toolbox')
            sub_window = main_window.findChild(QtWidgets.QWidget, 'updatehdamarker')
            if sub_window is None:
                ex = SaveHdaInfo.UpdateHdaMarker(hda_name=item.text(), path_type=current_folder)
                ex.setParent(self, QtCore.Qt.Window)
                ex.show()
            else:
                tool_error_info.show_exception_info('warning', 'open savehdainfo window failed')
        else:
            tool_error_info.show_exception_info('warning', 'please select a hda preset first')

    def __hda_preset_tab_list_widget_item_clicked(self) -> None:
        """
            hda preset list widget item clicked
        :param item:
        :return:
        """
        list_widget = self.__hda_preset_tab_list_widget
        current_item = list_widget.currentItem()
        if current_item:
            current_hda_folder = self.__hda_preset_tab_combo_box.currentText()
            hda_path = tool_path_manager.hda_path
            hda_name = current_item.text()
            image_path = hda_path + '/' + current_hda_folder + '/' + hda_name + '.jpg'
            if os.path.isfile(image_path):
                self.__hda_preset_tab_screen_shot_label.setPixmap(QtGui.QPixmap(image_path))
            else:
                self.__hda_preset_tab_screen_shot_label.setText(hda_name)
            json_path = hda_path + '/' + current_hda_folder + '/' + hda_name + '.json'
            marker_info = ''
            if os.path.isfile(json_path):
                with open(json_path, 'r') as f:
                    marker_info = json.load(f)
            else:
                marker_info = ''
            self.__hda_preset_tab_label_remark.setText(marker_info)

    def __create_common_tools_btn(self) -> None:
        """
            Create Tool Button To Grid Layout
        :return:
        """
        # current select button type
        btn_type = self.__common_tool_btn_type_combo_box.currentText()
        btn_name_dict = None
        btn_name_list_path = tool_path_manager.common_tools_btn_name_list_path
        btn_preset_path = tool_path_manager.common_tools_path
        with open(btn_name_list_path, 'r') as f:
            btn_name_dict = json.load(f)

        # load button file preset
        all_btn_files = os.listdir(btn_preset_path)
        btn_py_files = [x for x in all_btn_files if x.split('.')[-1].startswith('py')]

        # current tool button row number in grid layout
        btn_rows_number = 0

        # current tool button column number in grid layout
        btn_columns_number = 0

        self.btn_label_to_object_dict = {}

        for i in self.previous_common_tool_btn_list:
            i.deleteLater()  # delete previous type button when type changed

        self.previous_common_tool_btn_list = []

        for file in btn_py_files:
            if file.startswith(btn_type):
                btn_info_name = file.split('.')[0] + '.json'
                btn_tool_json_path = tool_path_manager.common_tools_path + '/' + btn_info_name
                btn_info = None
                try:
                    with open(btn_tool_json_path, 'r') as f:
                        btn_info = json.load(f)
                except:
                    tool_error_info.show_exception_info('error', 'load {} file got wrong'.format(btn_info_name))
                    print(btn_tool_json_path)
                else:
                    # create custom button
                    common_tool_btn = CustomButton.CustomButton()

                    # json info
                    btn_tool_tip = btn_info['tips']
                    btn_label_name = btn_info['label_name']
                    btn_object_name = btn_info['object_name']
                    btn_icon_name = btn_info['icon_name']
                    self.btn_label_to_object_dict[btn_label_name] = btn_type + '_' + btn_object_name

                    # tool tip
                    common_tool_btn.setStatusTip(btn_tool_tip)

                    # icon
                    icon_path = tool_path_manager.icon_path + '/' + btn_icon_name
                    if not os.path.isfile(icon_path):
                        btn_icon_name = 'common_tool'
                    tool_widget_utility_func.set_widget_icon(common_tool_btn, btn_icon_name)

                    # set custom button ui
                    common_tool_btn.setText(btn_label_name)
                    common_tool_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
                    common_tool_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                    common_tool_btn.resize(QtCore.QSize(80, 80))
                    common_tool_btn.setMinimumSize(QtCore.QSize(81, 68))
                    common_tool_btn.setMaximumSize(QtCore.QSize(220, 85))
                    common_tool_btn.setAutoRaise(True)

                    # connect
                    common_tool_btn._leftClicked.connect(self.__common_btn_start_work)  # 不希望每次创建按钮的时候导入模块用到这句
                    common_tool_btn._rightClicked.connect(self.__common_btn_delete)
                    self.layout.addWidget(common_tool_btn, btn_columns_number, btn_rows_number, 1, 1)
                    self.previous_common_tool_btn_list.append(common_tool_btn)
                    btn_rows_number += 1
                    # how many buttons in one row
                    if btn_rows_number % 4 == 0:
                        btn_columns_number += 1
                        btn_rows_number = 0

    def __common_btn_start_work(self) -> None:
        """
            Execute Tool Button Python Code
        :return:
        """
        # current select button label name
        btn_name = self.sender().text()
        # get button object name by label name
        btn_code_module = self.btn_label_to_object_dict[btn_name]
        exec('from Presets.CommonTools import ' + btn_code_module)
        exec('reload(' + btn_code_module + ')')
        exec(btn_code_module + '.start_work()')

    def __common_btn_delete(self) -> None:
        """
            Delete Common Tool Button
        :return:
        """
        tool_error_info.show_exception_info('warning', 'Doing')

    def __read_config_value(self, key: dict.keys) -> str:
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
        """
            Refresh All Tab UI Info
        :return:
        """
        main_tab_index = self.__main_tab_widget.currentIndex()
        if main_tab_index == 0:  # code info preset tab
            self.__setup_vex_py_tab_list_widget_info()
            self.__refresh_vex_py_tab_code_tags()
        elif main_tab_index == 1:  # node presets tab
            self.__setup_node_preset_tab_list_widget_info()
        elif main_tab_index == 2:  # hda presets tab
            self.__hda_preset_tab_combo_box_current_index_changed()
        elif main_tab_index == 3:  # common tools tab
            self.__setup_common_tools_tab_widget_layout()
        elif main_tab_index == 4:  # file manager tab
            self.__setup_file_manager_tree_view_info()

    def __on_config_toolbar_btn_clicked(self) -> None:
        """
            Modify Tool Configs
        :return:
        """
        main_window = hou.qt.mainWindow().findChild(QtWidgets.QMainWindow, 'toolbox')
        sub_window = main_window.findChild(QtWidgets.QWidget, 'toolconfig')
        if sub_window is None:
            ex = ToolConfigManager.ToolConfigManager()
            ex.setParent(self, QtCore.Qt.Window)
            # style_file = './style.qss'
            # style_sheet = ToolConfigManager.QSSLoader.read_qss_file(style_file)
            # ex.setStyleSheet(style_sheet)
            # apply_stylesheet(ex, theme='dark_teal.xml')
            ex.show()

    def __on_file_location_toolbar_btn_clicked(self) -> None:
        """
            Open Current File By Tab Type And Current Selected
        :return:
        """
        main_tab_index = self.__main_tab_widget.currentIndex()
        if main_tab_index == 0:  # code info preset tab
            os.startfile(tool_path_manager.code_preset_path)
        elif main_tab_index == 1:  # node presets tab
            os.startfile(tool_path_manager.node_preset_path)
        else:
            os.startfile(tool_path_manager.env_path)

    def __on_help_toolbar_btn_clicked(self) -> None:
        """
            Show Tool Help Doc
        :return:
        """
        confluence_url = 'http://confluence.oa.zulong.com/display/EngineHub/Houdini+Python+Tools'
        webbrowser.open(confluence_url)

    def __on_scale_toolbar_btn_clicked(self) -> None:
        """
            Make Tool Box Main UI Scaled To Min or Max
        :return:
        """
        current_window_size = self.geometry()
        # current is max size
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
            self.__common_tool_node_add_btn.setEnabled(False)
        # current is min size
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
            self.__common_tool_node_add_btn.setEnabled(True)

    def search_text_in_list_widget(self, list_widget: QtWidgets.QListWidget, text: str) -> None:
        """
            Search Current Text In List Widget, If Match Text, Select Current List Widget Item
        :param list_widget: List Widget To Search
        :param text: Target Text
        """
        model = list_widget.model()
        match = model.match(model.index(0, list_widget.modelColumn()), QtCore.Qt.DisplayRole, text,
                            flags=QtCore.Qt.MatchContains)
        if match:
            list_widget.setCurrentIndex(match[0])

    def search_item(self) -> None:
        """
            Search Current Text In Tree View, If Match Text, Select Current Item
        """
        filter_text = self.__line_edit_filter.text()
        if filter_text:
            result = self.__file_manager_tree_view_model.findItems(filter_text,
                                                                   flags=QtCore.Qt.MatchExactly |
                                                                         QtCore.Qt.MatchRecursive |
                                                                         QtCore.Qt.MatchStartsWith)
            for i in result:
                item = self.__file_manager_tree_view_model.indexFromItem(i)
                self.__file_manager_tree_view_widget.selectionModel().select(item, QtCore.QItemSelectionModel.Select)
        else:
            self.__file_manager_tree_view_widget.selectionModel().clear()

    def change_vex_py_tag_combo_by_str(self, tag: str) -> None:
        """
            If Combo Box Text List Has Current Tag, Change Current Combo Tex To Specify Tag
        :param tag:
        """
        if tag:
            self.__vex_py_tab_code_tag.update_check_state_by_str(tag)

    def __on_filter_tab_edit_changed(self) -> None:
        """
            Filter UI Info By Tab Type
        :return:
        """
        filter_text = self.__line_edit_filter.text()
        main_tab_index = self.__main_tab_widget.currentIndex()
        if main_tab_index == 0:  # code info preset tab

            self.search_text_in_list_widget(self.__vex_py_tab_list_widget, filter_text)
            self.__on_vex_py_tab_list_selection_change()
            if filter_text.lower().startswith('t:'):
                filter_text = filter_text[2:]
                self.change_vex_py_tag_combo_by_str(filter_text)
        elif main_tab_index == 1:  # node preset tab
            self.search_text_in_list_widget(self.__node_preset_tab_list_widget, filter_text)
            self.__on_node_preset_tab_list_selection_change()
        elif main_tab_index == 2:  # hda preset tab
            self.search_text_in_list_widget(self.__hda_preset_tab_list_widget, filter_text)
            self.__hda_preset_tab_list_widget_item_clicked()
        elif main_tab_index == 4:  # file manager tab
            self.search_item()

    def __common_tool_node_add_btn_clicked(self) -> None:
        """
            Abort a Window To Dump New Common Tool Button To Preset
        :return:
        """
        main_window = hou.qt.mainWindow().findChild(QtWidgets.QMainWindow, 'toolbox')
        sub_window = main_window.findChild(QtWidgets.QWidget, 'add_common_tool_btn')
        if sub_window is None:
            ex = SaveCommonToolNodeInfo.SaveCommonToolNodeInfo()
            ex.setParent(self, QtCore.Qt.Window)
            ex.show()

    def __on_vex_py_tab_add_btn_clicked(self) -> None:
        """
            Abort a Window To Dump New Code Info To Preset
        :return:
        """
        main_window = hou.qt.mainWindow().findChild(QtWidgets.QMainWindow, 'toolbox')
        sub_window = main_window.findChild(QtWidgets.QWidget, 'save_vex_py_node_info')
        if sub_window is None:
            ex = SaveVexPyNodeInfo.SaveVexPyNodeInfo()
            ex.setParent(self, QtCore.Qt.Window)
            ex.set_update_flag(False)
            ex.show()
        return

    def on_vex_py_tab_code_tag_changed(self) -> None:
        """
            If Current Tag Changed Hide Current List Widget
        """
        self.__setup_vex_py_tab_list_widget_info()
        if self.__vex_py_tab_code_tag.currentText():
            list_widget = self.__vex_py_tab_list_widget
            dict_list = self.__vex_py_tab_code_tag_dict_list
            for dict in dict_list:
                for item_node in dict.keys():
                    for i in range(list_widget.count()):
                        if list_widget.item(i):
                            item_name = list_widget.item(i).text()
                            show_flag = False
                            if dict['item_name'] == item_name:
                                for tag in dict['item_tag']:
                                    if tag in self.__vex_py_tab_code_tag.currentText():
                                        show_flag = True
                                if not show_flag:
                                    list_widget.takeItem(i)

    def __setup_vex_py_tab_list_widget_info(self) -> None:
        """
            Load Json Code Info To List Widget
        :return:
        """
        self.__vex_py_tab_list_widget.clear()
        self.code_type = self.__vex_py_tab_code_type_combo_box.currentIndex()
        self.code_path = tool_widget_utility_func.get_current_code_path_by_combo_box_index(self.code_type)

        # load code info from json file
        self.__vex_py_tab_code_tag_dict_list = tool_widget_utility_func.add_code_info_to_list_widget(
            self.__vex_py_tab_list_widget, self.code_path)

    def __on_vex_py_tab_list_selection_change(self) -> None:
        """
            Refresh UI Code Info By Current List Widget Selected
        :return:
        """
        self.current_item = self.__vex_py_tab_list_widget.currentItem()

        # load current select code info from json file
        code_info = tool_widget_utility_func.get_code_info_by_current_list_widget_item(self.code_path,
                                                                                       self.current_item)
        # self.__vex_py_tab_code_tag.setText(code_info[0])
        if code_info:
            self.__vex_py_tab_code_info.setPlainText(code_info[1])

    def __refresh_vex_py_tab_code_tags(self) -> None:
        """
            If Add A New Tag Refresh Tag List
        :return:
        """
        self.__vex_py_tab_code_tag.clear()
        vex_py_info_class = SaveVexPyNodeInfo.SaveVexPyNodeInfo()
        self.tag_list = vex_py_info_class.get_all_code_tag_list()
        if self.tag_list:
            for tag in self.tag_list:
                self.__vex_py_tab_code_tag.addItem(tag)

    def __on_vex_py_tab_import_btn_clicked(self) -> None:
        """
            Import Current Select Code Info To Houdini
        :return:
        """
        if self.current_item is None:
            self.current_item = self.__vex_py_tab_list_widget.currentItem()
        code_info = tool_widget_utility_func.get_code_info_by_current_list_widget_item(self.code_path,
                                                                                       self.current_item)
        # import current code info to houdini
        tool_hou_node_utility_func.import_code_to_houdini_by_code_info(code_info, self.code_type)

    def __on_vex_py_tab_update_btn_clicked(self) -> None:
        """
            Update Current Select Code Info By List Widget
        :return:
        """
        # overwrite current code info to json file
        if self.current_item:
            main_window = hou.qt.mainWindow().findChild(QtWidgets.QMainWindow, 'toolbox')
            sub_window = main_window.findChild(QtWidgets.QWidget, 'save_vex_py_node_info')
            if sub_window is None:
                ex = SaveVexPyNodeInfo.SaveVexPyNodeInfo()
                ex.setParent(self, QtCore.Qt.Window)
                ex.set_update_flag(True)
                ex.update_code_by_select_node_info(self.current_item, self.code_type)
                ex.show()
            self.__setup_vex_py_tab_list_widget_info()
        else:
            tool_error_info.show_exception_info('warning', 'please select current code preset to update')

    def __on_vex_py_tab_delete_btn_clicked(self) -> None:
        """
            Delete Current Select Code Info By List Widget
        :return:
        """
        # delete current code info from json file
        SaveVexPyNodeInfo.SaveVexPyNodeInfo.delete_select_code_info(self.current_item, self.code_type)
        self.__setup_vex_py_tab_list_widget_info()

    def __on_node_preset_tab_add_btn_clicked(self) -> None:
        """
            Abort A Window To Dump Node Preset Info
        :return:
        """
        main_window = hou.qt.mainWindow().findChild(QtWidgets.QMainWindow, 'toolbox')
        sub_window = main_window.findChild(QtWidgets.QWidget, 'save_node_preset_info')
        if sub_window is None:
            ex = SaveNodePresetInfo.SaveNodePresetInfo()
            ex.setParent(self, QtCore.Qt.Window)
            # is update mode
            ex.is_update_node_preset(False)
            ex.show()
        return

    def __setup_node_preset_tab_list_widget_info(self) -> None:
        """
            Refresh List Widget By Node Preset Info
        :return:
        """
        self.__node_preset_tab_list_widget.clear()
        self.node_type = self.__node_preset_tab_type_combo_box.currentText()

        self.node_path = tool_path_manager.node_preset_path

        # load node preset info from json file
        tool_widget_utility_func.add_node_preset_info_to_list_widget(self.__node_preset_tab_list_widget,
                                                                     self.node_path,
                                                                     self.node_type)

    def __on_node_preset_tab_import_btn_clicked(self) -> None:
        """
            Import Current Select Node Preset Info To Houdini
        :return:
        """
        self.current_item = self.__node_preset_tab_list_widget.currentItem()
        # create node by json node info and create in houdini
        tool_widget_utility_func.create_node_preset_info_by_current_list_widget_item(self.node_path,
                                                                                     self.current_item,
                                                                                     self.node_type)

    def __on_node_preset_tab_list_selection_change(self) -> None:
        """
            Refresh List Widget UI Node Info By Current Selected
        :return:
        """
        self.current_item = self.__node_preset_tab_list_widget.currentItem()
        # node screen shot
        image_path = tool_widget_utility_func.get_node_image_path_by_current_list_widget_item(
            self.node_path,
            self.current_item,
            self.node_type)
        self.__node_preset_tab_screen_shot_label.setPixmap(QtGui.QPixmap(image_path))
        # node marker
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
        """
            Update Current Select Node Preset Screen Shot Picture
        :return:
        """
        self.current_item = self.__node_preset_tab_list_widget.currentItem()
        self.node_type = self.__node_preset_tab_type_combo_box.currentText()
        # update current select screen shot
        SaveNodePresetInfo.SaveNodePresetInfo.update_screen_shot(self.current_item,
                                                                 self.node_type)

    def __on_node_preset_tab_update_info_btn_clicked(self) -> None:
        """
            Update Current Node Info Preset To File Preset
        :return:
        """
        self.current_item = self.__node_preset_tab_list_widget.currentItem()
        if self.current_item:
            name = self.current_item.text()
            main_window = hou.qt.mainWindow().findChild(QtWidgets.QMainWindow, 'toolbox')
            sub_window = main_window.findChild(QtWidgets.QWidget, 'update_node_preset_info')
            if sub_window is None:
                ex = SaveNodePresetInfo.SaveNodePresetInfo()
                ex.setParent(self, QtCore.Qt.Window)
                # is update node
                ex.is_update_node_preset(True, self.node_type, name)
                ex.show()
            return
        else:
            QtWidgets.QMessageBox.about(self, 'warning', 'please select node to update')

    def __on_node_preset_tab_delete_btn_clicked(self) -> None:
        """
            Delete Current Select Node Preset From File Preset
        :return:
        """
        list_widget = self.__node_preset_tab_list_widget
        self.node_type = self.__node_preset_tab_type_combo_box.currentText()
        # delete node preset from json file
        SaveNodePresetInfo.SaveNodePresetInfo.delete_node_preset(list_widget, self.node_type)

    def __on_file_manager_tab_add_btn_clicked(self) -> None:
        """
            Abort A Window To Dump New File Info To File Manager
        :return:
        """
        main_window = hou.qt.mainWindow().findChild(QtWidgets.QMainWindow, 'toolbox')
        sub_window = main_window.findChild(QtWidgets.QWidget, 'save_file_manager_info')
        if sub_window is None:
            ex = SaveFileManagerInfo.SaveFileManagerInfo()
            ex.setParent(self, QtCore.Qt.Window)
            ex.show()
        return

    def __on_file_manager_tab_update_btn_clicked(self) -> None:
        """
            Update Current File Info To File Manager Info Preset
        :return:
        """
        if self.current_select_file_name:
            main_window = hou.qt.mainWindow().findChild(QtWidgets.QMainWindow, 'toolbox')
            sub_window = main_window.findChild(QtWidgets.QWidget, 'update_file_manager_info')
            if sub_window is None:
                ex = SaveFileManagerInfo.SaveFileManagerInfo()
                ex.setParent(self, QtCore.Qt.Window)
                ex.update_current_index_info(project_name=self.current_select_file_project,
                                             folder_name=self.current_select_file_folder,
                                             file_name=self.current_select_file_name,
                                             file_type=self.current_select_file_type,
                                             file_dir=self.current_select_file_dir,
                                             file_marker=self.current_select_file_marker)
                ex.show()
        else:
            tool_error_info.show_exception_info('waring', 'please select filename')

    def __on_file_manager_tab_delete_btn_clicked(self) -> None:
        """
            Delete Current Select File Info In File Manager Info Preset
        :return:
        """
        delete_project = False
        delete_folder = False
        if self.current_select_file_project:
            if self.current_select_file_folder is None and self.current_select_file_name is None:
                delete_project = True
        if self.current_select_file_folder:
            if self.current_select_file_name is None:
                delete_folder = True

        # delete current project
        if delete_project:
            result = QtWidgets.QMessageBox.warning(self, "warning",
                                                   "are you want to delete this project? ",
                                                   QtWidgets.QMessageBox.Yes |
                                                   QtWidgets.QMessageBox.No)
            if result == QtWidgets.QMessageBox.Yes:
                ex = SaveFileManagerInfo.SaveFileManagerInfo()

                ex.delete_current_index_info(project_name=self.current_select_file_project,
                                             folder_name=self.current_select_file_folder,
                                             file_name=self.current_select_file_name,
                                             delete_project=delete_project)
                file_project = self.__file_manager_tree_view_model.itemFromIndex(self.current_select_file_project_item)
                row = file_project.index().row()
                self.__file_manager_tree_view_model.removeRow(row, self.current_select_file_project_item)
                self.__setup_file_manager_tree_view_info()

        # delete current folder:
        if delete_folder:
            result = QtWidgets.QMessageBox.warning(self, 'warning',
                                                   "are you want to delete this folder?",
                                                   QtWidgets.QMessageBox.Yes |
                                                   QtWidgets.QMessageBox.No)
            if result == QtWidgets.QMessageBox.Yes:
                ex = SaveFileManagerInfo.SaveFileManagerInfo()

                ex.delete_current_index_info(project_name=self.current_select_file_project,
                                             folder_name=self.current_select_file_folder,
                                             file_name=self.current_select_file_name,
                                             delete_folder=delete_folder)
                file_folder = self.__file_manager_tree_view_model.itemFromIndex(self.current_select_file_folder_item)
                row = file_folder.index().row()
                self.__file_manager_tree_view_model.removeRow(row, self.current_select_file_project_item)
                self.__setup_file_manager_tree_view_info()
        # delete current file item
        if not delete_project and not delete_folder:
            if self.current_select_file_name:
                result = QtWidgets.QMessageBox.warning(self, "warning",
                                                       "are you want to delete this file? ",
                                                       QtWidgets.QMessageBox.Yes |
                                                       QtWidgets.QMessageBox.No)
                if result == QtWidgets.QMessageBox.Yes:
                    ex = SaveFileManagerInfo.SaveFileManagerInfo()
                    # remove item info from file
                    ex.delete_current_index_info(project_name=self.current_select_file_project,
                                                 folder_name=self.current_select_file_folder,
                                                 file_name=self.current_select_file_name,
                                                 delete_project=delete_project,
                                                 delete_folder=delete_folder)
                    file_name = self.__file_manager_tree_view_model.itemFromIndex(self.current_select_file_name_item)
                    row = file_name.index().row()
                    # remove item from tree view
                    self.__file_manager_tree_view_model.removeRow(row, self.current_select_file_folder_item)
            else:
                tool_error_info.show_exception_info('waring', 'please select filename')

    def __setup_file_manager_tree_view_info(self) -> None:
        """
            Load File Preset From Json File And Dump To TreeView Widget
        :return:
        """
        # json file
        all_info_list = SaveFileManagerInfo.SaveFileManagerInfo.load_file_info_from_json_file()
        model = self.__file_manager_tree_view_model
        model.clear()
        model.setHorizontalHeaderLabels(['file', 'file_type', 'file_marker', 'file_dir'])
        for info in all_info_list:

            item_project = QtGui.QStandardItem(info['project_name'])
            model.appendRow(item_project)

            for folder in info['folder']:
                item_folder = QtGui.QStandardItem(folder['folder_name'])
                item_project.appendRow(item_folder)

                file_info = folder['file_info']
                for i in range(0, len(file_info['file_name'])):
                    item_file = QtGui.QStandardItem(folder['file_info']['file_name'][i])
                    item_file_type = QtGui.QStandardItem(folder['file_info']['file_type'][i])
                    item_file_marker = QtGui.QStandardItem(folder['file_info']['file_marker'][i])
                    item_file_dir = QtGui.QStandardItem(folder['file_info']['file_dir'][i])

                    item_folder.appendRow(item_file)
                    item_folder.setChild(item_file.index().row(), 1, item_file_type)
                    item_folder.setChild(item_file.index().row(), 2, item_file_marker)
                    item_folder.setChild(item_file.index().row(), 3, item_file_dir)

        tree_view = self.__file_manager_tree_view_widget
        tree_view.setModel(model)
        tree_view.header().resizeSection(0, 160)
        tree_view.setStyle(QtWidgets.QStyleFactory.create('windows'))
        tree_view.selectionModel().currentChanged.connect(self.__on_current_tree_view_change)
        tree_view.expandAll()

    def __on_current_tree_view_change(self, current):
        """
            Recording Current File Info By Current Selected TreeView Item
        :param current:
        :return:
        """
        self.current_select_file_name_item = current.sibling(current.row(), 0)
        self.current_select_file_name = self.current_select_file_name_item.data()

        self.current_select_file_type_item = current.sibling(current.row(), 1)
        self.current_select_file_type = self.current_select_file_type_item.data()

        self.current_select_file_marker_item = current.sibling(current.row(), 2)
        self.current_select_file_marker = self.current_select_file_marker_item.data()

        self.current_select_file_dir_item = current.sibling(current.row(), 3)
        self.current_select_file_dir = self.current_select_file_dir_item.data()

        # if select file
        if self.current_select_file_dir:
            self.current_select_file_folder_item = current.parent()
            self.current_select_file_folder = self.current_select_file_folder_item.data()

            self.current_select_file_project_item = current.parent().parent()
            self.current_select_file_project = self.current_select_file_project_item.data()
        else:
            self.current_select_file_type = None
            self.current_select_file_name = None
            self.current_select_file_marker = None

            # if select folder
            if self.__file_manager_tree_view_model.itemFromIndex(current.parent()):

                self.current_select_file_folder_item = current
                self.current_select_file_folder = current.data()

                self.current_select_file_project_item = current.parent()
                self.current_select_file_project = current.parent().data()

            # select project
            else:

                self.current_select_file_folder = None
                self.current_select_file_project_item = current
                self.current_select_file_project = current.data()

        if self.current_select_file_type is not None:
            info = str(self.current_select_file_type).lower()
            hip_file = ['.hip', '.hiplc', '.hipnc']
            if info.find('.') == -1:
                info = '.' + info

            if info in hip_file:
                if info in self.current_select_file_dir:
                    self.__current_hip_file_path_from_file_manager = self.current_select_file_dir

                elif self.current_select_file_dir.endswith(self.current_select_file_name):
                    self.__current_hip_file_path_from_file_manager = self.current_select_file_dir + info

                else:

                    if self.current_select_file_name.find('.') == -1:

                        self.__current_hip_file_path_from_file_manager = \
                            self.current_select_file_dir + '\\' + self.current_select_file_name + info

                    else:
                        self.__current_hip_file_path_from_file_manager = \
                            self.current_select_file_dir + '\\' + self.current_select_file_name
            else:
                self.__current_hip_file_path_from_file_manager = None
        else:
            self.__current_hip_file_path_from_file_manager = None

        txt = 'project:[{}] '.format(self.current_select_file_project)
        txt += 'folder:[{}]'.format(self.current_select_file_folder)
        txt += 'filename:[{}]'.format(self.current_select_file_name)
        txt += 'filemarker:[{}]'.format(self.current_select_file_marker)

        self.statusBar().showMessage(txt)

    def open_context_menu(self) -> None:
        """
            Open Context Menu When Right Click Current TreeView Item
        :return:
        """
        self.file_manager_tree_view_menu = QtWidgets.QMenu('Menu', self)

        open_file_action = QtWidgets.QAction('open_file_location', self)
        tool_widget_utility_func.set_widget_icon(open_file_action, 'open.png')
        open_hip_action = QtWidgets.QAction('open_hip_file', self)
        tool_widget_utility_func.set_widget_icon(open_hip_action, 'open_hip.png')
        import_action = QtWidgets.QAction('import_to_hip_file', self)
        tool_widget_utility_func.set_widget_icon(import_action, 'import.png')

        open_file_action.triggered.connect(self.__on_menu_open_file_action)
        open_hip_action.triggered.connect(self.__on_menu_open_hip_action)
        import_action.triggered.connect(self.__on_menu_import_file_action)

        self.file_manager_tree_view_menu.addAction(open_file_action)
        self.file_manager_tree_view_menu.addAction(open_hip_action)
        self.file_manager_tree_view_menu.addAction(import_action)

        self.file_manager_tree_view_menu.exec_(QtGui.QCursor.pos())

    def __on_menu_open_file_action(self) -> None:
        """
            Open Current File Location By TreeView Current Select File Path
        :return:
        """
        file_dir = self.current_select_file_dir
        if file_dir is not None:
            if len(tool_path_manager.get_file_suffix(file_dir)):
                file_dir = tool_path_manager.get_parent_path(file_dir)
            try:
                os.startfile(file_dir)
            except:
                tool_error_info.show_exception_info('error', 'open file got wrong, please check file is really exist')

    def __on_menu_open_hip_action(self) -> None:
        """
            Open Houdini Files If Current TreeView Select File Extension Is End Of Hip
        :return:
        """
        if self.__current_hip_file_path_from_file_manager is not None:
            result = QtWidgets.QMessageBox.warning(self, "warning",
                                                   "are you want to open current file in this hou project? ",
                                                   QtWidgets.QMessageBox.Yes |
                                                   QtWidgets.QMessageBox.No)
            if result == QtWidgets.QMessageBox.Yes:
                try:
                    hou.hipFile.load(str(self.__current_hip_file_path_from_file_manager),
                                     suppress_save_prompt=True)
                except:
                    tool_error_info.show_exception_info('error',
                                                        'open file may got something wrong, please check file ')

    def __on_menu_import_file_action(self) -> None:
        """
            Import Current TreeView Select File By Extension
        :return:
        """
        tool_error_info.show_exception_info('warning', 'doing... try other function')

    def keyPressEvent(self, event) -> None:
        """
        :param event:  if press Escape close window
        :return: None
        """
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
