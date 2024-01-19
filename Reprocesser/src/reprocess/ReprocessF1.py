# -*- coding: utf-8 -*-
'''
Project : Reprocesser
Package: reprocess
Module: ReprocessF1
Version: 1.0
Usage: Used to reprocess
Author: BoxBoxJason
Date: 25/11/2023
'''

from resources.PathEnum import getFileContent,getDataPath,dumpJsonObject
from resources.utils import createPlayerMMR,createGameMMR,orderGamesTable

def fillF1MenData(games_table,players_table,sort_games=False):
    """
    Fills F1 database with dataset existing data, commits the changes into database file.

    :param dict games_table: Database Games table.
    :param dict players_table: Database Players table.
    :param path source_folder_path: Absolute path to dataset source folder.
    :param bool sort_games: Indicates if games should be sorted by date or not.
    """

    ## CREATE PLAYERS ##
    # Map of player numeric id and player string id
    players_redirect = {}

    for driver_line in getFileContent(getDataPath('F1','archive','drivers.csv')).replace('"','').split('\n')[1:-1]:
        driver_line_split = driver_line.split(',')
        players_redirect[driver_line_split[0]] = f"{driver_line_split[4]}-{driver_line_split[5]}".lower()

        createPlayerMMR(players_table,players_redirect[driver_line_split[0]])

    ## CREATE GAMES ##
    tmp_games = {}
    for race_line in getFileContent(getDataPath('F1','archive','races.csv')).replace('"','').split('\n')[1:-1]:
        race_line_split = race_line.split(',')
        race_date = '-'.join(race_line_split[5].split('/')[::-1])
        race_time = '00:00'
        if race_line_split[6] != '\\N':
            race_time = ':'.join(race_line_split[6].split(':')[:2])
        game_date = f"{race_date} {race_time}"
        createGameMMR(tmp_games,race_line_split[0],game_date,[])

    for result_line in getFileContent(getDataPath('F1','archive','results.csv')).replace('"','').split('\n')[1:-1]:
        result_line_split = result_line.split(',')
        tmp_games[result_line_split[1]]['RANKING'].append(players_redirect[result_line_split[2]])


    for tmp_game in tmp_games.values():
        if len(tmp_game['RANKING']) > 2:
            createGameMMR(games_table,f"{tmp_game['DATE']}-{'-'.join(tmp_game['RANKING'])}",tmp_game['DATE'],tmp_game['RANKING'])

    if sort_games:
        games_table = orderGamesTable(games_table)

    dumpJsonObject({'GAMES':games_table,'PLAYERS':players_table},getDataPath('F1','Men','defaultMMR-FFA.json'))
