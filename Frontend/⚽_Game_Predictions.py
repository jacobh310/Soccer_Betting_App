import pandas as pd
import requests
import streamlit as st
from IPython.display import HTML
from datetime import datetime
from io import BytesIO
from PIL import Image

# Important Functions


def get_games():
    """
    This function queries the rest api and returns either a JSON object with the stats for games in the
    next 3 coming days or returns a string that says "No Games"
    """
    API_URL = st.secrets['API_URL']
    resp = requests.get(API_URL)
    if resp.text == 'No Games':
        return resp.text
    else:
        dataframe = pd.DataFrame(resp.json())
        return dataframe


def to_dt(string):
    """
    Takes in timestamp string and return date time object version of timestamp string
    """
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


st.set_page_config(page_title="Game Predictions", layout='wide')

# query API to get upcoming games in Dataframe
df = get_games()

# checks if there is a games in the next 3 days. If there is games then it will reformat dataframe
# to be more visually appealing


# Formatting and Styling Page

st.title("Upcoming Game Predictions")

st.markdown('''##### <span style="color:gray">Predicts Home Win Probability and Implied Model Odds. </span>
            ''', unsafe_allow_html=True)
st.markdown("""Take bets when Model Home Win Prob is greater than the Bet 365 Home Win Prob. Or when the Implied 
                Model odds are less than the Bet365 Home Odds""")

# checking if there is games in the next 3 days. If there is a dataframe will appear
if isinstance(df,pd.DataFrame):
    df['Date_Time'] = df['Date_Time'].apply(to_dt)
    df = df[['Home_Team', 'Home_Logo_URL', 'Away_Team', 'Away_Logo_URL', 'Date_Time', 'Bet_365_Home_Win_Prob',
             'Model_Home_Win_Prob', 'Bet365_Home_Odds', 'Implied_Model_Odds']]
    new_cols = ['Home', 'H', 'Away', 'A', 'Game Time', 'Bet 365 Home Win Prob',
                'Model Home Win Prob', 'Bet365 Home Odds', 'Implied Model Odds']
    mapper = dict(zip(df.columns, new_cols))

    tol = 0.01
    highlight = df[(df['Model_Home_Win_Prob']+tol)>=df['Bet_365_Home_Win_Prob']].index.tolist()

    df = df.rename(columns=mapper).round(3)
    df = df.style.apply(lambda x:['background-color: #e6ffe6' if x.name in highlight else '' for i in x], axis=1)
    df = HTML(df.to_html(escape=False, formatters=dict(H=path_to_image_html, A=path_to_image_html)))
    st.write(df, unsafe_allow_html=True)
else:
    st.subheader("There is no games in the next 3 days")

st.sidebar.markdown(" ## BPL Predictor")
st.sidebar.markdown("""This Model was trained from British Premier League Data from 2000-2022. The data was collected 
from [Football-Data](https://www.football-data.co.uk/englandm.php). The data was split into Train Dev Test sets. Several 
different models were Hyperparameter tuned and the best one was deployed. Predictions for games scheduled in the next 
three days are posted on this page
""")

st.sidebar.info("Read more about how the model works on [Github](https://github.com/jacobh310/soccer_betting).",
                icon="ℹ️")

st.success('''**A Brief Note on Deployment:**  
XGBoost Classifier Model was deployed to make predictions. The model is hosted on google cloud storage. Every three days
 a Google Cloud Function is scheduled that will make inferences using the model on Cloud Storage and data collected from 
 the SportsMonk API. The Data and Predictions are then stored in a BigQuery DataBase where a REST API hosted on Cloud Run
 can make queries according to the request made from the front end (This Page). I know this solution is over-engineering.
 I wanted to display my skills and familiarity with these GCP technologies and my ability to deploy models. "Read more 
 app architecture works on
[Github](https://github.com/jacobh310/Soccer_Betting_App).''')


architect_url = "https://raw.githubusercontent.com/jacobh310/Soccer_Betting_App/main/Images/App%20Architecture.png"
architect_resp = requests.get(architect_url)
architect_img = Image.open(BytesIO(architect_resp.content))

st.subheader("Web App Architecture")
st.image(architect_img, width=700)

