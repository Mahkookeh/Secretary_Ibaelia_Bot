import pyrebase
import requests
import os

# FIREBASE_APIKEY = os.getenv("FIREBASE_APIKEY")
# file_path = "C:\\Users\\Mahkookeh\\Desktop\\source\\repos\\serviceAccountCredentials.json"

firebase_config = {
  "apiKey": os.getenv("FIREBASE_APIKEY"),
  "authDomain": "crosswords-20578.firebaseapp.com",
  "databaseURL": "https://crosswords-20578.firebaseio.com",
  "storageBucket": "crosswords-20578.appspot.com",
  'serviceAccount': {
    # Your "Service account ID," which looks like an email address.
    'client_email': os.getenv("FIREBASE_CLIENT_EMAIL"), 
    # The part of your Firebase database URL before `firebaseio.com`. 
    # e.g. `fiery-flames-1234`
    'client_id': os.getenv("FIREBASE_CLIENT_ID"),
    # The key itself, a long string with newlines, starting with 
    # `-----BEGIN PRIVATE KEY-----\n`
    'private_key': os.getenv("FIREBASE_PRIVATE_KEY").replace('\\n', '\n'),
    # Your service account "key ID." Mine is 40 alphanumeric characters.
    'private_key_id': os.getenv("FIREBASE_PRIVATE_KEY_ID"),
    'type': 'service_account'
  },
}

firebase = pyrebase.initialize_app(firebase_config)
ibaelia_db = firebase.database() 