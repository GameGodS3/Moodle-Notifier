# Moodle Notifier (Telegram Bot)

## Setup
To setup the notifier and bot for yourself:

1. Create a new Project in [Firebase](https://firebase.google.com/).
2. Go to *Project Settings* and **Add app**. Choose Web, give it a name, proceed and take note of the Firebase configuration shown.
3. Next, create a new Telegram bot via [BotFather](https://t.me/botfather) and take note of your Bot Token
4. Now, take note of your Telegram Chat ID from [Get Chat ID & User ID Bot](https://t.me/chatIDrobot)
5. Next, create a Heroku account, click this button, fill the fields with the information you gathered, and click **Deploy app**  
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/GameGodS3/Moodle-Notifier)
6. Finally, create a cronjob in [cron-job.org](https://cron-job.org) to ping `Your_App_Name.herokuapp.com/check` every 30 minutes


## Local Setup (for Development and Testing)
To setup and run the notifier locally, 

On Linux
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

Next run
```bash
python server.py
```
and visit `http://127.0.0.1:5000/check` to scrape and fetch notification
