import os, sys
import requests
import json
import datetime

apiToken = os.environ["Q_API_TOKEN"]     
dataCenter = os.environ["Q_DATA_CENTER"] 
libraryId = os.environ["Q_LIBRARY"]

surveyId = 'SV_eDwgadvLh4MLhf7'

headers = {
	"X-API-TOKEN": apiToken,
	"Content-Type": "application/json",
}




def create_survey_session():
	"""
	Starts a new survey session to submit user's answers and record in qualtrics
	"""
	print ("Attempting to create a new survey session") 
	
	data = "{\"language\": \"EN\"}"
	baseUrl = "https://{0}.qualtrics.com/API/v3/surveys/{1}/sessions/".format(dataCenter, surveyId)
	response = requests.post(baseUrl, headers=headers, data=data)

	
	# pp.pprint (response.json())

	if response.status_code != 201:
		print ("Error creating new survey session (error code: {0})".format(response.status_code))
		return None

	
	print ("Successfully created new survey session.")
	return response.json()


def update_survey_session(survey_sessionId):
	"""
	Update the current survey session with additional questions answered.
	"""
	print ("Attempting to update survey session {0}".format(survey_sessionId)) 

	
	"""
	the commented out data successfully updates a MC question, but can we update a text entry question
	"""

	# data = '{"advance": false, \
	# 		 "responses": { \
	# 		   "QID3": { \
	# 		      "1": { \
	# 		      	"selected": true \
	# 		      	} \
	# 		      } \
	# 		    } \
	# 		 }'

	"""
	the commented out data successfully updates a TE question, but can we update a text entry question
	"""

	# data = '{"advance": true, \
	# 		 "responses": { \
	# 		   "QID2": \
	# 		   		"test text (updated)"			\
	# 		    } \
	# 		 }'

	"""
	now we need to figure out how to update a form
	"""

	data = '{"advance": false, \
			 "responses": { \
			   "QID1":  \
			  	  "test@email.com" 		\
			    } \
			 }'

	# print (data)
	
	baseUrl = "https://{0}.qualtrics.com/API/v3/surveys/{1}/sessions/{2}".format(dataCenter, surveyId, survey_sessionId)
	
	response = requests.post(baseUrl, headers=headers, data=data)

	print (json.dumps(response.json(), indent=4))

	if response.status_code != 200:
		print ("Error updating the survey session (error code: {0})".format(response.status_code))
		return None

	print ("Successfully updated the current survey session ({0})".format(survey_sessionId))
	return None


def close_survey_session(survey_sessionId):
	"""
	Close the current survey session. 
	"""
	print ("Attempting to close survey session {0}".format(survey_sessionId)) 

	data = '{{"close": "True"}}'
	baseUrl = "https://{0}.qualtrics.com/API/v3/surveys/{1}/sessions/{2}".format(dataCenter, surveyId)
	response = requests.post(baseUrl, headers=headers, data=data)

	if response.status_code != 200:
		print ("Error closing the survey session (error code: {0})".format(response.status_code))
		return None

	print ("Successfully closed the survey session.")
	return None




def Qualtrics_connect():
	"""
	Parent function for communicating with Qualtrics APIs
	"""
	# print ("Connecting to Qualtrics' servers...")
	# survey_session = create_survey_session()
	# survey_sessionId = survey_session['result']['sessionId']
	# print (json.dumps(survey_session, indent=4))
	
	sessionId = "FS_0PQylAzReUcsKZ3"
	update_survey_session(sessionId)





Qualtrics_connect()

