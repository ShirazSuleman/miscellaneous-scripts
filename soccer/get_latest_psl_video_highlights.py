import aiohttp
import asyncio
import json

channel_id = 'UCZH6G3Z5XINU6r92QN1l5Lw'
api_key = ''
published_after_date = '2019-09-21T16%3A00%3A00Z'
published_before_date = '2019-09-22T16%3A00%3A00Z'
search_term = 'Absa%20Premiership'

URL = 'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={}&maxResults=25&order=date&publishedAfter={}&publishedBefore={}&q={}&key={}'

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    concrete_url = URL.format(channel_id, published_after_date, published_before_date, search_term, api_key)
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        response = await fetch(session, concrete_url)
        print(response)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())