import pandas as pd
import numpy as np
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.impute import SimpleImputer
from firestoreClient import client_setup
from confTeams import get_teams
import warnings

# columnSelection.py uses feature selection to determine the five most influential features in determining predicted
# values. Predictions for the result of the game are left in for example.

warnings.filterwarnings('ignore')

# Creates connection with Firestore Database
db = client_setup()

# Used to replace any nan values with the average
imp = SimpleImputer(missing_values=np.nan, strategy='mean')

# Convert the Firestore documents into a pandas DataFrame
data = pd.DataFrame()

# List of six major college basketball conferences
conferences = ['ACC', 'Big10', 'Big12', 'BigEast', 'PAC12', 'SEC']

# Store game data in the DataFrame
for conference in conferences:
    teams = get_teams(conference)

    years = ['2021', '2022', '2023']

    for year in years:
        collect = f'{year}GameLog'
        for team in teams:
            # Get the data from the Firestore database
            school = str(team)
            data_ref = db.collection(conference).document(school).collection(collect)
            data_docs = data_ref.stream()

            for doc in data_docs:
                if doc.id != 'Averages':
                    game = doc.to_dict()
                    data = data.append(game, ignore_index=True)

# Convert data from str to float
column_names = ['Date', 'Opp', 'Result']
for column in data.columns:
    if column not in column_names:
        data[[column]] = data[[column]].astype(float)

# Split the data into features (X) and target (y_team)
X = data[['Place', 'L3Pts', 'L3PtsOpp', 'L3TRB', 'L3TRBOpp', 'L33PPer', 'L33PPerOpp', 'L3FGPer', 'L3FGPerOpp',
              'L3FTA', 'L3FTAOpp', 'L3PF', 'L3PFOpp', 'L3TOV', 'L3TOVOpp', 'AVGPts', 'AVGPtsOpp', 'AVG3PA', 'AVG3PAOpp',
              'AVGAST', 'AVGASTOpp', 'AVGBLK', 'AVGBLKOpp', 'AVGFGA', 'AVGFGAOpp', 'AVGFTPer', 'AVGFTPerOpp',
              'AVGSTL', 'AVGSTLOpp', 'AVGORB', 'AVGORBOpp']]
X = imp.fit_transform(X)

# Change based on value to get features for predicting
y_team = data[['Result']]
y_team = y_team["Result"].replace({"W": 1, "L": 0})

y_team = imp.fit_transform(y_team)

# Reshape ndarray for the selector if needed
y_team = np.reshape(y_team, (-1, 1))

# Get five most important features for predicting above value
selector = SelectKBest(score_func=f_regression, k=5)
X_team = selector.fit_transform(X, y_team)

selected_indices = selector.get_support(indices=True)
print(selected_indices)

