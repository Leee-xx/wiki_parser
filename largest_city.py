from table import Table
from country_utils import CountryUtils
import re
import pprint

class LargestCity:
    #URL = 'https://en.wikipedia.org/wiki/List_of_countries_by_largest_and_second_largest_cities'
    URL = 'https://worldwideinterpreters.com.au/2024/04/17/the-largest-city-in-every-country/'

    def __init__(self):
        import pdb
        self.table = Table(self.URL)
        pdb.set_trace()
        #self.table = Table(self.URL).tables[0]
        self.data = self.to_dicts()

    def to_dicts(self):
        cities = {}

        # These places aren't listed in URL:
        manuals = {
                "Donetsk People's Republic": 'Donetsk',
                "Luhansk People's Republic": 'Luhansk'
                }
        for nation, city in manuals.items():
            cities[nation] = city

        for row in self.table.tbody.find_all('tr')[4:]:
            cells = row.find_all('td')
            if len(cells) > 3:
                country = CountryUtils.name(cells[0].a.string)
                city = None
                if cells[1].string:
                    city = cells[1].string
                else:
                    city = cells[1].a.string
                cities[country] = city

        dupes = {}
        for country, city in cities.items():
            city = re.sub(r'\W+', '', city.lower())
            if city not in dupes:
                dupes[city] = []
            dupes[city].append(country)

        dupes = { city:countries for (city, countries) in dupes.items() if len(countries) > 1 }

        if len(dupes) > 0:
            pp = pprint.PrettyPrinter()
            print('Close city name matches:')
            pp.pprint(dupes)

        return cities
