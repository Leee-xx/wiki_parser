from table import Table
import pdb
import re
import pprint
import bs4
from csv_writer import CsvWriter

class Decolonization:
    URL = 'https://en.wikipedia.org/wiki/Decolonization'
    def __init__(self):
        self.scraped_tables = Table(self.URL, start = 1, end = 4)
        self.data = self.to_dicts()
        CsvWriter('decolonization', self.data,
                headers = [
                    "Decolonized state",
                    "Colonizer",
                    "Year",
                    "Event"
            ])

    def to_dicts(self):
        pp = pprint.PrettyPrinter()
        temp = {}
        for table in self.scraped_tables.tables:
            headers = [content.string.rstrip() for content in table.tr.contents if content.string.rstrip()]
            colonizer = None
            year = None
            for row in table.find_all('tr')[1:]:
                tds = [td for td in row.find_all(re.compile("^t(?:d|h)"))]
                if len(tds) == 3:
                    tds = [year] + tds
                elif len(tds) == 2:
                    tds = [year, colonizer] + tds

                tds[3] = ' '.join(tds[3].stripped_strings)
                for i in range(0, 3):
                    if tds[i]:
                        if hasattr(tds[i], 'string') and tds[i].string is not None:
                            tds[i] = tds[i].string.rstrip()
                        elif hasattr(tds[i], 'stripped_strings') and tds[i].stripped_strings is not None:
                            tds[i] = ' '.join(tds[i].stripped_strings)

                data = dict(zip(headers, tds))
                if data.get('Year') is None:
                    data['Year'] = year
                else:
                    year = data['Year']

                if data.get('Colonizer') is None:
                    data['Colonizer'] = colonizer
                else:
                    colonizer = data['Colonizer']
                state = Decolonization.format_state(data['Decolonized state'])
                data['Colonizer'] = Decolonization.format_state(data['Colonizer'])
                if state not in temp:
                    temp[state] = {
                                'Year': [],
                                'Colonizer': [],
                                'Event': []
                            }

                # Avoid dupes but also retain insertion order:
                if data['Year'] not in temp[state]['Year']:
                    temp[state]['Year'].append(data['Year'])
                if data['Colonizer'] not in temp[state]['Colonizer']:
                    temp[state]['Colonizer'].append(data['Colonizer'])
                if data['Event'] not in temp[state]['Event']:
                    temp[state]['Event'].append(Table.format_sentence(data['Event']))
                #temp.append(data)
                #pp.pprint(zipped)

                '''
                for i, td in enumerate(row.find_all(re.compile("^t(?:d|h)"))):
                    if td.attrs:
                    if td.string:
                        data[headers[i]] = td.string.rstrip()
                temp.append(data)
                print(f'{row.attrs}')
                if row.attrs:
                    return
                #if row['rowspan']:
                    #breakpoint();
                    '''
        #pp.pprint([state for state, state_dict in temp.items()])
        dicts = []
        for state, state_dict in temp.items():
            temp_state = {
                'Decolonized state': state,
                'Colonizer': ', '.join(state_dict['Colonizer']),
                'Year': ', '.join(state_dict['Year']),
                'Event': '\n'.join(state_dict['Event'])
            }

            #other_data = { k: ', '.join(v) for (k, v) in state_dict.items() }
            #dicts.append({ **temp_state, **other_data })
            dicts.append(temp_state)


        return dicts

    def format_state(state):
        # Order matters here! Need to delete the footnotes first
        state = re.sub('\s?\[\d+\]', '', state)
        state = re.sub('\s?[^\w, \-\(\)]+', '', state)
        state = Table.format_sentence(state)
        return state

Decolonization()
