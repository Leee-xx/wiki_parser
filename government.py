from table import Table
from country_utils import CountryUtils
import re

class Government:
    URL = 'https://en.wikipedia.org/wiki/List_of_current_heads_of_state_and_government'

    def __init__(self):
        self.scraped_tables = Table(self.URL, end=3)
        self.data = self.to_dicts()

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

                cell = row.find('td', style=lambda value: value and 'LightGreen' in value)
                if cell:
                    leader =  self.get_leader(cell)

                    leader = self.reformat_leader(leader)
                    if leader == '':
                        temp_leader = self.get_leader(cell.contents[0])
                        if temp_leader:
                            leader = self.reformat_leader(temp_leader)

                    if leader:
                        leaders[nation] = leader

        return leaders

    def this_nation(self, row):
        if row.th and row.th.contents[-2] and row.th.contents[-2].string:
            return row.th.contents[-2].string

        return

    def should_change_nation(self, nation, new_nation):
        return nation is not new_nation and new_nation[0] != '[' and new_nation[-1] != ']'

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
            leader = re.sub('\(.+\)', '', leader)


        # Remove multiple consecutive whitespace
        leader = ' '.join(leader.split())
        return leader
