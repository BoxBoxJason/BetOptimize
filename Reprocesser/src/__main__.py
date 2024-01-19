# -*- coding: utf-8 -*-
'''
Created on 11 oct. 2023

@author: BoxBoxJason
'''
from os.path import join,dirname,realpath
from os import environ
from sys import stdout
import logging
project_path = realpath(dirname(dirname(__file__)))
environ['REPROCESSER'] = project_path
from reprocess.ReprocessF1 import fillF1MenData
##----------Logging setup----------##
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(join(project_path,"logging.log")),
        logging.StreamHandler(stdout)
    ]
)

fillF1MenData({},{},True)
