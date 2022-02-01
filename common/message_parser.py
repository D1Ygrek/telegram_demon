import random

from sqlalchemy.ext.asyncio.session import AsyncSession

from .db_work import get_repos, get_user_id, check_subs, check_repo_exist, create_sub, delete_sub
from .tg_responser import send_message, send_sticker

help_stickers = ['CAACAgUAAxkBAANqYfhoVLXXwTDX2gGSe08xfcHk3lQAAmoAA6fjtQx49Z0wZBUnsSME','CAACAgUAAxkBAANnYfhoNbScj4jrs1lMD7Korcw6H8wAAq8AA6fjtQxPb2WHlKc6ziME','CAACAgUAAxkBAANmYfhnj2794__VrjgR8HWZjg1TxWkAAkIAA6fjtQznohOtSK9n5CME']
sad_sticker = 'CAACAgEAAxkBAAPKYfh4qEYO_6NPInO2LXk53Y4xk0sAAjsDAAJdeJlHVtRZ-p3GxbkjBA'

async def parse_message(message: str, source, session: AsyncSession, settings, user):
    tg_id = user['id']
    if message[0] == '/':
        if message == '/get_repos':
            result = await get_repos(session)
            response = "все текущие репозитории:"
            for repo in result:
                response = f"""{response}
                /sub_repo_{repo.id} {repo.projectname}"""
            await send_message(response, settings, source)
        elif message == '/help':
            response = """
            Мои команды:
        /get_repos - просмотр всех доступных репозиториев
        /sub_repo_id - подписка на уведомления по репозиторию
        /unsub_repo_id - отписаться от уведомлений
        /my_repos - список репозиториев, на обновления которых вы подписаны
        /help - вывести этот список ещё раз
            """
            await send_message(response, settings, source)
            now_sticker = random.randint(0,2)
            await send_sticker(help_stickers[now_sticker], settings, source)
        elif message == '/my_repos':
            user_id = await get_user_id(session, tg_id)
            user_id = user_id.id
            subs = await check_subs(session, user_id)
            response = "Ваши репозитории:"
            for sub in subs:
                response = f"""{response}
        /unsub_repo_{sub.id}  {sub.projectname}  {sub.username}"""
            await send_message(response, settings, source)

        else:
            message_hard = message.split('_')
            if len(message_hard) == 3 and message_hard[1] == 'repo':
                if message_hard[0] == '/sub':
                    repo_id = message_hard[2]
                    user_id = await get_user_id(session, tg_id)
                    user_id = user_id.id
                    subs = await check_subs(session, user_id)
                    check = False
                    for subscr in subs:
                        if repo_id == str(subscr.id):
                            check = True
                    if check:
                        response = "У вас уже есть подписка на этот репозиторий"
                    else:
                        if await check_repo_exist(session, repo_id):
                            await create_sub(session, user_id, repo_id)
                            response = "Подписка создана"
                        else:
                            response = "Такой репозиторий не обнаружен"
                    await send_message(response, settings, source)
                elif message_hard[0] == '/unsub':
                    repo_id = message_hard[2]
                    user_id = await get_user_id(session, tg_id)
                    user_id = user_id.id
                    subs = await check_subs(session, user_id)
                    check = False
                    for subscr in subs:
                        if repo_id == str(subscr.id):
                            check = True
                    if check:
                        await delete_sub(session, user_id, repo_id)
                        response = "Подписка удалена"
                    else:
                        response = "Среди ваших подписок нет нужной"
                    
                    await send_message(response, settings, source)
                else:
                    await send_message('Я не знаю что вы от меня хотите (', settings, source)
                    await send_sticker(sad_sticker, settings, source)
            else:
                await send_message('Я не знаю что вы от меня хотите (', settings, source)
                await send_sticker(sad_sticker, settings, source)
    else:
        await send_message('Я не знаю что вы от меня хотите (', settings, source)
        await send_sticker(sad_sticker, settings, source)


                    




        
        

