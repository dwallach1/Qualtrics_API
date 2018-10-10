import urllib.request #default module for Python 3.X

import os, sys
import requests
import zipfile, io
import json

apiToken = os.environ["Q_API_TOKEN"]     
dataCenter = os.environ["Q_DATA_CENTER"] 

url = 'https://{}.qualtrics.com/API/v3/surveys'.format(dataCenter)
header = {'X-API-TOKEN': apiToken}

req = urllib.request.Request(url,None,header) #generating the request object

handler = urllib.request.urlopen(req) #running the request object

print(handler.status) #print status code
print(handler.reason)