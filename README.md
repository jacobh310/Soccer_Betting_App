# British Premier League Betting App
---
### 📌 [See the web app in action here](https://jacobh310-soccer-betting-app-frontend-game-predictions-cty251.streamlit.app)

## <b>Introduction</b>:  Succesfull Sports Betting?

The Sports Betting market is worth $74.2 billion dollars as of 2021 and is expected to reach $129.3 billion by 2028 according to [Global News Wire](https://www.globenewswire.com/en/news-release/2022/11/16/2556991/0/en/Sports-Betting-Market-Size-Share-to-Surpass-USD-129-3-Billion-by-2028-Vantage-Market-Research.html#:~:text=WASHINGTON%2C%20Nov.,forecast%20period%20of%202022%2D2028.)There is no question that your average sports gambler is competing against companies that put millions into having the best algorithims to price their odds all with the goal of making money of the average sports bettor. I tried to tilt the odds back to the sports bettor's favor by training a machine learning algorithm that predicts the home teams winning probability.

**Before Starting it is important to understand the following**
#### Bettting 101
- Decimal odds: The payout if a bet is won. Decimal odds of 2 means that if you bet $10 you would receive $20. $10 of the original bet and $10 profit. The higher the decimal odds the higher the pay
- Implied Probability: The probability implied by the decimal odds line. Implied probability = 1/Decimal Odds. A decimal odds of 2 has an implied probability of 50%. The higher the odds the lower the probability. Meaning low probably events have a higher payout.


#### Excpected Value
If a sports bettor knows that a home team has a 50% chance to win a game and the decimal odds are 2.2 for the home team then they have a 10% expected value. That means if the sports bettor bets $10 an infinite amount of times, the sports bettor would win 10% of the amount staked or 1 dollar. That is called having a positive expected value. In this scenario, no one knows that the home team has a 50% chance of winning but that is where machine learning comes in.

## Model Thesis
We can train machine learning algorithims on historical game statistics to predict the probability of the home team winning. That is exactly what this web app shows you. You can compare the model probability to the implied probability from different bookmakers and only take bets where the model probability is greater than the implied probability. Just like in the scenario above, the model predicts that the home team has a 50% of winning the game. Now a bookmaker has the decimal odds at 2.2. making the implied probability 45% (1/2.2). We would take that bet because the model has the higher home team probability. So as long as the model probability > book maker implied volatility, the model would take that bet.

Several machine learning algorithims were trained on data from 2000-2021. Data was split into train dev tests and the best model was chosen for the web app. The best model was chosen by looking at the historical profitability of the expected value trading strategy. So $100 would be staked if the model probability > book maker implied volatility. Out of all the algorithms, XGBosst was the most profitable and is also the one deployed in this web app.


## App Architecture

<p ><img align="center" src="https://raw.githubusercontent.com/jacobh310/Soccer_Betting_App/main/Images/App%20Architecture.png" 
      title="App Architecture" width="700"/></p>

**Cloud Storage**: Stores the best-performing machine learning Model

**Cloud Function:**
- Request fixture, team, and odds data for the next 4 days from Sportmonk and Rapid API.
- Cleans data and then loads model from **Cloud Storage** to make predictions on fixtures
- Fixture, team, and odds data along with prediction are stored in **BigQuery** table
- **Deployment Details**
    - Included API tokens in runtime variables
    - Used soccer-betting-storage service account which has access to **big query** and **cloud storage**
    - Have to allow all traffic so cloud scheduler can access the endpoint

**Cloud Scheduler:** Runs the cloud function every 4 days 
- **Deployment Details**
    - Get Request
    - Auth Header OIDC token
    - Service account: has to have access to a cloud function

**BigQuery:** Has fixture, team, and odds data along with predictions

**Cloud Run:** Rest API that takes GET requests and returns fixtures, teams, odds, and predictions for the games in the next three days. **Google Cloud Build** will redeploy containers using the **Container Registry** every time code is pushed into a GitHub Repository
- **Deployment Details**
    - Make Dockerfile
    - **Builds Container Image:** gcloud builds submit --tag gcr.io/<project_id>/<function_name>
    - **Deploys to Google Cloud Run:** gcloud run deploy --image gcr.io/<project_id>/<function_name> --platform managed
- **Cloud Build Details**
    - Need to make YAML file
        - Specified “./Flask_app” because that is the directory where the python script deployed to the cloud run is located 
    - No service account is needed
- **Container Registry**
    - Each new deployment is going to upload a container image located in the project folder/clour run name

**Streamlit Deploy:** The app is deployed using streamlit deploy which integrates with GitHub



## Resources
#### Deployment
https://github.com/lukebarousse/Data_Analyst_Streamlit_App_V1
https://github.com/patrickloeber/ml-deployment
#### APIs
https://football-postman.sportmonks.com/#23c7dbe0-863f-47a3-a079-c59d5cf775c4
https://rapidapi.com/sportmonks-data/api/football-pro
