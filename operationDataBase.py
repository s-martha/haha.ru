import dataBase as db
from dataBase import Base, session_factory


def insert_data():
    pelmen = db.Users(username = "IIeJIbMeHb", login = "IIeJIbMeHb2005", password_hash = 14522)
    nagibator = db.Users(username = "Nagibator3000", login = "NagibatorDA", password_hash = 202305)
    with session_factory() as session:
        session.add(pelmen)
        session.add(nagibator)
        session.commit()
        print("Been added user:",pelmen.username, "with id:",  pelmen.id)
        print("Been added user:",nagibator.username, "with id:",  nagibator.id)

def print_data(table):
    with session_factory() as session:
        for i in session.query(table).all():
            print("id:", i.id)
        


insert_data()
print_data(db.Users)


