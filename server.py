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
    # pretty_diff = json.dumps(dump_diff, sort_keys=True, indent=4)
    # print(pretty_diff)

    for k, v in dump_diff['iterable_item_added'].items():
        s = ["["+e for e in k.split("[") if e]

    s = s[-3:-1]
    for i in range(len(s)):
        s[i] = s[i][1:-1]

    print(f"New {s[1]} posted in {s[0]}: {v}")

    return dump_diff


if __name__ == '__main__':
    app.run()
