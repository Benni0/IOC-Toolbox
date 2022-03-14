from io import BytesIO
from zipfile import ZipFile
import requests
import time


class BaseLookupList():
    def __init__(self, url, filename):
        self.url = url
        self.file = filename
        self.domain_cache = {}
        self.cache_timstamp = 0

    def update_when_cache_outdated(self):
        if self.cache_timstamp < time.time() - 3600*10:
            self.update()
            self.cache_timstamp = time.time()

    def update(self):
        content = requests.get(self.url).content
        zipfile = ZipFile(BytesIO(content))
        self.domain_cache = {}
        for line in zipfile.open(self.file).readlines():
            rank, domain = line.decode("utf-8").rstrip().split(',')
            self.domain_cache[domain] = rank

    def lookup_domain(self, domain):
        self.update_when_cache_outdated()
        if domain in self.domain_cache:
            return (domain, self.domain_cache[domain])
        else:
            return None


class CiscoUmbrellaOneMill(BaseLookupList):
    def __init__(self):        
        self.url = "http://s3-us-west-1.amazonaws.com/umbrella-static/top-1m.csv.zip"
        self.file = "top-1m.csv"
        super(CiscoUmbrellaOneMill, self).__init__(self.url, self.file)

class AlexaOneMill(BaseLookupList):
    def __init__(self):        
        self.url = "http://s3.amazonaws.com/alexa-static/top-1m.csv.zip"
        self.file = "top-1m.csv"
        super(AlexaOneMill, self).__init__(self.url, self.file)

ALEXA_ONE_MILL = AlexaOneMill()
CISCO_UMBRELLA_ONE_MILL = CiscoUmbrellaOneMill()