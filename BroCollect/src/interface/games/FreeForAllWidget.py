# -*- coding: utf-8 -*-
'''
Created on 9 oct. 2023

@author: BoxBoxJason
'''
import logging
from json import load,dump
from PyQt6.QtCore import Qt,QDate,QStringListModel
from PyQt6.QtWidgets import QWidget,QLineEdit,QListWidget,QVBoxLayout,QCompleter,QPushButton,\
    QHBoxLayout,QListWidgetItem,QLabel,QMenu, QInputDialog
from PyQt6.QtGui import QAction
from interface.TemplateWidget import TemplatePageWidget
from interface.games.DateTimePicker import DateTimePicker

class FreeForAllWidget(TemplatePageWidget):

    def __init__(self,parent):
        super().__init__(parent)
        self.database = {}
        self.__database_path = None

        # Players ranking widget
        self.__ranking_widget = RankingWidget(self)
        self.layout().addWidget(self.__ranking_widget,2,0,1,1,Qt.AlignmentFlag.AlignHCenter)

        # Game date picker
        self.__date_picker = DateTimePicker(self)
        self.layout().addWidget(self.__date_picker,2,1,1,1,Qt.AlignmentFlag.AlignHCenter)

        add_button = QPushButton('ADD',self)
        add_button.setObjectName('submit')
        add_button.clicked.connect(self.__createGame)
        self.layout().addWidget(add_button,3,0,1,2,Qt.AlignmentFlag.AlignCenter)


    def setDatabasePath(self,database_path):
        """
        Sets the widget database, changes the pickable players in corresponding widgets

        @param (path) database_path : Absolute path to database file
        """
        self.__database_path = database_path
        with open(self.__database_path,'r',encoding='utf-8') as database_file:
            self.database = load(database_file)
        self.__ranking_widget.updatePlayersList(self.database['PLAYERS'])


    def __createGame(self):
        game_info_dict = {}
        players_ranking = self.__ranking_widget.getRanking()
        if len(players_ranking) > 1 and any(player_id.strip() for player_id in players_ranking):
            game_info_dict['DATE'] = self.__date_picker.getDateTime()
            game_info_dict['ID'] = f"{game_info_dict['DATE']}-{'-'.join(players_ranking)}"
            game_info_dict['RANKING'] = players_ranking

            game_info_dict['PROCESSED'] = False

            self.database['GAMES'][game_info_dict['ID']] = game_info_dict

            for player_id in players_ranking:
                if not player_id in self.database['PLAYERS']:
                    createMMRPlayer(self.database['PLAYERS'],player_id)
            self.__ranking_widget.updatePlayersList(self.database['PLAYERS'])

            with open(self.__database_path,'w',encoding='utf-8') as database_file:
                dump(self.database,database_file)

            logging.info(f"Game {game_info_dict['ID']} saved in database")

        else:
            logging.error('Could not create game because of a lack of valid players')


    def clean(self):
        """
        Cleans the widget
        """
        self.database.clear()
        self.__date_picker.clean()
        self.__database_path = None

START_SKILL = 1500
START_SKILL_DEVIATION = 350

def createMMRPlayer(players_table,player_id):
    players_table[player_id] = {
        'ID':player_id,
        'SKILL':START_SKILL,
        'SKILL_DEVIATION':START_SKILL_DEVIATION,
        'PERF_HISTORY':[START_SKILL],
        'PERF_WEIGHT':[1/START_SKILL_DEVIATION],
        'GAMES':[]
    }


WRONG_INPUT_STYLE = "QLineEdit {background-color: #edab9f; border: 2px ridge #bf1d00; padding: 5px 10px;}"
UNKNOWN_INPUT_STYLE = "QLineEdit {background-color: #d792f0; border: 2px ridge #61157d; padding: 5px 10px;}"
CORRECT_INPUT_STYLE = "QLineEdit {background-color: #b3f5a4;border: 2px ridge #229608;padding: 5px 10px;}"

class RankingWidget(QWidget):

    def __init__(self,parent,top_label='Players'):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.__players_set = set()
        # Title label
        players_qlabel = QLabel(top_label,self)
        players_qlabel.setObjectName('h3')
        layout.addWidget(players_qlabel,0,Qt.AlignmentFlag.AlignHCenter)

        # List widget
        self.__list_widget = QListWidget(self)
        self.__list_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.__list_widget.customContextMenuRequested.connect(self.__openMenu)
        self.__list_widget.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        layout.addWidget(self.__list_widget,0,Qt.AlignmentFlag.AlignHCenter)

        search_widget = QWidget(self)
        search_bar_layout = QHBoxLayout(search_widget)
        # Player search bar
        self.__search_bar = QLineEdit(self)
        self.__search_bar.setStyleSheet(CORRECT_INPUT_STYLE)
        self.__search_bar.textChanged.connect(self.__updateBgColor)
        search_bar_layout.addWidget(self.__search_bar,0,Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        # Add button
        add_button = QPushButton('<<',self)
        add_button.clicked.connect(self.__addPlayerIdToList)
        add_button.setObjectName('submit-small')
        search_bar_layout.addWidget(add_button,0,Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(search_widget,0,Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        # Search bar completer
        self.__completer = QCompleter(self)
        self.__completer.setCompletionMode(QCompleter.CompletionMode.InlineCompletion)
        self.__search_bar.setCompleter(self.__completer)


    def __addPlayerIdToList(self):
        player_id = self.__search_bar.text().strip()
        if player_id and not player_id in self.__players_set:
            self.__list_widget.addItem(QListWidgetItem(player_id))
            self.__players_set.add(player_id)


    def __updateBgColor(self,text):
        if text.strip():
            first_suitable_element = None
            for player_id in self.parent().database['PLAYERS']:
                if text in player_id:
                    first_suitable_element = player_id
                    break

            if first_suitable_element == text:
                self.__search_bar.setStyleSheet(CORRECT_INPUT_STYLE)
            else:
                self.__search_bar.setStyleSheet(UNKNOWN_INPUT_STYLE)
        else:
            self.__search_bar.setStyleSheet(WRONG_INPUT_STYLE)


    def __openMenu(self,position):
        item = self.__list_widget.itemAt(position)
        if item is not None:
            menu = QMenu()
            edit_action = QAction("Edit", self)
            delete_action = QAction("Delete", self)

            edit_action.triggered.connect(lambda: self.__editItem(item))
            delete_action.triggered.connect(lambda: self.__deleteItem(item))

            menu.addAction(edit_action)
            menu.addAction(delete_action)

            menu.exec(self.mapToGlobal(position))


    def __deleteItem(self,item):
        self.__players_set.remove(item.text())
        self.__list_widget.takeItem(self.row(item))
    def __editItem(self, item):
        text, ok = QInputDialog.getText(self, "Edit Item", "Enter new text:", text=item.text())
        if ok:
            item.setText(text)


    def updatePlayersList(self,players_ids):
        self.__completer.setModel(QStringListModel(players_ids, self.__completer))


    def getRanking(self):
        return [self.__list_widget.item(i).text() for i in range(self.__list_widget.count())]


    def clean(self):
        self.__list_widget.clear()
        self.__search_bar.clear()
