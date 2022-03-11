import aiosqlite


async def create_database_file():
    """
    Creates db file
    """
    async with aiosqlite.connect("utils/database/discord.db") as db:
        await db.execute("""CREATE TABLE IF NOT EXISTS Presence (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            status TEXT,
            activity TEXT
        )""")

        await db.commit()
    

async def user_exists(user_id : int):
    async with aiosqlite.connect("utils/database/discord.db") as db:
        cursor = await db.execute("SELECT * FROM Presence WHERE user_id={}".format(user_id))
        data = await cursor.fetchall()

    if len(data) == 0:
        async with aiosqlite.connect("utils/database/discord.db") as db:
            await db.execute("INSERT INTO Presence (user_id) VALUES ({})".format(user_id))
            await db.commit()


async def update_status(user_id : int, status :str = "None"):
    await user_exists(user_id)

    async with aiosqlite.connect("utils/database/discord.db") as db:
        await db.execute("UPDATE Presence SET status='{}' WHERE user_id={}".format(status, user_id))
        await db.commit()


async def update_activity(user_id : int, activity : str = None):
    await user_exists(user_id)

    async with aiosqlite.connect("utils/database/discord.db") as db:
        await db.execute("UPDATE Presence SET activity='{}' WHERE user_id={}".format(activity, user_id))
        await db.commit()


async def get_db_user(user_id : int):
    async with aiosqlite.connect("utils/database/discord.db") as db:
        cur = await db.execute("SELECT * FROM Presence WHERE user_id={}".format(user_id))
        data = await cur.fetchall()

    if len(data) == 0:
        return False

    else:
        return data[0]