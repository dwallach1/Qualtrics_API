# Qualtrics_API


Python scripts that use the Qualtrics APIs.


Methods for all public APIs listed [here](https://api.qualtrics.com/)

The currently (constantly updating) supported methods:

* `list_surveys` ([documentation](https://api.qualtrics.com/docs/list-surveys))
* `get survey` ([documentation](https://api.qualtrics.com/docs/get-survey))

### Custom Methods

* `retake_response` allows you to reake a repsonse. Old surveys built on Qualtrics' old engine (not JFE) are not compatible with this call. This is because how the baseURL is formatted. 

		**Parameters**  

		* `surveyId` (string) --> the survey that the response is associated with
		* `responseId` (string) --> the specific ID of the response you want to retake
		* `delete` (bool) --> defaults to False, this allows you to either delete the old response that you are retaking or "retake as new response" and keep the prior response as well


* `retake_unfinished_responses` allows you to reake all unfinished repsonses assicated with a survey. Old surveys built on Qualtrics' old engine (not JFE) are not compatible with this call. This is because how the baseURL is formatted. 


		**Parameters** 

		* `surveyId` (string) --> the survey that the response is associated with
		* `delete` (bool) --> defaults to False, this allows you to either delete the old response that you are retaking or "retake as new response" and keep the prior response as well


* `retake_unfinished_responses` allows you to reake all unfinished repsonses assicated with a survey. Old surveys built on Qualtrics' old engine (not JFE) are not compatible with this call. This is because how the baseURL is formatted. 


		**Parameters** 

		* `surveyId` (string) --> the survey that the response is associated with
		* `delete` (bool) --> defaults to False, this allows you to either delete the old response that you are retaking or "retake as new response" and keep the prior response as well


## Dependencies 

* Selenium
* requests