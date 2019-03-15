import sys

from utilities import initialize_chrome_driver
from player_data_collection import get_player_box_scores, parse_player_box_scores, \
                                   get_player_season_stats, parse_player_season_stats


class NbaDataCollector:
    """
    Class that collects NBA statistics from stats.nba.com
    """

    """XPATHs for buttons"""
    BUTTON_PAGE_SELECT = '/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[1]/div/div/select/option[{0}]'
    BUTTON_ALL_PLAYERS = '/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[1]/div/div/select/option[1]'
    LAST_PAGE = '/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[1]/div/div/text()[2]'

    """XPATHs For Generic Tables""" 
    SEASON_XPATHS = {
        "2018-2019": '/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/label/select/option[1]',
        "2017-2018": '/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/label/select/option[2]',
        "2016-2017": '/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/label/select/option[3]',
        "2015-2016": '/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/label/select/option[4]',
        "2014-2015": '/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/label/select/option[5]',
        "2013-2014": '/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/label/select/option[6]',
        "2012-2013": '/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/label/select/option[7]',
        "2011-2012": '/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/label/select/option[8]',
        "2010-2011": '/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/label/select/option[9]',
    }

    """XPATHs for Box Scores"""
    BOXSCORE_XPATHS = {
        "2018-2019": '/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/label/select/option[2]',
        "2017-2018": '/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/label/select/option[3]',
        "2016-2017": '/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/label/select/option[4]',
        "2015-2016": '/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/label/select/option[5]',
        "2014-2015": '/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/label/select/option[6]',
        "2013-2014": '/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/label/select/option[7]',
        "2012-2013": '/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/label/select/option[8]',
        "2011-2012": '/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/label/select/option[9]',
        "2010-2011": '/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/label/select/option[10]',
    }

    SEASON_STRINGS = {
        "2018-2019": "2018-2019",
        "2017-2018": "2017-2018",
        "2016-2017": "2016-2017",
        "2015-2016": "2015-2016",
        "2014-2015": "2014-2015",
        "2013-2014": "2013-2014",
        "2012-2013": "2012-2013",
        "2011-2012": "2011-2012",
        "2010-2011": "2010-2011",
    }


    def __init__(self):
        pass
    

    def collect_player_box_scores(self, season: str):
        """
        Scraps stats.nba.com to collect all box scores of a particular season.

        Args:
            season: String containing season of box scores to collect.
        Returns:
            Dataframe of players box score table
        """

        #Check valid season passed as parameter
        if(season not in self.SEASON_STRINGS):
            sys.exit("Invalid season option entered.")

        browser = initialize_chrome_driver()
        raw_box_scores = get_player_box_scores(browser, self.BOXSCORE_XPATHS[season])
        box_scores_df = parse_player_box_scores(raw_box_scores, season)

        return box_scores_df


    def collect_player_season_stats(self, season: str):
        """
        Scraps stats.nba.com to collect all box scores of a particular season.

        Args:
            season: String containing season of box scores to collect.
        Returns:
            Dataframe of players box score table
        """

        #Check valid season passed as parameter
        if(season not in self.SEASON_STRINGS):
            sys.exit("Invalid season option entered.")

        browser = initialize_chrome_driver()
        raw_season_stats = get_player_season_stats(browser, self.SEASON_XPATHS[season])
        season_scores_df = parse_player_season_stats(raw_season_stats, season)

        return season_scores_df


if __name__ == "__main__":
    print("The variable 'dc' is an available NbaDataCollector object")
    dc = NbaDataCollector()

