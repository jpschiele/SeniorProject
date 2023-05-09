import pandas as pd
import numpy as np
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from firestoreClient import client_setup
from confTeams import get_teams
import warnings

warnings.filterwarnings('ignore')

# Used to replace any nan values with the average
imp = SimpleImputer(missing_values=np.nan, strategy='mean')

# Used for normalizing data
scaler_lin = StandardScaler()
scaler_log = StandardScaler()

# Creates connection with Firestore Database
db = client_setup()

# Convert the Firestore documents to a Pandas DataFrame
data = pd.DataFrame()

# List of all major conferences
conferences = ['ACC', 'Big10', 'Big12', 'BigEast', 'PAC12', 'SEC']

for conference in conferences:
    teams = get_teams(conference)

    # List of years to collect data from (currently have 2021-2023)
    years = ['2021', '2022', '2023']

    for year in years:
        collect = f'{year}GameLog'
        for team in teams:
            # Get the data from the Firestore database
            school = str(team)
            data_ref = db.collection("ACC").document(school).collection(collect)
            data_docs = data_ref.stream()

            # Compute efficiency ratings and add data to DataFrame
            for doc in data_docs:
                if doc.id != 'Averages':
                    game = doc.to_dict()
                    game['tm1_EFG'] = float(game['offEFG']) - float(game['defEFG'])
                    game['tm2_EFG'] = float(game['defEFG']) - float(game['offEFG'])
                    game['tm1_TOP'] = float(game['offTOP']) - float(game['defTOP'])
                    game['tm2_TOP'] = float(game['defTOP']) - float(game['offTOP'])
                    game['tm1_ORB'] = float(game['offORB']) - float(game['defORB'])
                    game['tm2_ORB'] = float(game['defORB']) - float(game['offORB'])
                    game['tm1_FTR'] = float(game['offFTR']) - float(game['defFTR'])
                    game['tm2_FTR'] = float(game['defFTR']) - float(game['offFTR'])

                    data = data.append(game, ignore_index=True)

# Convert Strings into Floats
column_names = ['Date', 'Opp', 'Result']
for column in data.columns:
    if column not in column_names:
        data[[column]] = data[[column]].astype(float)

# Split the data into features (X) and target values (y_lin and y_log)
X = data[['Place', 'L3Pts', 'L3PtsOpp', 'L3TRB', 'L3TRBOpp', 'AVGPts', 'AVGPtsOpp',
              'AVGAST', 'AVGASTOpp', 'AVGFGA', 'AVGFGAOpp', 'tm1_EFG', 'tm2_EFG',
              'tm1_TOP', 'tm2_TOP', 'tm1_ORB', 'tm2_ORB', 'tm1_FTR', 'tm2_FTR']]


X_lin = imp.fit_transform(X)

# Using Linear Regression to predict scores
y_lin = data[['TmScore', 'OppScore']]
y_lin = imp.fit_transform(y_lin)

# Split the data into training and testing sets
X_lin_train, X_lin_test, y_lin_train, y_lin_test = train_test_split(X_lin, y_lin, test_size=0.2)

# Normalize the data
scaler_lin.fit(X_lin_train)

X_lin_train_norm = scaler_lin.transform(X_lin_train)
X_lin_test_norm = scaler_lin.transform(X_lin_test)
"""
# Save the fitted scaler
with open('scaler_lin.pkl', 'wb') as file:
    pickle.dump(scaler_lin, file)
"""
# Train the linear regression model
lin_reg = LinearRegression().fit(X_lin_train_norm, y_lin_train)

# Use the model to predict the scores for the normalized test data
y_lin_pred = lin_reg.predict(X_lin_test_norm)

# Calculate the mean squared error between the predicted and actual scores
mse = mean_squared_error(y_lin_test, y_lin_pred)

# Save the model to the Firestore Database
model_data = pickle.dumps(lin_reg)

data_ref = db.collection("Models").document('new_lin_reg_model')

data_ref.set({'model_data': model_data})

print("Mean Squared Error:", mse)

"""
# Using Logistic Regression to get win probabilities
X_log = imp.fit_transform(X)
y_log = data[["Result"]]
y_log = y_log["Result"].replace({"W": 1, "L": 0})
X_log_train, X_log_test, y_log_train, y_log_test = train_test_split(X_log, y_log, test_size=0.2, random_state=42)

# Normalizing the data
scaler_log.fit(X_log_train)

X_log_train_norm = scaler_log.transform(X_log_train)
X_log_test_norm = scaler_log.transform(X_log_test)

# Save the fitted scaler
with open('scaler_log.pkl', 'wb') as file:
    pickle.dump(scaler_log, file)

# Train the logistic regression model
log_reg = LogisticRegression()

log_reg.fit(X_log_train_norm, y_log_train)

# Save the model to the Firestore Database
model_data = pickle.dumps(log_reg)

data_ref = db.collection("Models").document('log_reg_model')

data_ref.set({'model_data': model_data})

# Calculate the accuracy in predicting game outcomes
y_log_pred = log_reg.predict(X_log_test_norm)

accuracy = accuracy_score(y_log_test, y_log_pred)
print('Accuracy: ', accuracy)
"""
print("done")
