#!/usr/bin/env python3

import os

from selenium import webdriver
from dateutil.parser import parse

#----------------Utils---------------------------------------------------------------------------------------

all_players_option = '/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[1]/div/div/select/option[1]'

def initialize_chrome_driver():
    """
    Creates a chrome driver instance. 
    """
    cwd = os.getcwd()
    chromedriver_path = cwd + '/chromedriver' 
    browser = webdriver.Chrome(executable_path = chromedriver_path)
    return browser

def dateConversion(_date:str):
    dt = parse(_date)
    return dt.strftime('%Y-%m-%d')



