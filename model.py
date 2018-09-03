from peewee import Model, CharField, DateTimeField, ForeignKeyField
import os

from playhouse.db_url import connect

db = connect(os.environ.get('DATABASE_URL', 'sqlite:///my_database.db'))


class User(Model):
    # Inheriting from Model gives access to save(), select(), etc
    # http://docs.peewee-orm.com/en/latest/peewee/querying.html
    name = CharField(max_length=255, unique=True)
    password = CharField(max_length=255)

    class Meta:
        database = db


class Task(Model):
    # TODO: Add model fields here
    name = CharField(max_length=255)
    performed_by = ForeignKeyField(model=User, null=True)
    performed = DateTimeField(null=True)

    class Meta:
        database = db
