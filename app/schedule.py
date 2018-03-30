from flask import render_template
from flask_socketio import SocketIO
from app import celery, db
from app.models import Faction, Log, Question, Option, Answer, Player
from app.utils import divideIntoFactions

# we will have players logged in before apx. t-5 minutes
# as the players log in their creds are stored in the db and they will get a uid
# the following page which is returned will be the 'basepage'
# the player's uid will be provided to the javascript on that page
# a websocket connection will be established between the client and server
# the server will be at rest until t time
# at time t the video element in the basepage will be triggered through one of the
# socketio messages
# the video will play its full length. then after t+(length of video) time
# another message will be sent which will cause the execution of a script to remove
# the video element from display and
# then the instruction page will be opened through redirection and for 1 minute
# a countdown will be displayed indicating the start of quiz along with the
# instruction
# after that a message is sent to the server which will cause the instruction
# page to redirect to the question page
# in the question page there will be a listener for new question which will add
# a new question to the page as well as submit the answer of the current
# question to the server
# when all questions of the first round are done the server sends another message
# for redirecting to the faction allotment page and which will contain a listener
# for redirecting to the 2nd round questions page and the server will send the
# corresponding message for that after a 1 minute break
# on the 2nd round question page again the questions will be displayed and
# answers submitted after the interval of the time allotted for the given question
# when all rounds are done the message for redirecting to the results page
# will be sent and the results page will be rendered.
# ps: there will also have to be mechanisms to pause the time of server's
# scheduler to deal with any unforeseen problems on the venue as required

socketio = SocketIO(message_queue='redis://localhost:6379')


@celery.task()
def start_video():
    print('****RUNNING****')
    log = Log(message='Running start_video')
    db.session.add(log)
    db.session.commit()
    socketio.emit(
        'start video',
        {'snippet': render_template('snippet_video.html', macro='abcde')},
        namespace='/'
    )
    # t = render_template('snippet_video.html', macro='abcde')
    # print(t)
    # socketio.emit(
    #     'start video',
    #     {'snippet': 'This will contain the video sources etc.'},
    #     namespace='/'
    # )


@celery.task()
def stop_video():
    socketio.emit(
        'stop video',
        {'snippet': render_template('snippet_instruction.html', t='qwqwq')},
        namespace='/'
    )
    log = Log(message='Running stop_video')
    db.session.add(log)
    db.session.commit()

@celery.task()
def redirect_to_r1():
    socketio.emit('redirect to round 1', namespace='/')
    log = Log(message='Running redirect_to_r1')
    db.session.add(log)
    db.session.commit()


@celery.task()
def show_next_question():
    question = Question.query.filter_by(for_first_round=True, asked=False).first()
    if not question:
        print("No more questions present")
        socketio.emit(
            'show next question',
            {
                'q_present': False
            }
        )
        return
    question.asked = True
    db.session.commit()
    options = Option.query.filter_by(question=question)
    option_list = []
    for opt in options:
        option_list.append(
            {'id': opt.id, 'text': opt.text}
        )
    socketio.emit(
        'show next question',
        {'question': {'id': question.id, 'text': question.text},
         'options': option_list,
         'q_present': True
         }
    )
    '''
    socketio.emit(
        'show next question',
        {'snippet': render_template(
            'snippet_r1_question.html',
            question=Question.query.get(q_no),
            options=Option.query.filter_by(question_id=q_no)
        )},
        namespace='/'
    )
    '''
    log = Log(message='Running show_next_question')
    db.session.add(log)
    db.session.commit()


@celery.task()
def redirect_to_end_of_r1():
    # will tell the client to emit "display r1 results"
    socketio.emit('redirect to end of round 1', namespace='/')
    log = Log(message='Running redirect_to_end_of_r1')
    db.session.add(log)
    db.session.commit()


@celery.task()
def redirect_to_r2():
    socketio.emit('redirect to round 2', namespace='/')
    log = Log(message='Running redirect_to_r2')
    db.session.add(log)
    db.session.commit()


@celery.task()
def show_r2_question():
    factions = Faction.query.all()
    for faction in factions:
        print(faction.name)
        question = Question.query.filter_by(
            for_first_round=False,
            asked=False,
            faction=faction
        ).first()
        if not question:
            print('No question present')
            socketio.emit(
                'show next round 2 question',
                {
                    'q_present': False
                },
                room=faction.name,
                namespace='/'
            )
            continue
        question.asked = True
        db.session.commit()
        option_list = []
        options = Option.query.filter_by(question=question)
        for opt in options:
            option_list.append(
                {'id': opt.id, 'text': opt.text}
            )
        q = {}
        q['id'] = question.id
        q['text'] = question.text
        socketio.emit(
            'show next round 2 question',
            {'question': q, 'options': option_list, 'room': faction.name,
             'q_present': True},
            room=faction.name,
            namespace='/'
        )
        print('emitted, room: ' + faction.name)
    log = Log(message='Running show_r2_question')
    db.session.add(log)
    db.session.commit()


@celery.task()
def redirect_to_end_of_r2():
    socketio.emit('redirect to end of round 2', namespace='/')
    log = Log(message='Running redirect_to_end_of_r2')
    db.session.add(log)
    db.session.commit()


@celery.task()
def calculate_r1_scores():
    print('Running calculate_r1_scores')
    players = Player.query.all()
    pc = len(players)
    print('no. of players:', pc)
    load = {}
    for player in players:
        scores = [0.0,0.0,0.0,0.0,0.0]
        answers = Answer.query.filter_by(player=player).all()
        print('name of player:', player.name)
        print('answers:', answers)
        for answer in answers:
            option = Option.query.get(answer.option_id)
            # question = Question.query.get(option.question_id)
            scores[0] += option.weight.f1
            scores[1] += option.weight.f2
            scores[2] += option.weight.f3
            scores[3] += option.weight.f4
            scores[4] += option.weight.f5
        load[player.id] = scores
    print('load:', load)
    factions = divideIntoFactions(load)
    print(factions)
    facs = Faction.query.all()
    c = 0
    tp = 0
    # print(factions)
    # print(facs)
    for faction in factions:
        print(c)
        for pid in faction:
            player = Player.query.get(pid)
            player.allotted_faction_id = facs[c].id
            tp += 1
        c += 1
    db.session.commit()


    # integrate with the utils function
    # assuming the players' faction field is updated in the db
    socketio.emit('request for faction', namespace='/')


@celery.task()
def calculate_r2_scores():
    pass


@celery.task()
def test():
    f = Faction(name='celery test')
    db.session.add(f)
    log = Log(message='Running test')
    db.session.add(log)
    db.session.commit()
    print('Print** a test task running')
    return 'Running a celery task'