import requests
import datetime
import json
import csv
import aiohttp
import asyncio

URL = 'https://cmsapi.pulselive.com/rugby/rankings/mru?date={}&client=pulse'
CSV_FILE_NAME = 'irb_rankings.csv'

def all_mondays(year):
   d = datetime.date(year, 1, 1)                    # January 1st
   d += datetime.timedelta(days = (d.weekday() if d.weekday() == 0 else 7 - d.weekday()))  # First Monday
   while d.year == year:
      yield d
      d += datetime.timedelta(days = 7)

def create_csv_file():
    with open(CSV_FILE_NAME, mode='w') as irb_rankings_file:
        writer = csv.writer(irb_rankings_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Date', 'Team', 'Position', 'Points', 'Previous Position', 'Previous Points'])

def add_csv_row(date, team, pos, points, prev_pos, prev_points):
    with open(CSV_FILE_NAME, mode='a') as irb_rankings_file:
        writer = csv.writer(irb_rankings_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([date, team, pos, points, prev_pos, prev_points])

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def process_date(session, date):
    if date > date.today() or date < datetime.date(2003, 10, 13):
        return

    response = await fetch(session, URL.format(str(date)))
    entries = json.loads(response)['entries']

    for i in range(10):
        entry = entries[i]
        name = entry['team']['name']
        pos = entry['pos']
        points = round(entry['pts'], 2)
        prev_pos = entry['previousPos']
        prev_points = round(entry['previousPts'], 2)
        add_csv_row(date, name, pos, points, prev_pos, prev_points)

async def main():
    create_csv_file()
    for year in range(2003, 2020):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            await asyncio.gather(*(process_date(session, d) for d in all_mondays(year)))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
