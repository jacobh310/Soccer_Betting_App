from google.cloud import bigquery
from flask import Flask
import json
import os


def get_fixtures():
    client = bigquery.Client()

    query = """
   SELECT 
      Home_Team,
      Away_Team,
      Home_Logo_URL,
      Away_Logo_URL,
      Date_Time, 
      Bet_365_Home_Win_Prob, 
      Model_Home_Win_Prob, 
      Bet365_Home_Odds, 
      Implied_Model_Odds
    FROM
      `astute-winter-373022.Soccer_Stats.Stats_Predictions` 
    WHERE Date_Time BETWEEN CURRENT_DATE("America/Los_Angeles") AND DATE_ADD(CURRENT_DATE("America/Los_Angeles"), 
    INTERVAL 4 DAY)
    """

    df = client.query(query).to_dataframe()
    j = df.to_json(orient='records')
    if not json.loads(j):
        return "No Games"
    else:
        return j


app = Flask(__name__)


@app.route("/", methods=['GET'])
def predictions():
    response = get_fixtures()
    return response, 201


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
