import xgboost as xgb
import joblib
from dotenv import load_dotenv
import os
import sys
import utils
from datetime import date, timedelta
from google.cloud import bigquery, storage
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

prod = False


if not prod:
    model_path = '../Models/final_xgb_3.sav'
    load_dotenv()
    SM_API_TOKEN = os.getenv("SM_API_TOKEN")
    RAPID_API_KEY = os.getenv("RAPID_API_KEY")
    RAPID_API_HOST = os.getenv("RAPID_API_HOST")
    BUCKET_NAME = os.getenv('BUCKET_NAME')

else:
    model_path = ''
    SM_API_TOKEN = os.getenv("SM_API_TOKEN")
    RAPID_API_KEY = os.getenv("RAPID_API_KEY")
    RAPID_API_HOST = os.getenv("RAPID_API_HOST")
    BUCKET_NAME = os.getenv('BUCKET_NAME')


model = joblib.load(model_path)


headers = {
    "X-RapidAPI-Key": RAPID_API_KEY,
    "X-RapidAPI-Host": RAPID_API_HOST
    }

querystring = {"include":"standings.team","tz":"Europe/Amsterdam"}


date_1 = date.today().strftime("%Y-%m-%d")
date_2 = date.today() + timedelta(days=3)
date_2 = date_2.strftime("%Y-%m-%d")
bpl_league_id = 8
bpl_season_id = 19734


if __name__ == '__main__':

    stand_df = utils.get_stand(bpl_season_id,headers, querystring)
    all_stats = utils.get_team_stats(SM_API_TOKEN, bpl_season_id, stand_df)
    try:
        diff_fix_stats = utils.get_fixture_stats(bpl_league_id, date_1, date_2, all_stats, headers)
    except:
        print('No Games Today')
        sys.exit()
    probs = utils.model_inference(model, diff_fix_stats)

    final = diff_fix_stats.copy()
    final['Model Home Win Prob'] = probs
    final['Implied Model Odds'] = 1 / probs
    final = final[
        ['Hteam_id', 'Home Team', 'Ateam_id', 'Away Team', 'games_playedH', 'games_playedA', 'MW', 'HP', 'HFormPts',
         'HM1', 'HM2', 'HM3', 'HGS', 'HGC', 'HF', 'HTS', 'HC', 'HS', 'AP', 'AFormPts', 'AM1', 'AM2', 'AM3', 'AGS',
         'AGC', 'AF', 'ATS', 'AC', 'AS', 'HTGD', 'ATGD', 'FPD', 'Bet365 Home Odds', 'Bet 365 Home Win Prob',
         'Model Home Win Prob', 'Implied Model Odds', 'Home_Logo_URL', 'Away_Logo_URL', 'Date_Time','Request_Date_Time']]

    new_cols = [col.replace(' ', '_') for col in final.columns]
    mapper = dict(zip(final.columns, new_cols))
    final = final.rename(columns=mapper)

    client = bigquery.Client()
    table_id = 'astute-winter-373022.Soccer_Stats.Stats_Predictions'
    table = client.get_table(table_id)
    errors = client.insert_rows_from_dataframe(table, final)

    if errors == []:
        print("Data loaded into table")
    else:
        print(errors)

