# -*- coding: utf-8 -*-
'''
Created on 3 oct. 2023

@author: BoxBoxJason
'''
import logging
from PyQt6.QtWidgets import QMainWindow,QWidget,QVBoxLayout,QLabel,QStackedLayout
from PyQt6.QtGui import QIcon,QFontDatabase
from PyQt6.QtCore import Qt
from interface.Toolbar import TopNavBar
from interface.games.FreeForAllWidget import FreeForAllWidget
from interface.games.OneVOneWidget import OneVOneWidget
from interface.games.TeamWidget import TeamWidget
from interface.WelcomePage import WelcomePage
from resources.PathEnum import getImage,getDBPath,getFontsPaths,getConfig


class BroCollect(QMainWindow):
    """
    Collector main window
    
    GRIDLAYOUT:
                TITLE
              SUBTITLE
              
              MESSAGE
              
        P1 WIDGET    P2 WIDGET
        
        GAME INFORMATION WIDGET
        
                SUBMIT
    """

    def __init__(self):
        logging.debug("Setting up Collector main window")
        super().__init__()

        self.setWindowTitle("BroCollect")
        self.setWindowIcon(QIcon(getImage("Brocollect.png")))

        self.setMenuBar(TopNavBar(self))
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)

        self.setCentralWidget(MainWidget(self))

        logging.debug("Collector main window build successful")


class MainWidget(QWidget):
    """
    BroCollect main widget class
    LAYOUT:
    
                TITLE
              SUBTITLE
              
            EXPLANATION
            
           STACKEDLAYOUT
    """
    __INDEXBYEVENT = {"1v1 game":1,"free for all game":2,"team game":3}
    __DBNAMEBYEVENT = {"1v1 game":"defaultELO.json","free for all game":"defaultMMR-FFA.json","team game":"defaultMMR-Team.json"}

    def __init__(self,parent):
        super().__init__(parent)
        stacked_layout = QStackedLayout(self)
        stacked_layout.addWidget(WelcomePage(self))
        stacked_layout.addWidget(OneVOneWidget(self))
        stacked_layout.addWidget(FreeForAllWidget(self))
        stacked_layout.addWidget(TeamWidget(self))


    def switchSelection(self,sport,category,event):
        """
        Changes subtitle label text
        @param (str) subtitle : new subtitle text
        """
        config_dict = getConfig()
        db_name = MainWidget.__DBNAMEBYEVENT.get(event,config_dict['TOOLBAR'][sport]['database'])

        db_path = getDBPath(sport,category,db_name)
        self.clean(MainWidget.__INDEXBYEVENT[event])
        self.layout().widget(MainWidget.__INDEXBYEVENT[event]).setTitle(sport)
        self.layout().widget(MainWidget.__INDEXBYEVENT[event]).setSubtitle(f"{category} {event}")
        self.layout().widget(MainWidget.__INDEXBYEVENT[event]).setDatabasePath(db_path)
        self.layout().setCurrentIndex(MainWidget.__INDEXBYEVENT[event])


    def clean(self,index=None):
        """
        Cleans selected stacked layout's widget item
        @param (int) index : Stacked layout widget item index
        """
        if index is None:
            self.layout().currentWidget().clean()
        else:
            self.layout().widget(index).clean()


def addFonts():
    """
    Adds all available fonts to QFontDatabase
    """
    for font_path in getFontsPaths():
        QFontDatabase.addApplicationFont(font_path)
