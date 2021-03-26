import datetime

from flask_login import UserMixin
from peewee import *
from flask_bcrypt import generate_password_hash

db = SqliteDatabase("my_journal.db")


class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    is_admin = BooleanField(default=False)
    joined_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db
        order_by = ("-joined_at",)

    @classmethod
    def create_user(cls, username, email, password, admin=False):
        try:
            with db.transaction():
                cls.create(
                    username=username,
                    email=email,
                    password=generate_password_hash(password),
                    is_admin=admin
                )
        except IntegrityError:
            raise ValueError("User already exists")


class Entry(Model):
    user = ForeignKeyField(
        model=User,
        related_name="entries"
    )
    title = CharField()
    date = DateField()
    time = IntegerField()
    i_learned = TextField()
    resources = TextField()
    published = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db
        order_by = ("-published",)


def initialize():
    db.connect()
    db.create_tables([User, Entry], safe=True)
    db.close()
