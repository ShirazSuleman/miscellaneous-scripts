import requests
import csv
from bs4 import BeautifulSoup

URLS = { 1: 'http://stats.espncricinfo.com/ci/engine/stats/index.html?class=1;filter=advanced;orderby=start;size=200;spanmax1=25+Dec+2019;spanmin1=01+Dec+1992;spanval1=span;team=3;template=results;type=team;view=results',
         2: 'http://stats.espncricinfo.com/ci/engine/stats/index.html?class=1;filter=advanced;orderby=start;page=2;size=200;spanmax1=25+Dec+2019;spanmin1=01+Dec+1992;spanval1=span;team=3;template=results;type=team;view=results'}

RESULTS = { 'MATCHES': 0, 'WINS': 0, 'DRAWS': 0, 'LOSSES': 0 }

CSV_FILE_NAME = 'sa_boxing_day_tests.csv'

def create_csv_file():
    with open(CSV_FILE_NAME, mode='w', encoding='utf-8', newline='') as sa_boxing_day_tests_file:
        writer = csv.writer(sa_boxing_day_tests_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Team', 'Date', 'Venue', 'Result'])

def add_csv_row(date, venue, result):
    with open(CSV_FILE_NAME, mode='a', encoding='utf-8', newline='') as sa_boxing_day_tests_file:
        writer = csv.writer(sa_boxing_day_tests_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['South Africa', date, venue, result])

def run():
    create_csv_file()
    for name, url in URLS.items():
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        matches = soup.select('tr.data1')
        for match in matches:
            date = match.select('td[nowrap="nowrap"] > b')[0].get_text()
            if '26 Dec' in date:
                result = match.contents[3].get_text()
                venue = match.contents[15].select('a.data-link')[0].get_text()
                add_csv_row(date, venue, result)
                if result == 'won':
                    RESULTS['WINS'] += 1
                elif result == 'lost':
                    RESULTS['LOSSES'] += 1
                elif result == 'draw':
                    RESULTS['DRAWS'] += 1

                RESULTS['MATCHES'] += 1
    print(RESULTS)

if __name__ == '__main__':
    run()
