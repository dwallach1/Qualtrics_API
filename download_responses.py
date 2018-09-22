import os
import sys
import requests, zipfile, io
import json

apiToken = os.environ["Q_API_TOKEN"]     
dataCenter = os.environ["Q_DATA_CENTER"] 


headers = {
	"X-API-TOKEN": apiToken,
	"Content-Type": "application/json",
}



def download_responses(surveyId, format_type):
	"""
	download all responses from a survey
	"""

	data = '{{"surveyId": "{0}", "format": "{1}"}}'.format(surveyId, format_type)
	baseUrl = 'https://{0}.qualtrics.com/API/v3/responseexports'.format(dataCenter)
	response = requests.post(baseUrl, headers=headers, data=data)
	
	if response.status_code != 200:
		print ('error making post request to initate download -- aborted')
		return

	print ('successfully sent request to Qualtrics servers')

	key = response.json()['result']['id']

	done = False
	while not done:
		baseUrl = 'https://{0}.qualtrics.com/API/v3/responseexports/{1}'.format(dataCenter,key)
		response = requests.get(baseUrl, headers=headers)

		status = response.json()['result']['status']
		percent = response.json()['result']['percentComplete']

		print ("\rcompletion percentage:", percent, "%", end='\r')

		if status == 'complete':
			done = True

		if status == "cancelled" or status == "failed":
			print("error while generating download -- aborted")
			return


	print ("\nsuccessfully generated file, attempting to download...")

	baseUrl = "https://{0}.qualtrics.com/API/v3/responseexports/{1}/file".format(dataCenter,key)
	response = requests.get(baseUrl, headers=headers, stream=True)

	if response.status_code != 200:
		print ("error downloading file -- aborted")
		return

	handle = open("{}_{}_response.zip".format(surveyId, format_type), "wb")
	for chunk in response.iter_content(chunk_size=512):
		if chunk: 
			handle.write(chunk)
	handle.close()


	print ("successfully downloaded file\ndone.")
	return




download_responses("SV_eDHWohdKuzG2245", "json")




