import firebase_admin
from firebase_admin import credentials, firestore
from sklearn.linear_model import LinearRegression
import numpy as np


cred = credentials.Certificate("C:/Users/jpsch/OneDrive/Documents/SeniorProject/"
                               "schieleproject-firebase-adminsdk-m7rjq-33cb8281fc.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

doc_ref = db.collection("Models").document("basicModel")

doc = doc_ref.get()

if doc.exists:
    model_params = doc.to_dict()
    reg = LinearRegression(**model_params)
else:
    print('No model found')

stats = [["duke", .5, 26, .9, 20],
         ["kentucky", .33, 15, .8, 15],
         ["michigan", .4, 20, .85, 17],
         ["kansas", .41, 20, .83, 18]]

keep_going = 'y'
while keep_going == 'y':
    team1 = input("Enter team 1: ")
    team2 = input("Enter team 2: ")
    if team1 == "duke":
        team1 = 0
    elif team1 == "kentucky":
        team1 = 1
    elif team1 == "michigan":
        team1 = 2
    elif team1 == "kansas":
        team1 = 3
    if team2 == "duke":
        team2 = 0
    elif team2 == "kentucky":
        team2 = 1
    elif team2 == "michigan":
        team2 = 2
    elif team2 == "kansas":
        team2 = 3
    new_game = np.array([[2, stats[team1][1], stats[team1][2], stats[team1][3], stats[team1][4],
                          stats[team2][1], stats[team2][2], stats[team2][3], stats[team2][4]]])
    predicted_scores = reg.predict(new_game)
    print("Predicted Score:", predicted_scores[0])
    keep_going = input("Enter 'y' to run another game: ")
