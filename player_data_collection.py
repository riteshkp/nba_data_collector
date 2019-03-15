#!/usr/bin/env python3

from termcolor import colored

import sys
import time
import pandas

from utilities import dateConversion
from my_constants import BUTTON_ALL_PLAYERS, BUTTON_PAGE_SELECT


def get_player_box_scores(browser, season_xpath: str):
    """
    Collects the box scores of NBA players from a particular page 
        and season

    Args:
        browser: Chrome driver browser instance (created from 
                        initalizeChromeDriver() in utilities.py)
        season_xpath: XPATH of NBA season (from my_constants.py)
    Returns:
        Table (long string) separate by new lines and spaces of the NBA
        players stats for a particular season from the box scores.
    """

    #I found that the webpage becomes unresponsive when you click on the all option

    raw_table = ""

    browser.get('https://stats.nba.com/players/boxscores/')
    time.sleep(3) # Load stats.nba.com.

    try:
        browser.find_element_by_xpath(season_xpath).click()
    except:
        sys.exit("[-] ERROR: PAGE FAILED TO LOAD IN TIME. RETRY AGAIN")

    time.sleep(3) # Load the season.

    for page in range(2, 1000):
        #TODO fix constant structure.

        page_selected = BUTTON_PAGE_SELECT.format(str(page))

        try:
            browser.find_element_by_xpath(page_selected).click()
            message = '[+] GETTING PLAYER BOX SCORES TABLE \
                    FROM PAGE {0}'.format(str(page - 1))
            print(message)
        except:
            print("[+] REACHED END OF BOX SCORE TABLE FOR SEASON")
            break

        time.sleep(3) # Load selected page.

        raw_table += browser.find_element_by_class_name('nba-stat-table__overflow').text

    return raw_table


def parse_player_box_scores(raw_table, season: str):
    """
    Parses through the box scores table returned by get_player_box_scores().

    Args:
        raw_table: a table (long string) separate by new lines and spaces of the 
                   NBA players stats for a particular season.
        season: season to append at the end of dataframe as column.
    Returns:
        Dataframe of players box score table
    """

    is_name = True

    print("[+] PARSING PLAYERS BOX SCORES TABLE")

    player_names = list()
    player_stats = list()
    lines_to_parse = raw_table.split('\n')

    for line in lines_to_parse:
        if (line == "PLAYER TEAM MATCH UP GAME DATE W/L MIN PTS FGM FGA FG% 3PM 3PA 3P% FTM FTA FT% OREB DREB REB AST STL BLK TOV PF +/-"):
            continue
        elif (is_name):
            if "'" in line:
                line = line.replace("'", "")
            player_names.append(line)
            is_name = False
        elif (not is_name):
            line = line.replace("PLAYER TEAM MATCH UP GAME DATE W/L MIN PTS FGM FGA FG% 3PM 3PA 3P% FTM FTA FT% OREB DREB REB AST STL BLK TOV PF +/-", "")
            player_stats.append([i for i in line.split(' ')])
            is_name = True

    df = pandas.DataFrame({'player': player_names,
                       'team': [i[0] for i in player_stats],
                       'matchup': [i[3] for i in player_stats],
                       'gamedate': [i[4] for i in player_stats],
                       'wl': [i[5] for i in player_stats], 
                       'min': [i[6] for i in player_stats],
                       'pts': [i[7] for i in player_stats],
                       'fgm': [i[8] for i in player_stats],
                       'fga': [i[9] for i in player_stats],
                       'fgp': [i[10] for i in player_stats],
                       '3pm': [i[11] for i in player_stats],
                       '3pa': [i[12] for i in player_stats],
                       '3pp': [i[13] for i in player_stats],
                       'ftm': [i[14] for i in player_stats],
                       'fta': [i[15] for i in player_stats],
                       'ftp': [i[16] for i in player_stats],
                       'oreb': [i[17] for i in player_stats],
                       'dreb': [i[18] for i in player_stats],
                       'reb': [i[19] for i in player_stats],
                       'ast': [i[20] for i in player_stats],
                       'stl': [i[21] for i in player_stats],
                       'blk': [i[22] for i in player_stats],
                       'tov': [i[23] for i in player_stats],
                       'pf': [i[24] for i in player_stats],
                       'pm': [i[25] for i in player_stats],
                       })

    df.insert(len(df.columns), 'season', season) #Add the season

    return df


def get_player_season_stats(browser, season_xpath: str):
    """
    Collects data from NBA.com on all players season stats.

    Args
        browser: Chrome driver browser instance (from initalizeChromeDriver())
        season_xpath: XPATH of NBA season (defined on nba_data_scrapper.py)

    Returns:
        Table (long string) separate by new lines and spaces of the NBA
        players stats for a particular season.
    """

    print("[+] GETTING PLAYER SEASON STATS TABLE")

    #Get table of stats. 
    browser.get("https://stats.nba.com/players/traditional/?sort=PTS&dir=-1s")

    try:
        browser.find_element_by_xpath(season_xpath).click()
    except:
        sys.exit("[-] ERROR: PAGE FAILED TO LOAD IN TIME. RETRY AGAIN")

    time.sleep(3) # Load the season.

    try:
        browser.find_element_by_xpath(BUTTON_ALL_PLAYERS).click()
    except:
        sys.exit("[-] ERROR: PAGE FAILED TO LOAD IN TIME. RETRY AGAIN")
    
    time.sleep(3) # Load all players
    raw_table = browser.find_element_by_class_name('nba-stat-table__overflow')

    return raw_table.text


def parse_player_season_stats(table, season: str):
    """
    Parses through the season stats table returned by get_player_season_stats().
    
    Args:
        table: a table (long string) separate by new lines and spaces of the NBA
                     players stats for a particular season.
        season: season to append at the end (for my use for inserting into DB)
    Returns:
        A data frame of the player season stats.
    """

    print("[+] PARSING PLAYER SEASON STATS TABLE")

    player_names = list()
    player_stats = list()

    lines_to_parse = table.split('\n')

    for line_num, lines in enumerate(lines_to_parse):
        if line_num != 0:
            if line_num % 3 == 2:
                if "'" in lines:
                    lines = lines.replace("'", "")
                player_names.append(lines)
            elif line_num % 3 == 0:
                player_stats.append([i for i in lines.split(' ')])
    
    df = pandas.DataFrame({'player': player_names,
                       'team': [i[0] for i in player_stats],
                       'age': [i[1] for i in player_stats],
                       'gp': [i[2] for i in player_stats],
                       'w': [i[3] for i in player_stats], 
                       'l': [i[4] for i in player_stats],
                       'min': [i[5] for i in player_stats],
                       'pts': [i[6] for i in player_stats],
                       'fgm': [i[7] for i in player_stats],
                       'fga': [i[8] for i in player_stats],
                       'fgp': [i[9] for i in player_stats],
                       '3pm': [i[10] for i in player_stats],
                       '3pa': [i[11] for i in player_stats],
                       '3pp': [i[12] for i in player_stats],
                       'ftm': [i[13] for i in player_stats],
                       'fta': [i[14] for i in player_stats],
                       'ftp': [i[15] for i in player_stats],
                       'oreb': [i[16] for i in player_stats],
                       'dreb': [i[17] for i in player_stats],
                       'reb': [i[18] for i in player_stats],
                       'ast': [i[19] for i in player_stats],
                       'tov': [i[20] for i in player_stats],
                       'stl': [i[21] for i in player_stats],
                       'blk': [i[22] for i in player_stats],
                       'pf': [i[23] for i in player_stats],
                       'fp': [i[24] for i in player_stats],
                       'dd2': [i[25] for i in player_stats],
                       'td3': [i[26] for i in player_stats],
                       'pm': [i[27] for i in player_stats]
                       })

    df.insert(len(df.columns), 'season', season) #Add the season

    return df

