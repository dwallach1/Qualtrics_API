import os, sys
import requests
import zipfile, io
import json

apiToken = os.environ["Q_API_TOKEN"]     
dataCenter = os.environ["Q_DATA_CENTER"] 
libraryId = os.environ["Q_LIBRARY"]

headers = {
	"X-API-TOKEN": apiToken,
	"Content-Type": "application/json",
}


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



def get_mailinglist():
	"""
	check if there exists a mailinglist for the echo. If not,
	create one. It's name will be the applicationId of the Echo skill

	Returns the MailinglistId associated with this project
	"""

	baseUrl = "https://{0}.qualtrics.com/API/v3/mailinglists".format(dataCenter)
	response = requests.get(baseUrl, headers=headers)

	for elem in response.json()['result']['elements']:
		if elem['name'] == appId:
			return elem['id']


	# no mailinglist for this application exists -- create a new one
	data = '{{"libraryId": "{0}", "name": "{1}"}}'.format(libraryId, appId)
	response = requests.post(baseUrl, headers=headers, data=data)

	if response.status_code != 200:
		print ('error creating new mailinglist for {}\'s connected Qualtrics project'.format(appId))
		return

	return response.json()['result']['id']


def get_contact(mailinglistId):
	"""
	check if there exists a contact in the mailinglist for the userId. If not,
	create one. It's email will be the userId@echo.com of the Echo skill

	Returns the contactId associated with the echo making the call
	"""

	baseUrl = "https://{0}.qualtrics.com/API/v3/mailinglists/{1}/contacts".format(dataCenter, mailinglistId)
	response = requests.get(baseUrl, headers=headers)


	if response.status_code != 200:
		print ('error finding retrieving contacts from Qualtrics for mailinglist {}'.format(mailinglistId))
		return

	nextPage = response.json()['result']['nextPage']
	contacts = response.json()['result']['elements']

	while nextPage:

		response = requests.get(nextPage, headers=headers)


		if response.status_code != 200:
			print ('error finding retrieving contacts (nextPage) from Qualtrics for mailinglist {}'.format(mailinglistId))
			return


		nextPage = response.json()['result']['nextPage']
		contacts.extend(response.json()['result']['elements'])

	this_echo = "{}@echo.com".format(userId)

	for contact in contacts:
		if this_echo == contact['email']:
			return contact['id']


	# no contact for this echo exists -- create a new one
	data = '{{"email": "{0}", "externalDataRef": "{1}"}}'.format(this_echo, userId) 
	response = requests.post(baseUrl, headers=headers, data=data)

	if response.status_code != 200:
		print ('error creating new contact for {}'.format(this_echo))
		return

	return response.json()['result']['id']




def Qualtrics_connect():
	"""
	"""
	mailinglistId = get_mailinglist()
	contactId = get_contact(mailinglistId)






