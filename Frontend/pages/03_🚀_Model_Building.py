import streamlit as st
from PIL import Image
import requests
from io import BytesIO


st.set_page_config(page_title="Game Predictions",  layout='wide')

st.title('Model Building')

st.markdown("""##### <span style="color:gray">This Model Building was done with Sci-Kit Learn and XGBoost on 5 algorithms. </span>""", unsafe_allow_html=True)

st.markdown("""<p>  The model was trained on past team in-game statistics to predict if the home team will win. 
             The models were evaluated first with accuracy, precision, and recall but the true evaluation was the net 
             profit/loss of each algorithm. The baseline was the profit/loss you were to bet $100 on every game so
             betting odds were also collected. Two different betting strategies were deployed. 
             </p>""",  unsafe_allow_html=True)

col1, col2 = st.columns(2)

hw_url = "https://raw.githubusercontent.com/jacobh310/Soccer_Betting_App/main/Frontend/pages/Images/hw_pl.png"
ev_url = "https://raw.githubusercontent.com/jacobh310/Soccer_Betting_App/main/Frontend/pages/Images/ev_pl.png"
hw_resp = requests.get(hw_url)
ev_resp = requests.get(ev_url)

hw_img = Image.open(BytesIO(hw_resp.content))
ev_img = Image.open(BytesIO(ev_resp.content))

col1.subheader('1st Strategy: Home over 50%')
col1.markdown("""<p style="color:silver"> In this strategy, a $100 bet is taken when the model gives the home
            team a greater than 50% of winning. If the home team won then I would use the betting odds to calculate the 
            Payout and add it to the current balance. If the home team lost then $100 is deducted from the current balance. The baseline profit/loss by betting the home
             team to win every time</p>""",  unsafe_allow_html=True)
col1.image(hw_img, width=650)

col2.subheader('2nd Strategy: Expected Value/Misprinted Odds')
col2.markdown("""<p style="color:silver"> In this strategy, we convert the odds we get from the bookmaker into implied 
            probability. This implied probability is the probability the bookmaker set for a particular outcome. In this
             case, it's the home team. We take $100 bets only when our model probability is higher than the bookmakers. 
             If the home team wins, I use the odds to calculate the winnings and add it to the current balance. If the 
             home team loses,  $100 is deducted from the current balance. The baseline profit/loss is calculated by 
             betting the home team to win every time.</p>""",  unsafe_allow_html=True)
col2.image(ev_img, width=650)
