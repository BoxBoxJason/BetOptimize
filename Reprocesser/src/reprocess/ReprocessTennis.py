# -*- coding: utf-8 -*-
'''
Project : Reprocesser
Package: reprocess
Module: ReprocessTennis
Version: 1.5
Usage: Used to reprocess Tennis ATP dataset into GamBible's readable database.
Author: BoxBoxJason
Date: 11/10/2023
'''
import logging
from resources.utils import createPlayerMMR,orderGamesTable
from resources.PathEnum import getJsonObject,dumpJsonObject,getDataPath

def fillMenTennisDataELO(games_table,players_table,source_folder_name,sort_games=False):
    """
    Fills database with dataset existing data, commits the changes into database file.

    :param dict games_table: Database Games table.
    :param dict players_table: Database Players table.
    :param path source_folder: Absolute path to dataset source folder.
    :param bool sort_games: Indicates if games should be sorted by date or not.
    """
    logging.info('Filling Tennis database (ELO)')
    terrains_by_tournament = {"wimbledon": "Grass", "us-open": "Hard", "australian-open": "Hard", "roland-garros": "Clay", "bournemouth": "Clay", "manchester": "Grass", "london": "Grass", "dublin": "Hard", "gstaad": "Clay", "montreal": "Hard", "hamburg": "Clay", "los-angeles": "Hard", "buenos-aires": "Clay", "perth": "Grass", "hobart": "Hard", "melbourne": "Grass", "sydney": "Hard", "auckland": "Hard", "philadelphia": "Hard", "new-york": "Hard", "south-african-open": "Hard", "durban": "Hard", "monte-carlo": "Clay", "brussels": "Carpet", "rome": "Clay", "bristol": "Grass", "houston": "Clay", "amersfoort": "Clay", "kitzbuhel": "Clay", "las-vegas": "Hard", "stockholm": "Hard", "paris": "Hard", "antwerp": "Hard", "north-miami-beach": "Carpet", "richmond": "Carpet", "salisbury": "Carpet", "chorpus-christi": "Hard", "macon": "Carpet", "szczecin": "Carpet", "wembley": "Carpet", "madeira": "Hard", "san-juan": "Hard", "st-petersburg": "Hard", "bermuda": "Clay", "dallas": "Carpet", "atlanta": "Hard", "st-louis": "Carpet", "casablanca": "Hard", "nottingham": "Grass", "eastbourne": "Grass", "newport": "Grass", "bastad": "Clay", "hoylake": "Grass", "washington": "Hard", "leicester": "Grass", "cincinnati": "Hard", "osaka": "Hard", "munich": "Clay", "boston": "Hard", "fort-worth": "Hard", "merion": "Grass", "south-orange": "Clay", "san-jose": "Hard", "vancouver": "Hard", "barcelona": "Clay", "midland": "Hard", "tucson": "Hard", "phoenix": "Hard", "nitto-atp-finals": "Hard", "budapest": "Clay", "caracas": "Hard", "east-london": "Hard", "palermo": "Clay", "catania": "Clay", "chicago": "Carpet", "tehran": "Clay", "tanglewood": "Hard", "columbus": "Hard", "quebec": "Hard", "senigallia": "Clay", "sacramento": "Carpet", "cologne": "Clay", "bologna": "Clay", "baltimore": "Carpet", "roanoke": "Carpet", "adelaide": "Hard", "omaha": "Hard", "des-moines": "Hard", "kansas-city": "Hard", "toronto": "Carpet", "sao-paulo": "Clay", "madrid": "Clay", "denver": "Carpet", "bretton-woods": "Clay", "tel-aviv": "Hard", "seattle": "Hard", "alamo": "Hard", "tokyo": "Hard", "essen": "Carpet", "nuembrecht": "Carpet", "rotterdam": "Hard", "singapore": "Hard", "jacksonville": "Hard", "birmingham": "Carpet", "la-costa": "Hard", "milan": "Carpet", "salt-lake-city": "Hard", "calgary": "Hard", "copenhagen": "Hard", "paramus": "Hard", "charleston": "Carpet", "calabasas": "Carpet", "bukhara": "Clay", "oporto": "Clay", "masters-doubles-wct": "Carpet", "berlin": "Clay", "aptos": "Hard", "manila": "Clay", "new-delhi": "Hard", "prague": "Clay", "hong-kong": "Hard", "jakarta": "Hard", "christchurch": "Hard", "lakeway": "Hard", "tulsa": "Hard", "hempstead": "Hard", "guaruja": "Hard", "tempe": "Hard", "tuscon": "Clay", "palm-desert": "Hard", "new-orleans": "Carpet", "surbiton": "Grass", "cedar-grove": "Hard", "san-diego": "Hard", "vienna": "Hard", "bombay": "Clay", "oslo": "Hard", "dusseldorf": "Clay", "nassau": "Carpet", "jerusalem": "Carpet", "basel": "Hard", "boca-west": "Hard", "san-antonio": "Carpet", "fairfield": "Carpet", "cairo": "Clay", "shreveport": "Carpet", "memphis": "Hard", "bronx": "Carpet", "istanbul": "Clay", "north-conway": "Clay", "aviles": "Hard", "calcutta": "Clay", "monterrey": "Carpet", "costa-rica": "Carpet", "lagos": "Clay", "honolulu": "Hard", "khartoum": "Hard", "tangier": "Carpet", "mexico-city": "Carpet", "indian-wells": "Hard", "mallorca": "Clay", "pepsi-grand-slam": "Clay", "sawgrass": "Clay", "bangalore": "Clay", "santiago": "Clay", "armonk": "Carpet", "napa": "Hard", "ocean-city": "Hard", "helsinki": "Carpet", "murcia": "Clay", "virginia-beach": "Clay", "laguna-niguel": "Hard", "aix-en-provence": "Clay", "bogota": "Hard", "oviedo": "Hard", "taipei": "Carpet", "hamilton": "Grass", "zurich": "Carpet", "sarasota": "Clay", "guadalajara": "Clay", "forest-hills": "Clay", "stuttgart": "Grass", "stowe": "Hard", "hartford": "Carpet", "capetown": "Clay", "bolton": "Carpet", "dorado-beach": "Hard", "nancy": "Hard", "louisville": "Hard", "lafayette": "Carpet", "brasilia": "Hard", "quito": "Clay", "ostrava": "Carpet", "metz": "Hard", "tampa": "Clay", "geneva": "Clay", "canton": "Carpet", "bangkok": "Hard", "sofia": "Hard", "vina-del-mar": "Clay", "mar-del-plata": "Clay", "linz": "Clay", "liege": "Clay", "venice": "Clay", "budaors": "Grass", "maceio": "Clay", "delray-beach": "Hard", "genova": "Carpet", "strasbourg": "Carpet", "hilton-head": "Clay", "zell-am-see": "Clay", "cap-dadge": "Clay", "naples": "Carpet", "amsterdam": "Carpet", "toulouse": "Hard", "ancona": "Carpet", "dortmund": "Carpet", "bahia": "Hard", "detroit": "Carpet", "lisbon": "Clay", "ferrara": "Carpet", "luxembourg": "Carpet", "livingston": "Hard", "treviso": "Clay", "miami": "Hard", "fort-myers": "Hard", "marbella": "Clay", "new-haven": "Hard", "athens": "Clay", "san-remo": "Clay", "atp-doubles-challenge-cup": "Hard", "lyon": "Clay", "seoul": "Hard", "schenectady": "Hard", "rye-brook": "Hard", "wellington": "Hard", "indianapolis": "Hard", "buzios": "Hard", "warsaw": "Clay", "marrakech": "Clay", "oeiras": "Clay", "umag": "Clay", "s-hertogenbosch": "Grass", "long-island": "Hard", "moscow": "Hard", "doha": "Hard", "kuala-lumpur": "Hard", "dubai": "Hard", "marseille": "Hard", "acapulco": "Hard", "besancon": "Carpet", "halle": "Grass", "bucharest": "Clay", "beijing": "Hard", "oahu": "Hard", "montevideo": "Clay", "ho-chi-minh-city": "Carpet", "split": "Carpet", "chennai": "Hard", "rio-de-janeiro": "Clay", "brighton": "Hard", "tashkent": "Hard", "merano": "Clay", "valencia": "Hard", "zagreb": "Hard", "mumbai": "Hard", "brisbane": "Hard", "johannesburg": "Hard", "belgrade": "Clay", "shanghai": "Hard", "montpellier": "Hard", "winston-salem": "Hard", "shenzhen": "Hard", "estoril": "Clay", "los-cabos": "Hard", "chengdu": "Hard", "antalya": "Grass"}
    games_wins_dict = getJsonObject(getDataPath('Tennis',source_folder_name,'gamesWin.json'))
    tourneys_max_round = {}
    new_games = set()

    for game in games_wins_dict:
        if not game['match_id'] in games_table:
            new_games.add(game['match_id'])
            createTennisGameELO(games_table,game,tourneys_max_round,terrains_by_tournament)

            for player_slug in game['winner_slug'],game['loser_slug']:
                if not player_slug in players_table:
                    createTennisPlayerELO(players_table,player_slug)

    for tourney_year_id,round_set in tourneys_max_round.items():
        tourneys_max_round[tourney_year_id] = max(round_set)

    for game in games_wins_dict:
        if game['match_id'] in new_games:
            tourney_year_id = game['tourney_year_id']
            games_table[game['match_id']]['DATE'] = f"{tourney_year_id.split('-')[0]}-{game['tourney_order']}-{1 + tourneys_max_round[tourney_year_id] - game['round_order']}-{game['match_order']}"

    if sort_games:
        games_table = orderGamesTable(games_table)

    dumpJsonObject({'GAMES':games_table,'PLAYERS':players_table},getDataPath('Tennis','Men','defaultELO.json'))


def createTennisGameELO(games_table,game_dict,tourneys_max_round,terrains_by_tournament):
    """
    Creates a new game dict in the Games table (used only for tennis games).

    :param dict games_table: Database Games table.
    :param dict game_dict: Source folder game dictionary.
    :param dict tourneys_max_round: Dictionary used to count the maximum number of rounds per tournament.
    :param dict terrains_by_tournament: Tournament terrain by name.
    """
    tourney_year_id = game_dict['tourney_year_id']
    round_order = game_dict['round_order']
    if not tourney_year_id in tourneys_max_round:
        tourneys_max_round[tourney_year_id] = set()
    tourneys_max_round[tourney_year_id].add(round_order)

    games_table[game_dict['match_id']] = {
    'ID':game_dict['match_id'],
    'DATE':f"{tourney_year_id.split('-')[0]}-{game_dict['tourney_order']}-{round_order}-{game_dict['match_order']}",
    'TERRAIN':terrains_by_tournament.get(game_dict['tourney_slug'],'Unknown'),
    'WINNER_ID':game_dict['winner_slug'],
    'LOSER_ID':game_dict['loser_slug'],
    'PROCESSED':False
    }


START_ELO = 1500

def createTennisPlayerELO(players_table,player_slug):
    """
    Creates a new player dict in the Players table.

    :param dict players_table: Database Players table.
    :param str player_slug: Source (unique) player slug (id).
    """
    players_table[player_slug] = {
        'ID':player_slug,
        'ELO':START_ELO,
        'FAV_TERRAIN':{},
        'GAMES':[]
    }


def fillMenTennisDataMMR(games_table,players_table,source_folder_name,sort_games=False):
    """
    Fills database with dataset existing data, commits the changes into database file.

    :param dict games_table: Database Games table.
    :param dict players_table: Database Players table.
    :param path source_folder: Absolute path to dataset source folder.
    :param bool sort_games: Indicates if games should be sorted by date or not.
    """
    logging.info('Filling Tennis database (MMR)')

    games_wins_dict = getJsonObject(getDataPath('Tennis',source_folder_name,'gamesWin.json'))

    tourneys_max_round = {}

    for game in games_wins_dict:
        if not game['match_id'] in games_table:
            createTennisGameMMR(games_table,players_table,game,tourneys_max_round)

    for tourney_year_id,round_set in tourneys_max_round.items():
        tourneys_max_round[tourney_year_id] = max(round_set)

    for game in games_wins_dict:
        tourney_year_id = game['tourney_year_id']
        games_table[game['match_id']]['DATE'] = f"{tourney_year_id.split('-')[0]}-{game['tourney_order']}-{1 + tourneys_max_round[tourney_year_id] - game['round_order']}-{game['match_order']}"

    if sort_games:
        games_table = orderGamesTable(games_table)

    dumpJsonObject({'GAMES':games_table,'PLAYERS':players_table},getDataPath('Tennis','Men','defaultMMR-FFA.json'))


def createTennisGameMMR(games_table,players_table,game_dict,tourneys_max_round):
    """
    Creates a new row in Games table (used only for tennis games).

    :param dict games_table: Database Games table.
    :param dict players_table: Database Players table.
    :param dict game_dict: Source game dictionary.
    :param dict tourneys_max_round: Dictionary used to count the maximum number of rounds per tournament.
    """
    tourney_year_id = game_dict['tourney_year_id']
    round_order = game_dict['round_order']
    if not tourney_year_id in tourneys_max_round:
        tourneys_max_round[tourney_year_id] = set()
    tourneys_max_round[tourney_year_id].add(round_order)

    games_table[game_dict['match_id']] = {
        'ID':game_dict['match_id'],
        'DATE':f"{tourney_year_id.split('-')[0]}-{game_dict['tourney_order']}-{round_order}-{game_dict['match_order']}",
        'RANKING':[game_dict['winner_slug'],game_dict['loser_slug']],
        'PROCESSED':False
    }

    for player_id in game_dict['winner_slug'],game_dict['loser_slug']:
        if not player_id in players_table:
            createPlayerMMR(players_table,player_id)
