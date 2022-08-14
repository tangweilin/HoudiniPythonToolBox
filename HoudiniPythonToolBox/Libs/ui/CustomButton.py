# -*- coding: utf-8 -*-
from PySide2.QtCore import Signal, Qt
from PySide2.QtWidgets import QToolButton


#
class CustomButton(QToolButton):
    _rightClicked = Signal(int)
    _leftClicked = Signal(int)
    _mClicked = Signal(int)

    def __init__(self, parent=None):
        super(CustomButton, self).__init__(parent)

    def mousePressEvent(self, event):
        if event.buttons() == Qt.RightButton:
            self._rightClicked.emit(1)
        if event.buttons() == Qt.LeftButton:
            self._leftClicked.emit(1)
        if event.buttons() == Qt.MidButton:
            self._mClicked.emit(1)



