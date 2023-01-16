import pandas as pd
import plotly.express as px
import math


def change_date(string):
    try:
        date = pd.to_datetime(string, format="%d/%m/%Y")
    except:
        date = pd.to_datetime(string, format="%d/%m/%y", errors='coerce')

    return date


def get_label(row_number):
    # Calculate the label based on the row number

    row_number = row_number + 1
    label = math.ceil(row_number / 380)
    return label


def wdl(row):
    if row['Goals'] > row['Opp Goals']:
        return 'W'
    elif row['Goals'] == row['Opp Goals']:
        return 'D'
    else:
        return 'L'


def make_scatter(df, x, y, animation_frame, hover_name, color, animation_group=None, size=None, title=None):
    range_x = [df[x].min(), df[x].max()]
    range_y = [df[y].min(), df[y].max()]

    fig = px.scatter(df, title=title, x=x, y=y, animation_frame = animation_frame, animation_group = animation_group,
    size = size, hover_name = hover_name, color = color, range_x = range_x, range_y = range_y, width = 700,
    height = 500, color_discrete_sequence=px.colors.qualitative.Antique)

    if not size:
        fig.update_traces(marker_line_width=1, marker_size=8)

    return fig

class DataImport:

    def __init__(self):
        self.stats = None

    def fetch_and_clean_data(self):
        data_url = "https://raw.githubusercontent.com/jacobh310/soccer_betting/main/Clean%20Data/Whole_Clean_data.csv"
        stats_df = pd.read_csv(data_url)
        stats_df['HTGD'] = stats_df['HTGS'] - stats_df['HTGC']
        stats_df['ATGD'] = stats_df['ATGS'] - stats_df['ATGC']
        stats_df['FPD'] = stats_df['HTFormPts'] - stats_df['ATFormPts']

        cols = ['HTGS', 'HTGC', 'ATGS', 'ATGC', 'HTGD', 'HTS', 'HTTS', 'HTF', 'HTC', 'HTY', 'HTR', 'ATGD', 'ATS',
                'ATTS', 'ATF', 'ATC', 'ATY', 'ATR', 'HTP', 'ATP']

        stats_df.MW = stats_df.MW.astype(float)
        stats_df[cols] = stats_df[cols].divide(stats_df.MW, axis=0)
        stats_df['HW'] = stats_df.FTR.apply(lambda string: 1 if string == 'H' else 0)

        stats_df['Season'] = stats_df.apply(lambda row: get_label(row.name), axis=1) + 2000
        stats_df['Date'] = stats_df['Date'].apply(change_date)
        stats_df['Home Result'] = stats_df['HW'].apply(lambda x: 'Home Win' if x == 1 else 'Draw or Away Win')
        self.stats = stats_df

    def prep_data(self):

        home_stats = self.stats[
            ['HomeTeam', 'AwayTeam', 'Date', 'Season', 'HTGD', 'FTHG', 'HTGS', 'HTGC', 'HS', 'HTS', 'HST', 'HTTS', 'HF',
             'HC', 'HY', 'HR', 'ATGD', 'FTAG', 'ATGS', 'ATGC', 'AS', 'ATS', 'AST', 'ATTS', 'AF', 'AC', 'AY', 'AR']]
        away_stats = self.stats[
            ['AwayTeam', 'HomeTeam', 'Date', 'Season', 'ATGD', 'FTAG', 'ATGS', 'ATGC', 'AS', 'ATS', 'AST', 'ATTS', 'AF',
             'AC', 'AY', 'AR', 'HTGD', 'FTHG', 'HTGS', 'HTGC', 'HS', 'HTS', 'HST', 'HTTS', 'HF', 'HC', 'HY', 'HR']]

        home_mapper = dict(
            zip(['HomeTeam', 'AwayTeam', 'HTGD', 'FTHG', 'HTGS', 'HTGC', 'HS', 'HTS', 'HST', 'HTTS', 'HF', 'HC', 'HY',
                 'HR', 'ATGD', 'FTAG', 'ATGS', 'ATGC', 'AS', 'ATS', 'AST', 'ATTS', 'AF', 'AC', 'AY', 'AR'],
                ['Team', 'Opponent', 'Avg Goal Diff', 'Goals', 'Avg Goals', 'Avg Goals Conceded', 'Shots', 'Avg Shots',
                 'Target Shots', 'Avg Target Shots', 'Fouls', 'Corners', 'Yellows', 'Reds', 'Opp Avg Goal Diff',
                 'Opp Goals', 'Avg Opp Goals', 'Avg Opp Goals Conceded', 'Opp Shots', 'Avg Opp Shots',
                 'Opp Target Shots', 'Avg Opp Target Shots', 'Opp Fouls', 'Opp Corners', 'Opp Yellows', 'Opp Reds']))

        away_mapper = dict(
            zip(['AwayTeam', 'HomeTeam', 'ATGD', 'FTAG', 'ATGS', 'ATGC', 'AS', 'ATS', 'AST', 'ATTS', 'AF', 'AC', 'AY',
                 'AR', 'HTGD', 'FTHG', 'HTGS', 'HTGC', 'HS', 'HTS', 'HST', 'HTTS', 'HF', 'HC', 'HY', 'HR'],
                ['Team', 'Opponent', 'Avg Goal Diff', 'Goals', 'Avg Goals', 'Avg Goals Conceded', 'Shots', 'Avg Shots',
                 'Target Shots', 'Avg Target Shots', 'Fouls', 'Corners', 'Yellows', 'Reds', 'Opp Avg Goal Diff',
                 'Opp Goals', 'Avg Opp Goals', 'Avg Opp Goals Conceded', 'Opp Shots', 'Avg Opp Shots',
                 'Opp Target Shots', 'Avg Opp Target Shots', 'Opp Fouls', 'Opp Corners', 'Opp Yellows', 'Opp Reds']))

        home_stats.rename(columns=home_mapper, inplace=True)
        away_stats.rename(columns=away_mapper, inplace=True)

        home_stats['Place'] = 'Home'
        away_stats['Place'] = 'Away'

        team_stats = home_stats.append(away_stats).sort_values('Date')
        team_stats['WDL'] = team_stats.apply(wdl, axis=1)

        game_team_stats_season = team_stats.groupby(['Season', 'Team', 'WDL']).mean()[
            ['Goals', 'Target Shots', 'Shots']].reset_index()

        return game_team_stats_season


