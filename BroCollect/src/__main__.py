# -*- coding: utf-8 -*-
'''
Created on 3 oct. 2023

BroCollect
The purpose of this tool is to collect sport's games results data to constitute a database
The database has to respect a certain format to be readable by BoxGambi (gamble optimization tool)

@version 1.1
@copyright: Created by BoxBoxJason, All Rights Reserved
'''
import logging
import os
import sys
from PyQt6.QtWidgets import QApplication
projectPath = os.path.realpath(os.path.dirname(os.path.dirname(__file__)))
os.environ["BROCOLLECT"] = projectPath
from interface.BroCollect import BroCollect,addFonts
from resources.PathEnum import getStyleSheet

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(__file__),"logging.log")),
        logging.StreamHandler(sys.stdout)
    ]
)

logging.info("Starting BroCollect V1.1")

app = QApplication(sys.argv)
app.setStyleSheet(getStyleSheet())
collector = BroCollect()
addFonts()
collector.show()

app.exec()

logging.info("Closing BroCollect V1.1, See you later !")
