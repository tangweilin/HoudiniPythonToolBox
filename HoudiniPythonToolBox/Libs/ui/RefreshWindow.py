import hou
from Libs.ui import UserInterface
from imp import reload
reload(UserInterface)
from PySide2 import QtCore


class RefreshWindow():
    def refresh_window(self):
        # houMainWindow = hou.qt.mainWindow()
        # getChildWin = houMainWindow.findChild(QtWidgets.QMainWindow, 'toolbox')
        window = UserInterface.HoudiniPythonTools()
        window.setParent(hou.qt.mainWindow(), QtCore.Qt.Window)
        window.show()

