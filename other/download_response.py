import os, sys
import requests
import json

verbose = True


apiToken = "put your apiToken here"   
dataCenter = "put your dataCenter here"

headers = {
						"X-API-TOKEN": apiToken,
						"Content-Type": "application/json",
					}


def download_responses(surveyId, format_type="csv", path=None, download=True):
		"""
		Download all responses from a survey

		:format_type: - string - can be csv, json, or spss (defaults to "csv")
		:path: - string - path to download the data (defaults to None)

		Returns None
		"""

		if verbose: print ("Starting to download {}".format(surveyId))

		# data = '{{"surveyId": "{0}", "format": "{1}", "lastResponseId": "R_1r8Om56xflLiGWj"}}'.format(surveyId, format_type)
		data = '{{"surveyId": "{0}", "format": "{1}"}}'.format(surveyId, format_type)
		
		baseUrl = "https://{0}.qualtrics.com/API/v3/responseexports".format(dataCenter)
		response = requests.post(baseUrl, headers=headers, data=data)
		
		if response.status_code != 200:
			if verbose: print ("error making post request to initate download for survey {} -- aborted with status_code {}".format(surveyId, response.status_code))
			return

		if verbose: print ('successfully sent request to Qualtrics servers')

		key = response.json()['result']['id']

		done = False
		while not done:
			baseUrl = 'https://{0}.qualtrics.com/API/v3/responseexports/{1}'.format(dataCenter,key)
			response = requests.get(baseUrl, headers=headers)

			status = response.json()['result']['status']
			percent = response.json()['result']['percentComplete']

			if verbose: print ("\rcompletion percentage:", percent, "%", end='\r')

			if status == "complete":
				done = True

			elif status == "cancelled" or status == "failed":
				if verbose: print("error while generating download for survey {} -- aborted with status_code {}".format(surveyId, response.status_code))
				return

		if verbose: print ("\nsuccessfully generated file, attempting to download...")

		baseUrl = "https://{0}.qualtrics.com/API/v3/responseexports/{1}/file".format(dataCenter,key)
		response = requests.get(baseUrl, headers=headers, stream=True)

		if response.status_code != 200:
			if verbose: print ("error downloading file for survey {} -- aborted with status_code {}".format(surveyId, response.status_code))
			return

		if not download:
			if verbose: print ("Download has been turned off, returning content")
			return response.content

		if path == None:
			if not os.path.exists('downloads'):
				os.mkdir('downloads')
			path = "downloads/{}_{}_response.zip".format(surveyId, format_type)
		handle = open(path, "wb")
		for chunk in response.iter_content(chunk_size=512):
			if chunk: 
				handle.write(chunk)
		handle.close()


		if verbose: print ("successfully downloaded file\ndone.")
		return None



download_responses("put a survey id here")





