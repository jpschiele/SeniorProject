import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase app with a service account
cred = credentials.Certificate("C:/Users/jpsch/OneDrive/Documents/SeniorProject/"
                               "schieleproject-firebase-adminsdk-m7rjq-33cb8281fc.json")
firebase_admin.initialize_app(cred)

# Get a reference to the Firestore database
db = firestore.client()

years = ['2023']

teams = ['baylor', 'iowa-state', 'kansas', 'kansas-state', 'oklahoma',
         'oklahoma-state', 'texas', 'texas-christian',
         'texas-tech', 'west-virginia']

for year in years:

    collect = f'{year}GameLog'

    for team in teams:
        # Get the data from the Firestore database
        school = f'{team}'
        data_ref = db.collection("Big12").document(school).collection(collect)
        data_docs = data_ref.stream()

        for doc in data_docs:
            data = doc.to_dict()
            if data['Opp'] == "Baylor":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'baylor'})
            elif data['Opp'] == "Iowa State":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'iowa-state'})
            elif data['Opp'] == "Kansas":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'kansas'})
            elif data['Opp'] == "Kansas State":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'kansas-state'})
            elif data['Opp'] == "Oklahoma":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'oklahoma'})
            elif data['Opp'] == "Oklahoma State":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'oklahoma-state'})
            elif data['Opp'] == "Texas":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'texas'})
            elif data['Opp'] == "TCU":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'texas-christian'})
            elif data['Opp'] == "Texas Tech":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'texas-tech'})
            elif data['Opp'] == "West Virginia":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'west-virginia'})
            else:
                ref = data_ref.document(data['Date'])
                ref.delete()
