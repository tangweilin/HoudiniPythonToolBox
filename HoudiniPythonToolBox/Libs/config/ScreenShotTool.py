# -*- coding: utf-8 -*-

import hou
from PySide2 import QtCore, QtGui, QtWidgets

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import sys


class ScreenShotTool(QWidget):
    """
        Custom Screen Shot
    """

    def __init__(self, name, path, parent=None):
        super(ScreenShotTool, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet('''background-color:black; ''')
        self.setWindowOpacity(0.6)
        desktop_rect = QDesktopWidget().screenGeometry()
        self.setGeometry(desktop_rect)
        self.setCursor(Qt.CrossCursor)
        self.blackMask = QBitmap(desktop_rect.size())
        self.blackMask.fill(Qt.black)
        self.mask = self.blackMask.copy()
        self.is_drawing = False
        self.start_point = QPoint()
        self.end_point = QPoint()
        self.name = name
        self.path = path
        self.setParent(QApplication.desktop())

    def paintEvent(self, event) -> None:
        """
            Init QPainter
        :param event:
        """
        if self.is_drawing:
            self.mask = self.blackMask.copy()
            pp = QPainter(self.mask)
            pen = QPen()
            pen.setStyle(Qt.NoPen)
            pp.setPen(pen)
            brush = QBrush(Qt.white)
            pp.setBrush(brush)
            pp.drawRect(QRect(self.start_point, self.end_point))
            self.setMask(QBitmap(self.mask))

    def mousePressEvent(self, event) -> None:
        """
            Start Draw
        :param event:
        """
        if event.button() == Qt.LeftButton:
            self.start_point = event.pos()
            self.end_point = self.start_point
            self.is_drawing = True

    def mouseMoveEvent(self, event) -> None:
        """
            Update End Point
        :param event:
        """
        if self.is_drawing:
            self.end_point = QPoint(event.pos().x(), self.start_point.y() + event.pos().x() - self.start_point.x())

            self.update()

    def mouseReleaseEvent(self, event) -> None:
        """
            Save Picture
        :param event:
        """
        if event.button() == Qt.LeftButton:

            try:
                screenshot = QApplication.primaryScreen().grabWindow(0)
            except:
                screenshot = QApplication.primaryScreen().grabWindow(QApplication.desktop().winId())

            rect = QRect(self.start_point, self.end_point)
            outputRegion = screenshot.copy(rect)
            new_name = self.name
            outputRegion.save(self.path + '/' + new_name + '.jpg', format='JPG', quality=100)
            self.close()

    def closeEvent(self, event) -> None:
        """
            Set Parent To None When Window Closed
        :param event:
        """
        self.setParent(None)

    def keyPressEvent(self, event) -> None:
        """
            Close Window When Press Escape
        :param event:
        """
        if event.key() == Qt.Key_Escape:
            self.close()
