from firestoreClient import client_setup

# DO NOT RUN multiple times. Multiple runs deletes all data.

# Creates connection with Firestore Database
db = client_setup()

# Years to edit data
years = ['2023']

# List of Big10 teams
teams = ['illinois', 'indiana', 'iowa', 'maryland', 'michigan',
         'michigan-state', 'minnesota', 'nebraska', 'northwestern',
         'ohio-state', 'penn-state', 'purdue', 'rutgers', 'wisconsin']

# Standardize the naming conventions for teams in the ACC to match the name on sports-reference
for year in years:

    collect = f'{year}GameLog'

    for team in teams:
        # Get the data from the Firestore database
        school = f'{team}'
        data_ref = db.collection("Big10").document(school).collection(collect)
        data_docs = data_ref.stream()

        for doc in data_docs:
            data = doc.to_dict()
            if data['Opp'] == "Illinois":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'illinois'})
            elif data['Opp'] == "Indiana":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'indiana'})
            elif data['Opp'] == "Iowa":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'iowa'})
            elif data['Opp'] == "Maryland":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'maryland'})
            elif data['Opp'] == "Michigan":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'michigan'})
            elif data['Opp'] == "Michigan State":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'michigan-state'})
            elif data['Opp'] == "Minnesota":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'minnesota'})
            elif data['Opp'] == "Nebraska":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'nebraska'})
            elif data['Opp'] == "Northwestern":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'northwestern'})
            elif data['Opp'] == "Ohio State":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'ohio-state'})
            elif data['Opp'] == "Penn State":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'penn-state'})
            elif data['Opp'] == "Purdue":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'purdue'})
            elif data['Opp'] == "Rutgers":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'rutgers'})
            elif data['Opp'] == "Wisconsin":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'wisconsin'})
            else:
                ref = data_ref.document(data['Date'])
                ref.delete()
