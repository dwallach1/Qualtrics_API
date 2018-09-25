import os

from qualtrics import Qualtrics


apiToken = os.environ["Q_API_TOKEN"]     
dataCenter = os.environ["Q_DATA_CENTER"] 


qualtrics = Qualtrics(apiToken, dataCenter)


# print (json.dumps(qualtrics.get_survey("SV_b2QprbVgmMwO2fr"), indent=4))
# print (qualtrics.get_all_surveys())

# qualtrics.download_responses("SV_b2QprbVgmMwO2fr")
qualtrics.download_all_responses()
