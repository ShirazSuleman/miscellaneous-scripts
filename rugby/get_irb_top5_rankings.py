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
        writer.writerow(['Date', 'Team', 'Rank', 'Points'])

def add_csv_row(date, rank, team, points):
    with open(CSV_FILE_NAME, mode='a') as irb_rankings_file:
        writer = csv.writer(irb_rankings_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([date, team, rank, points])

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def process_date(session, date):
    if date > date.today() or date < datetime.date(2003, 10, 13):
        return

    response = await fetch(session, URL.format(str(date)))
    entries = json.loads(response)['entries']

    for i in range(5):
        entry = entries[i]
        add_csv_row(date, i + 1, entry['team']['name'], round(entry['pts'], 2))

async def main():
    create_csv_file()
    years = [2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]
    for year in years:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            await asyncio.gather(*(process_date(session, d) for d in all_mondays(year)))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
