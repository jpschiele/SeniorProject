import os
import firebase_admin
from google.cloud import firestore
from google.oauth2 import service_account
from firebase_admin import credentials, firestore
from dotenv import load_dotenv


# function created to establish a connection to the Firestore Database using Firebase credentials
def client_setup():
    load_dotenv()

    creds = {
        "type": os.environ.get('FIRESTORE_TYPE'),
        "project_id": os.environ.get('FIRESTORE_PROJECT_ID'),
        "private_key_id": os.environ.get('FIRESTORE_PRIVATE_KEY_ID'),
        "private_key": os.environ.get('FIRESTORE_PRIVATE_KEY'),
        "client_email": os.environ.get('FIRESTORE_CLIENT_EMAIL'),
        "client_id": os.environ.get('FIRESTORE_CLIENT_ID'),
        "auth_uri": os.environ.get('FIRESTORE_AUTH_URI'),
        "token_uri": os.environ.get('FIRESTORE_TOKEN_URI'),
        "auth_provider_x509_cert_url": os.environ.get('FIRESTORE_AUTH_PROVIDER_X509_CERT_URL'),
        "client_x509_cert_url": os.environ.get('FIRESTORE_CLIENT_X509_CERT_URL')
    }

    firebase_config = {
        'apiKey': os.environ.get('FIREBASE_API_KEY'),
        'authDomain': os.environ.get('FIREBASE_AUTH_DOMAIN'),
        'projectId': os.environ.get('FIREBASE_PROJECT_ID'),
        'storageBucket': os.environ.get('FIREBASE_STORAGE_BUCKET'),
        'messagingSenderId': os.environ.get('FIREBASE_MESSAGING_SENDER_ID'),
        'appId': os.environ.get('FIREBASE_APP_ID')
    }

    cred = service_account.Credentials.from_service_account_info(creds)

    try:
        firebase_admin.get_app()
    except ValueError:
        firebase_admin.initialize_app(cred, firebase_config)

    return firestore.client()
