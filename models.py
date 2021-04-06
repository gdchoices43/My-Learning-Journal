import datetime

from peewee import *


db = SqliteDatabase("myjournal.db")


class Entry(Model):
    title = CharField()
    date = DateField(default=datetime.datetime.now)
    time = IntegerField()
    i_learned = TextField()
    resources = TextField()

    class Meta:
        database = db
        order_by = ("-timestamp",)


def initialize():
    db.connect()
    db.create_tables([Entry], safe=True)
    db.close()
