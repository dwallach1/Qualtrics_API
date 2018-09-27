import os, sys
import requests
import json
import datetime

verbose = True

class Qualtrics(object):
	"""
	Qualtrics class for interacting with Qualtrics API (v3)

	* Qaultrics v3 API documentation: https://api.qualtrics.com/
	* Project page with documentation for this project: 
	"""

	def __init__(self, apiToken, dataCenter):
		"""
		Initalize new Qualtrics object
		"""
		self.apiToken = apiToken
		self.dataCenter = dataCenter
		self.headers = {
						"X-API-TOKEN": apiToken,
						"Content-Type": "application/json",
					}


	def get_survey(self, surveyId):
		"""
		Gets JSON of survey associated with surveyId

		:surveyId: - string - the ID of the survey you are querying for
		
		Returns JSON response 
		"""
		baseUrl = "https://{0}.qualtrics.com/API/v3/surveys/{1}".format(self.dataCenter, surveyId)
		response = requests.get(baseUrl, headers=self.headers)

		if response.status_code != 200:
			if verbose: print ("error making get request for survey ({0}) -- aborted with status_code {1}".format(surveyId, response.status_code))
			return

		return response.json()


	def get_all_surveys(self):
		"""
		Get the Survey IDs of all surveys in your account

		Returns an array of SurveyIds
		"""
		baseUrl = "https://{0}.qualtrics.com/API/v3/surveys".format(self.dataCenter)
		response = requests.get(baseUrl, headers=self.headers)

		if response.status_code != 200:
			if verbose: print ("error making get request for surveys -- aborted with status_code {0}".format(response.status_code))
			return

		ids = []
		for element in response.json()['result']['elements']: ids.append("{}".format(element['id']))

		nextPage = response.json()['result']['nextPage']

		while nextPage != None:

			response = requests.get(nextPage, headers=self.headers)

			if response.status_code != 200:
				if verbose: print ("error making get request for surveys (nextPage)-- aborted with status_code {0}".format(response.status_code))
				return

			nextPage = response.json()['result']['nextPage']
			for element in response.json()['result']['elements']: ids.append(element['id'])

		return ids


	def download_responses(self, surveyId, format_type="csv", path=None):
		"""
		Download all responses from a survey

		:format_type: - string - can be csv, json, or spss (defaults to "csv")
		:path: - string - path to download the data (defaults to None)

		Returns None
		"""

		if verbose: print ("Starting to download {}".format(surveyId))

		data = '{{"surveyId": "{0}", "format": "{1}"}}'.format(surveyId, format_type)
		baseUrl = "https://{0}.qualtrics.com/API/v3/responseexports".format(self.dataCenter)
		response = requests.post(baseUrl, headers=self.headers, data=data)
		
		if response.status_code != 200:
			if verbose: print ("error making post request to initate download for survey {} -- aborted with status_code {}".format(surveyId, response.status_code))
			return

		if verbose: print ('successfully sent request to Qualtrics servers')

		key = response.json()['result']['id']

		done = False
		while not done:
			baseUrl = 'https://{0}.qualtrics.com/API/v3/responseexports/{1}'.format(self.dataCenter,key)
			response = requests.get(baseUrl, headers=self.headers)

			status = response.json()['result']['status']
			percent = response.json()['result']['percentComplete']

			if verbose: print ("\rcompletion percentage:", percent, "%", end='\r')

			if status == "complete":
				done = True

			elif status == "cancelled" or status == "failed":
				if verbose: print("error while generating download for survey {} -- aborted with status_code {}".format(surveyId, response.status_code))
				return

		if verbose: print ("\nsuccessfully generated file, attempting to download...")

		baseUrl = "https://{0}.qualtrics.com/API/v3/responseexports/{1}/file".format(self.dataCenter,key)
		response = requests.get(baseUrl, headers=self.headers, stream=True)

		if response.status_code != 200:
			if verbose: print ("error downloading file for survey {} -- aborted with status_code {}".format(surveyId, response.status_code))
			return

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
		return


	def download_all_responses(self, format_type="csv", path=None):
		"""
		Download all responses from each survey in your projects page

		:format_type: - string - can be csv, json, or spss (defaults to "csv")
		:path: - string - path to download the data (defaults to None)

		Returns None
		"""
		surveyIds = self.get_all_surveys()
		if verbose: print ("found {} total surveys in your library".format(len(surveyIds)))
		for surveyId in surveyIds:
			self.download_responses(surveyId, "csv")


	def create_sesssion(self, surveyId):
		"""
		Starts a new survey session to submit user's answers and record in qualtrics

		:surveyId: - string - survey ID of the survey to start a new response session for

		Returns JSON representing the survey sesssion
		"""
		print ("Attempting to create a new survey session") 
		
		data = "{\"language\": \"EN\"}"
		baseUrl = "https://{0}.qualtrics.com/API/v3/surveys/{1}/sessions/".format(self.dataCenter, surveyId)
		response = requests.post(baseUrl, headers=self.headers, data=data)

		
		if response.status_code != 201:
			print ("Error creating new survey session (error code: {0})".format(response.status_code))
			return None

		
		print ("Successfully created new survey session.")
		return response.json()


	def get_session(self, sessionId, surveyId):
		"""
		Get the survey session assocaited with the sessionId.

		:sessionId: - string - ID of the existing session
		:surveyId: - string - ID of that the session is associated with
	
		Returns status of the API call
		"""
		print ("Attempting to get survey session {0}".format(sessionId)) 
	
		baseUrl = "https://{0}.qualtrics.com/API/v3/surveys/{1}/sessions/{2}".format(self.dataCenter, surveyId, sessionId)	
		response = requests.get(baseUrl, headers=self.headers)

		if response.status_code != 200:
			print ("Error getting the survey session (error code: {0})".format(response.status_code))
		else: 
			print ("Successfully got the current survey session ({0})".format(sessionId))
		
		return response.json()


	def update_session(self, sessionId, surveyId):
		"""
		Update the current survey session with additional questions answered or embedded data set.

		:sessionId: - string - ID of the existing session
		:surveyId: - string - ID of that the session is associated with
	
		Returns status of the API call
		"""
		print ("Attempting to update survey session {0}".format(sessionId)) 
		data = '{"advance": false, \
		 		 "responses": { \
		    			} \
		 		}'
		baseUrl = "https://{0}.qualtrics.com/API/v3/surveys/{1}/sessions/{2}".format(self.dataCenter, surveyId, sessionId)
		
		response = requests.post(baseUrl, headers=self.headers, data=data)

		if response.status_code != 200:
			print ("Error updating the survey session (error code: {0})".format(response.status_code))
		else: 
			print ("Successfully updated the current survey session ({0})".format(sessionId))
		
		return response.json()


	def close_session(self, sessionId, surveyId):
		"""
		Close the current survey session 

		:sessionId: - string - ID of the existing session
		:surveyId: - string - ID of that the session is associated with
	
		Returns status of the API call
		"""
		print ("Attempting to close survey session {0}".format(sessionId)) 

		data = '{"close": true}'
		baseUrl = "https://{0}.qualtrics.com/API/v3/surveys/{1}/sessions/{2}".format(self.dataCenter, surveyId, sessionId)
		response = requests.post(baseUrl, headers=self.headers, data=data)

		if response.status_code != 200:
			print ("Error closing the survey session (error code: {0})".format(response.status_code))
		else:
			print ("Successfully closed the survey session.")
		return response.json()



		


	def ask_question(self, session_json):
		"""
		"""
		# if session_json['question']['type'] == 'mc':


		pass


		