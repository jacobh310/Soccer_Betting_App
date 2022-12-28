import xgboost as xgb
import joblib
from dotenv import load_dotenv
import os
import requests
import json
import utils

dev = True

if dev:
    model_path = 'Models/final_xgb_3.sav'
    load_dotenv()
    SM_API_TOKEN = os.getenv("SM_API_TOKEN")
    RAPID_API_KEY = os.getenv("RAPID_API_KEY")
    RAPID_API_HOST = os.getenv("RAPID_API_HOST")

model = joblib.load(model_path)


headers = {
    "X-RapidAPI-Key": RAPID_API_KEY,
    "X-RapidAPI-Host": RAPID_API_HOST
    }

querystring = {"include":"standings.team","tz":"Europe/Amsterdam"}


date1 = '2022-12-25'
date2 = '2022-12-28'
bpl_league_id = 8
bpl_season_id = 19734

def get_stand(season_id, headers, querystring):

    url = f"https://football-pro.p.rapidapi.com/api/v2.0/standings/season/{season_id}"

    response = requests.request("GET", url, headers=headers, params=querystring)
    dic = json.loads(response.text)

    return dic

print(get_stand(bpl_season_id,headers, querystring))


#
# if __name__ == '__main__':
#
#     stand_df = utils.get_stand(bpl_season_id,headers, querystring)
#     all_stats = utils.get_team_stats(SM_API_TOKEN, bpl_season_id, stand_df)
#     diff_fix_stats = utils.get_fixture_stats(bpl_league_id, date1, date2, all_stats)
#     probs = utils.model_inference(model, diff_fix_stats)
#
#     final = diff_fix_stats.copy()
#     final['Model Home Win Prob'] = probs
#     final['Implied Model Odds'] = 1 / probs
#     final = final[
#         ['Hteam_id', 'Home Team', 'Ateam_id', 'Away Team', 'games_playedH', 'games_playedA', 'MW', 'HP', 'HFormPts',
#          'HM1', 'HM2', 'HM3', 'HGS', 'HGC', 'HF', 'HTS', 'HC', 'HS', 'AP', 'AFormPts', 'AM1', 'AM2', 'AM3', 'AGS',
#          'AGC', 'AF', 'ATS', 'AC', 'AS', 'HTGD', 'ATGD', 'FPD', 'Bet365 Home Odds', 'Bet 365 Home Win Prob',
#          'Model Home Win Prob', 'Implied Model Odds']]
#
#
#     print(final[['Home Team','Away Team','Bet 365 Home Win Prob' ,'Model Home Win Prob']])
#
#
#
#
#
#
#
