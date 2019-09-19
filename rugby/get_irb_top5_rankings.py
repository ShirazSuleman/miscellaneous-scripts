import requests
from datetime import date, timedelta
import json

URL = 'https://cmsapi.pulselive.com/rugby/rankings/mru?date={}&client=pulse'

IRB_RANKINGS = []

def all_mondays(year):
   d = date(year, 1, 1)                    # January 1st
   d += timedelta(days = (d.weekday() if d.weekday() == 0 else 7 - d.weekday()))  # First Monday
   while d.year == year:
      yield d
      d += timedelta(days = 7)

def main():
    for d in all_mondays(2019):
        if d > date.today():
            break

        response = requests.get(URL.format(str(d)))
        entries = json.loads(response.text)['entries']

        period = dict()
        period['Date'] = str(d)
        period['Rankings'] = []

        for i in range(5):
            period['Rankings'].append({
                "Team": entries[i]['team']['name'],
                "Position": i + 1,
                "Points": round(entries[i]['pts'], 2)
            })
        
        IRB_RANKINGS.append(period)
    print(IRB_RANKINGS)

if __name__ == '__main__':
    main()