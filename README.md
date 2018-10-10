# Qualtrics_API


Python scripts that use the Qualtrics APIs.


Methods for all public APIs listed [here](https://api.qualtrics.com/)

Additional methods:

* `download_all_responses` to download all responses from every survey in your library
* `delete_all_responses` delete every response of a single project
* `answer_questions` easily build the data to be sent while updating a survey session
* `create_completedResponse_event` provide the enpoint URL and the surveyId to easily create an enpoint for Qualtrics to ping when a new response is recorded

### Custom Methods

* `retake_response` allows you to reake a repsonse. Old surveys built on Qualtrics' old engine (not JFE) are not compatible with this call. This is because how the baseURL is formatted. 

Parameters: 

* `surveyId` (string) --> the survey that the response is associated with
* `responseId` (string) --> the specific ID of the response you want to retake
* `delete` (bool) --> defaults to False, this allows you to either delete the old response that you are retaking or "retake as new response" and keep the prior response as well


* `retake_unfinished_responses` allows you to reake all unfinished repsonses assicated with a survey. Old surveys built on Qualtrics' old engine (not JFE) are not compatible with this call. This is because how the baseURL is formatted. 
<br />
Parameters: 
<br />
* `surveyId` (string) --> the survey that the response is associated with
* `delete` (bool) --> defaults to False, this allows you to either delete the old response that you are retaking or "retake as new response" and keep the prior response as well



## Dependencies 

* Selenium
* requests