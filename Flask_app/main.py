from google.cloud import bigquery
from flask import Flask, request, jsonify
import pandas
import os


def get_fixtures():
    client = bigquery.Client()

    query = """
    SELECT 
      Home_Team,
      Away_Team,
      Date_Time, 
      Bet_365_Home_Win_Prob, 
      Model_Home_Win_Prob, 
      Bet365_Home_Odds, 
      Implied_Model_Odds
    FROM
      `astute-winter-373022.Soccer_Stats.Stats_Predictions` 
    WHERE Date_Time BETWEEN CURRENT_DATE() AND DATE_ADD(CURRENT_DATE(), INTERVAL 3 DAY);
    """

    query = """    SELECT 
      Home_Team,
      Away_Team,
      Date_Time, 
      Bet_365_Home_Win_Prob, 
      Model_Home_Win_Prob, 
      Bet365_Home_Odds, 
      Implied_Model_Odds
    FROM
      `astute-winter-373022.Soccer_Stats.Stats_Predictions` 
    WHERE Date_Time BETWEEN '2023-01-05' AND '2023-01-08'"""

    df = client.query(query).to_dataframe()
    json = df.to_json(orient='records')
    if json:
        return "No Games"
    else:
        return json


app = Flask(__name__)


@app.route("/", methods=['GET'])
def predictions():
    response = get_fixtures()
    return response, 201


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
