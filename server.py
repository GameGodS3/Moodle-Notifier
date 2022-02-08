import json
import scrapper
import db
from deepdiff import DeepDiff

from flask import Flask

app = Flask(__name__)


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

    dump_diff = DeepDiff(prev_dump, curr_dump)
    if dump_diff != {}:
        print(dump_diff)

        notif = {}

        for k, v in dump_diff['iterable_item_added'].items():
            subject_and_type = ["["+e for e in k.split("[") if e][-3:-1]
            notif[subject_and_type[0][2:-2]] = {subject_and_type[1][2:-2]: v}

        db.setData(curr_dump)

        return notif
    else:
        return "No new notifications"


if __name__ == '__main__':
    app.run()
