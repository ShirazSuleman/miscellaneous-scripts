import re
import csv
import aiohttp
import asyncio
import requests
from bs4 import BeautifulSoup
import os

CSV_FILE_NAME = 'rwc_players.csv'

async def get_soup(session, url):
    async with session.get(url) as response:
        html = await response.text()
        return BeautifulSoup(html, 'lxml')

async def get_players(url):
    players = []

    async with aiohttp.ClientSession() as session:
        soup = await get_soup(session, url)

    tables = soup.find_all('table', class_="sortable wikitable")

    for table in tables:
        team = table.parent.parent.parent.parent.find_previous_sibling('h3').find('span', class_='mw-headline').get_text()
        rows = table.find_all('tr', class_="vcard agent")
        for row in rows:
            attrs = row.select('td span.fn > a')[0].attrs
            if 'Captain (sports)' not in attrs['title']:
                player = { 'url': 'https://en.m.wikipedia.org' + attrs['href'], 'name': attrs['title'], 'team': team}
                players.append(player)

    return players

async def get_player_location(session, player_url):
    player_location = ''

    soup = await get_soup(session, player_url)

    table = soup.find('table', class_='infobox vcard')

    location_elements = table.find('th', text = re.compile('place.*birth', re.IGNORECASE)).next_sibling

    for element in location_elements:
        try:
            player_location = player_location + (element.get_text() + ', ')
        except Exception as e:
            print(e)

    return player_location[0:-2]

def new_csv_file():
    with open(CSV_FILE_NAME, mode='w', encoding='utf-8', newline='') as rwc_players_file:
        writer = csv.writer(rwc_players_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Name', 'URL', 'Born', 'Team'])

def add_csv_row(player):
    with open(CSV_FILE_NAME, mode='a', encoding='utf-8', newline='') as rwc_players_file:
        writer = csv.writer(rwc_players_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([player['name'], player['url'], player['born'], player['team']])

async def process_player(session, player):
    try:
        player['born'] = await get_player_location(session, player['url'])
    except Exception as e:
        print(e)
        player['born'] = ''
    finally:
        add_csv_row(player)

async def main():
    new_csv_file()

    url = 'https://en.m.wikipedia.org/wiki/2019_Rugby_World_Cup_squads'

    players = await get_players(url)

    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*(process_player(session, p) for p in players))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())