import firebase_admin
from firebase_admin import credentials, firestore
from firestoreClient import client_setup
from confTeams import get_teams
import pandas as pd
import numpy as np
import time
import warnings

# teamCollection.py is used in data collection. It accesses https://www.sports-reference.com/ and collects data
# for each game played during specified years and stores the data in the Firestore Database.

warnings.filterwarnings('ignore')

# Creates connection to Firestore Database
db = client_setup()

# List of conferences
conferences = ['ACC', 'Big10', 'Big12', 'BigEast', 'PAC12', 'SEC']

for conference in conferences:
    # Opens conference collection
    collection = db.collection(conference)

    # Creates pandas DataFrame
    final_df = pd.DataFrame()

    # List of conference schools
    schools = get_teams(conference)

    # List of years to collect data
    years = ['2023']

    for year in years:

        for school in schools:
            # sports-reference limits the number of HTTP calls
            # Automatic break occurs after each conference to refresh call timer
            url = f'https://www.sports-reference.com/cbb/schools/{school}/men/{year}-gamelogs.html'
            str(url)
            print(school)

            try:
                dfs = pd.read_html(url, header=1)
            except:
                print(f'Could not find data for {school}.')
                continue

            # Locates the game log table
            game_log_df = dfs[0]

            # Drop rows that have the school header
            game_log_df = game_log_df.dropna(thresh=len(game_log_df.columns) - 3)

            # List of rows that have the column headers
            game = game_log_df['G'].isin(['G'])

            # Only include win or loss not overtime
            game_log_df["W/L"] = game_log_df["W/L"].astype(str).str[0]

            # List of column names
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

            # Drop empty columns from the DataFrame
            game_log_df.drop(game_log_df.columns[[0, 23]], axis=1, inplace=True)

            # Store data in Firestore Database by converting DataFrame to dictionary
            games = game_log_df.to_dict('records')

            # Store each game under conference/team/year/date
            for game in games:
                # Ignores non-game data
                if game['Date'] == 'Date':
                    continue
                else:
                    doc_name = str(game['Date'])

                    sub_collection = f'{school}'
                    year_log = f'{year}GameLog'

                    doc_ref = collection.document(sub_collection).collection(year_log).document(doc_name)

                    doc_ref.set(game)

                    print(f'Document {doc_name} written to Firestore')

        time.sleep(120)
