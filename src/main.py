import os
import json

from qualtrics import Qualtrics


# # TA
# apiToken = os.environ["Q_API_TOKEN"]     
# dataCenter = os.environ["Q_DATA_CENTER"] 
# library = os.environ["Q_LIBRARY"] 

# CO
apiToken = os.environ["Q_API_TOKEN_1"]     
dataCenter = os.environ["Q_DATA_CENTER_1"]
library = os.environ["Q_LIBRARY_1"] 


qualtrics = Qualtrics(apiToken, dataCenter)



# Get JSON of survey
# print (json.dumps(qualtrics.get_survey("SV_b2QprbVgmMwO2fr"), indent=4))

# Get all surveyIds from projects page
# print (qualtrics.get_all_surveys())


# Download all responses for single survey
# qualtrics.download_responses("SV_b2QprbVgmMwO2fr")


# Download all repsonses for all surveys in project page
# qualtrics.download_all_responses()


# Try to download shared project
# qualtrics.download_responses("SV_eLPcHbH0EAg3yrX")
# print (json.dumps(qualtrics.get_survey("SV_5aufmvWxteSDxJz"), indent=4))


# Create new survey session
# session = qualtrics.create_sesssion("SV_eDwgadvLh4MLhf7")
# print (json.dumps(session, indent=4))
# sessionId = session['result']['sessionId']


# Update an existing session
# sessionId = "FS_Q51Cum30LK1z85j"
# session_update_response = qualtrics.update_session("FS_8crClCLWYZNwBKV","SV_eDwgadvLh4MLhf7")
# print (json.dumps(session_update_response, indent=4))


# Get an exisitng session
# sessionId = "FS_Q51Cum30LK1z85j"
# session_get_response = qualtrics.get_session("FS_Q51Cum30LK1z85j","SV_eDwgadvLh4MLhf7")
# print (json.dumps(session_get_response, indent=4))



# Close an existing session
# sessionId = "FS_8crClCLWYZNwBKV"
# session_close_response = qualtrics.close_session("FS_8crClCLWYZNwBKV","SV_eDwgadvLh4MLhf7")
# print (json.dumps(session_close_response, indent=4))


# Create new event to ping server on completed responses
# qualtrics.create_completedResponse_event("SV_3x5FBTgEtBVZdpH", "http://fc014752.ngrok.io")







