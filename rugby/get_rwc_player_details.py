import re
import csv
import aiohttp
import asyncio
import requests
from bs4 import BeautifulSoup

CSV_FILE_NAME = 'rwc_players.csv'

async def get_soup(session, url):
    async with session.get(url) as response:
        html = await response.text()
        return BeautifulSoup(html, 'lxml')

async def get_players(url):
    players = []

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        soup = await get_soup(session, url)

    tables = soup.find_all('table', class_="sortable wikitable")

    for table in tables:
        rows = table.find_all('tr', class_="vcard agent")
        for row in rows:
            attrs = row.select('td span.fn > a')[0].attrs
            player = { 'url': 'https://en.m.wikipedia.org' + attrs['href'], 'name': attrs['title']}
            players.append(player)

    return players

async def get_player_location(session, player_url):
    player_location = ''

    soup = await get_soup(session, player_url)

    table = soup.find('table', class_='infobox vcard')

    location_elements = table.find('th', text = re.compile('place.*birth', re.IGNORECASE)).next_sibling()

    for element in location_elements:
        player_location = player_location + (element.get_text() + ', ')

    return player_location[0:-2]

def create_csv_file():
    with open(CSV_FILE_NAME, mode='w') as rwc_players_file:
        writer = csv.writer(rwc_players_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Name', 'URL', 'Born'])

def add_csv_row(player):
    with open(CSV_FILE_NAME, mode='a') as rwc_players_file:
        writer = csv.writer(rwc_players_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([player['name'], player['url'], player['born']])

async def process_player(session, player):
    try:
        player['born'] = await get_player_location(session, player['url'])
    except Exception as e:
        print(e)
        player['born'] = ''
    finally:
        add_csv_row(player)

async def main():
    url = 'https://en.m.wikipedia.org/wiki/2019_Rugby_World_Cup_squads'

    create_csv_file()

    players = await get_players(url)

    for player in players:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            await asyncio.gather(*(process_player(session, p) for p in players))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())