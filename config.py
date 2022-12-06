import os

HOST = '0.0.0.0'
PORT = 80
NEWS_FILE = 'macronews.json'
BASE_DIR = os.getcwd()
TEMPLATES_FOLDER = os.path.join(BASE_DIR, 'templates')
STATIC_FOLDER = os.path.join(BASE_DIR, 'static')

RELOAD_TIMEOUT = 45
COUNTRIES_RELOAD_TIMEOUT = 60 * 60 * 24
PAGE_SIZE = 1000
LIMIT_ENTRIES_PER_SOURCE = 1000
LIMIT_FEED = 50000

BACKGROUND_RELOAD = True

NEWS_SOURCES_FIELDNAMES = [
    'name', 'link', 'rss', 'country', 'archive', 'country_image'
]

MACRONEWS_FEED_URL = 'https://www.financialjuice.com/feed.ashx?xy=rss'
DESCRIPTION_LENGTH = 15

TAB_IDS = {
    3: 'Bonds',
    2: 'Commodities',
    8: 'Crypto',
    4: 'Equities',
    5: 'Forex',
    9: 'Indexes',
    1: 'Macro'
}

COUNTRIES = [
    ('united-states', 'United States',),
    ('euro-area', 'Euro Area',),
    ('china', 'China ',),
    ('japan', 'Japan',),
    ('germany', 'Germany',),
    ('united-kingdom', 'United Kingdom',),
    ('france', 'France',),
    ('india', 'India',),
    ('italy', 'Italy',),
    ('brazil', 'Brazil',),
    ('canada', 'Canada',),
    ('south-korea', 'South Korea',),
    ('russia', 'Russia',),
    ('spain', 'Spain',),
    ('australia', 'Australia',),
    ('mexico', 'Mexico',),
    ('indonesia', 'Indonesia',),
    ('turkey', 'Turkey',),
    ('netherlands', 'Netherlands',),
    ('switzerland', 'Switzerland',),
    ('saudi-arabia', 'Saudi Arabia ',),
    ('argentina', 'Argentina',),
    ('south-africa', 'South Africa',),
    ('singapore', 'Singapore',),
]

COUNTRY_FLAGS = {
    'united-states': 'https://upload.wikimedia.org/wikipedia/en/thumb/a/a4/Flag_of_the_United_States.svg/1920px-Flag_of_the_United_States.svg.png',
    'euro-area': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Flag_of_Europe.svg/250px-Flag_of_Europe.svg.png',
    'china': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Flag_of_the_People%27s_Republic_of_China.svg/240px-Flag_of_the_People%27s_Republic_of_China.svg.png',
    'japan': 'https://upload.wikimedia.org/wikipedia/en/thumb/9/9e/Flag_of_Japan.svg/240px-Flag_of_Japan.svg.png',
    'germany': 'https://upload.wikimedia.org/wikipedia/en/thumb/b/ba/Flag_of_Germany.svg/240px-Flag_of_Germany.svg.png',
    'united-kingdom': 'https://upload.wikimedia.org/wikipedia/en/thumb/a/ae/Flag_of_the_United_Kingdom.svg/240px-Flag_of_the_United_Kingdom.svg.png',
    'france': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Flag_of_France_%281794%E2%80%931815%2C_1830%E2%80%931974%2C_2020%E2%80%93present%29.svg/240px-Flag_of_France_%281794%E2%80%931815%2C_1830%E2%80%931974%2C_2020%E2%80%93present%29.svg.png',
    'india': 'https://upload.wikimedia.org/wikipedia/en/thumb/4/41/Flag_of_India.svg/240px-Flag_of_India.svg.png',
    'italy': 'https://upload.wikimedia.org/wikipedia/en/thumb/0/03/Flag_of_Italy.svg/240px-Flag_of_Italy.svg.png',
    'brazil': 'https://upload.wikimedia.org/wikipedia/en/thumb/0/05/Flag_of_Brazil.svg/240px-Flag_of_Brazil.svg.png',
    'canada': 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/Flag_of_Canada_%28Pantone%29.svg/240px-Flag_of_Canada_%28Pantone%29.svg.png',
    'south-korea': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/Flag_of_South_Korea.svg/240px-Flag_of_South_Korea.svg.png',
    'russia': 'https://upload.wikimedia.org/wikipedia/en/thumb/f/f3/Flag_of_Russia.svg/240px-Flag_of_Russia.svg.png',
    'spain': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Bandera_de_Espa%C3%B1a.svg/240px-Bandera_de_Espa%C3%B1a.svg.png',
    'australia': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Flag_of_Australia_%28converted%29.svg/240px-Flag_of_Australia_%28converted%29.svg.png',
    'mexico': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Flag_of_Mexico.svg/240px-Flag_of_Mexico.svg.png',
    'indonesia': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Flag_of_Indonesia.svg/240px-Flag_of_Indonesia.svg.png',
    'turkey': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Flag_of_Turkey.svg/240px-Flag_of_Turkey.svg.png',
    'netherlands': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/Flag_of_the_Netherlands.svg/240px-Flag_of_the_Netherlands.svg.png',
    'switzerland': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Flag_of_Switzerland.svg/240px-Flag_of_Switzerland.svg.png',
    'saudi-arabia': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Flag_of_Saudi_Arabia.svg/240px-Flag_of_Saudi_Arabia.svg.png',
    'argentina': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Flag_of_Argentina.svg/240px-Flag_of_Argentina.svg.png',
    'south-africa': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Flag_of_South_Africa.svg/240px-Flag_of_South_Africa.svg.png',
    'singapore': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Flag_of_Singapore.svg/240px-Flag_of_Singapore.svg.png'
}

INDICATORS_LIST = [
    ('indicators', 'Currency'), ('indicators', 'Stock Market'), ('indicators', 'GDP Growth Rate'),
    ('indicators', 'GDP Annual Growth Rate'), ('indicators', 'Unemployment Rate'),
    ('indicators', 'Inflation Rate'), ('indicators', 'Interest Rate'),
    ('indicators', 'Balance of Trade'), ('indicators', 'Current Account'),
    ('indicators', 'Current Account to GDP'), ('indicators', 'Government Debt to GDP'),
    ('indicators', 'Government Budget'), ('indicators', 'Business Confidence'),
    ('indicators', 'Manufacturing PMI'), ('indicators', 'Non Manufacturing PMI'),
    ('indicators', 'Consumer Confidence'), ('indicators', 'Retail Sales MoM'),
    ('indicators', 'Corporate Tax Rate'), ('indicators', 'Personal Income Tax Rate'),
    ('indicators', 'GDP'), ('indicators', 'GDP Constant Prices'),
    ('indicators', 'Gross National Product'), ('indicators', 'GDP per Capita'),
    ('indicators', 'GDP per Capita PPP'), ('indicators', 'Full Year GDP Growth'),
    ('indicators', 'GDP Sales QoQ'), ('indicators', 'Real Consumer Spending'),
    ('indicators', 'Weekly Economic Index'), ('indicators', 'GDP from Agriculture'),
    ('indicators', 'GDP from Construction'), ('indicators', 'GDP from Manufacturing'),
    ('indicators', 'GDP from Mining'), ('indicators', 'GDP from Public Administration'),
    ('indicators', 'GDP from Services'), ('indicators', 'GDP from Transport'),
    ('indicators', 'GDP from Utilities'), ('indicators', 'Government Payrolls'),
    ('indicators', 'Employed Persons'), ('indicators', 'Unemployed Persons'),
    ('indicators', 'Average Hourly Earnings'), ('indicators', 'Average Weekly Hours'),
    ('indicators', 'Labor Force Participation Rate'), ('indicators', 'Long Term Unemployment Rate'),
    ('indicators', 'Youth Unemployment Rate'), ('indicators', 'Labour Costs'),
    ('indicators', 'Productivity'), ('indicators', 'Job Vacancies'), ('indicators', 'Job Offers'),
    ('indicators', 'Wages'), ('indicators', 'Minimum Wages'), ('indicators', 'Population'),
    ('indicators', 'Retirement Age Women'), ('indicators', 'Retirement Age Men'),
    ('indicators', 'Average Hourly Earnings YoY'), ('indicators', 'Employment Cost Index Benefits'),
    ('indicators', 'Employment Cost Index Wages'), ('indicators', 'Hiring Plans Announcements'),
    ('indicators', 'Job Quits'), ('indicators', 'Job Quits Rate'), ('indicators', 'Employment Rate'),
    ('indicators', 'Full Time Employment'), ('indicators', 'Core Inflation Rate'),
    ('indicators', 'GDP Deflator'), ('indicators', 'Producer Prices Change'),
    ('indicators', 'Export Prices'), ('indicators', 'Import Prices'),
    ('indicators', 'Food Inflation'),
    ('indicators', 'Energy Inflation'), ('indicators', 'Michigan 5 Year Inflation Expectations'),
    ('indicators', 'Michigan Inflation Expectations'),
    ('indicators', 'PCE Price Index Annual Change'),
    ('indicators', 'PCE Prices QoQ'), ('indicators', 'Hospital Beds'),
    ('indicators', 'Money Supply M0'),
    ('indicators', 'Money Supply M1'), ('indicators', 'Money Supply M2'),
    ('indicators', 'Banks Balance Sheet'), ('indicators', 'Central Bank Balance Sheet'),
    ('indicators', 'Foreign Exchange Reserves'), ('indicators', 'Loans to Private Sector'),
    ('indicators', 'Private Debt to GDP'), ('indicators', 'Exports'), ('indicators', 'Imports'),
    ('indicators', 'External Debt'), ('indicators', 'Capital Flows'),
    ('indicators', 'Foreign Direct Investment'), ('indicators', 'Gold Reserves'),
    ('indicators', 'Crude Oil Production'), ('indicators', 'Goods Trade Balance'),
    ('indicators', 'Oil Exports'), ('indicators', 'Tourism Revenues'),
    ('indicators', 'Tourist Arrivals'), ('indicators', 'Weapons Sales'),
    ('indicators', 'Government Budget Value'), ('indicators', 'Government Spending'),
    ('indicators', 'Government Revenues'), ('indicators', 'Government Debt'),
    ('indicators', 'Credit Rating'), ('indicators', 'Military Expenditure'),
    ('indicators', 'Industrial Production'), ('indicators', 'Industrial Production Mom'),
    ('indicators', 'Manufacturing Production'), ('indicators', 'Capacity Utilization'),
    ('indicators', 'Car Production'), ('indicators', 'Manufacturing Production MoM'),
    ('indicators', 'Corruption Index'), ('indicators', 'Corruption Rank'),
    ('indicators', 'Mining Production'), ('indicators', 'Refinery Crude Runs'),
    ('indicators', 'Steel Production'), ('indicators', 'Gasoline Prices'),
    ('indicators', 'Households Debt to GDP'), ('indicators', 'New Home Sales'),
    ('indicators', 'Pending Home Sales'), ('indicators', 'Existing Home Sales'),
    ('indicators', 'Construction Spending'), ('indicators', 'Housing Index')
]  # + [
#     ('forecasts', 'Stock Market'), ('forecasts', 'Currency'), ('forecasts', 'Government Bond 10Y'),
#     ('forecasts', 'GDP Growth Rate'), ('forecasts', 'GDP Annual Growth Rate'),
#     ('forecasts', 'Unemployment Rate'), ('forecasts', 'Non Farm Payrolls'),
#     ('forecasts', 'Inflation Rate'), ('forecasts', 'Inflation Rate MoM'),
#     ('forecasts', 'Interest Rate'), ('forecasts', 'Balance of Trade'),
#     ('forecasts', 'Current Account'), ('forecasts', 'Current Account to GDP'),
#     ('forecasts', 'Government Debt to GDP'), ('forecasts', 'Government Budget'),
#     ('forecasts', 'Business Confidence'), ('forecasts', 'GDP'), ('forecasts', 'Labour Costs'),
#     ('forecasts', 'Productivity'), ('forecasts', 'Job Vacancies'), ('forecasts', 'Job Offers'),
#     ('forecasts', 'Consumer confidence')
# ]
FORECASTS_LIST = [
    ('forecasts', 'Stock Market'), ('forecasts', 'Currency'), ('forecasts', 'Government Bond 10Y'),
    ('forecasts', 'GDP Growth Rate'), ('forecasts', 'GDP Annual Growth Rate'),
    ('forecasts', 'Unemployment Rate'), ('forecasts', 'Non Farm Payrolls'),
    ('forecasts', 'Inflation Rate'), ('forecasts', 'Inflation Rate MoM'),
    ('forecasts', 'Interest Rate'), ('forecasts', 'Balance of Trade'),
    ('forecasts', 'Current Account'), ('forecasts', 'Current Account to GDP'),
    ('forecasts', 'Government Debt to GDP'), ('forecasts', 'Government Budget'),
    ('forecasts', 'Business Confidence'), ('forecasts', 'GDP'), ('forecasts', 'Labour Costs'),
    ('forecasts', 'Productivity'), ('forecasts', 'Job Vacancies'), ('forecasts', 'Job Offers'),
    ('forecasts', 'Consumer confidence')
]
