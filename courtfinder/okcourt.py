import requests
from bs4 import BeautifulSoup

class OkCourt(object):
    def __init__(self, nameList):
        self.url = 'http://www.oscn.net/dockets/Results.aspx?db=all'
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
            
        caseRecords = []
        for data in fields:
            response = requests.get(self.url, data=data)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Clean up table data from page
            tables = soup.find_all('table')
            tables = [table.find_all('td') for table in tables]
            tables = list(filter(lambda x: x != [], tables))
            tables = [[each.get_text().encode('ascii') for each in table] for table in tables]
            for each in tables:
                caseRecords.append(each) # Append is likely to be slow; fix later
        
        # Return a string if caseRecord
        if not caseRecords:
            caseRecords = ['No records found']
        return caseRecords
    
if __name__ == '__main__':
    dadRecord = OkCourt([['Timothy','M', 'Gallup']])
    parentRecord = OkCourt([['Timothy', 'M', 'Gallup'], ['Patricia', 'S', 'Gallup']])
    meRecord = OkCourt([['Nathan', 'M', 'Gallup']])
    
    print dadRecord.names
    print parentRecord.names
    print meRecord.names
    
    print dadRecord.getRecords()
    print meRecord.getRecords()
    print parentRecord.getRecords()