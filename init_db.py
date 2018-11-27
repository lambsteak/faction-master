from sqlalchemy import Table, Column, Integer, ForeignKey, String, Float, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import datetime

engine = create_engine('sqlite:///db.sqlite3', echo=True)
Base = declarative_base()


class Faction(Base):
	__tablename__ = 'faction'
	id = Column(Integer, primary_key=True)
	name = Column(String(100), nullable=False, unique=True)
	questions = relationship('Question', backref='faction')
	avatars = relationship('Avatar', backref='faction')
	players = relationship('Player', backref='faction')

	def __str__(self):
		return self.name


class Avatar(Base):
	__tablename__ = 'avatar'
	id = Column(Integer, primary_key=True)
	url = Column(String(400), nullable=False)
	faction_id = Column(Integer, ForeignKey('faction.id'), nullable=False)
	category = Column(String(20), default='NORMAL')
	players = relationship('Player', backref='avatar')


class Player(Base):
	__tablename__ = 'player'
	id = Column(Integer, primary_key=True)
	name = Column(String(50), nullable=False)
	email = Column(String(120), nullable=False, unique=True)
	phone = Column(String(18), nullable=False)
	avatar_id = Column(Integer, ForeignKey('avatar.id'), nullable=False)
	answers = relationship('Answer', backref='player')
	allotted_faction_id = Column(Integer, ForeignKey('faction.id'),
								   nullable=True)
	r2_score = Column(Float, default=0.0)

	def __str__(self):
		return self.name


class Question(Base):
	__tablename__ = 'question'
	id = Column(Integer, primary_key = True)
	text = Column(Text, nullable=False)
	for_first_round = Column(Boolean, nullable=False)
	faction_id = Column(Integer, ForeignKey('faction.id'), nullable=True)
	options = relationship('Option', backref='question')
	duration = Column(Integer, default=60)
	asked = Column(Boolean, default=False)

	def __str__(self):
		return self.text[:100]


class Option(Base):
	__tablename__ = 'option'
	id = Column(Integer, primary_key=True)
	question_id = Column(Integer, ForeignKey('question.id'), nullable=False)
	text = Column(String(600), nullable=False)
	weight = relationship('Weight', backref='option', uselist=False)
	chosen_answers = relationship('Answer', backref='option')

	def __str__(self):
		return str(self.id) + ': ' + self.text[:100]


class Weight(Base):
	__tablename__ = 'weight'
	id = Column(Integer, primary_key=True)
	option_id = Column(Integer, ForeignKey('option.id'), nullable=False)
	f1 = Column(Float, nullable=True)
	f2 = Column(Float, nullable=True)
	f3 = Column(Float, nullable=True)
	f4 = Column(Float, nullable=True)
	f5 = Column(Float, nullable=True)

	def __str__(self):
		return str(self.option_id)


class Answer(Base):
	__tablename__ = 'answer'
	id = Column(Integer, primary_key=True)
	player_id = Column(Integer, ForeignKey('player.id'), nullable=False)
	option_id = Column(Integer, ForeignKey('option.id'), nullable=False)
	answered_at = Column(DateTime, nullable=False)

	def __str__(self):
		return str(self.option_id)


class Schedule(Base):
	__tablename__ = 'schedule'
	id = Column(Integer, primary_key=True)
	label = Column(String(25), default='Demo')
	start_time = Column(DateTime, nullable=False)
	video_length = Column(Integer, nullable=False)
	after_video_pause = Column(Integer, default=60)
	after_r1_pause = Column(Integer, default=60)
	active = Column(Boolean, default=True)
	event_paused = Column(Boolean, default=False)

	def __str__(self):
		return self.label


class Task(Base):
	__tablename__ = 'task'
	id = Column(Integer, primary_key=True)
	start_video_id = Column(String(200))
	stop_video_id = Column(String(200))
	redirect_1_id = Column(String(200))

	def __repr__(self):
		return self.id


class Log(Base):
	__tablename__ = 'log'
	id = Column(Integer, primary_key=True)
	message = Column(String(200), nullable=False)
	time = Column(DateTime, default=datetime.datetime.now)
	detail = Column(Text)

	def __repr__(self):
		return self.message


class Asset(Base):
	__tablename__ = 'asset'
	id = Column(Integer, primary_key=True)
	key = Column(String(50), nullable=False)
	value = Column(Text)

	def __repr__(self):
		return self.key


Base.metadata.create_all(engine)
