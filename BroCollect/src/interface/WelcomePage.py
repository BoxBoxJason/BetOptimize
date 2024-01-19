# -*- coding: utf-8 -*-
'''
Created on 7 oct. 2023

@author: BoxBoxJason
'''
from PyQt6.QtGui import QPixmap
from interface.TemplateWidget import TemplatePageWidget
from resources.PathEnum import getImage

class WelcomePage(TemplatePageWidget):
    """
    Collector Welcome page
    """
    def __init__(self,parent):
        super().__init__(parent)

        img = QPixmap(getImage('BroCollect.png'))
        self.title_qlabel.setPixmap(img)

        self.subtitle_qlabel.setText('Please pick a sport !')
        self.subtitle_qlabel.setObjectName('p')
