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

    load_dotenv()
    SM_API_TOKEN = os.getenv("SM_API_TOKEN")
    RAPID_API_KEY = os.getenv("RAPID_API_KEY")
    RAPID_API_HOST = os.getenv("RAPID_API_HOST")
    BUCKET_NAME = os.getenv('BUCKET_NAME')
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(f"models/final_xgb_3.sav")
    blob.download_to_filename('tmp/final_xgb_3.sav')
    model_path = 'tmp/final_xgb_3.sav'


else:

    SM_API_TOKEN = os.getenv("SM_API_TOKEN")
    RAPID_API_KEY = os.getenv("RAPID_API_KEY")
    RAPID_API_HOST = os.getenv("RAPID_API_HOST")
    BUCKET_NAME = os.getenv('BUCKET_NAME')
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(f"models/final_xgb_3.sav")
    blob.download_to_filename('/tmp/final_xgb_3.sav')
    model_path = '/tmp/final_xgb_3.sav'


model = joblib.load(model_path)


headers = {
    "X-RapidAPI-Key": RAPID_API_KEY,
    "X-RapidAPI-Host": RAPID_API_HOST
    }

querystring = {"include":"standings.team","tz":"America/Los_Angeles"}


date_1 = date.today().strftime("%Y-%m-%d")
date_2 = date.today() + timedelta(days=4)
date_2 = date_2.strftime("%Y-%m-%d")
bpl_league_id = 8
bpl_season_id = 19734


def send_data(request):

    if request:
        stand_df = utils.get_stand(bpl_season_id, headers, querystring)
        all_stats = utils.get_team_stats(SM_API_TOKEN, bpl_season_id, stand_df)
        try:
            diff_fix_stats = utils.get_fixture_stats(bpl_league_id, date_1, date_2, all_stats, headers)
        except:
            print('No Games Found')
            return 'No Games Found'
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

        bq_client = bigquery.Client()
        table_id = 'astute-winter-373022.Soccer_Stats.Stats_Predictions'
        table = bq_client.get_table(table_id)
        errors = bq_client.insert_rows_from_dataframe(table, final)

        if errors == [[]]:
            print("Data loaded into table")
            return "Success"
        else:
            print(errors)
            return 'Failed'
