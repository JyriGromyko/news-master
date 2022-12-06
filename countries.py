import asyncio
import json
from typing import Optional

import aiohttp
from bs4 import BeautifulSoup

from config import RELOAD_TIMEOUT, COUNTRIES, COUNTRIES_RELOAD_TIMEOUT

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

STRIPPING = ' \t\r\n'


async def parse_country(country_name: str) -> Optional[dict]:
    try:
        indicators_dict, forecasts_dict = await asyncio.gather(
            get_indicators(country_name), get_forecasts(country_name)
        )
        return {
            'indicators': indicators_dict,
            'forecasts': forecasts_dict
        }
    except Exception as exc:
        print(exc)
        return None


async def get_indicators(country: str) -> dict:
    session = aiohttp.ClientSession()
    async with session:
        resp = await session.get(f'https://tradingeconomics.com/{country}/indicators', headers=HEADERS)
        page = await resp.text()
    soup = BeautifulSoup(page, 'html.parser')
    indicators = {}
    for table in soup.find_all('table'):
        row_elems = table.find_all('tr')
        for row_elem in row_elems[1:]:
            key = row_elem.contents[1].a.text.strip()  # getting indicators name
            val = row_elem.contents[3].text.strip()  # getting "Last" field value
            indicators[key] = val
    return indicators


async def get_forecasts(country: str) -> dict:
    session = aiohttp.ClientSession()
    async with session:
        resp = await session.get(f'https://tradingeconomics.com/{country}/forecasts', headers=HEADERS)
        page = await resp.text()
    soup = BeautifulSoup(page, 'html.parser')

    forecasts = {}

    for table in soup.find_all('table'):

        row_elems = table.find_all('tr')

        column_names = []

        for row_elem in row_elems[0:1]:
            for th in row_elem.find_all('th'):
                column_names.append(th.text.strip(STRIPPING))

        for row_elem in row_elems[1:]:
            key = row_elem.contents[1].a.contents[0].text.strip(STRIPPING)
            forecasts[key] = []
            for td in row_elem.find_all('td')[1:]:
                forecasts[key].append(td.text.strip(STRIPPING))
    return forecasts


async def sync_countries():
    while True:
        with open('countries.json') as f:
            try:
                prev_data = {
                    'countries': json.load(f)['countries']
                }
            except Exception as exc:
                countries_data = {
                    'countries': {country: {} for country, country_name in COUNTRIES}
                }

        new_data = {
            'countries': {}
        }

        countries_info = await asyncio.gather(*[
            parse_country(country[0]) for country in COUNTRIES
        ])

        for (country, country_name), country_info in zip(COUNTRIES, countries_info):
            if not country_info:
                print(f'Couldn\'t load {country.capitalize()} data')
                new_data['countries'][country] = prev_data['countries'][country]
                continue

            new_data['countries'][country] = country_info
        with open('countries.json', 'w') as fout:
            json.dump(new_data, fout)
        await asyncio.sleep(COUNTRIES_RELOAD_TIMEOUT)


if __name__ == '__main__':
    asyncio.run(sync_countries())
