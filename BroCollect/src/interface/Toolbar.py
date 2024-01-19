# -*- coding: utf-8 -*-
'''
Created on 5 oct. 2023

@author: BoxBoxJason
'''
from PyQt6.QtWidgets import QMenuBar
from PyQt6.QtGui import QAction, QIcon
from resources.PathEnum import getConfig,getImage

class TopNavBar(QMenuBar):
    """
    Top navigation toolbar for BroCollect
    """

    def __init__(self,parent):
        super().__init__(parent)

        config_dict = getConfig()
        settings_menu = self.addMenu(QIcon(getImage('Gear.png')), 'Settings')

        for sport_name,sport_config_dict in config_dict['TOOLBAR'].items():
            self.__createMenuAndActions(sport_name, sport_config_dict['icon'],sport_config_dict['categories'],sport_config_dict['events'])


    def __createMenuAndActions(self,sport_name,sport_icon_name,categories,events):
        sport_menu = self.addMenu(QIcon(getImage(sport_icon_name)),'')
        self.__createCategoryMenu(sport_name,sport_menu,categories[0],events)
        for category in categories[1:]:
            sport_menu.addSeparator()
            self.__createCategoryMenu(sport_name,sport_menu,category,events)


    def __createCategoryMenu(self,sport_name,base_menu,category,events):
        category_menu = base_menu.addMenu(category)
        self.__createAction(category_menu, sport_name,events[0],
                            lambda : self.parent().centralWidget().switchSelection(sport_name,category,events[0]))
        for event_name in events[1:]:
            category_menu.addSeparator()
            self.__createAction(category_menu, sport_name, event_name,
                                lambda : self.parent().centralWidget().switchSelection(sport_name,category,event_name))


    def __createAction(self,parentMenu,sport_name,event_name,action_call):
        action = QAction(event_name.capitalize(),self)
        action.setToolTip(f"Open {sport_name} {event_name} window")
        action.triggered.connect(action_call)
        parentMenu.addAction(action)
