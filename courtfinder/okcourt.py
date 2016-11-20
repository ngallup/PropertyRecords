import requests
from bs4 import BeautifulSoup

class OkCourt(object):
    def __init__(self, nameList):
        self.url = 'http://www.oscn.net/dockets/Search.aspx'
        self.names = nameList
        
    def getRecords(self):
        # Takes list of names in list format e.g. ['Nathan','Gallup']
        # and performs search on the OK court records database
        
        fields = []
        for name in self.names:
            first = name[0]
            last = name[-1]
            
            data = {'fname' : first,
                    'lname' : last}
            fields.append(data)
            
        pages = []
        for data in fields:
            response = requests.get(self.url, data=data)
            with open('test.html', 'w') as testpage:
                testpage.write(response.text)
    
if __name__ == '__main__':
    dadRecord = OkCourt([['Timothy','M', 'Gallup']])
    parentRecord = OkCourt([['Timothy', 'M', 'Gallup'], ['Patricia', 'S', 'Gallup']])
    meRecord = OkCourt([['Nathan', 'M', 'Gallup']])
    
    print dadRecord.names
    print parentRecord.names
    print meRecord.names
    
    dadRecord.getRecords()