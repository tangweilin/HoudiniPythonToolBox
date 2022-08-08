# -*- coding: utf-8 -*-
from PySide2.QtCore import Signal
from PySide2 import QtWidgets


class CustomLabel(QtWidgets.QLabel):
    _Signal = Signal(int)
    _Click = Signal(int)
    _Resize = Signal(int)

    # 自定义单击信号
    # clicked = pyqtSignal()
    # 自定义双击信号

    def __init__(self, parent=None):
        super(CustomLabel, self).__init__(parent)

    def mousePressEvent(self, e) -> Signal:
        # print 'mousePressEvent'
        self._Signal.emit(0)
        self._Click.emit(1)

    def mouseReleaseEvent(self, event) -> Signal:
        self._Signal.emit(1)



