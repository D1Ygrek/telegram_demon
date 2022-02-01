from sqlalchemy import text
from sqlalchemy.ext.asyncio.session import AsyncSession

async def check_db_existence(session: AsyncSession):
    try:
        sql_text = text(f"""
            SELECT * from users
        """)
        result = await session.execute(sql_text)
        await session.commit()
        if result:
            return True
    except Exception as exc:
        print(f'Got exception while checking database existence: {exc}')
        return False

async def create_db_tables(session: AsyncSession):
    try:
        sql_text = text(f"""
            CREATE table users (
                id integer primary key AUTOINCREMENT,
                username text,
                tg_id integer,
                chat_id integer
            )
        """)
        await session.execute(sql_text)
        await session.commit()

        sql_text = text(f"""
            CREATE table projects (
                id integer primary key AUTOINCREMENT,
                projectname text
            )
        """)
        await session.execute(sql_text)
        await session.commit()

        sql_text = text(f"""
            CREATE table subscriptions (
                user_id integer,
                project_id integer
            )
        """)
        await session.execute(sql_text)
        await session.commit()
    except Exception as exc:
        print(f'Got exception while trying to create tables in db: {exc}')

