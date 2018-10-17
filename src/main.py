import os
import json
from qualtrics import Qualtrics


# CA
# apiToken = os.environ["Q_API_TOKEN"]     
# dataCenter = os.environ["Q_DATA_CENTER"] 
# library = os.environ["Q_LIBRARY"] 

# CO
apiToken = os.environ["Q_API_TOKEN_1"]     
dataCenter = os.environ["Q_DATA_CENTER_1"]
# library = os.environ["Q_LIBRARY_1"] 


# apiToken = "test"
# dataCenter = "test"

qualtrics = Qualtrics(apiToken, dataCenter)



print ("{} errored".format(qualtrics.download_all_responses(format="csv")))


# qualtrics.download_responses(surveyId="SV_7VxdTzu3DoPzIfb", format="csv", limit="2")
# qualtrics.download_responses_new(surveyId="SV_7VxdTzu3DoPzIfb", format="csv", limit="2")