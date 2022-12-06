import asyncio
import calendar
import json
from heapq import merge

import aiohttp.web
import aiohttp_jinja2
import jinja2
from aiohttp import web
from aiohttp.web_app import Application

from config import HOST, PORT, NEWS_FILE, TEMPLATES_FOLDER, STATIC_FOLDER, PAGE_SIZE, COUNTRIES, INDICATORS_LIST, \
    FORECASTS_LIST, COUNTRY_FLAGS


class WebServer:
    app: Application

    def __init__(self):
        self.app = web.Application(debug=True)
        self.set_handlers()

    def set_handlers(self):
        routes = web.RouteTableDef()

        @routes.get('/news')
        async def get_news(request: web.Request):
            try:
                page = int(request.query.get('page', '1')) - 1
            except Exception:
                page = 0
            with open(NEWS_FILE) as f:
                with open('macronews.json') as f:
                    try:
                        macrodata = json.load(f)
                    except json.JSONDecodeError:
                        macrodata = {'entries': []}
                with open('worldnews.json') as f:
                    try:
                        worlddata = json.load(f)
                    except json.JSONDecodeError:
                        worlddata = {'entries': {}}

                with open('countries.json') as f:
                    try:
                        countries_data = json.load(f)['countries']
                    except json.JSONDecodeError:
                        countries_data = {
                            country: {} for country, country_name in COUNTRIES
                        }

                indicators = {}

                for category, indicator in INDICATORS_LIST:
                    indicators[indicator] = [country_data[category].get(indicator, '0') for country, country_data in
                                             countries_data.items()]

                news_lists = [value
                              for key, value in worlddata['entries'].items()]
                world_news_iter = iter(merge(*news_lists, key=lambda entry: calendar.timegm(entry['published_parsed']),
                                             reverse=True, ))

                world_news = []
                SINCE = PAGE_SIZE * page
                UNTIL = PAGE_SIZE * (page + 1)
                for i in range(UNTIL):
                    try:
                        a = next(world_news_iter)
                        if SINCE <= i:
                            world_news.append(a)
                    except StopIteration:
                        break
                context = {
                    'macroentries': macrodata['entries'],
                    'worldentries': world_news,
                    'page': page,
                    'countries_data': countries_data,
                    'countries': COUNTRIES,
                    'indicators': indicators,
                    'country_flags': COUNTRY_FLAGS,
                }

            response = aiohttp_jinja2.render_template('index.html',
                                                      request,
                                                      context)
            response.headers['Content-Language'] = 'ru'
            return response

        @routes.get('/news/{country}')
        async def get_news(request: web.Request):
            country = request.match_info['country']
            with open(NEWS_FILE) as f:
                with open('countries.json') as f:
                    try:
                        data = json.load(f)
                        countries_data = data['countries']
                    except (json.JSONDecodeError, KeyError):
                        countries_data = {
                            country: {} for country, country_name in COUNTRIES
                        }


                if country not in countries_data:
                    return aiohttp.web.HTTPNotFound()

                country_name = next(filter(lambda x: x[0] == country, COUNTRIES))

                indicators = {}
                forecasts = {}

                for category, indicator in INDICATORS_LIST:
                    indicators[indicator] = countries_data[country][category].get(indicator, '0')

                for category, indicator in FORECASTS_LIST:
                    forecasts[indicator] = countries_data[country][category].get(indicator, '0')


                context = {
                    'countries_data': countries_data,
                    'indicators': indicators,
                    'country': country,
                    'forecasts': forecasts,
                    'country_name': country_name
                }

            response = aiohttp_jinja2.render_template('single.html',
                                                      request,
                                                      context)
            response.headers['Content-Language'] = 'ru'
            return response

        self.app.add_routes(routes)
        self.app.add_routes([web.static('/static/', STATIC_FOLDER)])

        aiohttp_jinja2.setup(self.app,
                             loader=jinja2.FileSystemLoader(TEMPLATES_FOLDER + '/'))

    async def run(self):
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, HOST, PORT)
        await site.start()

        while True:
            await asyncio.sleep(1000)
