import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import numpy as np
import time
import warnings

warnings.filterwarnings('ignore')

cred = credentials.Certificate("C:/Users/jpsch/OneDrive/Documents/SeniorProject/schieleproject-firebase-adminsdk"
                               "-m7rjq-33cb8281fc.json")
firebase_admin.initialize_app(cred)

db = firestore.client()  # this connects to our Firestore database
collection = db.collection('PAC12')  # opens 'PAC12' collection

final_df = pd.DataFrame()

# list of PAC12 schools
schools = ['arizona', 'arizona-state', 'california', 'colorado', 'oregon',
           'oregon-state', 'southern-california', 'stanford', 'ucla', 'utah',
           'washington', 'washington-state']

# list of years to collect data from
years = ['2022']

for year in years:

    for school in schools:
        # sports-reference limits the number of HTTP calls
        # automatic break occurs after 9 schools to refresh call timer
        url = f'https://www.sports-reference.com/cbb/schools/{school}/men/{year}-gamelogs.html'
        str(url)
        print(school)

        try:
            dfs = pd.read_html(url, header=1)
        except:
            print(f'Could not find data for {school}.')
            continue

        # locates the game log table
        game_log_df = dfs[0]

        # drop rows that have the school header
        game_log_df = game_log_df.dropna(thresh=len(game_log_df.columns) - 3)

        # rows that have the column headers
        game = game_log_df['G'].isin(['G'])

        # only include win or loss not overtime
        game_log_df["W/L"] = game_log_df["W/L"].astype(str).str[0]

        # list of column names
        game_log_df.columns = ['G', 'Date', 'Place', 'Opp', 'Result', 'TmScore',
                               'OppScore', 'FG', 'FGA', 'FG%', '3PM',
                               '3PA', '3P%', 'FTM', 'FTA', 'FT%', 'ORB', 'TRB',
                               'AST', 'STL', 'BLK', 'TOV', 'PF', 'Empty',
                               'FGOpp', 'FGAOpp', 'FG%Opp', '3POpp', '3PAOpp',
                               '3P%Opp', 'FTOpp', 'FTAOpp', 'FT%Opp',
                               'ORBOpp', 'TRBOpp', 'ASTOpp', 'STLOpp',
                               'BLKOpp', 'TOVOpp', 'PFOpp']

        # Home/Away: 0 = away, 1 = home, 2 = neutral
        game_log_df.loc[game_log_df["Place"] == "@", "Place"] = 0
        game_log_df.loc[game_log_df["Place"] == "N", "Place"] = 2
        game_log_df["Place"] = game_log_df["Place"].replace(np.nan, 1)

        # drop empty columns from the DataFrame
        game_log_df.drop(game_log_df.columns[[0, 23]], axis=1, inplace=True)

        # store data in firebase by converting DataFrame to dictionary
        games = game_log_df.to_dict('records')

        # store each game under conference/team/year/date
        for game in games:
            if game['Date'] == 'Date':
                continue
            else:
                doc_name = str(game['Date'])

                subcollection = f'{school}'
                year_log = f'{year}GameLog'

                doc_ref = collection.document(subcollection).collection(year_log).document(doc_name)

                doc_ref.set(game)

                print(f'Document {doc_name} written to Firestore')

    time.sleep(120)
