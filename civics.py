from government import Government
from largest_city import LargestCity
from csv_writer import CsvWriter
import pprint
from country_utils import CountryUtils

class Civics:
    def __init__(self):
        self.cities = LargestCity()
        self.leaders = Government()

    def write_csv(self):
        data = self.combine_data()

        csv = CsvWriter(
                'countries',
                data,
                headers = [
                    'Country',
                    'Country info',
                    'Most populous city',
                    'Head of government'
                    ],
                datestamp=True
                )

        csv.diff()
        csv.archive()

    def combine_data(self):
        cities = self.cities.data
        leaders = self.leaders.data
        combined = {}
        pp = pprint.PrettyPrinter()
        self.add_dicts(combined, cities, 'Most populous city')
        self.add_dicts(combined, leaders, 'Head of government')
        self.add_notes(combined)
        return self.to_list(combined)

    def add_dicts(self, target, src, key):
        for nation, v in src.items():
            if nation not in target:
                target[nation] = {}
            target[nation][key] = v

    def add_notes(self, combined):
        for nation, note in CountryUtils.NOTES.items():
            combined[nation]['Country info'] = note

    def to_list(self, combined):
        data = []
        for nation, nation_data in combined.items():
            nation_dict = nation_data
            nation_dict['Country'] = nation
            data.append(nation_dict)

        return data

Civics().write_csv()
