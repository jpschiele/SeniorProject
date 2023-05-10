import firebase_admin
from firebase_admin import credentials, firestore


# function created to establish a connection to the Firestore Database using JSON credentials file
def client_setup():
    cred = credentials.Certificate("schieleproject-firebase-adminsdk-m7rjq-33cb8281fc.json")
    try:
        firebase_admin.get_app()
    except ValueError:
        firebase_admin.initialize_app(cred)

    return firestore.client()
