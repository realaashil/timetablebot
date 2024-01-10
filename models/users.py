from peewee import BooleanField, CharField, IntegerField, Model, SqliteDatabase

db = SqliteDatabase("users.db")


class Users(Model):
    user_id = IntegerField(unique=True)
    username = CharField(default=None, null=True)
    first_name = CharField(default=None, null=True)
    last_name = CharField(default=None, null=True)
    mess_noti = BooleanField(default=True)

    class Meta:
        database = db
