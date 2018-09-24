import os, sys
import requests
import zipfile, io
import json

apiToken = os.environ["Q_API_TOKEN"]     
dataCenter = os.environ["Q_DATA_CENTER"] 


headers = {
	"X-API-TOKEN": apiToken,
	"Content-Type": "application/json",
}


def download_responses(surveyId, format_type):
	"""
	Download all responses from a survey

	format_type can be csv, json, or spss
	"""

	print ("Starting to download {}".format(surveyId))

	data = '{{"surveyId": {0}, "format": "{1}"}}'.format(surveyId, format_type)
	baseUrl = "https://{0}.qualtrics.com/API/v3/responseexports".format(dataCenter)
	response = requests.post(baseUrl, headers=headers, data=data)
	
	if response.status_code != 200:
		print ("error making post request to initate download for survey {} -- aborted with status_code {}".format(surveyId, response.status_code))
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

		if status == "complete":
			done = True

		elif status == "cancelled" or status == "failed":
			print("error while generating download for survey {} -- aborted with status_code {}".format(surveyId, response.status_code))
			return

	print ("\nsuccessfully generated file, attempting to download...")

	baseUrl = "https://{0}.qualtrics.com/API/v3/responseexports/{1}/file".format(dataCenter,key)
	response = requests.get(baseUrl, headers=headers, stream=True)

	if response.status_code != 200:
		print ("error downloading file for survey {} -- aborted with status_code {}".format(surveyId, response.status_code))
		return


	if not os.path.exists('downloads'):
		os.mkdir('downloads')
	handle = open("downloads/{}_{}_response.zip".format(surveyId, format_type), "wb")
	for chunk in response.iter_content(chunk_size=512):
		if chunk: 
			handle.write(chunk)
	handle.close()


	print ("successfully downloaded file\ndone.")
	return

def list_all_surveys():
	"""
	Get the Survey IDs of all surveys in your account

	Returns an array of SurveyIds
	"""
	baseUrl = "https://{0}.qualtrics.com/API/v3/surveys".format(dataCenter)
	response = requests.get(baseUrl, headers=headers)

	if response.status_code != 200:
		print ("error making post request to initate download -- aborted with status_code {}".format(surveyId, response.status_code))
		return

	ids = []
	for element in response.json()['result']['elements']: ids.append("{}".format(element['id']))

	nextPage = response.json()['result']['nextPage']

	while nextPage != None:

		response = requests.get(nextPage, headers=headers)

		if response.status_code != 200:
			print ("error making post request to initate download -- aborted with status_code {}".format(surveyId, response.status_code))
			return

		nextPage = response.json()['result']['nextPage']
		for element in response.json()['result']['elements']: ids.append(element['id'])

	return ids


surveyIds = list_all_surveys()
print ("found {} total surveys in your library".format(len(surveyIds)))
for surveyId in surveyIds:
	double_quotes_id = '"' + surveyId + '"' 	# necessary for JSON
	download_responses(double_quotes_id, "csv")



