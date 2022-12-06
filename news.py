import asyncio
import csv
import datetime
import json
import time
from typing import Optional

import aiohttp
import feedparser
from bs4 import BeautifulSoup
from feedparser import FeedParserDict

from config import LIMIT_ENTRIES_PER_SOURCE, RELOAD_TIMEOUT, MACRONEWS_FEED_URL, DESCRIPTION_LENGTH, TAB_IDS


def struct_to_seconds(struct: list) -> datetime:
    return datetime.datetime.fromtimestamp(time.mktime(tuple(struct)))


async def sync_macronews():
    while True:
        try:
            session = aiohttp.ClientSession()
            async with session:
                resp = await (await session.get(MACRONEWS_FEED_URL)).text()
                news_feed = feedparser.parse(resp)
                with open('macronews.json', 'r') as fin:
                    try:
                        data = json.load(fin)
                    except json.JSONDecodeError:
                        data = {}
                last_timestamp = datetime.datetime.fromtimestamp(
                    data.get('last_timestamp', 0)
                )
                entries = data.get('entries', [])
                new_entries = list(filter(
                    lambda entry: (datetime.datetime.utcnow() >= struct_to_seconds(
                        entry['published_parsed']) > last_timestamp),
                    news_feed.entries
                ))
                new_entries = [dict(entry) for entry in new_entries]
                if new_entries:
                    additionals = await get_images(len(new_entries))
                    images = additionals['images']
                    streamids = additionals['streamids']
                    infos = await asyncio.gather(
                        *[get_info(session, entry['link']) for entry in new_entries]
                    )
                    for entry, info in zip(new_entries, infos):
                        # info = await get_info(session, entry['link'])
                        prefix = 'FinancialJuice: '
                        if entry['title'].startswith(prefix):
                            entry['title'] = entry['title'][len(prefix):]
                        entry['categories'] = info['categories']

                        if 'summary' in entry and entry['summary']:
                            description = ' '.join(
                                BeautifulSoup(entry['summary'], "html5lib").text.strip().split()[:DESCRIPTION_LENGTH])
                        else:
                            description = ''

                        entry['description'] = description

                        guid = int(entry['id'])
                        if guid in streamids:
                            entry['streamids'] = [TAB_IDS[num].lower() for num in streamids[guid] if num in TAB_IDS]
                        if guid in images:
                            entry['imageURL'] = f'https://www.financialjuice.com{images[guid]}'
                new_entries += entries

                new_data = {
                    'last_timestamp': datetime.datetime.utcnow().timestamp(),
                    'entries': new_entries[:LIMIT_ENTRIES_PER_SOURCE]
                }

                with open('macronews.json', 'w') as fout:
                    dump = json.dumps(new_data)
                    fout.write(dump)
        except Exception as exc:
            print(exc)
        await asyncio.sleep(RELOAD_TIMEOUT)


async def get_images(count: int = None) -> dict:
    session = aiohttp.ClientSession()
    data = {
        'images': {},
        'streamids': {},
    }
    async with session:
        oldID = 0

        counter = 0
        headers = {
            'authority': 'www.financialjuice.com',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7',
            'cache-control': 'no-cache',
            'content-type': 'application/json; charset=utf-8',
            'cookie': 'ASP.NET_SessionId=rnamiboz1rtr4a2mp2clg1ji; _ga=GA1.2.1210893041.1659721557; FJSignupAllowClose=0; FJ-UName=daemonbiker15; FJ-Email=shilyaev.danila@gmail.com; .ASPXAUTH=E6C350766B6F59C6F18E53FB569E16CD3272C9978F1B616B4F14AF0D8A7511BFC216086F71217CF168BE0D0D031A2DDC52C1F532FFE7FC115FC3681A38A15BF98BF1160B45D393C6468CA560852EFC87695F72969180681142243AD7FD767171289A9B7D21C4E0DBADBC1560A7C777F7AD93CB1D; FJ-UID=164462; FJ-Pop=show; _gid=GA1.2.2145006863.1660164912; FJ-Referral=rss; FJNewsSummary=1',
            'pragma': 'no-cache',
            'referer': 'https://www.financialjuice.com/home',
            'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        while counter <= count:
            url = f"https://www.financialjuice.com/FJService.asmx/GetPreviousNews?info" \
                  f"=%22EAAAAB56HHThX3dZDAjEe4q0aI0TzYjx78AMJQ1Bs25IivM09LbBYH3b8qnMujcwU61taiN7odD8fklhWPXmqNq9KrBiWd8ufl56IXMgAKR7LL98HaAwj2uoAVZcT5KksizEH9e3P1Zu%2BBYaM1ekmU8MNhnqKxrUsONFpksdN7enTJWfXaiHLFyOGu645yOCDOxQ2RZtm%2BgfDonmhblgiidBs2qKUESq8SQtkLfHoBDcsqArSealiV24nIAVJOakjWKXTVoNiwHfr2J3eemrW0Ds%2F2TDiojEXHOErvOVQC2JScO3%22&TimeOffset=3&tabID=0&oldID={oldID}&TickerID=0&FeedCompanyID=0&strSearch=%22%22&extraNID=0 "
            params = {}
            resp = json.loads(json.loads(await (await session.get(url, headers=headers, params=params)).text())['d'])
            if not resp:
                break
            for entry in resp:
                if entry['Img']:
                    data['images'][entry['NewsID']] = entry['Img']
                data['streamids'][entry['NewsID']] = entry['StreamIDs']

            oldID = resp[-1]['NewsID']
            counter += len(resp)
    return data


async def get_info(session: aiohttp.ClientSession, link: str) -> dict:
    page = await (await session.get(link)).text()
    soup = BeautifulSoup(page, 'html5lib')
    labels = soup.find_all(class_='news-label')
    categories = [label.text.strip() for label in labels]
    return {
        'categories': categories
    }


def get_sources() -> list:
    with open('news_sources.csv', 'r') as fin:
        reader = csv.DictReader(fin)
        sources = list(reader)
    return sources


async def get_world_news_info(entry: dict, source: dict):
    archive_needed = source['archive'] == 'true'
    # session = aiohttp.ClientSession()
    # async with session:
    #     if archive_needed:
    if archive_needed:
        extralink = f'https://archive.ph/{entry["link"]}'
    else:
        extralink = entry["link"]
    if 'content' in entry:
        description = ' '.join(BeautifulSoup(entry['content'][0].value, "html5lib").text.split()[:DESCRIPTION_LENGTH])
    else:
        description = ''
    return {
        'extralink': extralink,
        'description': description,
    }


async def load_source_feed(source: dict) -> Optional[FeedParserDict]:
    session = aiohttp.ClientSession()
    async with session:
        try:
            if source['user agent'] != 'none':
                user_agent = source['user agent']
            else:
                user_agent = feedparser.USER_AGENT

            res = await session.get(source['rss'], headers={
                'user-agent': user_agent
            })
            text = await res.text()
            news_feed = feedparser.parse(text)

            return news_feed
        except Exception as exc:
            print(exc)
            return None


async def sync_world_news():
    while True:
        try:
            with open('worldnews.json', 'r') as fin:
                try:
                    data = json.load(fin)
                except json.JSONDecodeError:
                    data = {}
            last_timestamp = datetime.datetime.fromtimestamp(
                data.get('last_timestamp', 0)
            )
            sources = get_sources()

            session = aiohttp.ClientSession()
            new_data = {
                'last_timestamp': datetime.datetime.utcnow().timestamp(),
                'entries': {}
            }

            async with session:
                responses = await asyncio.gather(
                    *[load_source_feed(source) for source in sources], return_exceptions=True
                )
                for i, source in enumerate(sources):
                    old_entries = data.get('entries', {}).get(source['name'], [])
                    try:
                        news_feed = responses[i]
                        if not news_feed:
                            raise ValueError(f'No entries for {source["name"]}')
                        new_entries = [dict(entry) for entry in new_entries]
                        for new_entry in new_entries:
                            if 'published_parsed' not in new_entry and 'updated_parsed' in new_entry:
                                new_entry['published_parsed'] = new_entry['updated_parsed']
                            elif 'published_parsed' not in new_entry:
                                new_entry['published_parsed'] = time.struct_time(datetime.datetime.utcnow())

                        new_entries = list(filter(
                            lambda entry: (datetime.datetime.utcnow() >= struct_to_seconds(
                                entry['published_parsed']) > last_timestamp),
                            news_feed.entries
                        ))

                        for entry in new_entries:
                            entry['country'] = source['country']
                            entry['country_image'] = source['country_image']
                            info = await get_world_news_info(entry, source)
                            entry['extralink'] = info['extralink']
                            entry['description'] = info['description']
                    except Exception as exc:
                        new_entries = []
                        print(exc)

                    new_entries += old_entries
                    new_data['entries'][source['name']] = new_entries[:LIMIT_ENTRIES_PER_SOURCE]
            with open('worldnews.json', 'w') as fout:
                json.dump(new_data, fout)
        except Exception as exc:
            print(exc)
        await asyncio.sleep(RELOAD_TIMEOUT)
