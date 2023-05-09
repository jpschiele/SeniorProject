from firestoreClient import client_setup

# DO NOT RUN multiple times. Multiple runs deletes all data.

# Creates connection with Firestore Database
db = client_setup()

# Years to edit data
years = ['2023']

# List of PAC12 teams
teams = ['arizona', 'arizona-state', 'california', 'colorado', 'oregon',
         'oregon-state', 'southern-california', 'stanford', 'ucla', 'utah',
         'washington', 'washington-state']

# Standardize the naming conventions for teams in the ACC to match the name on sports-reference
for year in years:

    collect = f'{year}GameLog'

    for team in teams:
        # Get the data from the Firestore database
        school = f'{team}'
        data_ref = db.collection("PAC12").document(school).collection(collect)
        data_docs = data_ref.stream()

        for doc in data_docs:
            data = doc.to_dict()
            if data['Opp'] == "Arizona":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'arizona'})
            elif data['Opp'] == "Arizona State":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'arizona-state'})
            elif data['Opp'] == "California":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'california'})
            elif data['Opp'] == "Colorado":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'colorado'})
            elif data['Opp'] == "Oregon":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'oregon'})
            elif data['Opp'] == "Oregon State":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'oregon-state'})
            elif data['Opp'] == "USC":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'southern-california'})
            elif data['Opp'] == "Stanford":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'stanford'})
            elif data['Opp'] == "UCLA":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'ucla'})
            elif data['Opp'] == "Utah":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'utah'})
            elif data['Opp'] == "Washington":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'washington'})
            elif data['Opp'] == "Washington State":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'washington-state'})
            else:
                ref = data_ref.document(data['Date'])
                ref.delete()
