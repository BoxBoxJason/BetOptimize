# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import QWidget,QDateTimeEdit,QLabel,QVBoxLayout
from PyQt6.QtCore import Qt,QDateTime

class DateTimePicker(QWidget):

    def __init__(self,parent):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        # Date picker
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground,True)

        # Date label
        date_qlabel = QLabel('Date',self)
        date_qlabel.setObjectName('h3')
        layout.addWidget(date_qlabel,0,Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        # Date Picker
        self.__date_picker = QDateTimeEdit(self)
        self.__date_picker.setDateTime(QDateTime.currentDateTime())
        layout.addWidget(self.__date_picker,0,Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)


    def getDateTime(self):
        """
        @return (str) picked date to format yyyy-MM-dd HH:mm
        """
        return self.__date_picker.date().toString('yyyy-MM-dd HH:mm')


    def clean(self):
        """
        Resets date picker date to current date
        """
        self.__date_picker.setDateTime(QDateTime.currentDateTime())
