from firebase import Firebase
import os
# from decouple import config
from dotenv import load_dotenv
load_dotenv()


firebase_config = {
    "apiKey": os.getenv("APIKEY"),
    "authDomain": os.getenv("AUTHDOMAIN"),
    "databaseURL": os.getenv("DBURL"),
    "projectId": os.getenv("PROJID"),
    "storageBucket": os.getenv("STOBUCK"),
    "messagingSenderId": os.getenv("MSGID"),
    "appId": os.getenv("APPID")
}

firebase = Firebase(firebase_config)

db = firebase.database()


def getData():
    """ Returns the scraped notifications from the Firebase Database as dictionary """
    # data = []
    # subjects = db.get().val()
    # for notif in subjects:
    #     data.append(notif)
    return dict(db.get().val())


def setData(data):
    """ Updates the notifications Firebase DB with the new notifications """
    db.set(data)


def users():
    """ Gathers the list of Users from the Firebase Database as a dictionary"""
    users = []
    users = db.child("subs").get()
    return dict(users.val())


def subscribe(chat_id):
    """ Adds the user as a Subscriber in the Firebase Database """
    db.child("subs").child(str(chat_id)).set("T")


def relevantsub(chat_id):
    """ Adds the user as subscriber of Relevant notifications in the Firebase Database """
    db.child("subs").child(str(chat_id)).set("R")


def unsubscribe(chat_id):
    """ Sets the Subscription status of user to False in the Firebase Database """
    db.child("subs").child(str(chat_id)).set("F")
