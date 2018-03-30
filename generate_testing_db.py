from app import db
from app.models import Question, Option, Weight, Faction

Question.query.delete()
Option.query.delete()
Weight.query.delete()

for i in range(10):
    q = Question(text='Question no. %d' % (i + 1), for_first_round=True, duration=40)
    db.session.add(q)
db.session.commit()
factions = Faction.query.all()
for faction in factions:
    c = 0
    for i in range(15):
        q = Question(
            text='%s q.no. %d' % (faction.name, (c + 1)),
            for_first_round=False, duration=20,
            faction_id=faction.id
        )
        db.session.add(q)
        c += 1
db.session.commit()

questions = Question.query.all()
for question in questions:
    c = 0
    for i in range(4):
        o = Option(question=question, text='option no. %d' % c)
        db.session.add(o)
        c += 1
db.session.commit()

options = Option.query.join(Question).filter(Question.for_first_round == True)
c = 0
for option in options:
    if c % 4 == 0:
        w = Weight(option=option, f1=60, f2=20, f3=10, f4=0, f5=0)
    elif c % 4 == 1:
        w = Weight(option=option, f1=0, f2=70, f3=0, f4=50, f5=20)
    elif c % 4 == 2:
        w = Weight(option=option, f1=20, f2=10, f3=70, f4=20, f5=40)
    elif c % 4 == 3:
        w = Weight(option=option, f1=20, f2=0, f3=20, f4=30, f5=60)
    db.session.add(w)
    c += 1
db.session.commit()

c = 0
for faction in Faction.query.all():
    options = Option.query.join(
        Question).filter(Question.faction_id==faction.id).all()
    print(options)
    for option in options:
        wts = {}
        for i in range(5):
            wts['f%d' % (i+1)] = 0
        wts['f%d' % (c+1)] = 1
        wts['option_id'] = option.id
        w = Weight(**wts)
        db.session.add(w)
    c += 1
db.session.commit()