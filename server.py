import json
import scrapper
import db
import os
from deepdiff import DeepDiff
from dotenv import load_dotenv
load_dotenv()

import telegram

from flask import Flask

app = Flask(__name__)
bot = telegram.Bot(os.getenv("TELEGRAMBOTTOKEN"))
@app.route('/')
def hello_world():
    return 'Hello World'


@app.route('/check')
def notif_check():
    prev_dump = db.getData()
    curr_dump = scrapper.scrape()

    # with open('courseContents.json', 'r') as f:
    #     prev_dump = json.loads(f.read())
    # with open('courseContents copy.json', 'r') as g:
    #     curr_dump = json.loads(g.read())

    chat_id = os.getenv("TELEGRAMCHATID")
    dump_diff = DeepDiff(prev_dump, curr_dump)
    if dump_diff != {}:
        print(dump_diff)

        notif = {}

        for k, v in dump_diff['iterable_item_added'].items():
            subject_and_type = ["["+e for e in k.split("[") if e][-3:-1]
            notif[subject_and_type[0][2:-2]] = {subject_and_type[1][2:-2]: v}

        db.setData(curr_dump)

        for i in notif:
            [subject, restype, title] = [i, list(notifs[i].keys())[0], list(notifs[i].values())[0]]
            print(subject, restype, title)
            bot.send_message(chat_id = chat_id, text = f"New {restype} posted in {subject} : {title}")
        print("Message Sent")

        return notif
    else:
        bot.send_message(chat_id = chat_id, text = "No New Notifications")
        print("Message Sent")
        return "No new notifications"


if __name__ == '__main__':
    app.run()
