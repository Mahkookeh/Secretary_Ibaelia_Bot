import pyrebase
import requests
import os

FIREBASE_APIKEY = os.getenv("FIREBASE_APIKEY")
file_path = "C:\\Users\\Mahkookeh\\Desktop\\source\\repos\\serviceAccountCredentials.json"

firebase_config = {
  "apiKey": FIREBASE_APIKEY,
  "authDomain": "crosswords-20578.firebaseapp.com",
  "databaseURL": "https://crosswords-20578.firebaseio.com",
  "storageBucket": "crosswords-20578.appspot.com",
  "serviceAccount": file_path
}

firebase = pyrebase.initialize_app(firebase_config)
ibaelia_db = firebase.database() 