# -*- coding: utf-8 -*-
from PySide2.QtCore import Signal, Qt
from PySide2.QtWidgets import QToolButton


#
class CustomButton(QToolButton):
    """
        override left/right click signal of QToolButton
    """
    _rightClicked = Signal(int)
    _leftClicked = Signal(int)

    def __init__(self, parent=None):
        super(CustomButton, self).__init__(parent)

    def mousePressEvent(self, event) -> None:
        """
            Mouse Press Event Override
        :param event:
        """
        if event.buttons() == Qt.RightButton:
            # right click
            self._rightClicked.emit(1)
        if event.buttons() == Qt.LeftButton:
            # left click
            self._leftClicked.emit(1)


