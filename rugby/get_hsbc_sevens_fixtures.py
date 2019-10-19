import requests
import datetime
import json
import csv
import datetime
import aiohttp
import asyncio

URL = 'https://cmsapi.pulselive.com/rugby/event/1954/schedule?language=en'
CSV_FILE_NAME = 'hsbc_sevens_fixtures.csv'
DATE_FORMAT = '%a %d %b %Y, %H:%M %Z%z'

def create_csv_file():
    with open(CSV_FILE_NAME, mode='w', encoding='utf-8', newline='') as irb_rankings_file:
        writer = csv.writer(irb_rankings_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Date', 'Team #1', 'Team #2', 'Description', 'Venue'])

def add_csv_row(date, team_1, team_2, description, venue):
    with open(CSV_FILE_NAME, mode='a', encoding='utf-8', newline='') as irb_rankings_file:
        writer = csv.writer(irb_rankings_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([date, team_1, team_2, description, venue])

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def download_matches(session):
    response = await fetch(session, URL)
    matches = json.loads(response)['matches']

    for match in matches:
        date_text = match['time']['label']
        last_colon_index = str.rfind(date_text, ':')
        date_text = date_text[:last_colon_index] + date_text[last_colon_index + 1:]
        date = datetime.datetime.strptime(date_text, DATE_FORMAT).astimezone()

        team_1 = match['teams'][0]['name']
        team_2 = match['teams'][1]['name']

        description = match['description']

        venue = match['venue']['city'] + ', ' + match['venue']['country']

        add_csv_row(date, team_1, team_2, description, venue)

async def run():
    create_csv_file()
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        await download_matches(session)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())