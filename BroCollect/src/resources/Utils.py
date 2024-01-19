# -*- coding: utf-8 -*-
'''
Created on 4 oct. 2023

@author: BoxBoxJason
'''
import os
import json
from json.decoder import JSONDecodeError
import logging
from sys import exit as sysExit
from resources.PathEnum import PathEnum


def checkSource(sourceFilePath,loadDict=True):
    """
    Checks source file and fixes issues with it if possible, ends program otherwise
    
    @param (path) sourceFilePath : path to source .json file
    
    @return (dict) sourceDict : Existing source dictionary with game history information
    """
    logging.debug(f"Checking source file at {sourceFilePath}")
    sourceDict = {}

    if os.path.isdir(sourceFilePath):
        logging.fatal(f"{sourceFilePath} was replaced by a folder with the same name, please don't pull such pranks")
        sysExit(1)

    elif os.path.exists(sourceFilePath):
        if loadDict:
            try:
                with open(sourceFilePath,'r',encoding='utf-8') as sourceFileContent:
                    sourceDict = json.load(sourceFileContent)
                    logging.info(f"Source data successfuly retrieved, ({len(sourceDict)} existing games)")
            except (TypeError,JSONDecodeError):
                logging.fatal(f"Source .json file is corrupted, check at {sourceFilePath}")
                sysExit(1)

    else:
        logging.error(f"Source file not found, creating an empty one at {sourceFilePath}")
        os.makedirs(os.path.dirname(sourceFilePath),777,True)

        with open(sourceFilePath,'w',encoding='utf-8') as outputFile:
            json.dump(sourceDict,outputFile,indent=2)

    return sourceDict


def checkConfig():
    """
    Checks if config file can be found and read
    """
    configContent = {}
    if os.path.exists(PathEnum.CONFIG) and os.access(PathEnum.CONFIG, os.W_OK) and os.access(PathEnum.CONFIG,os.R_OK):
        try:
            with open(PathEnum.CONFIG,'r',encoding='utf-8') as sourceFileContent:
                configContent = json.load(sourceFileContent)
        except (TypeError,JSONDecodeError):
            logging.fatal(f"Config .json file is corrupted, check at {PathEnum.CONFIG}")
            sysExit(1)

    else:
        logging.fatal(f"Config file not found or does not have read and write permissions at {PathEnum.CONFIG}")
        sysExit(1)
    
    return configContent

def buildGameId(gameTimestamp,idP1,idP2):
    """
    Builds a unique game id from game data
    
    @param (int) gameTimestamp : timestamp representing datetime at which game started
    @param (str) idP1 : Player 1 id
    @param (str) idP2 : Player 2 id
    
    @return (str) gameId : Unique game id
    """
    gameId = f"{gameTimestamp}-{idP1}vs{idP2}"
    return gameId
