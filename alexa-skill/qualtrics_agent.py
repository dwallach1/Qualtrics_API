import os, sys
import requests
import json
import datetime

apiToken = os.environ["Q_API_TOKEN"]     
dataCenter = os.environ["Q_DATA_CENTER"] 
libraryId = os.environ["Q_LIBRARY"]

surveyId = 'SV_01dtmd5EwhWdP7v'

headers = {
	"X-API-TOKEN": apiToken,
	"Content-Type": "application/json",
}

"""

from ask_sdk_core.skill_builder import SkillBuilder

sb = SkillBuilder()


from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard

class LaunchRequestHandler(AbstractRequestHandler):
     def can_handle(self, handler_input):
         # type: (HandlerInput) -> bool
         return is_request_type("LaunchRequest")(handler_input)

     def handle(self, handler_input):
         # type: (HandlerInput) -> Response
         speech_text = "Welcome to the Alexa Skills Kit, you can say hello!"

         handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(
            False)
         return handler_input.response_builder.response

class HelloWorldIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Hello World"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(
            True)
        return handler_input.response_builder.response

class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "You can say hello to me!"

        handler_input.response_builder.speak(speech_text).ask(speech_text).set_card(
            SimpleCard("Hello World", speech_text))
        return handler_input.response_builder.response

class CancelAndStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.CancelIntent")(handler_input)
                 or is_intent_name("AMAZON.StopIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Goodbye!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text))
        return handler_input.response_builder.response

class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # any cleanup logic goes here

        return handler_input.response_builder.response


from ask_sdk_core.dispatch_components import AbstractExceptionHandler

class AllExceptionHandler(AbstractExceptionHandler):

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        # Log the exception in CloudWatch Logs
        print(exception)

        speech = "Sorry, I didn't get it. Can you please say it again!!"
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response



sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_exception_handler(AllExceptionHandler())

handler = sb.lambda_handler()



userId = event['session']['user']['userId']
appId = event['context']['application']['applicationId'].split('.')[-1]
"""

userId = "alexa-test-userid"
appId = "alexa-test-appId"


def get_mailinglist():
	"""
	check if there exists a mailinglist for the echo. If not,
	create one. It's name will be the applicationId of the Echo skill

	Returns the MailinglistId associated with this project
	"""

	print ("Attempting to find {0}'s associated contact list".format(appId))

	baseUrl = "https://{0}.qualtrics.com/API/v3/mailinglists".format(dataCenter)
	response = requests.get(baseUrl, headers=headers)

	if response.status_code != 200:
		print ("Error retrieving potential mailinglists for {} (error code: {1})".format(appId, response.status_code))
		return None

	for elem in response.json()['result']['elements']:
		if elem['name'] == appId:
			print ("Found a mailinglist ({0}) associated with {1}".format(elem['id'], appId))
			return elem['id']


	# no mailinglist for this application exists -- create a new one
	print ("No mailinglist associated with {0} exists. Creating a new one".format(appId))

	data = '{{"libraryId": "{0}", "name": "{1}"}}'.format(libraryId, appId)
	response = requests.post(baseUrl, headers=headers, data=data)

	if response.status_code != 200:
		print ("Error creating new mailinglist for {0} (error code: {1})".format(appId, response.status_code))
		return None

	print("Successfully created a new mailinglist")
	return response.json()['result']['id']


def get_contact(mailinglistId):
	"""
	check if there exists a contact in the mailinglist for the userId. If not,
	create one. It's email will be the userId@echo.com of the Echo skill

	Returns the contactId associated with the echo making the call
	"""

	print ("Attempting to find this {0}'s associated contact in the mailinglist {1}".format(userId, mailinglistId)) 

	baseUrl = "https://{0}.qualtrics.com/API/v3/mailinglists/{1}/contacts".format(dataCenter, mailinglistId)
	response = requests.get(baseUrl, headers=headers)


	if response.status_code != 200:
		print ("Error finding retrieving contacts from mailinglist {0} (error code: {1})".format(mailinglistId, response.status_code))
		return None

	nextPage = response.json()['result']['nextPage']
	contacts = response.json()['result']['elements']

	while nextPage:

		response = requests.get(nextPage, headers=headers)

		if response.status_code != 200:
			print ("Error finding retrieving contacts (nextPage) for mailinglist {0} (error code: {1})".format(mailinglistId, response.status_code))
			return None

		nextPage = response.json()['result']['nextPage']
		contacts.extend(response.json()['result']['elements'])

	this_echo = "{}@echo.com".format(userId)

	for contact in contacts:
		if this_echo == contact['email']:
			return contact


	# no contact for this echo exists -- create a new one
	print ("No contact associated with {0} exists. Creating a new one".format(appId))

	data = '{{"email": "{0}", "externalDataRef": "{1}"}}'.format(this_echo, userId) 
	response = requests.post(baseUrl, headers=headers, data=data)

	if response.status_code != 200:
		print ("Error creating new contact for {0} (error code: {1})".format(this_echo, response.status_code))
		return None

	print ("Successfully created a new contact.")
	return response.json()['result']['id']


def update_contact(mailinglistId, contact):
	"""
	Update the associated contact for this project in the Qualtrics application.
	This allows you to track user interactions.
	"""
	if isinstance(contact, str):
		contactId = contact
		timesSurveyed = 0
	else:
		contactId = contact['id']
		timesSurveyed = 0 if contact['embeddedData'] == None else contact['embeddedData']['TimesSurveyed']

	now = str(datetime.datetime.now())

	data = '{{"embeddedData": {{ "LastSurveyed": "{0}", "TimesSurveyed": "{1}"}}}}'.format(now, int(timesSurveyed)+1) 
	baseUrl = "https://{0}.qualtrics.com/API/v3/mailinglists/{1}/contacts/{2}".format(dataCenter, mailinglistId, contactId)
	response = requests.put(baseUrl, headers=headers, data=data)

	if response.status_code != 200:
		print ("Error updating contact {0} (error code: {1})".format(contactId, response.status_code))
		return None
	
	print ("Successfully recorded interation in Qualtrics.")
	return None


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

	
	print ("Successfully created new survey session ({0}).".format(survey_sessionId))
	return response.json()


def update_survey_session(survey_sessionId):
	"""
	Update the current survey session with additional questions answered.
	"""
	print ("Attempting to update survey session {0}".format(survey_sessionId)) 
	data = '{{"close": "True"}}'
	baseUrl = "https://{0}.qualtrics.com/API/v3/surveys/{1}/sessions/{2}".format(dataCenter, surveyId)
	
	response = requests.post(baseUrl, headers=headers, data=data)

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


def ask(question):
	"""
	"""
	pass


def Qualtrics_connect():
	"""
	Parent function for communicating with Qualtrics APIs
	"""
	print ("Connecting to Qualtrics' servers...")
	survey_session = create_survey_session()
	survey_sessionId = survey_session['result']['sessionId']
	questions = survey_session['result']['questions']
	for question in questions:
		ask(question)

	# update_survey_session(survey_sessionId)
	# close_survey_session(survey_sessionId)


	# mailinglistId = get_mailinglist()
	# contact = get_contact(mailinglistId)
	# update_contact(mailinglistId, contact)

	

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



Qualtrics_connect()

