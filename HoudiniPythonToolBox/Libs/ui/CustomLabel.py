# -*- coding: utf-8 -*-
from PySide2.QtCore import Signal
from PySide2 import QtWidgets


class CustomLabel(QtWidgets.QLabel):
    """
        override left click and release click signal of QLabel
    """
    _Signal = Signal(int)
    _Click = Signal(int)
    _Resize = Signal(int)

    def __init__(self, parent=None):
        super(CustomLabel, self).__init__(parent)

    # custom signal of left click
    def mousePressEvent(self, e) -> Signal:
        """
            Left Click
        :param e:
        """
        self._Signal.emit(0)
        self._Click.emit(1)

    # custom signal of right click
    def mouseReleaseEvent(self, event) -> Signal:
        """
            Release Click
        :param event:
        """
        self._Signal.emit(1)



