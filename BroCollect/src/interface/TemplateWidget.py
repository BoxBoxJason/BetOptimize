# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import QWidget,QLabel,QGridLayout
from PyQt6.QtCore import Qt


class TemplatePageWidget(QWidget):
    """
    Template widget for GamBible pages
    """
    def __init__(self,parent,total_span=2):
        super().__init__(parent)
        layout = QGridLayout()

        # Widget title
        self.title_qlabel = QLabel('',self)
        self.title_qlabel.setObjectName('h1')
        layout.addWidget(self.title_qlabel,0,0,1,total_span,Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        # Widget subtitle
        self.subtitle_qlabel = QLabel('',self)
        self.subtitle_qlabel.setObjectName('h2')
        layout.addWidget(self.subtitle_qlabel,1,0,1,total_span,Qt.AlignmentFlag.AlignHCenter |Qt.AlignmentFlag.AlignTop)

        self.setLayout(layout)


    def setTitle(self,title):
        """
        Sets a new widget title
        
        @param (str) title : new title
        """
        self.title_qlabel.setText(title)


    def setSubtitle(self,subtitle):
        """
        Sets a new widget subtitle

        @param (str) subtitle : new subtitle
        """
        self.subtitle_qlabel.setText(subtitle)


    def clean(self):
        """
        Remove text from labels
        """
        self.title_qlabel.clear()
        self.subtitle_qlabel.clear()
