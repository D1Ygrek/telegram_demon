import uvicorn

from fastapi import  FastAPI, HTTPException, status
from fastapi.param_functions import Depends

from pydantic import BaseSettings

from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.asyncio import engine
from sqlalchemy.ext.asyncio.session import AsyncSession

from common.authentification_module import (
    authentificate_bot, prepare_auth, NotAuthentificated,
    check_password
    )
from common.db_init import check_db_existence, create_db_tables
from common.db_work import check_user, add_user, get_project_subscriptions
from common.message_parser import parse_message
from common.tg_responser import send_message

from annotations.tg_annotations import TGBody, BackResponse

#<-- dotenv settings class -->

class Settings(BaseSettings):
    back_token: str
    tg_token: str
    sqlite_config: str
    user_password: str
    tg_base_url: str
    class Config:
        env_file = ".env"

settings = Settings()

#<-- session creator for sqlite db -->

engine = engine.create_async_engine(settings.sqlite_config, echo=True)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


#<-- auth helper -->

not_auth_list = NotAuthentificated()

#<-- init app -->

app = FastAPI()

@app.on_event('startup')
async def startup_event():
    async with async_session() as session: 
        if not await check_db_existence(session):
            await create_db_tables(session)


@app.get('/telegram_demon')
async def main_try():
    return {'ok'}

@app.post('/telegram_demon/tg/{bot_id}')
async def bot_webhook(
    tg_body: TGBody,
    bot_id: str,
    session: AsyncSession = Depends(get_session)
    ):

    if not authentificate_bot(bot_id, settings.tg_token):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = 'wrong bot id'
        )

    user = tg_body.message.from_
    chat_id = tg_body.message.chat['id']
    message_text = tg_body.message.text

    print(tg_body)

    if user:
        if not await check_user(session, user):
            if not not_auth_list.check_existance(user['id']):
                await prepare_auth(settings, chat_id)
            else:
                if await check_password(settings, chat_id, message_text):
                    not_auth_list.remove_not_auth(user['id'])
                    await add_user(session, user, chat_id)
        else:
            if message_text:
                await parse_message(message_text, chat_id, session, settings, user)

@app.post('/telegram_demon/wh-u/{token}')
async def alarm_for_users(
    back: BackResponse,
    token: str,
    session: AsyncSession = Depends(get_session) 
    ):
    if token==settings.back_token:
        subs = await get_project_subscriptions(session, back.project)
        message = f"""Проект: {back.project}
Версия: {back.v}
Состояние: {back.message}"""
        for sub in subs:
            await send_message(message, settings, sub)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7777, reload = False)