import pickle
from firestoreClient import client_setup
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


# Linear Regression model for score predictions and Logistic Regression model for win probability were trained
# completely separate, but with the same features. There may be discrepancies between win probabilities and the
# predicted final scores due to this. For example, Team A may have a 52% win probability, but the final score may
# be Team A: 64.3 and Team B: 64.7. Although this may seem contradictory, it is due to the different models in use.

# Gives a prediction for the final score of a game
def run_score_model(conf, team1, team2, place):
    print(conf, team1, team2, place)
    db = client_setup()

    with open('scaler_lin.pkl', 'rb') as file:
        scaler_lin = pickle.load(file)

    doc_ref = db.collection('Models').document('lin_reg_model')
    doc = doc_ref.get()

    model_data = doc.to_dict().get('model_data')

    lin_reg = pickle.loads(model_data)

    data1 = pd.DataFrame()
    data1_ref = db.collection(conf).document(team1).collection('2023GameLog')
    data1_docs = data1_ref.stream()

    for doc in data1_docs:
        data1 = data1.append(doc.to_dict(), ignore_index=True)

    team1_avg = data1.iloc[-2]
    team1_eff = data1.iloc[-1]

    data2 = pd.DataFrame()
    data2_ref = db.collection(conf).document(team2).collection('2023GameLog')
    data2_docs = data2_ref.stream()

    for doc in data2_docs:
        data2 = data2.append(doc.to_dict(), ignore_index=True)

    team2_avg = data2.iloc[-2]
    team2_eff = data2.iloc[-1]

    tm1_EFG = float(team1_eff[['offEFG']]) - float(team2_eff[['offEFG']])
    tm2_EFG = float(team1_eff[['defEFG']]) - float(team2_eff[['defEFG']])
    tm1_TOP = float(team1_eff[['offTOP']]) - float(team2_eff[['offTOP']])
    tm2_TOP = float(team1_eff[['defTOP']]) - float(team2_eff[['defTOP']])
    tm1_ORB = float(team1_eff[['offORB']]) - float(team2_eff[['offORB']])
    tm2_ORB = float(team1_eff[['defORB']]) - float(team2_eff[['defORB']])
    tm1_FTR = float(team1_eff[['offFTR']]) - float(team2_eff[['offFTR']])
    tm2_FTR = float(team1_eff[['defFTR']]) - float(team2_eff[['defFTR']])

    new_game = np.array([[place, team1_avg[['L3Pts']], team2_avg[['L3Pts']], team1_avg[['L3TRB']],
                          team2_avg[['L3TRB']], team1_avg[['AVGPts']], team2_avg[['AVGPts']],
                          team1_avg[['AVGAST']], team2_avg[['AVGAST']], team1_avg[['AVGFGA']], team2_avg[['AVGFGA']],
                          tm1_EFG, tm2_EFG, tm1_TOP, tm2_TOP, tm1_ORB, tm2_ORB, tm1_FTR, tm2_FTR]])

    new_game = scaler_lin.transform(new_game)

    predicted_scores = lin_reg.predict(new_game)

    return predicted_scores[0]


# Gives the prediction for the win probability of a team
def run_win_model(conf, team1, team2, place):
    db = client_setup()

    with open('scaler_log.pkl', 'rb') as file:
        scaler_log = pickle.load(file)

    doc_ref = db.collection('Models').document('log_reg_model')
    doc = doc_ref.get()

    model_data = doc.to_dict().get('model_data')

    log_reg = pickle.loads(model_data)

    data1 = pd.DataFrame()
    data1_ref = db.collection(conf).document(team1).collection('2023GameLog')
    data1_docs = data1_ref.stream()

    for doc in data1_docs:
        data1 = data1.append(doc.to_dict(), ignore_index=True)

    team1_avg = data1.iloc[-2]
    team1_eff = data1.iloc[-1]

    data2 = pd.DataFrame()
    data2_ref = db.collection(conf).document(team2).collection('2023GameLog')
    data2_docs = data2_ref.stream()

    for doc in data2_docs:
        data2 = data2.append(doc.to_dict(), ignore_index=True)

    team2_avg = data2.iloc[-2]
    team2_eff = data2.iloc[-1]

    tm1_EFG = float(team1_eff[['offEFG']]) - float(team2_eff[['offEFG']])
    tm2_EFG = float(team1_eff[['defEFG']]) - float(team2_eff[['defEFG']])
    tm1_TOP = float(team1_eff[['offTOP']]) - float(team2_eff[['offTOP']])
    tm2_TOP = float(team1_eff[['defTOP']]) - float(team2_eff[['defTOP']])
    tm1_ORB = float(team1_eff[['offORB']]) - float(team2_eff[['offORB']])
    tm2_ORB = float(team1_eff[['defORB']]) - float(team2_eff[['defORB']])
    tm1_FTR = float(team1_eff[['offFTR']]) - float(team2_eff[['offFTR']])
    tm2_FTR = float(team1_eff[['defFTR']]) - float(team2_eff[['defFTR']])

    new_game = np.array([[place, team1_avg[['L3Pts']], team2_avg[['L3Pts']], team1_avg[['L3TRB']],
                          team2_avg[['L3TRB']], team1_avg[['AVGPts']], team2_avg[['AVGPts']],
                          team1_avg[['AVGAST']], team2_avg[['AVGAST']], team1_avg[['AVGFGA']], team2_avg[['AVGFGA']],
                          tm1_EFG, tm2_EFG, tm1_TOP, tm2_TOP, tm1_ORB, tm2_ORB, tm1_FTR, tm2_FTR]])

    new_game = scaler_log.transform(new_game)

    win_prob = log_reg.predict_proba(new_game)[:, 1]

    return win_prob[0] * 100
