from peewee import SqliteDatabase

from models.users import Users


class Database:
    def __init__(self, db):
        self.db = db

    def add_user(self, user):
        if Users.select().where(Users.user_id == user.id).exists():
            return
        Users.create(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            mess_noti=False,
        )

    def list_all_user_id_mess(self):
        return Users.select(Users.user_id).where(Users.mess_noti == True)

    def remove_mess(self, user_id):
        Users.update(mess_noti=False).where(Users.user_id == user_id).execute()

    def add_mess(self, user_id):
        Users.update(mess_noti=True).where(Users.user_id == user_id).execute()

    def get_mess(self, user_id):
        return Users.get(Users.user_id == user_id).mess_noti


db = SqliteDatabase("users.db")
db = Database(db)
