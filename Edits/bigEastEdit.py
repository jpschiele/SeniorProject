from firestoreClient import client_setup

# DO NOT RUN multiple times. Multiple runs deletes all data.

# Creates connection with Firestore Database
db = client_setup()

# Years to edit data
years = ['2023']

# List of BigEast teams
teams = ['butler', 'connecticut', 'creighton', 'depaul', 'georgetown',
         'marquette', 'providence', 'seton-hall', 'st-johns-ny',
         'villanova', 'xavier']

# Standardize the naming conventions for teams in the ACC to match the name on sports-reference
for year in years:

    collect = f'{year}GameLog'

    for team in teams:
        # Get the data from the Firestore database
        school = f'{team}'
        data_ref = db.collection("BigEast").document(school).collection(collect)
        data_docs = data_ref.stream()

        for doc in data_docs:
            data = doc.to_dict()
            if data['Opp'] == "Butler":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'butler'})
            elif data['Opp'] == "UConn":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'connecticut'})
            elif data['Opp'] == "Creighton":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'creighton'})
            elif data['Opp'] == "DePaul":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'depaul'})
            elif data['Opp'] == "Georgetown":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'georgetown'})
            elif data['Opp'] == "Marquette":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'marquette'})
            elif data['Opp'] == "Providence":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'providence'})
            elif data['Opp'] == "Seton Hall":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'seton-hall'})
            elif data['Opp'] == "St. John's (NY)":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'st-johns-ny'})
            elif data['Opp'] == "Villanova":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'villanova'})
            elif data['Opp'] == "Xavier":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'xavier'})
            else:
                ref = data_ref.document(data['Date'])
                ref.delete()
