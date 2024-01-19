# -*- coding: utf-8 -*-
'''
Created on 9 oct. 2023

@author: BoxBoxJason
'''
import logging
from json import load,dump
from PyQt6.QtWidgets import QWidget,QLabel,QPushButton,QVBoxLayout,QLineEdit,QCompleter,QRadioButton,QDateEdit,QHBoxLayout
from PyQt6.QtCore import Qt,QStringListModel,QDate
from interface.TemplateWidget import TemplatePageWidget
from interface.games.DateTimePicker import DateTimePicker

class OneVOneWidget(TemplatePageWidget):
    """
    1v1 games widget,
    Allows to pick players and predict the outcome of a game between them
    """
    def __init__(self,parent):
        super().__init__(parent)
        self.database = {}
        self.__database_path = None

        # Players widgets
        self.__player1_widget = PlayerWidget(self,1)
        self.__player2_widget = PlayerWidget(self,2)
        self.layout().addWidget(self.__player1_widget,2,0,1,1,Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        self.layout().addWidget(self.__player2_widget,2,1,1,1,Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)

        # Game information widget
        self.__game_information_widget = MatchWidget(self)
        self.layout().addWidget(self.__game_information_widget,3,0,1,2,Qt.AlignmentFlag.AlignCenter)

        # Predict button
        add_button = QPushButton('ADD',self)
        add_button.setObjectName('submit')
        add_button.clicked.connect(self.__createGame)
        self.layout().addWidget(add_button,4,0,1,2,Qt.AlignmentFlag.AlignCenter)


    def setDatabasePath(self,database_path):
        """
        Sets the widget database, changes the pickable players in corresponding widgets

        @param (path) database_path : Absolute path to database file
        """
        self.__database_path = database_path
        with open(self.__database_path,'r',encoding='utf-8') as database_file:
            self.database = load(database_file)
        self.__player1_widget.updatePlayersList(self.database['PLAYERS'])
        self.__player2_widget.updatePlayersList(self.database['PLAYERS'])


    def __createGame(self):
        player1_id = self.__player1_widget.search_bar.text().strip()
        player2_id = self.__player2_widget.search_bar.text().strip()
        if player1_id.strip() and player2_id.strip() and player1_id != player2_id:
            game_info_dict = self.__game_information_widget.getGameInfo()

            game_info_dict['ID'] = f"{game_info_dict['DATE']}-{player1_id}-{player2_id}"

            if game_info_dict['WINNER_ID'] == 'Player 1':
                game_info_dict['WINNER_ID'] = player1_id
                game_info_dict['LOSER_ID'] = player2_id
            else:
                game_info_dict['WINNER_ID'] = player2_id
                game_info_dict['LOSER_ID'] = player1_id

            game_info_dict['PROCESSED'] = False

            self.database['GAMES'][game_info_dict['ID']] = game_info_dict

            for player_id in player1_id,player2_id:
                if not player_id in self.database['PLAYERS']:
                    createELOPlayer(self.database['PLAYERS'],player_id)
            self.__player1_widget.updatePlayersList(self.database['PLAYERS'])
            self.__player2_widget.updatePlayersList(self.database['PLAYERS'])

            with open(self.__database_path,'w',encoding='utf-8') as database_file:
                dump(self.database,database_file)

            logging.info(f"Game {game_info_dict['ID']} saved in database")


    def clean(self):
        """
        Cleans the widget
        """
        super().clean()
        self.database.clear()
        self.__player1_widget.clean()
        self.__player2_widget.clean()
        self.__game_information_widget.clean()


START_ELO = 1500

def createELOPlayer(players_table,player_id):
    players_table[player_id] = {
        'ID':player_id,
        'GAMES':[],
        'ELO':START_ELO
        }


WRONG_INPUT_STYLE = "QLineEdit {background-color: #edab9f; border: 2px ridge #bf1d00; padding: 5px 10px;}"
UNKNOWN_INPUT_STYLE = "QLineEdit {background-color: #d792f0; border: 2px ridge #61157d; padding: 5px 10px;}"
CORRECT_INPUT_STYLE = "QLineEdit {background-color: #b3f5a4;border: 2px ridge #229608;padding: 5px 10px;}"

class PlayerWidget(QWidget):
    """
    Player picker widget
    """
    def __init__(self,parent,player_index):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground,True)
        layout = QVBoxLayout(self)
        self.setObjectName('container-border')

        # Player title label
        title_qlabel = QLabel(f"Player {player_index}",self)
        title_qlabel.setObjectName('h3')
        layout.addWidget(title_qlabel,0,Qt.AlignmentFlag.AlignHCenter)

        # Player search bar
        self.search_bar = QLineEdit(self)
        self.search_bar.setStyleSheet(CORRECT_INPUT_STYLE)
        self.search_bar.textChanged.connect(self.__updateBgColor)
        layout.addWidget(self.search_bar,0,Qt.AlignmentFlag.AlignHCenter)

        # Search bar completer
        self.completer = QCompleter(self)
        self.completer.setCompletionMode(QCompleter.CompletionMode.InlineCompletion)
        self.search_bar.setCompleter(self.completer)

        # Player winrate
        self.player_winrate_qlabel = QLabel(self)
        self.player_winrate_qlabel.setObjectName('p')
        layout.addWidget(self.player_winrate_qlabel,0,Qt.AlignmentFlag.AlignHCenter)


    def __updateBgColor(self,text):
        if text.strip():
            first_suitable_element = None
            for player_id in self.parent().database['PLAYERS']:
                if text in player_id:
                    first_suitable_element = player_id
                    break

            if first_suitable_element == text:
                self.search_bar.setStyleSheet(CORRECT_INPUT_STYLE)
            else:
                self.search_bar.setStyleSheet(UNKNOWN_INPUT_STYLE)
        else:
            self.search_bar.setStyleSheet(WRONG_INPUT_STYLE)


    def clean(self):
        """
        Cleans the widget
        """
        for i in range(1,3):
            self.layout().itemAt(i).widget().clear()


    def updatePlayersList(self, players_ids):
        self.completer.setModel(QStringListModel(players_ids, self.completer))


class WinnerWidget(QWidget):
    """
    Winner picker widget
    """
    def __init__(self,parent):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground,True)
        layout = QVBoxLayout(self)
        # Title QLabel
        title_qlabel = QLabel('Winner',self)
        title_qlabel.setObjectName('h3')
        layout.addWidget(title_qlabel,0,Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        radio_widget = QWidget(self)
        radio_layout = QVBoxLayout(radio_widget)
        # Radio Button 1
        radio_button = QRadioButton('Player 1',self)
        radio_layout.addWidget(radio_button,0,Qt.AlignmentFlag.AlignLeft)
        radio_button.toggled.connect(self.__changeWinner)
        radio_button.setChecked(True)

        # Radio Button 2
        radio_button = QRadioButton('Player 2',self)
        radio_layout.addWidget(radio_button,0,Qt.AlignmentFlag.AlignLeft)
        radio_button.toggled.connect(self.__changeWinner)

        layout.addWidget(radio_widget,0,Qt.AlignmentFlag.AlignCenter)

    def __changeWinner(self,winner_text):
        self.parent().winner = winner_text


class MatchWidget(QWidget):

    def __init__(self,parent):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setSpacing(65)
        self.winner = 'Player 1'

        # Date picker
        self.__date_picker = DateTimePicker(self)
        layout.addWidget(self.__date_picker,0,Qt.AlignmentFlag.AlignCenter)

        # Winner picker
        layout.addWidget(WinnerWidget(self),0,Qt.AlignmentFlag.AlignCenter)


    def getGameInfo(self):
        return {'DATE':self.__date_picker.getDateTime(),'WINNER_ID':self.winner}
    

    def clean(self):
        self.__date_picker.clean()
