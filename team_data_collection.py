#!/usr/bin/env python3

import time
import pandas
from termcolor import colored

from utilities import dateConversion
from my_constants import BUTTON_PAGE_SELECT


def get_team_box_scores(browser, season_xpath: str, page_option: int):
    """
    Collects the team box scores from NBA.com

    Args:
        browser: Chrome driver browser instance (from initalizeChromeDriver())
        season_xath: XPATH of NBA season (defined on nba_data_scrapper.py)
        page_option: page on team box scores to collect

    Returns:
        table (long string) separate by new lines and spaces of the NBA
        team stats for a particular season from the team box score table.
    """

    page_selected = BUTTON_PAGE_SELECT.format(str(page_option))
    message = '[+] GETTING BOX SCORES TABLE FROM PAGE {0}'.format(str(page_option - 1))
    print(colored(message, 'green'))

    #Get table of stats. 
    browser.get('https://stats.nba.com/teams/boxscores/')
    browser.find_element_by_xpath(season_xpath).click()
    time.sleep(3) #Delay needed to let page load.

    browser.find_element_by_xpath(page_selected).click()
    time.sleep(3) #Delay needed to let page load.

    table = browser.find_element_by_class_name('nba-stat-table__overflow')

    return table


def parse_team_box_scores(table, season: str):
    """
    Parses through the box score table returned by get_team_box_scores().

    Args:
        table: (long string) separate by new lines and spaces of the NBA
            team box score stats for a particular season.
        season: season to append at the end of the data frame as a column.

    Returns:
        Data frame of the team box scores. 
    """

    message = '[+] PARSING TEAM BOX SCORE TABLE'
    print(colored(message, 'green'))

    team_stats = list()
    lines_to_parse = table.text.split('\n')

    for line_num, lines in enumerate(lines_to_parse):
        if line_num != 0:
            team_stats.append([i for i in lines.split(' ')])
    
    df = pandas.DataFrame({'team': [i[0] for i in team_stats],
                       'opp': [i[3] for i in team_stats],
                       'date': [i[4] for i in team_stats],
                       'wl': [i[5] for i in team_stats],
                       'min': [i[6] for i in team_stats], 
                       'pts': [i[7] for i in team_stats],
                       'fgm': [i[8] for i in team_stats],
                       'fga': [i[9] for i in team_stats],
                       'fgp': [i[10] for i in team_stats],
                       '3pm': [i[11] for i in team_stats],
                       '3pa': [i[12] for i in team_stats],
                       '3pp': [i[13] for i in team_stats],
                       'ftm': [i[14] for i in team_stats],
                       'fta': [i[15] for i in team_stats],
                       'ftp': [i[16] for i in team_stats],
                       'oreb': [i[17] for i in team_stats],
                       'dreb': [i[18] for i in team_stats],
                       'reb': [i[19] for i in team_stats],
                       'ast': [i[20] for i in team_stats],
                       'stl': [i[21] for i in team_stats],
                       'blk': [i[22] for i in team_stats],
                       'tov': [i[23] for i in team_stats],
                       'pf': [i[24] for i in team_stats],
                       'pm': [i[25] for i in team_stats],
                       })

    df.insert(len(df.columns), 'season', season)

    return df


def team_box_to_string(row):
    """
    Converts each row from generic team stats rows to a string so it can 
    be inserted with SQL commands.  

    Arg: 
        row: iterative row called from insertGenericTeamDFtoTable()
            in database_wrapper.py()
    
    Returns: 
        String of the row passed as an argument.
    """

    result = "('" + row['team'] + "',"
    result += "'" + str(row['opp']) + "',"
    result += "'" + str(dateConversion(row['date'])) + "',"
    result += "'" + str(row['wl']) + "',"
    result += str(row['min']) + ','
    result += str(row['pts']) + ','
    result += str(row['fgm']) + ','
    result += str(row['fga']) + ','
    result += str(row['fgp']) + ','
    result += str(row['3pm']) + ','
    result += str(row['3pa']) + ','
    result += str(row['3pp']) + ','
    result += str(row['ftm']) + ','
    result += str(row['fta']) + ','
    result += str(row['ftp']) + ','
    result += str(row['oreb']) + ','
    result += str(row['dreb']) + ','
    result += str(row['reb']) + ','
    result += str(row['ast']) + ','
    result += str(row['stl']) + ','
    result += str(row['blk']) + ','
    result += str(row['tov']) + ','
    result += str(row['pf']) + ','
    result += str(row['pm']) + ','
    result += "'" + row['season'] + "')"

    return result


def get_team_season_stats(browser, season_xpath: str):
    """
    Collects the season stats for all teams from NBA.com

    Args:
        browser: Chrome driver browser instance (from initalizeChromeDriver())
        seasonPath: XPATH of NBA season (defined on nba_data_scrapper.py)

    Returns: 
        Table (long string) separate by new lines and spaces of the NBA
        team stats for a particular season from the season stats table.
    """

    message = '[+] GETTING GENERIC SEASON TEAM STATS TABLE'
    print(colored(message, 'green'))

    #Get table of stats. 
    browser.get('https://stats.nba.com/teams/traditional/?sort=W_PCT&dir=-1')
    browser.find_element_by_xpath(season_xpath).click()
    time.sleep(3) #Delay needed to let page load.

    table = browser.find_element_by_class_name('nba-stat-table__overflow')

    return table


def parse_team_season_stats(table, season: str):
    """
    Parses through the table (long string) returned from get_season_team_stats()

    Args:
        table: a table (long string) separate by new lines and spaces of the NBA
            team stats for a particular season.
        season: season to append at the end (for my use for inserting into DB)

    Returns:
        Data frame of the 
    """

    message = '[+] PARSING GENERIC TABLE'
    print(colored(message, 'green'))

    team_names = list()
    team_stats = list()
    lines_to_parse = table.text.split('\n')

    for line_num, lines in enumerate(lines_to_parse):
        if line_num != 0:
            if line_num % 3 == 2:
                team_names.append(lines)
            elif line_num % 3 == 0:
                team_stats.append([i for i in lines.split(' ')])
    #player_stats now list of lists
    
    df = pandas.DataFrame({'team': team_names,
                       'gp': [i[0] for i in team_stats],
                       'w': [i[1] for i in team_stats],
                       'l': [i[2] for i in team_stats],
                       'winpct': [i[3] for i in team_stats], 
                       'min': [i[4] for i in team_stats],
                       'pts': [i[5] for i in team_stats],
                       'fgm': [i[6] for i in team_stats],
                       'fga': [i[7] for i in team_stats],
                       'fgp': [i[8] for i in team_stats],
                       '3pm': [i[9] for i in team_stats],
                       '3pa': [i[10] for i in team_stats],
                       '3pp': [i[11] for i in team_stats],
                       'ftm': [i[12] for i in team_stats],
                       'fta': [i[13] for i in team_stats],
                       'ftp': [i[14] for i in team_stats],
                       'oreb': [i[15] for i in team_stats],
                       'dreb': [i[16] for i in team_stats],
                       'reb': [i[17] for i in team_stats],
                       'ast': [i[18] for i in team_stats],
                       'tov': [i[19] for i in team_stats],
                       'stl': [i[20] for i in team_stats],
                       'blk': [i[21] for i in team_stats],
                       'blka': [i[22] for i in team_stats],
                       'pf': [i[23] for i in team_stats],
                       'pfd': [i[24] for i in team_stats],
                       'pm': [i[25] for i in team_stats],
                       })

    df.insert(len(df.columns), 'season', season) #Add the season

    return df


def team_season_to_string(row):
    """
    Converts each row from generic team stats rows to a string so it can 
    be inserted with SQL commands.  

    Arg: 
        row = iterative row called from insertGenericTeamDFtoTable()
            in database_wrapper.py()
    
    Returns:
        String of the row passed as the argument
    """

    result = "('" + row['team'] + "',"
    result += str(row['gp']) + ','
    result += str(row['w']) + ','
    result += str(row['l']) + ','
    result += str(row['winpct']) + ','
    result += str(row['min']) + ','
    result += str(row['pts']) + ','
    result += str(row['fgm']) + ','
    result += str(row['fga']) + ','
    result += str(row['fgp']) + ','
    result += str(row['3pm']) + ','
    result += str(row['3pa']) + ','
    result += str(row['3pp']) + ','
    result += str(row['ftm']) + ','
    result += str(row['fta']) + ','
    result += str(row['ftp']) + ','
    result += str(row['oreb']) + ','
    result += str(row['dreb']) + ','
    result += str(row['reb']) + ','
    result += str(row['ast']) + ','
    result += str(row['tov']) + ','
    result += str(row['stl']) + ','
    result += str(row['blk']) + ','
    result += str(row['blka']) + ','
    result += str(row['pf']) + ','
    result += str(row['pfd']) + ','
    result += str(row['pm']) + ','
    result += "'" + row['season'] + "')"

    return result

