import asyncio

import aiohttp
from bs4 import BeautifulSoup


class Client:
    default_headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
    }

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self._session = aiohttp.ClientSession(headers=self.default_headers)
        self._csrftoken = ''

    async def login(self):
        headers = {
            'authority': 'ankiweb.net',
            'origin': 'https://ankiweb.net',
            'content-type': 'application/x-www-form-urlencoded',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'referer': 'https://ankiweb.net/account/login',
            'accept-language': 'en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7',
            'cookie': 'ankiweb=login',
        }

        data = {
            'submitted': '1',
            'csrf_token': await self._get_csrftoken(),
            'username': self.username,
            'password': self.password
        }

        response = await self._session.post('https://ankiweb.net/account/login', headers=headers, data=data)
        response.raise_for_status()
        body = await response.content.read()

        assert 'Create Deck' in body.decode(), 'Failed to login: ' + body.decode()

    async def get_decks(self):
        response = await self._session.get('https://ankiweb.net/decks')
        response.raise_for_status()

        body = await response.content.read()
        body

    async def _get_csrftoken(self):
        if not self._csrftoken:
            response = await self._session.get('https://ankiweb.net/account/login')
            response.raise_for_status()
            body = await response.read()
            soup = BeautifulSoup(body.decode(), 'html.parser')
            self._csrftoken = soup.find('input', {'name': 'csrf_token'}).get('value')

        return self._csrftoken


async def main():
    client = Client('fenchel.fen@gmail.com', 'duh')
    try:
        await client.login()
        # await client.get_decks()
    except Exception as e:
        await client._session.close()
        raise e

    await client._session.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
