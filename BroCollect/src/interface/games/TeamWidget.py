# -*- coding: utf-8 -*-

import logging
from json import load,dump
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton
from interface.TemplateWidget import TemplatePageWidget
from interface.games.DateTimePicker import DateTimePicker
from interface.games.FreeForAllWidget import RankingWidget,createMMRPlayer

class TeamWidget(TemplatePageWidget):
    """
    """

    def __init__(self,parent):
        super().__init__(parent,3)

        self.database = {}
        self.__database_path = None

        # Player pickers
        self.__team1_widget = RankingWidget(self,'Team 1')
        self.__team2_widget = RankingWidget(self,'Team 2')
        self.layout().addWidget(self.__team1_widget,2,0,1,1,Qt.AlignmentFlag.AlignCenter)
        self.layout().addWidget(self.__team2_widget,2,1,1,1,Qt.AlignmentFlag.AlignCenter)

        # Date picker
        self.__date_picker = DateTimePicker(self)
        self.layout().addWidget(self.__date_picker,2,2,1,1,Qt.AlignmentFlag.AlignCenter)

        # Add button
        add_button = QPushButton('ADD',self)
        add_button.setObjectName('submit')
        add_button.clicked.connect(self.__createGame)
        self.layout().addWidget(add_button,3,1,1,1,Qt.AlignmentFlag.AlignCenter)


    def __createGame(self):
        game_info_dict = {}
        players_ranking = [self.__team1_widget.getRanking(),self.__team2_widget.getRanking()]

        if any(len(team_ranking) > 1 for team_ranking in players_ranking) and any(player_id.strip() for team_ranking in players_ranking for player_id in team_ranking):

            game_info_dict['DATE'] = self.__date_picker.getDateTime()
            game_info_dict['ID'] = f"{game_info_dict['DATE']}-{'-'.join(sum(players_ranking))}"
            game_info_dict['RANKING'] = players_ranking

            game_info_dict['PROCESSED'] = False

            self.database['GAMES'][game_info_dict['ID']] = game_info_dict

            for player_id in sum(players_ranking):
                if not player_id in self.database['PLAYERS']:
                    createMMRPlayer(self.database['PLAYERS'],player_id)
            self.__ranking_widget.updatePlayersList(self.database['PLAYERS'])

            with open(self.__database_path,'w',encoding='utf-8') as database_file:
                dump(self.database,database_file)

            logging.info(f"Game {game_info_dict['ID']} saved in database")

        else:
            logging.error('Could not create game because of a lack of valid players')


    def setDatabasePath(self,database_path):
        """
        Sets the widget database, changes the pickable players in corresponding widgets

        @param (path) database_path : Absolute path to database file
        """
        self.__database_path = database_path
        with open(self.__database_path,'r',encoding='utf-8') as database_file:
            self.database = load(database_file)
        self.__team1_widget.updatePlayersList(self.database['PLAYERS'])
        self.__team2_widget.updatePlayersList(self.database['PLAYERS'])


    def clean(self):
        self.__date_picker.clean()
        self.__team1_widget.clean()
        self.__team2_widget.clean()
        self.__database_path = None
        self.database.clear()
