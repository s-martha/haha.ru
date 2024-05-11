from sqlalchemy import select
import dataBase.models as db

async def insert_data(session_factory):
    pelmen = db.User(username = "IIeJIbMeHb", login = "IIeJIbMeHb2005", password_hash = 14522)
    nagibator = db.User(username = "Nagibator3000", login = "NagibatorDA", password_hash = 202305)
    async with session_factory() as session:
        session.add_all([pelmen,nagibator])
        print("Been added user:",pelmen.username, "with id:",  pelmen.id)
        print("Been added user:",nagibator.username, "with id:",  nagibator.id)
        await session.commit()

async def create_role(session_factory):
    user = db.Role(role_name = "user")
    admin = db.Role(role_name = "admin")
    TheArabSheikh = db.Role(role_name = "The Arab sheikh")

    async with session_factory() as session:
        session.add_all([user, admin, TheArabSheikh])
        await session.commit()


async def erase_data(session_factory, table): 
    async with session_factory() as session:
        res_ = await session.execute(select(table))
        for i in res_.scalars().all():
            await session.delete(i)
        await session.commit()

async def print_data(session_factory, table):
    async with session_factory() as session:
        res1_ = await session.execute(select(table))

        for i in res1_.scalars().all():
            print("id:", i.id)
        


# insert_data()
# print_data(db.Users),


