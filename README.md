# Qualtrics_API


Python scripts that use the Qualtrics APIs.

```python

import Qualtrics

apiToken = os.environ["Q_API_TOKEN"]     
dataCenter = os.environ["Q_DATA_CENTER"] 

qualtrics = Qualtrics(apiToken, dataCenter)

qualtrics.download_all_responses()

```

### To Do

[ ] add pagination to list_groups
[ ] add support for divisionId to list_groups



Methods for all public APIs listed [here](https://api.qualtrics.com/)

The currently (constantly updating) supported methods:

* `list_surveys` (List Surveys API [documentation](https://api.qualtrics.com/docs/list-surveys))
* `get survey` (Get Survey API [documentation](https://api.qualtrics.com/docs/get-survey))
* `list_groups` (List Groups API [documentation](https://api.qualtrics.com/docs/list-groups)) 
* `get_group` (Get Group API [documentation](https://api.qualtrics.com/docs/get-group))
* `update_response`
* `delete_response`
* `create_session`
* `get_session`
* `update_session`
* `close_session`


### Custom Methods

* `retake_response` allows you to reake a repsonse. Old surveys built on Qualtrics' old engine (not JFE) are not compatible with this call. This is because how the baseURL is formatted. 

		Parameters  

		* surveyId (string) --> the survey that the response is associated with
		* responseId (string) --> the specific ID of the response you want to retake
		* delete (bool) --> defaults to False, this allows you to either delete the old response that you are retaking or "retake as new response" and keep the prior response as well


* `retake_unfinished_responses` allows you to reake all unfinished repsonses assicated with a survey. Old surveys built on Qualtrics' old engine (not JFE) are not compatible with this call. This is because how the baseURL is formatted. 


		Parameters

		* surveyId (string) --> the survey that the response is associated with
		* delete (bool) --> defaults to False, this allows you to either delete the old response that you are retaking or "retake as new response" and keep the prior response as well


* `get_all_surveys` returns an array of the JSON objects for each survey returned from a get_survey call. (No parameters)


* `download_responses` first creates the response export, then once the file is ready to be downloaded, it initates the download by either writing it to disk or unzipping the data in memory and returning it.


		Parameters

		* surveyId (string) --> the survey that the response is associated with
		* format_type (string) --> defaults to csv, can be json, csv, csv2013, or spss
		* lastResponseId (string) --> 	Export all responses received after the specified response. This parameter will be ignored if you use the startDate parameter
		* startDate (string) --> Only export responses recorded after the specified date. Using this parameter causes the API to ignore lastResponseId
		* endDate (string) --> Only exports responses recorded before the specified date
		* limit (int) --> Maximum number of responses exported

		...

* `download_responses_new` first creates the response export, then once the file is ready to be downloaded, it initates the download by either writing it to disk or unzipping the data in memory and returning it. This gets data from the new Data rather than the Legacy format.


		Parameters

		* surveyId (string) --> the survey that the response is associated with
		* format_type (string) --> defaults to csv, can be json, csv, csv2013, or spss
		* lastResponseId (string) --> 	Export all responses received after the specified response. This parameter will be ignored if you use the startDate parameter
		* startDate (string) --> Only export responses recorded after the specified date. Using this parameter causes the API to ignore lastResponseId
		* endDate (string) --> Only exports responses recorded before the specified date
		* limit (int) --> Maximum number of responses exported

		...

* `download_all_responses` allows you to download all of the data associated with all of your surveys. This call will create a directory called "downloads" at whatever path the call is made from. 
	
		Parameters

		* format_type (string) --> defaults to csv, can be json, csv, csv2013, or spss


* `delete_all_responses` allows you to delete all of your data and clear out all of your responses associated with all of your data.



## Dependencies 

* Selenium
* requests