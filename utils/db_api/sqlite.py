import aiosqlite
"""Module for interacting with SQLite database asynchronously using aiosqlite."""

class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return aiosqlite.connect(self.path_to_db)

    async def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        async with self.connection as connection:
            cursor = await connection.cursor()
            data = None
            await cursor.execute(sql, parameters)

            if commit:
                await connection.commit()
            if fetchall:
                data = await cursor.fetchall()
            if fetchone:
                data = await cursor.fetchone()
            return data

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER NOT NULL UNIQUE,
            full_name TEXT,
            is_access BOOLEAN DEFAULT FALSE
        );
        """
        await self.execute(sql, commit=True)

    async def add_user(self, telegram_id: int, full_name: str):
        sql = """
        INSERT OR IGNORE INTO Users(telegram_id, full_name, is_access) VALUES(?, ?, False)
        """
        await self.execute(sql, parameters=(telegram_id, full_name), commit=True)

    async def select_user(self, telegram_id: int):
        sql = "SELECT * FROM Users WHERE telegram_id = ?"
        return await self.execute(sql, parameters=(telegram_id,), fetchone=True)

    async def count_users(self):
        return await self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    async def update_user_access(self, telegram_id: int, is_access: bool):
        sql = "UPDATE Users SET is_access = ? WHERE telegram_id = ?"
        await self.execute(sql, parameters=(is_access, telegram_id), commit=True)
        
    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetchall=True)

    async def delete_user(self, telegram_id: int):
        sql = "DELETE FROM Users WHERE telegram_id = ?"
        await self.execute(sql, parameters=(telegram_id,), commit=True)
