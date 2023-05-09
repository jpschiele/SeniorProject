import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase app with a service account
cred = credentials.Certificate("C:/Users/jpsch/OneDrive/Documents/SeniorProject/"
                               "schieleproject-firebase-adminsdk-m7rjq-33cb8281fc.json")
firebase_admin.initialize_app(cred)

# Get a reference to the Firestore database
db = firestore.client()

years = ['2023']

teams = ['alabama', 'arkansas', 'auburn', 'florida', 'georgia', 'kentucky',
         'louisiana-state', 'mississippi', 'mississippi-state', 'missouri',
         'south-carolina', 'tennessee', 'texas-am', 'vanderbilt']

for year in years:

    collect = f'{year}GameLog'

    for team in teams:
        # Get the data from the Firestore database
        school = f'{team}'
        data_ref = db.collection("SEC").document(school).collection(collect)
        data_docs = data_ref.stream()

        for doc in data_docs:
            data = doc.to_dict()
            if data['Opp'] == "Alabama":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'alabama'})
            elif data['Opp'] == "Arkansas":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'arkansas'})
            elif data['Opp'] == "Auburn":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'auburn'})
            elif data['Opp'] == "Florida":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'florida'})
            elif data['Opp'] == "Georgia":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'georgia'})
            elif data['Opp'] == "Kentucky":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'kentucky'})
            elif data['Opp'] == "LSU":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'louisiana-state'})
            elif data['Opp'] == "Ole Miss":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'mississippi'})
            elif data['Opp'] == "Mississippi State":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'mississippi-state'})
            elif data['Opp'] == "Missouri":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'missouri'})
            elif data['Opp'] == "South Carolina":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'south-carolina'})
            elif data['Opp'] == "Tennessee":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'tennessee'})
            elif data['Opp'] == "Texas A&M":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'texas-am'})
            elif data['Opp'] == "Vanderbilt":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'vanderbilt'})
            else:
                ref = data_ref.document(data['Date'])
                ref.delete()
