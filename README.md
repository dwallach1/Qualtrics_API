# Qualtrics_API


Python scripts that use the Qualtrics APIs.


Methods for all public APIs listed [here](https://api.qualtrics.com/)

Additional methods:

* `download_all_responses` to download all responses from every survey in your library
* `delete_all_responses` delete every response of a single project
* `answer_questions` easily build the data to be sent while updating a survey session
* `create_completedResponse_event` provide the enpoint URL and the surveyId to easily create an enpoint for Qualtrics to ping when a new response is recorded