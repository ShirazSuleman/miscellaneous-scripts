import requests
from bs4 import BeautifulSoup

url = 'https://www.transfermarkt.co.uk/bidvest-wits-fc/spielplan/verein/10680/saison_id/2016'
headers = {'User-Agent': 'a'}

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, 'html.parser')
