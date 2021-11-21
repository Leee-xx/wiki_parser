import csv
from datetime import date
#import pprint

class CsvWriter:
    '''
    A class that creates a CSV file. Instantiating this class will generate the CSV file.
    Also includes file management methods (archiving, diffs, etc.)

    :param str filename: the CSV filename (extension optional)
    :param list(dict(str, str)) data: a list of dictionaries that will be
    printed to a single CSV row
    :keyword bool datestamp: flag that appends a datestamp to the filename
    (default: False)
    :keyword list(str) headers: a list of keys that determines the order in
    which the columns are printed (default: order of the keys of the first
    entry in data)

    '''

    def __init__(self, filename, data, **opts):
        self.base_filename = filename
        self.files = []
        if opts.get('datestamp', False):
            filename += "_" + date.today().strftime('%F')
        if not filename.endswith('.csv'):
            filename += '.csv'

        self.filename = filename
        #pp = pprint.PrettyPrinter()
        with open(filename, 'w') as csvfile:
            writer = csv.writer(csvfile)
            headers = opts.get('headers', data[0].keys())
            # Anki doesn't have an option to ignore headers, so we can't really
            # write them:
            #writer.writerow(headers)
            for datum in data:
                writer.writerow([datum[key] if key in datum else '' for key in headers])

        print(f'Wrote to {filename}')

    
    def diff(self):
        import subprocess

        if len(self.files) == 0:
            self.glob()
        
        self.glob()
        if len(self.files) > 1:
            subprocess.run(['diff', self.files[-2], self.files[-1]])
        
    def glob(self):
        import glob

        self.files = glob.glob(f'{self.base_filename}*.csv')

    def archive(self):
        import subprocess

        if len(self.files) == 0:
            self.glob()
        
        if len(self.files) > 1:
            subprocess.run(['mv', f'{self.files[-2]}', 'archived/'])
        else:
            print('No other files to archive')
        
