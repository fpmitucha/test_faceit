import asyncpg

pool = None

async def InitDb():
    global pool
    pool = await asyncpg.create_pool(
        user='postgres', 
        password='',
        database='faceit',
        host='127.0.0.1',
        port=5432
    )

    #NEED TO CHANGE CREATE POOL ARGUMENTS

    async with pool.acquire() as connection:
        await connection.execute('''
            CREATE TABLE IF NOT EXISTS user_info(
                discord_id BIGINT PRIMARY KEY,
                nickname VARCHAR(50),
                game_id TEXT NOT NULL,
                device TEXT NOT NULL,
                serial_number TEXT NOT NULL,
                elo INT DEFAULT 0,
                balance BIGINT DEFAULT 0
            )
        ''') 

async def CheckIfUserExists(discord_id):
    async with pool.acquire() as connection:
        user = await connection.fetchrow('''
            SELECT * FROM user_info WHERE discord_id = $1
        ''', discord_id)
        if user:
            return True
        return False

async def registerUser(discord_id, nickname, game_id, device, serial_number_of_device):
    if pool is None:
        raise RuntimeError("Database pool is not initialized. Call InitDb() first.")

    async with pool.acquire() as connection:

        await connection.execute('''
            INSERT INTO user_info(discord_id, nickname, game_id, device, serial_number)
            VALUES ($1, $2, $3, $4, $5)
        ''', discord_id, nickname, game_id, device, serial_number_of_device)

async def closeConnection():
    if pool:
        await pool.close()
