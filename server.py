from flask import Flask, request
import telegram
import json
import scrapper
import db
import os
from deepdiff import DeepDiff
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
token = os.getenv("TELEGRAMBOTTOKEN")
bot = telegram.Bot(token)
herokuURL = os.getenv("HEROKUURL")


@app.route('/')
def hello_world():
    return 'Hello World'


@app.route('/{}'.format(token), methods=['POST'])
def respond():
    """
    Responds to slash commands issued to bot via Telegram
    """

    # Retrieve message in JSON and transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.effective_message.chat.id
    msg_id = update.effective_message.message_id
    user_id = update.effective_user.id

    # UTF-8 formatting
    text = update.message.text.encode('utf-8').decode()
    # for debugging
    print("Got text message: ", text)
    print("UserID: ", user_id)

    # Slash Command
    # Welcome message / Start Message
    if text == "/start":
        bot_welcome = """
You have subscribed to notifications for LMS CET CS
        """
        bot.sendMessage(chat_id=chat_id, text=bot_welcome,
                        reply_to_message_id=msg_id)
        db.subscribe(user_id)
    elif text == "/unsubscribe":
        db.unsubscribe(user_id)
    return str(user_id)


@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.set_webhook('{URL}{HOOK}'.format(URL=herokuURL, HOOK=token))

    # debugging prints
    if s:
        return "Webhook setup OK"
    else:
        return "Webhook setup failed"


@app.route('/testping')
def testping():
    msg = request.args.get("msg")
    users = db.users()
    for user in users:
        if users[user] == "T":
            if msg:
                bot.send_message(chat_id=user, text=str(msg),
                                 parse_mode="Markdown")
            else:
                bot.send_message(
                    chat_id=user, text="This is a test ping from Moodle Notifier Bot to all users. Bot is under maintainence and testing. Sorry for the inconvenience")
    if msg:
        return f"Sent {msg} to all users"
    else:
        return "Pinged all users"


@app.route('/check')
def notif_check():
    print("Getting previous course contents...")
    prev_dump = db.getData()

    print("Scraping course contents...")
    curr_dump = scrapper.scrape()

    # with open('courseContents.json', 'r') as f:
    #     prev_dump = json.loads(f.read())
    # with open('courseContents copy.json', 'r') as g:
    #     curr_dump = json.loads(g.read())

    dump_diff = DeepDiff(prev_dump, curr_dump)
    if dump_diff != {}:
#        print(dump_diff)

        notif = {}

        for k, v in dump_diff['iterable_item_added'].items():
            subject_and_type = ["["+e for e in k.split("[") if e][-3:-1]
            notif[subject_and_type[0][2:-2]] = {subject_and_type[1][2:-2]: v}

#        print(notif)

        users = db.users()
        for user in users:
            if users[user] == "T":
                for i in notif:
                    [subject, restype, title] = [
                        i, list(notif[i].keys())[0], list(notif[i].values())[0]]
                    print(subject, restype, title)
                    bot.send_message(
                        chat_id=user, text=f"*{subject}*\n\n{title} ({restype.capitalize()})", parse_mode="Markdown")
        print("Message Sent")

        db.setData(curr_dump)

        return notif
    else:
        #    bot.send_message(chat_id = chat_id, text = "No New Notifications")
        #    print("Message Sent")
        return "No new notifications"


if __name__ == '__main__':
    app.run(threaded=True)
