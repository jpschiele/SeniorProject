import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase app with a service account
cred = credentials.Certificate("C:/Users/jpsch/OneDrive/Documents/SeniorProject/"
                               "schieleproject-firebase-adminsdk-m7rjq-33cb8281fc.json")
firebase_admin.initialize_app(cred)

# Get a reference to the Firestore database
db = firestore.client()

years = ['2023']

teams = ['boston-college', 'clemson', 'duke', 'florida-state', 'georgia-tech',
         'louisville', 'miami-fl', 'north-carolina', 'north-carolina-state', 'notre-dame',
         'pittsburgh', 'syracuse', 'virginia', 'virginia-tech', 'wake-forest']

for year in years:

    collect = f'{year}GameLog'

    for team in teams:
        # Get the data from the Firestore database
        school = f'{team}'
        data_ref = db.collection("ACC").document(school).collection(collect)
        data_docs = data_ref.stream()

        for doc in data_docs:
            data = doc.to_dict()
            if data['Opp'] == "Boston College":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'boston-college'})
            elif data['Opp'] == "Clemson":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'clemson'})
            elif data['Opp'] == "Duke":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'duke'})
            elif data['Opp'] == "Florida State":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'florida-state'})
            elif data['Opp'] == "Georgia Tech":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'georgia-tech'})
            elif data['Opp'] == "Louisville":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'louisville'})
            elif data['Opp'] == "Miami (FL)":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'miami-fl'})
            elif data['Opp'] == "UNC":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'north-carolina'})
            elif data['Opp'] == "NC State":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'north-carolina-state'})
            elif data['Opp'] == "Notre Dame":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'notre-dame'})
            elif data['Opp'] == "Pitt":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'pittsburgh'})
            elif data['Opp'] == "Syracuse":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'syracuse'})
            elif data['Opp'] == "Virginia":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'virginia'})
            elif data['Opp'] == "Virginia Tech":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'virginia-tech'})
            elif data['Opp'] == "Wake Forest":
                ref = data_ref.document(data['Date'])
                ref.update({'Opp': 'wake-forest'})
            else:
                ref = data_ref.document(data['Date'])
                ref.delete()
