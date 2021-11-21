from page import Page
import pdb
import re
from pprint import PrettyPrinter

class Table(Page):
    def __init__(self, url, **kwargs):
        super().__init__(url)
        tables = self.soup.find_all('table', class_='wikitable')
        end = kwargs.get('end', len(tables))
        start = kwargs.get('start', 0)
        self.tables = tables[start:end + 1]

    #@classmethod
    def to_dicts(self):
        dicts = []
        pp = PrettyPrinter()
        for table in self.tables:
            headers = [content.string.rstrip() for content in table.tr.contents]
            pp.pprint(headers)
            for row in table.find_all('tr')[1:]:
                data = {}
                #tds = [td for td in row.find_all(re.compile("^t(?:d|h)"))]
                #data = dict(zip(headers, tds))
                #pp.pprint(data)
                for i, td in enumerate(row.find_all(re.compile("^t(?:d|h)"))):
                #for i in range(len(row.contents)):
                    if td.string:
                        data[headers[i]] = td.string.rstrip()
                dicts.append(data)
                #if row['rowspan']:
                    #breakpoint();
        return dicts

