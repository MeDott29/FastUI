async def create_thread_id(thread_id: str) -> None:
    async with _connect() as conn:
        await conn.execute('insert into thread_ids (thread_id) values (?)', (thread_id,))


async def get_thread_id(thread_id: str) -> str | None:
    async with _connect() as conn:
        rs = await conn.execute('select thread_id from thread_ids where thread_id = ?', (thread_id,))
        if rs.rows:
            return rs.rows[0][0]
        return None


async def update_thread_id(old_thread_id: str, new_thread_id: str) -> None:
    async with _connect() as conn:
        await conn.execute('update thread_ids set thread_id = ? where thread_id = ?', (new_thread_id, old_thread_id))


async def delete_thread_id(thread_id: str) -> None:
    async with _connect() as conn:
        await conn.execute('delete from thread_ids where thread_id = ?', (thread_id,))
