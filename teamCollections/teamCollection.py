from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time

final_df = pd.DataFrame()

# list of all D1 schools for 2023 season
# schools may change depending on year
schools = ['texas-am']

delay = 1
for school in schools:
    if delay % 10 == 0:
        time.sleep(120)
        delay = 1

    # sports-reference limits the number of HTTP calls
    # use 10 schools at a time with a small break between runs
    url = f'https://www.sports-reference.com/cbb/schools/{school}/men/2022-gamelogs.html'
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

    # add school name as the 'Team' column
    school_name = []

    for i in range(0, len(game_log_df)):
        school_name.append(school)

    game_log_df["Team"] = school_name

    # only include win or loss not overtime
    game_log_df["W/L"] = game_log_df["W/L"].astype(str).str[0]

    # add team game log to the final DataFrame
    final_df = final_df.append(game_log_df[~game])

    delay += 1

# list of column names
final_df.columns = ['G', 'Date', 'Place', 'Opp', 'Result', 'TmScore',
                    'OppScore', 'FG', 'FGA', 'FG%', '3PM',
                    '3PA', '3P%', 'FTM', 'FTA', 'FT%', 'ORB', 'TRB',
                    'AST', 'STL', 'BLK', 'TOV', 'PF', 'Empty',
                    'FGOpp', 'FGAOpp', 'FG%Opp', '3POpp', '3PAOpp',
                    '3P%Opp', 'FTOpp', 'FTAOpp', 'FT%Opp',
                    'ORBOpp', 'TRBOpp', 'ASTOpp', 'STLOpp',
                    'BLKOpp', 'TOVOpp', 'PFOpp', 'Team']

# Home/Away: 0 = away, 1 = home, 2 = neutral
final_df.loc[final_df["Place"] == "@", "Place"] = 0
final_df.loc[final_df["Place"] == "N", "Place"] = 2
final_df["Place"] = final_df["Place"].replace(np.nan, 1)

# drop empty columns from the DataFrame
final_df.drop(final_df.columns[[0, 23]], axis=1, inplace=True)

# save the game log table as a CSV file
final_df.to_csv('C:/Users/jpsch/OneDrive/Documents/SeniorProject/2021_1team_data.csv', index=False)



