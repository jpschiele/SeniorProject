import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase app with a service account
cred = credentials.Certificate("C:/Users/jpsch/OneDrive/Documents/SeniorProject/"
                               "schieleproject-firebase-adminsdk-m7rjq-33cb8281fc.json")
firebase_admin.initialize_app(cred)

# Get a reference to the Firestore database
db = firestore.client()

years = ['2023']

teams = ['arizona', 'arizona-state', 'california', 'colorado', 'oregon',
         'oregon-state', 'southern-california', 'stanford', 'ucla', 'utah',
         'washington', 'washington-state']

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
