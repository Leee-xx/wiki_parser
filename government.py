from table import Table
from country_utils import CountryUtils
import re
import pdb
from csv_writer import CsvWriter
#import warnings

class PossibleNoLeader(Exception):
    def __init__(self, details):
        super().__init__(details)

class Government:
    URL = 'https://en.wikipedia.org/wiki/List_of_current_heads_of_state_and_government'

    def __init__(self):
        self.ignore_hyphen_warnings = {
                'blue': ['Sudan']
                }
        self.ignore_cells = {
                'green': ['Serbia']
                }
        self.council_executives = ['Bosnia and Herzegovina', 'Switzerland']
        self.regex_countries = ['Haiti']
        self.scraped_tables = Table(self.URL, end=3)
        self.data = self.to_dicts()

    def to_list(self):
        return [{'Country': country, 'Head of government': leader } for country, leader in self.data.items()]

    def to_dicts(self):
        leaders = {}
        for table in self.scraped_tables.tables:
            nation = None
            for row in table.tbody.find_all('tr')[1:]:
                # We'll need to cache this at some point when we have merged
                # rows/cells:
                this_nation = self.this_nation(row)
                if this_nation and self.should_change_nation(nation, this_nation):
                    nation = CountryUtils.name(this_nation)

                if nation in self.council_executives:
                    if nation not in leaders and row.li:
                        leader = self.reformat_parenthetical_line(row.li.text)
                        if leader:
                            leaders[nation] = leader
                elif nation in self.regex_countries:
                    if nation not in leaders and re.search('\(.+\)', row.text):
                        leader = self.reformat_parenthetical_line(row.text)
                        if leader:
                            leaders[nation] = leader
                    #pdb.set_trace()
                else:
                    green_cell = row.find('td', style=lambda value: value and '#9EFF9E' in value)
                    blue_cell = row.find('td', style=lambda value: value and '#CEF' in value)
                    #if nation == 'Haiti':
                        #pdb.set_trace()
                    if green_cell:

                        leader = self.parse_leader_cell(green_cell, nation, 'green')
                        if leader:
                            leaders[nation] = leader
                            #quit()

                    if blue_cell and nation not in leaders:
                        #print(f'No leader in green found for {nation}, trying blue')
                        #pdb.set_trace()
                        leader = self.parse_leader_cell(blue_cell, nation, 'blue')
                        if leader:
                            leaders[nation] = leader
                        #leader = self.get_leader(blue_cell)
                        #print(f'blue leader: {leader}')

        return leaders

    def this_nation(self, row):
        if row.th and row.th.contents[-2] and row.th.contents[-2].string:
            return row.th.contents[-2].string

        return

    def should_change_nation(self, nation, new_nation):
        return nation is not new_nation and new_nation[0] != '[' and new_nation[-1] != ']'

    def reformat_parenthetical_line(self, text):
        matches = re.search('([^\(]+) \((.+)\)', text)
        if matches.group().strip():
            return f"{matches.group(2).strip()} {matches.group(1).strip()}"

    def parse_leader_cell(self, cell, nation, color):
        if self.should_ignore_cell(nation, color):
            print(f'\033[93mIgnoring {color} cell for {nation}\33[0m')
            return

        if self.check_cell_has_leader(cell, nation, color) is False:
            print(f'\033[31m{nation} might not have leader\033[0m')
            print(cell.text)
            return

        leader = self.get_leader(cell)

        #try:
        leader = self.reformat_leader(leader)
        # This doesn't seem to happen anymore
        if leader == '':
            temp_leader = self.get_leader(cell.contents[0])
            if temp_leader:
                leader = self.reformat_leader(temp_leader)

        #except PossibleNoLeader:
            #warnings.warn(f'{nation} might not have leader: ')
        return leader

    def should_ignore_cell(self, nation, color):
        return color in self.ignore_cells and nation in self.ignore_cells[color]

    def check_cell_has_leader(self, el, nation, color):
        if self.ignore_missing_hyphen(nation, color):
            return True
        return "–" in el.text

    def ignore_missing_hyphen(self, nation, color):
        return color in self.ignore_hyphen_warnings and nation in self.ignore_hyphen_warnings[color]

    # At this point cell has multiple children, so we'll need to filter the
    # ones we want (i.e. not the footnotes) and then join them together.
    def get_leader(self, element):
        return ' '.join([el.string for el in element.contents if el.name != 'sup' and el.string])

    def reformat_leader(self, leader):
        # Remove nbsp
        leader = leader.replace(u'\xa0', '')
        # Remove the en-dash
        leader = leader.replace("–", "")

        if '(' in leader and ')' in leader:
            leader = self.reformat_parenthetical_line(leader)
            #leader = re.sub('\(.+\)', '', leader)

        # Remove multiple consecutive whitespace
        leader = ' '.join(leader.split())
        return leader.strip()

    def write_csv(self):
        csv = CsvWriter('government',
                self.to_list(),
                headers=['Country', 'Head of government'],
                datestamp=True
                )
        csv.diff()
        csv.archive()
