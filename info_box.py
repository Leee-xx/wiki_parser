from page import Page
#from pprint import PrettyPrinter
import unicodedata
import pdb

class InfoBox(Page):
    def __init__(self, url, **kwargs):
        super().__init__(url)
        boxes = self.soup.find_all('table', class_='infobox')
        end = kwargs.get('end', len(boxes))
        start = kwargs.get('start', 0)
        self.boxes = boxes[start:end + 1]

    def to_dict(self, **kwargs):
        data = {}
        keys = kwargs.get('keys', [])
        lambdas = kwargs.get('lambdas', {})
        #keys_lambdas = [k for k in keys if type(k) is dict]
        #keys = [k for k in keys if type(k) is str]
        text_only = kwargs.get('text_only', [])
        #pp = PrettyPrinter()
        for box in self.boxes:
            #pdb.set_trace()
            #print(repr(box))
            #pp.pprint(InfoBox.get_labels(box))
            #for html_label in box.find_all(class_='infobox-label'):
            for html_label in InfoBox.get_labels(box):
                label = html_label.string
                #print(f"INitial label {label}")
                if label is None:
                    #pdb.set_trace()
                    label = InfoBox.first_intersection(keys, html_label.stripped_strings)

                if not keys or label in keys or InfoBox.contained_in(keys, label):
                    #print(f"Found label {label}")
                    sibling = None
                    if label in lambdas:
                        #print(f'LAMBDA {label}')
                        #pdb.set_trace()
                        sibling = lambdas[label](html_label)
                        #print(repr(html_label))
                    else:
                        sibling = html_label.next_sibling
                    #value = sibling.string
                    #if value is None and hasattr(sibling, 'stripped_strings') and sibling.stripped_strings is not None:
                        #value = ' '.join(sibling.stripped_strings)
                    #data[label] = value
                    if InfoBox.contained_in(keys, label):
                        label = next(filter(lambda k: k in label, keys), None)

                    if label in text_only:
                        data[label] = sibling.string
                        if data[label] is not None:
                            data[label] = unicodedata.normalize('NFKD',
                                          data[label]).strip()
                    else:
                        data[label] = sibling

        return data

    @staticmethod
    def get_labels(box):
        return box.find_all(class_='infobox-label') + box.find_all(class_='infobox-header')

    @staticmethod
    def first_intersection(arr1, arr2):
        return next(filter(lambda x: x in arr1, arr2), None)

    @staticmethod
    def contained_in(keys, label):
        if label is None:
            return False

        return any(k in label for k in keys)
