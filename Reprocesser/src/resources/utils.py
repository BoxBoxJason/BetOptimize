# -*- coding: utf-8 -*-
'''
Project : Reprocesser
Package: resources
Module: utils
Author: BoxBoxJason
Date: 23/11/2023
'''

START_SKILL = 1500
START_DEVIATION = 350
def createPlayerMMR(players_table,player_slug):
    """
    Creates a new row in Players table

    :param dict players_table: Database Players table.
    :param str player_slug: Source player (unique) slug (id).
    """
    players_table[player_slug] = {
        'ID':player_slug,
        'SKILL':START_SKILL,
        'SKILL_DEVIATION':START_DEVIATION,
        'PERF_HISTORY':[START_SKILL],
        'PERF_WEIGHT':[1/START_DEVIATION],
        'GAMES':[]
    }


def createGameMMR(games_table,game_id,game_date,game_ranking):
    """
    Creates a new row in the Games table.

    :param dict games_table: Database Games table.
    :param str game_id: (unique) game id.
    :param str game_date: Game date.
    :param list[str]: List of players ids ranked by game performance (0: winner, -1: loser)
    """
    games_table[game_id] = {
        'ID':game_id,
        'DATE':game_date,
        'RANKING':game_ranking,
        'PROCESSED':False
    }


def orderGamesTable(games_table):
    """
    Orders the Games table by dates and returns a list of ids ordered by corresponding date.

    :param dict games_table: Database Games table.

    :return: list[str] - List of games ids ordered by date.
    """
    games_table_list = list(games_table.values())
    games_table_list.sort(key = lambda x : x['DATE'])

    return [game_dict['ID'] for game_dict in games_table_list]
