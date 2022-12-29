import pandas as pd
import requests
import json
import numpy as np
from sklearn.preprocessing import OneHotEncoder


def get_points(result):
    if result == 'W':
        return 3
    elif result == 'D':
        return 1
    else:
        return 0


def get_form_points(string):
    sum = 0
    for letter in string:
        sum += get_points(letter)
    return sum


def correct_odds(i):
    if i['market_id'] == 1 and i['odds'][0]['label'] == '1' and i['odds'][0]['handicap'] == None:
        return True

    else:
        return False


# Get Most Up to date team statistics in dictionary

def get_season_stats(team_id, token, season_id):
    """Retrieves dictionary of most recent team statistics from the Sports Monk API"""

    url = f"https://soccer.sportmonks.com/api/v2.0/teams/{team_id}/?api_token={token}&include=stats"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    dic = json.loads(response.text)

    # for loop to get the stats for the current season.

    seasons = dic['data']['stats']['data']

    for season in seasons:
        if season['season_id'] == season_id:
            current_season = season

    current_season['name'] = dic['data']['name']

    return current_season


# Makes stats dictionary into a Data Frame

def make_stats_df(season_stats):
    """Gets relevant stats from stats dictionary and converts it to a dataframe where each column is a different stat """

    keys = ['avg_goals_per_game_scored', 'avg_goals_per_game_conceded', 'avg_shots_off_target_per_game',
            'avg_shots_on_target_per_game', 'avg_corners', 'avg_fouls_per_game']

    stats = {key: value for key, value in season_stats.items() if key in keys}
    stats['avg_goals_per_game_scored'] = stats['avg_goals_per_game_scored']['total']
    stats['avg_goals_per_game_conceded'] = stats['avg_goals_per_game_conceded']['total']

    stats_df = pd.DataFrame(stats, index=[0]).astype(float)
    stats_df.rename({0: season_stats['team_id']}, inplace=True)

    return stats_df


# Gets Standing stats of all teams. Returns Dictionary

def get_stand(season_id, headers, querystring):
    url = f"https://football-pro.p.rapidapi.com/api/v2.0/standings/season/{season_id}"

    response = requests.request("GET", url, headers=headers, params=querystring)
    dic = json.loads(response.text)
    team_stand = dic['data'][0]['standings']['data']

    stand_stats = {}

    for i in range(len(team_stand)):
        team_id = team_stand[i]['team_id']
        team_name = team_stand[i]['team_name']
        points = team_stand[i]['points']
        recent_form = team_stand[i]['recent_form'][:3]
        matchweek = team_stand[i]['round_name']
        games_played = team_stand[i]['overall']['games_played']

        stand_stats[team_id] = [team_name, matchweek, games_played, points, recent_form]

    stand_df = pd.DataFrame.from_dict(stand_stats, orient='index',
                                      columns=['team_name', 'MW', 'games_played', 'points', 'recent_form'])

    stand_df['FormPts'] = stand_df['recent_form'].apply(get_form_points)

    stand_df['M1'] = stand_df['recent_form'].str[0]
    stand_df['M2'] = stand_df['recent_form'].str[1]
    stand_df['M3'] = stand_df['recent_form'].str[2]

    stand_df.drop(columns='recent_form', inplace=True)

    return stand_df


# gets all team  game stats

def get_team_stats(API_TOKEN, season_id, standings):
    every_team_stats = pd.DataFrame()

    for index, row in standings.iterrows():
        team_stats = get_season_stats(index, API_TOKEN, season_id)
        df = make_stats_df(team_stats)

        every_team_stats = every_team_stats.append(df)

    all_stats = standings.join(every_team_stats)

    all_stats['avg_shots_per_game'] = all_stats['avg_shots_off_target_per_game'] + all_stats[
        'avg_shots_on_target_per_game']
    all_stats.drop(columns='avg_shots_off_target_per_game', inplace=True)

    new_col = ['P', 'GS', 'GC', 'TS', 'S', 'C', 'F']

    old_col = ['points', 'avg_goals_per_game_scored', 'avg_goals_per_game_conceded', 'avg_shots_on_target_per_game',
               'avg_shots_per_game', 'avg_corners', 'avg_fouls_per_game']

    all_stats.rename(columns=dict(zip(old_col, new_col)), inplace=True)
    all_stats = all_stats.reset_index().rename(columns={'index': 'team_id'})

    return all_stats


# gets fixtures and combines the stand stats and ingame stats

def get_fixture_stats(league_id, date1, date2, all_stats,headers):
    url = f"https://football-pro.p.rapidapi.com/api/v2.0/fixtures/between/{date1}/{date2}"

    querystring = {"bookmakers": "2", "leagues": str(league_id), "tz": "Europe/Amsterdam",
                   "include": "localTeam,visitorTeam,season,flatOdds"}
    response = requests.request("GET", url, headers=headers, params=querystring)

    dic = json.loads(response.text)
    fixtures_stats = pd.DataFrame()

    for game in range(len(dic['data'])):
        home_id = dic['data'][game]['localTeam']['data']['id']
        away_id = dic['data'][game]['visitorTeam']['data']['id']

        all_odds = dic['data'][game]['flatOdds']['data']
        wdl_odds = [i for i in all_odds if correct_odds(i)]
        home_odds = float(wdl_odds[0]['odds'][0]['value'])
        home_prob = round(float(wdl_odds[0]['odds'][0]['probability'][:-1]) / 100, 3)

        home_stats = all_stats[all_stats['team_id'] == home_id].reset_index().drop(columns='index')
        home_stats['Bet365 Home Odds'] = home_odds
        home_stats['Bet 365 Home Win Prob'] = home_prob

        away_stats = all_stats[all_stats['team_id'] == away_id].reset_index().drop(columns='index')

        fix = pd.merge(home_stats, away_stats, left_index=True, right_index=True, suffixes=('H', 'A'))

        fixtures_stats = fixtures_stats.append(fix)

    old_cols = ['team_idH', 'team_idA', 'PH', 'FormPtsH', 'M1H', 'M2H', 'M3H', 'GSH', 'GCH', 'FH', 'TSH', 'CH', 'SH',
                'PA', 'FormPtsA', 'M1A', 'M2A', 'M3A', 'GSA', 'GCA', 'FA', 'TSA', 'CA', 'SA']
    # Make suffix into prefix
    new_cols = [i[-1] + i[:-1] for i in old_cols]
    mapper = dict(zip(old_cols, new_cols))
    fixtures_stats = fixtures_stats.rename(columns=mapper)
    fixtures_stats = fixtures_stats.drop(columns=['MWA']).rename(columns={'MWH': 'MW'})

    cols = ['Hteam_id', 'team_nameH', 'Ateam_id', 'team_nameA', 'games_playedH', 'games_playedA', 'Bet365 Home Odds',
            'Bet 365 Home Win Prob', 'MW', 'HP', 'HFormPts', 'HM1', 'HM2', 'HM3', 'HGS', 'HGC', 'HF', 'HTS', 'HC', 'HS',
            'AP', 'AFormPts', 'AM1', 'AM2', 'AM3', 'AGS', 'AGC', 'AF', 'ATS', 'AC', 'AS']
    fixtures_stats = fixtures_stats[cols]
    fixtures_stats = fixtures_stats.reset_index().drop(columns='index')
    fixtures_stats = fixtures_stats.rename(columns={'team_nameH': 'Home Team', 'team_nameA': 'Away Team'})

    ### Differences

    diff_fix_stats = fixtures_stats.copy()

    diff_fix_stats['HTGD'] = diff_fix_stats['HGS'] - diff_fix_stats['HGC']
    diff_fix_stats['ATGD'] = diff_fix_stats['AGS'] - diff_fix_stats['AGC']
    diff_fix_stats['FPD'] = diff_fix_stats['HFormPts'] - diff_fix_stats['AFormPts']

    # AVG Points
    diff_fix_stats['HP'] = diff_fix_stats['HP'] / diff_fix_stats['games_playedH']
    diff_fix_stats['AP'] = diff_fix_stats['AP'] / diff_fix_stats['games_playedA']

    return diff_fix_stats


# Gets prediction probability from fixture stats

def model_inference(model, diff_fix_stats):
    cols = ['HM1', 'HM2', 'HM3', 'AM1', 'AM2', 'AM3']

    ohe = OneHotEncoder()

    dummy = np.array([['W', 'W', 'W', 'W', 'W', 'W'],
                      ['L', 'L', 'L', 'L', 'L', 'L'],
                      ['D', 'D', 'D', 'D', 'D', 'D']], dtype=object)

    ohe.fit(dummy)
    t = ohe.transform(diff_fix_stats[cols]).toarray()
    inf_df = diff_fix_stats[
        ['HTGD', 'HS', 'HTS', 'HF', 'HC', 'ATGD', 'AS', 'ATS', 'AF', 'AC', 'HP', 'AP', 'MW', 'FPD', 'HM1', 'HM2', 'HM3',
         'AM1', 'AM2', 'AM3']]
    features = inf_df.iloc[:, :-6].values
    features = np.append(features, t, axis=1)
    probs = model.predict_proba(features)[:, 1]

    return probs


