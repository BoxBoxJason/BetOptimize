'''
Created on 5 oct. 2023

@author: BoxBoxJason
'''
import os
from json import dump,load

class PathEnum:
    """
    Paths enum, contains absolute paths to project resources
    """
    # Project root folder path
    BROCOLLECT = os.getenv("BROCOLLECT")
    # Results path
    RESULTS = os.path.join(BROCOLLECT,"results")
    # Project resources folder path
    RESOURCES = os.path.join(BROCOLLECT,"src","resources")
    # Project images folder path
    IMAGES = os.path.join(RESOURCES,"images")
    # Config file path
    CONFIG = os.path.join(RESOURCES,"config","config.json")


def getImage(imageName):
    """
    @param (str) imageName : name of the image to get
    
    @return (path) imagePath : absolute path to the requested image
    """
    return os.path.join(PathEnum.IMAGES,imageName)


def getStyleSheet():
    with open(os.path.join(PathEnum.RESOURCES,'BroCollect.qss'),'r',encoding='utf-8') as stylesheet_file:
        return stylesheet_file.read()


def getDBPath(sport,category,db_name):
    """
    @param (str) sport : sport name
    @param (str) category : sport category
    @param (str) db_name : database file name


    """
    db_path = os.path.join(PathEnum.RESULTS,sport,category,db_name)
    os.makedirs(os.path.dirname(db_path),777,True)
    if not os.path.exists(db_path):
        with open(db_path,'w',encoding='utf-8') as db_file:
            dump({'PLAYERS':{},'GAMES':{}},db_file)
    return db_path


def getConfig():
    """
    @return (dict) configuration dict
    """
    with open(PathEnum.CONFIG,'r',encoding='utf-8') as config_file:
        config_dict = load(config_file)
    return config_dict


def getFontsPaths():
    """    
    @return (path[]) absolute paths to font files
    """
    fonts_path = os.path.join(PathEnum.RESOURCES,'fonts')
    return [os.path.join(fonts_path,file_name) for file_name in os.listdir(fonts_path)]
