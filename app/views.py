import json
import time
from datetime import timedelta, datetime
from flask import render_template, request, session, redirect, url_for
from flask_socketio import emit, join_room
from app import app, socketio, db, celery
from .models import Player, Schedule, Question, Answer, Option, Faction, Weight
from .schedule import (
    start_video, stop_video, redirect_to_r1, show_next_question,
    redirect_to_end_of_r1, redirect_to_r2, show_r2_question,
    redirect_to_end_of_r2, calculate_r1_scores, test,
    calculate_r2_scores
)


@app.route('/')
def index():
    if 'email' not in session:
        return redirect(url_for('login'))
    schedule = Schedule.query.filter_by(active=True).first()
    seconds = (schedule.start_time - datetime.now()).total_seconds()
    print(seconds)
    return render_template(
        'intro2.html', player=Player.query.filter_by(email=session['email']).first(),
        seconds=seconds
    )


@app.route('/video_page')
def video_page():
    if 'email' not in session:
        return redirect(url_for('login'))
    return render_template('video.html')


@app.route('/round1')
def round1():
    if 'email' not in session:
        return redirect(url_for('login'))

    player = Player.query.filter_by(email=session['email']).first()
    # question = Question.query.filter_by(for_first_round=True, asked=False).first()
    # question.asked = True
    # db.session.commit()
    # options = Option.query.filter_by(question=question)
    return render_template('questions3.2.html', player=player,
                           )
    # return render_template('round1_questions.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('Index.html')
    em = request.form.get('email', False)
    if not em:
        return "<h1>Email address not entered</h1>"
    nm = request.form.get('name', False)
    if not nm:
        return "<h1>Name not entered</h1>"
    ph = request.form.get('phone', False)
    if not ph:
        return "<h1>Phone number not entered</h1>"
    player = Player.query.filter_by(email=em).first()
    if player:
        session['email'] = request.form['email']
        return redirect(url_for('index'))
    avatar_id = request.form.get('avatar_id', '1')
    if not avatar_id:
        return "<h1>Avatar not selected</h1>"
    player = Player(
        name=request.form['name'],
        phone=request.form['phone'],
        email=request.form['email'],
        avatar_id=avatar_id
    )
    db.session.add(player)
    db.session.commit()
    session['email'] = request.form['email']
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))


@app.route('/conf/refresh_schedule/')
def refresh_schedule():
    schedule = Schedule.query.filter_by(active=True).first()
    if not schedule:
        return "No active schedule found!"
    Schedule.query.filter(Schedule.id != schedule.id).update({'active':False})
    # remove older tasks from queue
    # celery.control.purge()
    c = schedule.start_time
    c = c - timedelta(hours=5, minutes=30)
    start_video.apply_async(eta=c)
    c = c + timedelta(seconds=schedule.video_length)
    stop_video.apply_async(eta=c)
    c = c + timedelta(seconds=schedule.after_video_pause)
    redirect_to_r1.apply_async(eta=c)
    c = c + timedelta(seconds=1)
    show_next_question.apply_async(eta=c)
    questions = Question.query.filter_by(for_first_round=True)
    for q in questions:
        c = c + timedelta(seconds=q.duration)
        show_next_question.apply_async(eta=c)
    c = c + timedelta(seconds=1)
    calculate_r1_scores.apply_async(eta=c)
    c = c + timedelta(seconds=3)
    redirect_to_end_of_r1.apply_async(eta=c)
    c = c + timedelta(seconds=schedule.after_r1_pause)
    redirect_to_r2.apply_async(eta=c)
    c = c + timedelta(seconds=1)
    show_r2_question.apply_async(eta=c)
    questions = Question.query.filter_by(for_first_round=False)
    for q in range(15):  # no. of 2nd round questions per faction
        c = c + timedelta(seconds=60)  # time per 2nd round questions
        show_r2_question.apply_async(eta=c)
    c = c + timedelta(seconds=1)
    calculate_r2_scores.apply_async(eta=c)
    c = c + timedelta(seconds=120)
    redirect_to_end_of_r2.apply_async(eta=c)
    return "Schedule reconfigured and activated."


@app.route('/question_response/', methods=['POST'])
def question_response():
    # if 'email' not in session:
    #     return redirect(url_for('login'))
    data = request.get_json(force=True)
    player = Player.query.filter_by(email=data['email']).first()
    round = data['round']
    # print(data['round'])
    # # print(data['room'])
    # print(data['question_id'])
    # print(data.get('option_id', None))
    faction = ''
    if round == 1:
        questions = Question.query.filter_by(for_first_round=True).all()
    else:
        faction = Faction.query.filter_by(name=data['room']).first()
        questions = Question.query.filter_by(for_first_round=False,
                                             faction=faction).all()
    # question = questions.offset(
    #     data['question_id']
    # ).limit(1).first()
    question = questions[int(data['question_id'])]
    opt = data.get('option_id', False)
    if opt:
        option = Option.query.filter_by(question=question)
        option = option[int(opt)-1]
    else:
        option = None
    resp = Answer(
        player_id=player.id,
        option=option,
        answered_at=datetime.now()
    )
    db.session.add(resp)

    if round == 2:
        faction = option.question.faction
        weight = Weight.query.filter_by(option=option).first()
        if faction.id == 1:
            score = weight.f1
        elif faction.id == 2:
            score = weight.f2
        elif faction.id == 3:
            score = weight.f3
        elif faction.id == 4:
            score = weight.f4
        elif faction.id == 5:
            score = weight.f5
        player.r2_score += score

    db.session.commit()
    return json.dumps({'success': True})


@app.route('/instructions')
def instructions():
    return render_template('instructions.html')


@app.route('/display_r1_results/<email>')
def r1_results(email):
    player = Player.query.filter_by(email=email).first()
    return render_template('r1_results.html', player=player,
                           faction=player.faction.name)


@app.route('/round2')
def round2():
    if 'email' not in session:
        return redirect(url_for('login'))
    player = Player.query.filter_by(email=session['email']).first()
    room = player.faction.name
    return render_template('round2_questions.html', room=room, player=player)


@app.route('/display_r2_results/<email>')
def r2_results(email):
    player = Player.query.filter_by(email=email).first()
    '''
    winners = []
    for faction in Faction.query.all():
        winner = Player.query.filter_by(faction=faction).order_by(
            Player.r2_score.desc()
        ).first()
        winners.append(winner)
    print(winners)
    '''
    f = Faction.query.first()
    winner = Player.query.filter_by(faction=f).order_by(
        Player.r2_score.desc()
    ).first()
    factions = Faction.query.all()
    for faction in factions:
        wn = Player.query.filter_by(faction=faction).order_by(
            Player.r2_score.desc()
            ).first()
        if wn.r2_score > winner.r2_score:
            winner = wn



    if winner.id == player.id:
        message = 'WON!!'
        return render_template('r2_results.html', player=player, message=message)
    else:
        message = 'lost'
        return render_template('losers_page.html')



@socketio.on('connected', namespace='/')
def on_connect():
    # print('Connected TO client')
    # join_room('all')
    # emit('test event', {'data': 'Hello!'})
    # time.sleep(5)
    # socketio.emit('start video', {'snippet': 'video code blah'}, namespace='/')
    # start_video.delay()
    pass


@socketio.on('client message')
def onmsg(msg):
    print(msg)
    print(msg['data'])
    emit('my message', {'data': 'Hello from the trrrr'})


@socketio.on('allot faction')
def allot_faction(message):
    email = message['email']
    player = Player.query.filter_by(email=email).first()
    join_room(player.faction.name)
    print('player joined ROOM:', player.faction.name)

'''
@socketio.on('display r1 results')
def display_r1_results(message):
    room = message['room']
    emit('r1 results', {})
'''