import os
import secrets
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime

import libsql_client


@dataclass
class User:
    token: str
    email: str
    last_active: datetime


async def get_user(token: str) -> User | None:
    async with _connect() as conn:
        rs = await conn.execute('select * from users where token = ?', (token,))
        if rs.rows:
            await conn.execute('update users set last_active = current_timestamp where token = ?', (token,))
            return User(*rs.rows[0])


async def create_user(email: str) -> str:
    async with _connect() as conn:
        await _delete_old_users(conn)
        token = secrets.token_hex()
        await conn.execute('insert into users (token, email) values (?, ?)', (token, email))
        return token


async def delete_user(user: User) -> None:
    async with _connect() as conn:
        await conn.execute('delete from users where token = ?', (user.token,))


async def count_users() -> int:
    async with _connect() as conn:
        await _delete_old_users(conn)
        rs = await conn.execute('select count(*) from users')
        return rs.rows[0][0]


async def create_db() -> None:
    async with _connect() as conn:
        rs = await conn.execute("select 1 from sqlite_master where type='table' and name='users'")
        if not rs.rows:
            await conn.execute(SCHEMA)


SCHEMA = """
create table if not exists thread_ids (
    thread_id varchar(255) primary key,
    timestamp_column timestamp
);
"""


async def _delete_old_users(conn: libsql_client.Client) -> None:
    await conn.execute('delete from users where last_active < datetime(current_timestamp, "-1 hour")')


@asynccontextmanager
async def _connect() -> libsql_client.Client:
    auth_token = os.getenv('SQLITE_AUTH_TOKEN')
    if auth_token:
        url = 'libsql://fastui-samuelcolvin.turso.io'
    else:
        url = 'file:users.db'
    async with libsql_client.create_client(url, auth_token=auth_token) as conn:
        yield conn


import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Thread:
    thread_id: str


async def create_thread_id(thread_id: str) -> Thread:
    async with _connect() as conn:
        try:
            existing_thread = await get_thread_id(thread_id)
            if existing_thread is None:
                await conn.execute('insert into thread_ids (thread_id) values (?)', (thread_id,))
                logger.info(f'Thread ID {thread_id} created.')
                return Thread(thread_id=thread_id)
            return existing_thread
        except Exception as e:
            logger.error(f'Error creating thread ID: {e}')
            raise


async def get_thread_id(thread_id: str) -> Thread | None:
    async with _connect() as conn:
        try:
            rs = await conn.execute(
                'select thread_id from thread_ids where thread_id = ? order by timestamp_column desc limit 1',
                (thread_id,),
            )
            if rs.rows:
                return Thread(thread_id=rs.rows[0][0])  # Create a Thread object and return it
            return None
        except Exception as e:
            logger.error(f'Error retrieving most recent thread ID: {e}')
            raise


async def create_thread_id(thread_id: str) -> Thread:
    async with _connect() as conn:
        try:
            existing_thread = await get_thread_id(thread_id)  # Pass the thread_id as an argument
            if existing_thread is None:
                await conn.execute(
                    'insert into thread_ids (thread_id, timestamp_column) values (?, ?)', (thread_id, datetime.now())
                )
                logger.info(f'Thread ID {thread_id} created.')
                return Thread(thread_id=thread_id)
            return existing_thread
        except Exception as e:
            logger.error(f'Error creating thread ID: {e}')
            raise


async def count_thread_ids() -> int:
    async with _connect() as conn:
        rs = await conn.execute('select count(*) from thread_ids')
        count = rs.rows[0][0]
        logger.info(f'Number of thread IDs in the database: {count}')
        return count


async def create_db() -> None:
    async with _connect() as conn:
        try:
            rs = await conn.execute("select 1 from sqlite_master where type='table' and name='thread_ids'")
            if not rs.rows:
                await conn.execute(SCHEMA)
                logger.info('Database tables created.')
            else:
                logger.info('Database tables already exist.')
        except Exception as e:
            logger.error(f'Error creating database tables: {e}')
            raise
