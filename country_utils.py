import re

class CountryUtils:
    NAMES = {
            'Bahamas': 'The Bahamas',
            'Cape Verde': 'Cabo Verde',
            'Congo, Democratic Republic of the': 'Democratic Republic of the Congo',
            'Congo, Republic of the': 'Republic of the Congo',
            'Czech Republic': 'Czechia',
            'Gambia, The': 'The Gambia',
            'Ivory Coast': "Côte d'Ivoire",
            'Korea, North': 'North Korea',
            'Korea, South': 'South Korea',
            'Republic of China': 'Taiwan',
            'Sahrawi Republic': 'Sahrawi Arab Democratic Republic',
            'State of Palestine': 'Palestine',
            'Western Sahara': 'Sahrawi Arab Democratic Republic',
            'United States': 'United States of America',
            'Virgin Islands, British': 'British Virgin Islands',
            'Virgin Islands, United States': 'United States Virgin Islands'
            }

    SOV_NOTE = 'Sovereign country'
    NOT_SOV_NOTE = 'Not a sovereign country'
    NOTES = {
            'Aruba': SOV_NOTE,
            'Bermuda': NOT_SOV_NOTE,
            'Cayman Islands': NOT_SOV_NOTE,
            'Grenada': SOV_NOTE,
            'Guyana': SOV_NOTE
            }

    @staticmethod
    def name(country):
        new_name = country
        if country in CountryUtils.NAMES:
            new_name = CountryUtils.NAMES[country]
        elif ', the' in country.lower():
            new_name = re.sub(
                    pattern=r'(?i)(.+), the',
                    repl='The \\1',
                    string=country
                    )
            

        return new_name

    @staticmethod
    def notes(country):
        if country in CountryUtils.NOTES:
            return CountryUtils.NOTES[country]

        return
