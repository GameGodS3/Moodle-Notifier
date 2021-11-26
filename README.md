# Moodle Notifier

To setup the notifier, first run
```bash
pip3 install virtualenv
python3 -m venv venv
python3 setup.py
source venv/bin/activate
pip3 install -r requirements.txt
```
Or on Windows
```powershell
pip install virtualenv
python -m venv venv
python setup.py
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

and follow the instructions.

Next run
```bash
python3 run.py
```
to run the script. The logged in page will be written into a `moodletest.html` file.