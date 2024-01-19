# -*- coding: utf-8 -*-
'''
Project : GamBible
Package: interface.games
Module:  OneVOneWidget
Version: 2.0
Usage: 1v1 game prediction widget, allows to pick two players and predict the game outcome (with a confidence rate)

Author: BoxBoxJason
Date: 09/10/2023
'''
from PyQt6.QtWidgets import QWidget,QLabel,QPushButton,QVBoxLayout,QLineEdit,QCompleter,QSlider
from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtCore import Qt,QStringListModel
from interface.TemplateWidget import TemplatePageWidget
from resources.PathEnum import getJsonObject
from ranking.ELO import determineWinProbability,processGames
from ranking.bet import applyKellyCriterion

class OneVOneWidget(TemplatePageWidget):
    """
    1v1 game outcome prediction widget.

    :ivar dict players_table: Database Players table.
    :ivar PlayerWidget __player1_widget: Player 1 information collection display widget.
    :ivar PlayerWidget __player2_widget: Player 2 information collection display widget.
    :ivar QLabel __prediction_confidence_rate_qlabel: Label used to display prediction confidence rate.
    """
    def __init__(self,parent):
        """
        Constructor for OneVOneWidget

        :param QWidget parent: Parent widget.
        """
        super().__init__(parent)
        self.players_table = {}

        # Player selection  
        self.__player1_widget = PlayerWidget(self,1)
        self.__player2_widget = PlayerWidget(self,2)
        self.layout().addWidget(self.__player1_widget,2,0,1,1,Qt.AlignmentFlag.AlignCenter)
        self.layout().addWidget(self.__player2_widget,2,1,1,1,Qt.AlignmentFlag.AlignCenter)

        # Bet amount selection
        bet_amount_label = QLabel('Max Bet amount',self)
        bet_amount_label.setObjectName('h3')
        self.layout().addWidget(bet_amount_label,3,0,1,2,Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)

        self.__betSlider = QSlider(Qt.Orientation.Horizontal,self)
        self.__betSlider.setRange(0,100)
        self.__betSlider.setValue(20)
        self.__betSlider.setTickInterval(1)
        self.__betSlider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.layout().addWidget(self.__betSlider,4,0,1,1,Qt.AlignmentFlag.AlignRight)

        self.__bet_amount_label = QLabel(self)
        self.__bet_amount_label.setObjectName('p')
        self.__bet_amount_label.setText(f"Bet amount: {self.__betSlider.value()}€")
        self.__betSlider.valueChanged.connect(lambda: self.__bet_amount_label.setText(f"Bet amount: {self.__betSlider.value()}€"))
        self.layout().addWidget(self.__bet_amount_label,4,1,1,1,Qt.AlignmentFlag.AlignLeft)

        # Predict button
        predict_button = QPushButton('PREDICT',self)
        predict_button.setObjectName('submit')
        predict_button.clicked.connect(self.__predictGameOutput)
        self.layout().addWidget(predict_button,5,0,1,2,Qt.AlignmentFlag.AlignCenter)


    def setDatabase(self,database_path):
        """
        Sets the widget database, changes the pickable players in corresponding widgets.

        :param path database_path: Absolute path to database file.
        """
        database = getJsonObject(database_path)
        games_table = database['GAMES']
        self.players_table = database['PLAYERS']
        processGames(database_path,games_table,self.players_table,28.163265306122447,3.33265306122449,1,True)
        self.__player1_widget.updatePlayersList(self.players_table)
        self.__player2_widget.updatePlayersList(self.players_table)


    def __predictGameOutput(self):
        """
        Predicts the outcome of the game and displays prediction confidence rate
        """
        player1_id = self.__player1_widget.search_bar.text()
        player2_id = self.__player2_widget.search_bar.text()
        if player1_id in self.players_table and player2_id in self.players_table and player1_id != player2_id:
            player1_winrate = determineWinProbability(self.players_table[player1_id]['ELO'],self.players_table[player2_id]['ELO'])
            player2_winrate = 1 - player1_winrate

            # Player 1 winrate display
            self.__player1_widget.player_winrate_qlabel.setText(f"Win chances: {'{:.2f}'.format(player1_winrate*100)}%")

            # Player 2 winrate display
            self.__player2_widget.player_winrate_qlabel.setText(f"Win chances: {'{:.2f}'.format(player2_winrate*100)}%")

            p1_bet_suggestion = applyKellyCriterion(player1_winrate,self.__player1_widget.getPlayerOdds()) * self.__betSlider.value()
            self.__player1_widget.player_bet_suggestion.setText(f"Suggested bet: {'{:.2f}'.format(p1_bet_suggestion) if p1_bet_suggestion > 0 else '0'}€")
            
            p2_bet_suggestion = applyKellyCriterion(player2_winrate,self.__player2_widget.getPlayerOdds()) * self.__betSlider.value()
            self.__player2_widget.player_bet_suggestion.setText(f"Suggested bet: {'{:.2f}'.format(p2_bet_suggestion) if p2_bet_suggestion > 0 else '0'}€")


    def clean(self):
        """
        Cleans the widget
        """
        super().clean()
        self.players_table.clear()
        self.__player1_widget.clean()
        self.__player2_widget.clean()


WRONG_INPUT_STYLE = "QLineEdit {background-color: #edab9f; border: 2px ridge #bf1d00; padding: 5px 10px;}"
CORRECT_INPUT_STYLE = "QLineEdit {background-color: #b3f5a4;border: 2px ridge #229608;padding: 5px 10px;}"

class PlayerWidget(QWidget):
    """
    Player picker widget. Contains a search bar with auto complete. The search bar goes green if input is in database, else it goes red
    Contains a victory rate display

    :ivar QLineEdit search_bar: Player search bar, used to add players to game.
    :ivar QCompleter completer: Search bar completer. Contains players ids in database.
    :ivar QLabel player_winrate_qlabel: Player win probability display.
    """
    def __init__(self,parent,player_index):
        """
        Constructor for PlayerWidget.

        :param QWidget parent: Parent widget.
        :param int player_index: Player index (for head label display purposes).
        """
        super().__init__(parent)
        layout = QVBoxLayout(self)

        # Player title label
        title_qlabel = QLabel(f"Player {player_index}",self)
        title_qlabel.setObjectName('h3')
        layout.addWidget(title_qlabel,0,Qt.AlignmentFlag.AlignHCenter)

        # Player search bar
        self.search_bar = QLineEdit(self)
        self.search_bar.setStyleSheet(CORRECT_INPUT_STYLE)
        self.search_bar.textChanged.connect(self.__updateBg)
        layout.addWidget(self.search_bar,0,Qt.AlignmentFlag.AlignHCenter)

        # Search bar completer
        self.completer = QCompleter(self)
        self.completer.setCompletionMode(QCompleter.CompletionMode.InlineCompletion)
        self.search_bar.setCompleter(self.completer)

        # Odds input
        self.__player_odds_input = QLineEdit(self)
        self.__player_odds_input.setPlaceholderText('Odds')
        self.__player_odds_input.setValidator(QDoubleValidator())
        layout.addWidget(self.__player_odds_input,0,Qt.AlignmentFlag.AlignHCenter)

        # Player winrate
        self.player_winrate_qlabel = QLabel(self)
        self.player_winrate_qlabel.setObjectName('p')
        layout.addWidget(self.player_winrate_qlabel,0,Qt.AlignmentFlag.AlignHCenter)

        # Player bet suggestion
        self.player_bet_suggestion = QLabel(self)
        self.player_bet_suggestion.setObjectName('p')
        layout.addWidget(self.player_bet_suggestion,0,Qt.AlignmentFlag.AlignHCenter)


    def getPlayerOdds(self):
        """
        Returns the player odds input.

        :return: float - Player odds input.
        """
        odds_txt = self.__player_odds_input.text().strip().replace(',','.')
        return float(odds_txt) if odds_txt else 1e-9


    def __updateBg(self,text):
        """
        Updates search bar background color depending if the player is known in database or not.

        :param str text: Text in the search bar.
        """
        first_suitable_element = None
        for player_id in self.parent().players_table:
            if text in player_id:
                first_suitable_element = player_id
                break
        
        if first_suitable_element is not None:
            self.search_bar.setStyleSheet(CORRECT_INPUT_STYLE)
        else:
            self.search_bar.setStyleSheet(WRONG_INPUT_STYLE)


    def clean(self):
        """
        Cleans the widget
        """
        for i in range(1,self.layout().count()):
            self.layout().itemAt(i).widget().clear()


    def updatePlayersList(self, players_ids):
        """
        Updates players list in the completer.

        :param list[str] players_ids: List of players ids.
        """
        self.completer.setModel(QStringListModel(players_ids, self.completer))
