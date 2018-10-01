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

		:apiToken: - string - the API token found in your account settings > Qualtrics IDs
		:dataCenter: - string - the datacenter your data is stored in

		Returns a new initalized object 
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


	def download_responses(self, surveyId, format_type="csv", path=None, download=True):
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


	def answer_questions(self, session, QIDs, answers, advance=False):
		"""
		Builds out the data to be sent back to update 

		:session: - JSON - the JSON returned from either create_session or get_session
		:QIDs: - list - list of question IDs 
		:answers: - list - list of associated answers to each question
		:anvance: - bool - required parameter of the update session API call

		Returns the data to be passed with the update_session API call
		"""

		if advance:
			advance = "true"
		else:
			advance = "false"

		answer_builder = []

		for i, QID in enumerate(QIDs):
			if session['result']['question']['type'] == 'mc':
				if isinstance(answers[i], list):
					for j in answers[i]:

						pass



				elif isinstance(answers[i], int) or isinstance(answers[i], str):
					answer_str = '"{{ {0}": {{"{1}": {{ "selected": true }} }} }}'.format(QID, answers[i])
					answer_builder.append(answer_str)
					

				else:
					print ("unsupported answer type for multilpe choice question {}".format(type(answers[i])))
					return -1

			elif session['result']['question']['type'] == 'te':

				if isinstance(answers[i], str):
					answer_str = '"{0}": "{1}"'.format(QID, answers[i])
					answer_builder.append(answer_str)

				else:
					print ("unsupported answer type for multilpe choice question {}".format(type(answers[i])))
					return -1

			else:
				print ("Question type {0} is not currently supported by the session API (QID: {1})".format(session['result']['question']['type'], QID))
				return -1


		answers = ""
		for answer in answer_builder:
			answers += answer + ','
		data = '{"advance": {0}, "responses": {{  {1} }} }'.format(advance, answers)
		print (data)
		return data


	def update_response(self, surveyId, responseId, embeddedData):
		"""
		Update embedded data of survey response

		:surveyId: - string - 
		:responseId: - string - 
		:embeddedData: - string of dict - 

		Returns response code of API call (200 = success)
		"""
		baseUrl = "https://{0}.qualtrics.com/API/v3/responses/{1}".format(self.dataCenter, responseId)
		data = '{{"surveyId": "{0}", "embeddedData": {1}}}'.format(surveyId, embeddedData)
		# print (data)
		response = requests.put(baseUrl, headers=self.headers, data=data)

		return response.status_code


	def delete_response(self, surveyId, responseId, decrementQuotas=True):
		"""
		Delete a survey response

		:surveyId: - string - the ID of the survey you want to delete the responses from
		:responseId: - string - the ID of the response you want to delete
		:decrementQuotas: - boolean -  whether or not you want to decrement the quotas associated with the responses

		Returns response code of API call (200 = success)
		"""
		if decrementQuotas:
			decrementQuotas = "true"
		else:
			decrementQuotas = "false"

		baseUrl = "https://{0}.qualtrics.com/API/v3/responses/{1}?surveyId={2}&decrementQuotas={3}".format(self.dataCenter, responseId, surveyId, decrementQuotas)
		print (baseUrl)
		response = requests.delete(baseUrl, headers=self.headers)

		return response.status_code
		


	def delete_all_responses(self, surveyId, decrementQuotas=True):
		"""
		Delete all the responses in a survey

		:surveyId: - string - the ID of the survey you want to delete the responses from
		:decrementQuotas: - boolean - whether or not you want to decrement the quotas associated with the responses

		Returns a list of the responseIds that errored
		"""
		content = self.download_responses(surveyId)

		print (content)

		rID = 0
		responseIds = []

		for i, line in enumerate(content):
			if i == 0:
				for j, val in enumerate(line.split(',')):
					if val == "ResponseId":
						rID = j
			else:
				responseIds.append(line.split(',')[rID])

		total = len(responseIds)
		errors = []
		for responseId in responseIds:
			val = self.delete_response(surveyId, responseId)
			if val != 200:
				errors.append(responseId)

		print ("Deleted {}/{} responses".format(total - len(errors), total))
		return errors



	def create_completedResponse_event(self, surveyId, serverURL):
		"""
		Create an endpoint for QUaltrics to ping when a completed response is processed

		:surveyId: - string - the ID of the survey you want to delete the responses from
		:serverURL: - string - the server endpoint for Qualtrics to ping

		Returns the response from the API call
		"""
		baseUrl = "https://{0}.qualtrics.com/API/v3/eventsubscriptions".format(self.dataCenter)
		data = '{"topics": "surveyengine.completedResponse.{}", "publicationUrl": "{}"}'.format(surveyId, serverURL)
		# print(data)
		response = requests.post(baseUrl, headers=self.headers, data=data)

		return response.json()









