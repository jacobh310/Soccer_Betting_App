import os
import pandas as pd
import requests
import streamlit as st
from IPython.display import Image, HTML
from datetime import datetime

# Retrieve Data from Rest API
def get_games():
    API_URL = st.secrets['API_URL']
    resp = requests.get(API_URL).json()
    df = pd.DataFrame(resp)
    return df


def to_dt(string):
    timestamp = int(string) / 1000
    dt = datetime.fromtimestamp(timestamp)

    return dt


def path_to_image_html(path):
    """
     This function essentially convert the image url to
     '<img src="'+ path + '"/>' format. And one can put any
     formatting adjustments to control the height, aspect ratio, size etc.
     within as in the below example.
    """

    return '<img src="' + path + '" style=max-height:50px;"/>'


# Reformat DataFrame for Display
df = get_games()
df['Date_Time'] = df['Date_Time'].apply(to_dt)
df = df[['Home_Team', 'Home_Logo_URL', 'Away_Team', 'Away_Logo_URL', 'Date_Time', 'Bet_365_Home_Win_Prob',
         'Model_Home_Win_Prob', 'Bet365_Home_Odds', 'Implied_Model_Odds']]
new_cols = ['Home', 'H', 'Away', 'A', 'Game Time', 'Bet 365 Home Win Prob',
            'Model Home Win Prob', 'Bet365 Home Odds', 'Implied Model Odds']
mapper = dict(zip(df.columns, new_cols))
df = df.rename(columns=mapper).round(3)
df = HTML(df.to_html(escape=False, formatters=dict(H=path_to_image_html, A=path_to_image_html)))

# Formatting and Styling Page

st.set_page_config(page_title="Game Predictions",  layout='wide')

st.title("Upcoming Game Predictions")

st.markdown('''##### <span style="color:gray">Predicts Home Win Probability and Implied Model Odds. </span>
            ''', unsafe_allow_html=True)
st.markdown("""Take bets when Model Home Win Prob is greater than the Bet 365 Home Win Prob. Or when the Implied 
                Model odds are less than the Bet365 Home Odds""")

st.write(df, unsafe_allow_html=True)

st.sidebar.markdown(" ## BPL Predictor")
st.sidebar.markdown("""This Model was trained from British Premier League Data from 2000-2022. The data was collected 
from [Football-Data](https://www.football-data.co.uk/englandm.php). Data was split into Train Dev Test sets. Several 
different models were Hyperparameter tuned and the best one was deployed. Predictions for games scheduled in the next 
three days are posted on this page""")

st.sidebar.info("Read more about how the model works and [Github](https://github.com/jacobh310/soccer_betting).",
                icon="ℹ️")

st.success('''**A Brief Note on Deployment:**  
XGBoost Classifier Model was deployed to make predictions. The model is hosted on google cloud storage. Every three days
 a Google Cloud Function is scheduled that will make inference using the model on Cloud Storage and data collected from 
 the SportsMonk API. The Data and Predictions are then stored in a BigQuery DataBase where a REST API hosted on Cloud Run
 can make queries according to the request made from the front end (This Page). I know this solution is over engineering.
 I wanted to display my skills and familiarity with these GCP technologies and my ability to deploy models''')
