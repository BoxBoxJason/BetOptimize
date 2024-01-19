# -*- coding: utf-8 -*-
'''
Project : 
Package: 
Module: 
Version: 1.0
Usage: 
Author: BoxBoxJason
Date: 
'''

def applyKellyCriterion(win_prob,odds):
    """
    Applies the Kelly criterion to a bet.

    :param float win_prob: Probability of winning the bet.
    :param float odds: Odds of the bet.

    :return: float - Kelly criterion bet percentage.
    """
    return win_prob - (1 - win_prob) / odds
