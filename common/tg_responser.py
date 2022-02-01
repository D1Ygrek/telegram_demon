import aiohttp

async def fetch(client, settings, source, message, method):
    url = f'{settings.tg_base_url}{settings.tg_token}/{method}'
    body = {
        'chat_id': source,
        'text': message
    }
    async with client.post(url, json = body) as resp:
        assert resp.status == 200
        return await resp.json()

async def fetch_sticker(client, settings, source, file_id):
    url = f'{settings.tg_base_url}{settings.tg_token}/sendSticker'
    body = {
        'chat_id': source,
        'sticker': file_id
    }
    async with client.post(url, json = body) as resp:
        assert resp.status == 200
        return await resp.json()


async def send_message(message: str, settings, chat_id):
    async with aiohttp.ClientSession() as cli:
        try:
            response = await fetch(cli, settings, chat_id, message, 'sendMessage')
            print(f'successfull delivery of message {message}; response: {response}')
        except Exception as exc:
            print(f'''Got exception trying to send message: {exc}
            with parameters: {chat_id}, {message}
            ''')

async def send_sticker(file_id: str, settings, chat_id):
    async with aiohttp.ClientSession() as cli:
        try:
            response = await fetch_sticker(cli, settings, chat_id, file_id)
            print(f'successfull delivery of message {file_id}; response: {response}')
        except Exception as exc:
            print(f'''Got exception trying to send message: {exc}
            with parameters: {chat_id}, {file_id}
            ''')
