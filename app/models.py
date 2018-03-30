import datetime
from app import db


class Faction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    questions = db.relationship('Question', backref='faction')
    avatars = db.relationship('Avatar', backref='faction')
    players = db.relationship('Player', backref='faction')

    def __str__(self):
        return self.name


class Avatar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(400), nullable=False)
    faction_id = db.Column(db.Integer, db.ForeignKey('faction.id'), nullable=False)
    category = db.Column(db.String(20), default='NORMAL')
    players = db.relationship('Player', backref='avatar')


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone = db.Column(db.String(18), nullable=False)
    avatar_id = db.Column(db.Integer, db.ForeignKey('avatar.id'), nullable=False)
    answers = db.relationship('Answer', backref='player')
    allotted_faction_id = db.Column(db.Integer, db.ForeignKey('faction.id'),
                                   nullable=True)
    r2_score = db.Column(db.Float, default=0.0)

    def __str__(self):
        return self.name


class Question(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.Text, nullable=False)
    for_first_round = db.Column(db.Boolean, nullable=False)
    faction_id = db.Column(db.Integer, db.ForeignKey('faction.id'), nullable=True)
    options = db.relationship('Option', backref='question')
    duration = db.Column(db.Integer, default=60)
    asked = db.Column(db.Boolean, default=False)

    def __str__(self):
        return self.text[:100]


class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    text = db.Column(db.String(600), nullable=False)
    weight = db.relationship('Weight', backref='option', uselist=False)
    chosen_answers = db.relationship('Answer', backref='option')

    def __str__(self):
        return str(self.id) + ': ' + self.text[:100]


class Weight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    option_id = db.Column(db.Integer, db.ForeignKey('option.id'), nullable=False)
    f1 = db.Column(db.Float, nullable=True)
    f2 = db.Column(db.Float, nullable=True)
    f3 = db.Column(db.Float, nullable=True)
    f4 = db.Column(db.Float, nullable=True)
    f5 = db.Column(db.Float, nullable=True)

    def __str__(self):
        return str(self.option_id)


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    option_id = db.Column(db.Integer, db.ForeignKey('option.id'), nullable=False)
    answered_at = db.Column(db.DateTime, nullable=False)

    def __str__(self):
        return str(self.option_id)


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(25), default='Demo')
    start_time = db.Column(db.DateTime, nullable=False)
    video_length = db.Column(db.Integer, nullable=False)
    after_video_pause = db.Column(db.Integer, default=60)
    after_r1_pause = db.Column(db.Integer, default=60)
    active = db.Column(db.Boolean, default=True)
    event_paused = db.Column(db.Boolean, default=False)

    def __str__(self):
        return self.label


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_video_id = db.Column(db.String(200))
    stop_video_id = db.Column(db.String(200))
    redirect_1_id = db.Column(db.String(200))

    def __repr__(self):
        return self.id


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(200), nullable=False)
    time = db.Column(db.DateTime, default=datetime.datetime.now)
    detail = db.Column(db.Text)

    def __repr__(self):
        return self.message


class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), nullable=False)
    value = db.Column(db.Text)

    def __repr__(self):
        return self.key


