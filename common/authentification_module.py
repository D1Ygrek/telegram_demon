from .tg_responser import send_message

class NotAuthentificated():

    __user_ids = set()
    
    def __init__(self) -> None:
        pass

    def __add_not_auth(self, uid: int):
        self.__user_ids.add(uid)

    def remove_not_auth(self, uid:int):
        self.__user_ids.remove(uid)

    def check_existance(self, uid: int):
        if uid not in self.__user_ids:
            self.__add_not_auth(uid)
            return False
        return True


def authentificate_bot(incoming_id, saved_id):
    return incoming_id == saved_id

async def prepare_auth(settings, source):
    hello_text = 'Здравствуйте. Похоже, мы не знакомы. Введите пароль для продолжения'
    await send_message(hello_text, settings, source)

async def check_password(settings, source, password):
    if settings.user_password == password:
        success_message = """
        Пароли совпадлают! Мои команды:
        /get_repos - просмотр всех доступных репозиториев
        /sub_repo_id - подписка на уведомления по репозиторию
        /unsub_repo_id - отписаться от уведомлений
        /my_repos - список репозиториев, на обновления которых вы подписаны
        /help - вывести этот список ещё раз
        """
        await send_message(success_message, settings, source)
        return True
    else:
        await send_message("Ваш пароль неверен.", settings, source)
        return False
