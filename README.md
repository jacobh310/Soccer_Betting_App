# British Premier League Betting App
---
### 📌 [See the web app in action here](https://jacobh310-soccer-betting-app-frontend-game-predictions-cty251.streamlit.app)

## <b>Introduction</b>:  Succesfull Sports Betting?

The Sports Betting market is worth $74.2 billion dolalrs as of 2021 and is expexted to reach $129.3 billion by 2028 according to [Global News Wire](https://www.globenewswire.com/en/news-release/2022/11/16/2556991/0/en/Sports-Betting-Market-Size-Share-to-Surpass-USD-129-3-Billion-by-2028-Vantage-Market-Research.html#:~:text=WASHINGTON%2C%20Nov.,forecast%20period%20of%202022%2D2028.) There is no question that your average sports gambler is competeting against 
companies that put in millions into having the best algorithims to price their odds all with the goal of making money of the average sports bettor.

#### Excpected Value
If a sports bettor knows that a home team has 50% chance to win a game and the decimal odds are 2.2 for the home team then they have a 10% expected value. That means if the sports bettor was bet $10 an infinite amount of time, the sports bettor would win 10% of the amount staked or 1 dollar. That is called having positive expected value.  It is also important to understand the relationship between decimal odds and implied probability. We can get the implied probability from decimal odds line with the following equation: Implied probability = 1/Decimal Odds.  In the example above the implied probability is 1/2.2= 45.45%. To add more contezt, the bookmaker priced the odds of the home team winning at 45.45% but in this hypothetical situation, you know the home team has 50% chance of winning. 



#### Model Thesis

As mentioned before, each bookmaker has propteiry algorithims for setting odds optmized for giving the house an edge. If their was only on market for then there would be very little hope in making money. But there are countless bookmakers that are competing with each other to have the most appealing odds. Any sports bettor can shop around different bookmakers for the best odds. When I say best odds, I mean higher odds. The higher the odds the higher the payout and the lower the implied probability. 


Our model was trained to predict the home team win probability. We can compare the the implied 


In this situation, our machine learning model thinks the home team has a higher chance of winning than what the bookmaker gives hence a odds price discrepancy. Only when that condition is met is when the model signals to the bettor using it to bet on the home team. Different models were back tested on historical data and take bets when the model signaled. XGBoost had the highest return



