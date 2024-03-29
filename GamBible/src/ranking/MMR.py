#-*- coding: utf-8 -*-
'''
Project : GamBible
Package: Ranking
Module:  MMR
Version: 2.0
Usage: Provides all MMR algorithm functionalities, allows for player ranking and games processing

Author: BoxBoxJason
Date: 13/10/2023
'''
from math import tanh,pi,sqrt
from copy import copy
import logging
from optuna import create_study,load_study,visualization
from resources.utils import findZeroBisection
from resources.PathEnum import getDBPath,getJsonObject,dumpJsonObject
from ranking.general import orderGamesTable

# Player default skill value
START_SKILL = 1500
# Player default skill deviation (skill uncertainty)
START_DEVIATION = 350

def processGames(output_file_path,games_table,players_table,γ=39.948612168502336,β=21.314329431412908,ρ=5675.089387551527,commit=False,games_ordered_ids=None):
    """
    Processes the entire history file and updates players dict with new games informations.
    
    :param path output_file_path: Absolute path to database file.
    :param dict games_table: Database games table.
    :param dict players_table: Database players_table.
    :param float γ: Temporal diffusion [0,inf[.
    :param float β: Performance deviation [0,inf[.
    :param float ρ: 1/ρ Inverse momentum -> player ranking volatility in case of sudden level change.
    :param bool commit: States if changes should be commited to database or not.

    :return: float - MMR algorithm prediction success rate
    """
    logging.info('Processing new games')
    if games_ordered_ids is None:
        games_ordered_ids = orderGamesTable(games_table)

    total_processed_games = 0
    predicted_output = 0
    for game_id in games_ordered_ids:
        if not games_table[game_id]['PROCESSED']:
            predicted_output += processGame(players_table,games_table[game_id],γ,β,ρ)
            total_processed_games += 1

    if commit:
        dumpJsonObject({'GAMES':games_table,'PLAYERS':players_table},output_file_path)

    success_rate = 0
    if total_processed_games != 0:
        success_rate = predicted_output / total_processed_games

    logging.debug(f"Processed {total_processed_games} new games")
    return success_rate


def processGame(players_table,game_dict,γ,β,ρ):
    """
    Updates all rankings according to game results.
    
    :param dict players_table: Database Players table.
    :param str game_dict: Database Games table row.
    :param float γ: Temporal diffusion [0,inf[.
    :param float β: Performance deviation [0,inf[.
    :param float ρ: 1/ρ Inverse momentum -> player ranking volatility in case of sudden level change.

    :return: float - Success rate of game outcome prediction by MMR algorithm
    """
    # Adding unknown players to playersDict
    ranking_skills = [players_table[player_id]['SKILL'] - 3 * players_table[player_id]['SKILL_DEVIATION'] for player_id in game_dict['RANKING']]
    sorted_skill = sorted(ranking_skills,reverse=True)
    result_predicted = sum(x == y for x, y in zip(ranking_skills[:3], sorted_skill[:3])) / len(ranking_skills[:3])

    for player_id in game_dict['RANKING']:
        diffuse(players_table[player_id],γ,ρ)
        players_table[player_id]['SKILL_DEVIATION'] = sqrt(players_table[player_id]['SKILL_DEVIATION'] ** 2 + β ** 2)

    new_dicts = []
    # Perform update in parallel
    for i in range(len(game_dict['RANKING'])):
        new_dicts.append(update([copy(players_table[player_id]) for player_id in game_dict['RANKING']],i,β))

    # Apply update
    for i,player_id in enumerate(game_dict['RANKING']):
        players_table[player_id] = new_dicts[i]

    game_dict['PROCESSED'] = True

    return result_predicted


def diffuse(player_dict,γ,ρ):
    """
    Updates changes in player skill.

    :param dict player_dict: Database Players row.
    :param float γ: Temporal diffusion [0,inf[.
    :param float ρ: 1/ρ Inverse momentum -> player ranking volatility in case of sudden level change.
    """
    ϰ = 1 / (1 + (γ / player_dict['SKILL_DEVIATION']) ** 2)
    wg = ϰ ** ρ * player_dict['PERF_WEIGHT'][0]
    wl = (1 - ϰ ** ρ) * sum(player_dict['PERF_WEIGHT'])

    w = wg + wl
    if w != 0:
        player_dict['PERF_HISTORY'][0] = (wg * player_dict['PERF_HISTORY'][0] + wl * player_dict['SKILL']) / (wg + wl)
        player_dict['PERF_WEIGHT'][0] = ϰ * (wg + wl)
    else:
        player_dict['PERF_HISTORY'][0] = player_dict['PERF_HISTORY'][0] + player_dict['SKILL']
        player_dict['PERF_WEIGHT'][0] = 0

    for i in range(len(player_dict['PERF_WEIGHT'])):
        player_dict['PERF_WEIGHT'][i] *= ϰ ** (1 + ρ)
    player_dict['SKILL_DEVIATION'] *= sqrt(ϰ)


def update(players_ranking,selected_player_index,β):
    """
    Updates the player average skill evaluation.

    :param list[dict] players_ranking: List of player dicts, order corresponds to game outcome.
    :param int selected_player_index: Index (in players_ranking) of the player to update.
    :param float β: Performance deviation [0,inf[.
    """
    p = getPerfEstimation(players_ranking, selected_player_index)
    players_ranking[selected_player_index]['PERF_HISTORY'].append(p)
    players_ranking[selected_player_index]['PERF_WEIGHT'].append(1 / β ** 2)

    players_ranking[selected_player_index]['SKILL'] = getAverageSkillEstimation(players_ranking[selected_player_index],β)

    return players_ranking[selected_player_index]


def getAverageSkillEstimation(player_dict,β):
    """
    Returns updated player's average skill.

    :param dict player_dict: Database Players table row.
    :param float β: Performance deviation [0,inf[.

    :return: float - Player updated average skill.
    """
    def estimationFunction(x):
        val = player_dict['PERF_WEIGHT'][0] * (x - player_dict['PERF_HISTORY'][0])
        for game_index,perf_weight in enumerate(player_dict['PERF_WEIGHT']):
            val += perf_weight * β / (sqrt(3) / pi) * tanh((x - player_dict['PERF_HISTORY'][game_index]) / (2 * sqrt(3) / pi * β))

        return val

    return findZeroBisection(estimationFunction)


def getPerfEstimation(players_ranking,selected_player_index):
    """
    Returns updated player's average performance for a game.

    :param list[dict] players_ranking: List of player dicts, order corresponds to game outcome.
    :param int selected_player_index: Index (in players_ranking) of the player to update.

    :return: float - Player's game performance estimation
    """
    def estimationFunction(x):
        val = 0
        for player_dict in players_ranking[0:selected_player_index+1]:
            val += 1 / player_dict['SKILL_DEVIATION'] * (tanh((x - player_dict['SKILL']) / (2 * sqrt(3) / pi * player_dict['SKILL_DEVIATION'])) - 1)

        for player_dict in players_ranking[selected_player_index:]:
            val += 1 / player_dict['SKILL_DEVIATION'] * (tanh((x - player_dict['SKILL']) / (2 * sqrt(3) / pi * player_dict['SKILL_DEVIATION'])) + 1)

        return val

    return findZeroBisection(estimationFunction)


def createGame(games_table,players_table,game_id,game_date,game_ranking):
    """
    Creates a new game dict in the Games table.

    :param dict games_table: Database Games table.
    :param dict players_table: Database Players table.
    :param str game_id: Game (unique) id.
    :param str game_date : Game date.
    :param list[int] game_ranking: List of player ids ranked (winner is first, loser is last).
    """
    games_table[game_id] = {
    'ID':game_id,
    'DATE':game_date,
    'RANKING':game_ranking,
    'PROCESSED':False
    }

    for player_id in game_ranking:
        players_table[player_id]['GAMES'].append(game_id)


def optimizeHyperparametersBayesian(sport,category):
    db_path = getDBPath(sport,category,'defaultMMR-FFA.json')
    games_ordered_ids = orderGamesTable(getJsonObject(db_path)['GAMES'])

    def objective(trial):
        γ = trial.suggest_float('γ',1e-6,50)
        β = trial.suggest_float('β',1e-6,50)
        ρ = trial.suggest_float('ρ',1e-6,10000)
        gambible_db = getJsonObject(db_path)
        success_rate = processGames(db_path,gambible_db['GAMES'],gambible_db['PLAYERS'],γ,β,ρ,False,games_ordered_ids)

        return success_rate

    study_name = f"{sport} MMR-{category} configuration"
    configuration_db_path = f"sqlite:///{getDBPath(sport,category,'configurationMMR.db',False)}"

    try:
        study = load_study(study_name=study_name,storage=configuration_db_path)
    except:
        study = create_study(direction='maximize',study_name=study_name,storage=configuration_db_path)
    
    #visualization.plot_optimization_history(study).show()
    #visualization.plot_parallel_coordinate(study).show()
    #visualization.plot_slice(study).show()
    #visualization.plot_param_importances(study).show()
    study.optimize(objective,n_trials=1000)
    print(study.best_params,study.best_value)
