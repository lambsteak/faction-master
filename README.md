# Faction Master

## A dynamic quizzing app written in Flask using WebSockets (Flask-SocketIO library) and Celery (for task scheduling)

This is a dynamic quiz application with two rounds of quiz. In the first round there are same questions for all the players. Based on the scores of the players for each of the five factions they are alloted a faction and in the second round they are asked questions related to that faction. Celery is used to schedule the questions (using websocket for pushing and pulling messages between the client and server). For the second round the players are put into rooms based on faction and the questions and answers are sent and processed separately for each of the rooms.

### Setting up the project:
Download and install redis db from [this link](https://github.com/MicrosoftArchive/redis/releases/download/win-3.0.504/Redis-x64-3.0.504.msi)
 *(in case of Windows)*
 
 For linux follow these commands:
 
```
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make
sudo make install
```
If running the app for the first time:

```
git clone https://lambsteak@bitbucket.org/lambsteak/faction_master.git
cd faction_master.git
```

If running the project after any changes have been made in project **as well as
when running for the first time**:

- `pip install -r requirements.txt`
- Open a python interpreter and enter:
`from app import db`

- If any changes have been made in the db schema:
`db.drop_all()`

- Regardless of changes also run:

```
db.create_all()
db.session.commit()
exit()
```

- in case of linux open up a new terminal and start the redis server with command:
redis-server
 You might optionally want to daemonize the redis-server process and start it on system boot
 automatically (read [here](https://redis.io/topics/quickstart) for more)
 *(in case of windows the server is already running as a service)*

- open up another terminal and activate the virtual environment if using one
and cd into the root project directory (the one containing the app
directory inside) and run the following command:
`celery -A app.celery worker --loglevel=info -P eventlet`
- in the other terminal run: `python run.py`

### Using socketio

- to test particular events (eg 'start video') open up a new terminal and:
```
from app.schedule import start_video
start_video.delay()  # to immediately fire the given event from server
```
- to test the entire event sequence go to /admin and create a schedule
with the start time a couple of minutes from the present time, then go back to
admin's home page and click on 'Refresh Quiz Schedule Configuration'
After that go to the / (root url) and log in. The events will then occur
according to the timeline provided.
- **if creating/editing the schedule again and refreshing, if the previously
 scheduled tasks haven't expired (ie their time of execution hasn't passed) they will
 still be fired. The same can also occur when stopping or interrupting the events midway
 from celery itself. To solve this problem purge all the enqueued tasks from celery by:
 `celery -A app.celery purge -f`
- **IF YOU MAKE ANY CHANGES TO SCHEDULE.PY'S TASKS OR ANYTHING ASSOCIATED WITH IT
(sometimes including the template html files as well if required), YOU MUST
RESTART THE CELERY WORKER FOR CHANGES TO TAKE EFFECT**
