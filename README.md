# British Premier League Betting App
---
### 📌 [See the web app in action here](https://jacobh310-soccer-betting-app-frontend-game-predictions-cty251.streamlit.app)

## <b>Introduction</b>:  Succesfull Sports Betting?

The Sports Betting market is worth $74.2 billion dolalrs as of 2021 and is expexted to reach $129.3 billion by 2028 according to [Global News Wire](https://www.globenewswire.com/en/news-release/2022/11/16/2556991/0/en/Sports-Betting-Market-Size-Share-to-Surpass-USD-129-3-Billion-by-2028-Vantage-Market-Research.html#:~:text=WASHINGTON%2C%20Nov.,forecast%20period%20of%202022%2D2028.) There is no question that your average sports gambler is competeting against 
companies that put in millions into having the best algorithims to price their odds all with the goal of making money of the average sports bettor. I tried to tilt the odds back to the sports bettor favor by training a machine learning algorithim that predicts the home teams winning probability.

**Before Starting it is important to understand the following**
#### Bettting 101
- Decimal odds: The payout if a bet is won. Decmal odds of 2 means that if you bet $10 you would recieve $20. $10 of the original bet and $10 profit. The higher the decimal odds the higher the pay
- Implied Probability: The probability implied by the decmial odds line. Implied probability = 1/Decimal Odds. A decimal odds of 2 has an implied probability of 50%. The higher the odds the lower the probability. Meaning low proably events have a higher payout.

#### Excpected Value
If a sports bettor knows that a home team has 50% chance to win a game and the decimal odds are 2.2 for the home team then they have a 10% expected value. That means if the sports bettor was bet $10 an infinite amount of times, the sports bettor would win 10% of the amount staked or 1 dollar. That is called having positive expected value. In this scnerio, no one knows that the home team has a 50% chance of winning but that is where machine learning comes in. 

## Model Thesis
We can train machine learning algorithims on historical game statistics predict the probability of the home team winning. That is exactly what this web app shows you. You can compare the model probability to the implied probability from different bookmakers and only take bets where the model probabilty is greater than the implied probability. Just like in the scenario above, the model predicts that the home team has a 50% of winning the game. Now a bookmaker has the decimal odds at 2.2. making the implied probality is 45% (1/2.2). We would take that bet becasue the model has the higher home team probability. So as long as the model probability > book maker implied volatility, the model would take that bet.

Several machine learning algorithims were trained on data from 2000-2021. Data was split into train dev test and the best model was chosen for the web app. The best model was chosen by looking at the historical profitability of the expected value trading stategy. So $100 would be staked if and only if the model probability > book maker implied volatility. Which every algorithim made the most money was deployed on this web app. That model being XGBoost. 


## App Architecture

<p ><img align="center" src="https://raw.githubusercontent.com/jacobh310/Soccer_Betting_App/main/Images/App%20Architecture.png" 
      title="App Architecture" width="700"/></p>



