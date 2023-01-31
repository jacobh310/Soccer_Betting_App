import streamlit as st
from PIL import Image



st.set_page_config(page_title="Game Predictions",  layout='wide')

st.title('Model Building')

st.markdown("""##### <span style="color:gray">This Model Building was done with Sci-Kit Learn and XGBoost on 5 algorithms. </span>""", unsafe_allow_html=True)

st.markdown("""<p> The model was trained on past team in-game statistics to predict if the home team will win. 
             The models were evaluated first with accuracy, precision and recall but the true evaluation was the net 
             profit/loss of each algorithm. The baseline was the profit/loss you were to bet $100 on every game so
             betting odds were also collected. Two different betting strategies were deployed. 
             </p>""",  unsafe_allow_html=True)

col1, col2 = st.columns(2)

hw_img = Image.open("pages/Images/hw_pl.png")
ev_img = Image.open("pages/Images/ev_pl.png")

col1.subheader('1st Strategy: Home over 50%')
col1.markdown("""<p style="color:silver"> In this strategy a $100 bet is taken when the model gives the home
            team a greater than 50% of winning. If the home team won then I would use the betting odds to calculate the 
            payout. If the home team lost then the loss was $100. The baseline profit/loss loss by betting the home
             team to win every time.
             </p>""",  unsafe_allow_html=True)
col1.image(hw_img, width=650)

col2.subheader('2nd Strategy: Expected Value/Misprinted Odds')
col2.markdown("""<p style="color:silver"> In this strategy we convert the odds we get from the bookmaker into implied 
            probability. This implied probability is the probability the bookmaker set for a particular outcome. In this
             case its the home team. We take $100 bets only when our model probability is higher than the bookmakers.If 
              the home team wins, I use the odds to calculate how much. If the home team loses, Ie lose $100
            The baseline profit/loss loss by betting the home team to win every time.
             </p>""",  unsafe_allow_html=True)
col2.image(ev_img, width=650)
