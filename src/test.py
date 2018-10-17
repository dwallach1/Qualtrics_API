# Python 3

import requests
import zipfile
import json
import io, os

# Setting user Parameters
apiToken = ""
surveyId = ""
dataCenter = ""
fileFormat = "csv"

# Setting static parameters
requestCheckProgress = 0.0
progressStatus = "inProgress"
baseUrl = "https://{0}.qualtrics.com/API/v3/surveys/{1}/export-responses/".format(dataCenter, surveyId)
headers = {
    "content-type": "application/json",
    "x-api-token": apiToken,
    }

# Step 1: Creating Data Export
downloadRequestUrl = baseUrl
downloadRequestPayload = '{"format":"' + fileFormat + '"}'
downloadRequestResponse = requests.request("POST", downloadRequestUrl, data=downloadRequestPayload, headers=headers)
progressId = downloadRequestResponse.json()["result"]["progressId"]
print(downloadRequestResponse.text)

# Step 2: Checking on Data Export Progress and waiting until export is ready
while progressStatus != "complete" and progressStatus != "failed":

    requestCheckUrl = baseUrl + progressId
    requestCheckResponse = requests.request("GET", requestCheckUrl, headers=headers)
    requestCheckProgress = requestCheckResponse.json()["result"]["percentComplete"]
    print("Download is " + str(requestCheckProgress) + " complete")
    progressStatus = requestCheckResponse.json()["result"]["status"]

#step 2.1: Check for error
if progressStatus is "failed":
    raise Exception("export failed")

fileId = requestCheckResponse.json()["result"]["fileId"]

# Step 3: Downloading file
requestDownloadUrl = baseUrl + fileId + '/file'
requestDownload = requests.request("GET", requestDownloadUrl, headers=headers, stream=True)

# Step 4: Unzipping the file
zipfile.ZipFile(io.BytesIO(requestDownload.content)).extractall("MyQualtricsDownload")
print('Complete')