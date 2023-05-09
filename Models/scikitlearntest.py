from google.cloud import firestore

# set up a Firestore client object
db = firestore.Client()

# get a reference to a specific collection
collection_ref = db.collection('SampleData')

# add a document to the collection
data = {'gameID': 6, 'team1': 'St. Josephs', 'team1AvgPoints': 65, 'team1Points': 69, 'team2': 'Richmond', 'team2AvgPoints': 64, 'team2Points': 62, 'totalPoints': 131}
doc_ref = collection_ref.add(data)

# print the ID of the newly added document
print('Document created with ID: {}'.format(doc_ref.id))
