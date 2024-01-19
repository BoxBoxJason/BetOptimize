# -*- coding: utf-8 -*-
'''
Project : Reprocesser
Package: resources
Module:  PathEnum
Version: 1.5
Usage: Contains project useful paths and path / files related functions

Author: BoxBoxJason
Date: 23/11/2023
'''

import os
import logging
from json import load,dump

class PathEnum:
    """
    PathEnum contains absolute paths to project files system.

    :cvar path REPROCESSER: Absolute path to project root folder.
    :cvar path RESOURCES: Absolute path to project resources folder.
    :cvar path CONFIG: Absolute path to project config json file.
    :cvar path DATA: Absolute path to project data folder.
    """
    REPROCESSER = os.getenv('REPROCESSER')

    RESOURCES = os.path.join(REPROCESSER,'src','resources')

    CONFIG = os.path.join(RESOURCES,'config','config.json')

    DATA = os.path.join(REPROCESSER,'data')


def getDataPath(sport,folder_name,file_name):
    """
    Returns requested data resource absolute path. Creates parent folder if it does not exist.

    :param str sport: Sport folder name.
    :param str folder_name: Subfolder name.
    :param str file_name: File name.

    :return: path - Absolute path to resource.
    """
    data_path = os.path.join(PathEnum.DATA,sport,folder_name,file_name)
    os.makedirs(os.path.dirname(data_path),511,True)
    return data_path


def getFileContent(file_path):
    """
    Returns the content of a file.
    If file does not exists, returns an empty string.

    :param path file_path: Absolute path to file.

    :return: str - Content of the file.
    """
    result = ""
    if os.access(file_path,os.R_OK):
        with open(file_path,'r',encoding='utf-8') as file:
            result = file.read()
    else:
        logging.warning(f"File {file_path} does not exist or is unreadable")

    return result


def getJsonObject(file_path):
    """
    Returns the content of a file casted into a python json compatible object.

    :param path file_path: Absolute path to file.

    :return: Result from parsing the file content with json.load
    """
    os.makedirs(os.path.dirname(file_path),511,True)
    result = {}
    if os.access(file_path,os.R_OK):
        with open(file_path,'r',encoding='utf-8') as json_file:
            result = load(json_file)
    else:
        logging.warning(f"File {file_path} does not exist or is unreadable")

    return result


def dumpJsonObject(json_object,file_path):
    """
    Overwrites json object to file_path.

    :param JsonObject json_object: JSON compatible object to save in file.
    :param path file_path: Absolute path to destination file.
    """
    os.makedirs(os.path.dirname(file_path),511,True)
    if not (os.path.exists(file_path) and not os.access(file_path,os.W_OK)):
        with open(file_path,'w',encoding='utf-8') as json_file:
            dump(json_object,json_file,indent=2)
    else: 
        logging.error(f"Cannot overwrite file at {file_path}. Lacking write permissions")
