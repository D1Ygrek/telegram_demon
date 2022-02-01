from sqlalchemy import text
from sqlalchemy.ext.asyncio.session import AsyncSession


async def check_user(session: AsyncSession, user: dict):
    try:
        sql_text = text(f"""
            SELECT * from users where tg_id = {user['id']}
        """)
        result = await session.execute(sql_text)
        await session.commit()
        if result.one():
            return True
    except Exception as exc:
        print(f'Got exception while trying to check user: {exc}')
        return False

async def add_user(session: AsyncSession, user: dict, chat_id: int):
    try:
        username = user['username']
        tg_id = user['id']

        sql_text = text(f"""
            INSERT into users (username, tg_id, chat_id) values ('{username}', {tg_id}, {chat_id})
        """)
        await session.execute(sql_text)
        await session.commit()
    except Exception as exc:
        print(f'Got exception while trying to insert user: {exc}')

async def get_repos(session: AsyncSession):
    try:
        sql_text = text(f"""
            SELECT * FROM projects 
        """)
        result = await session.execute(sql_text)
        await session.commit()
        return result.all()
    except Exception as exc:
        print(f'Got exception while trying to get repos: {exc}')

async def get_user_id(session: AsyncSession, tg_id: int):
    try:
        sql_text = text(f"""
            SELECT id from users where tg_id = {tg_id}
        """)
        result = await session.execute(sql_text)
        await session.commit()
        return result.one()
    except Exception as exc:
        print(f'Got exception while trying to get user_id ny tg_id: {exc}')

async def check_subs(session: AsyncSession, user_id: int):
    try:
        sql_text = text(f"""
            SELECT u.username, p.projectname, p.id
                from subscriptions s
                    join projects p on p.id = s.project_id
                    join users u on u.id = s.user_id
                where s.user_id = {user_id}
        """)
        result = await session.execute(sql_text)
        await session.commit()
        return result.all()
    except Exception as exc:
        print(f'Got exception while trying to get subs: {exc}')

async def check_repo_exist(session: AsyncSession, repo_id: int):
    try:
        sql_text = text(f"""
            SELECT * from projects WHERE id = {repo_id}
        """)
        result = await session.execute(sql_text)
        await session.commit()
        if result.one():
            return True
    except Exception as exc:
        print(f'Got exception while trying to check repo: {exc}')
        return False

async def create_sub(session: AsyncSession, user_id:int, repo_id: int):
    try:
        sql_text = text(f"""
                INSERT INTO subscriptions values ({user_id}, {repo_id})
            """)
        await session.execute(sql_text)
        await session.commit()
    except Exception as exc:
        print(f'Got exception while trying to create subscription: {exc}')

async def delete_sub(session: AsyncSession, user_id: int, repo_id: int):
    try:
        sql_text = text(f"""
            DELETE FROM subscriptions where user_id = {user_id} and project_id = {repo_id}
        """)
        await session.execute(sql_text)
        await session.commit()
    except Exception as exc:
        print(f'Got exception while trying to remove subscription: {exc}')

async def get_project_subscriptions(session: AsyncSession, project_name: str):
    try:
        sql_text = text(f"""
            SELECT id FROM projects WHERE projectname = '{project_name}'
        """)
        res = await session.execute(sql_text)
        proj_id = res.one().id
        sql_text = text(f"""
            SELECT user_id FROM subscriptions WHERE project_id = {proj_id}
        """)
        res = await session.execute(sql_text)
        subscribers = res.all()
        db_resp = []
        for sub in subscribers:
            sql_text = text(f"""
                SELECT chat_id FROM users WHERE id = {sub.user_id}
            """)
            res = await session.execute(sql_text)
            user_chat = res.one().chat_id
            db_resp.append(user_chat)
        await session.commit()
        return db_resp
    except Exception as exc:
        print(f'Got exception while trying to get project subs: {exc}')

    
    
