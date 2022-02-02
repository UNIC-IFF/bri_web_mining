import dotenv
import os
from googleapiclient.discovery import build
import json

dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
google_api_key = os.getenv('google_api_key')
cse_key = os.getenv('cse_key')
resource = build("customsearch", 'v1', developerKey=google_api_key).cse()


def api_search_engine(query, action, country=None, word=None, keyword=None, daterange=None):

    # query = 'intext:{} ~{} ~({})'.format(
    #             country.lower(), word, action)

    # sort="date:r:20210101:20211231"

    result = resource.list(q=query, hq=action, cx=cse_key).execute()
    # , sort="date:r:20210101:20211231"
    # result_json = json.dumps(result, indent=4)
    
    if (country != None):
        print('    {} TOTAL RESULTS:\n        country: {}\n        positive_statement: {}\n        action: {}\n        total_results: {}\n        query: {}\n'.format(keyword.upper(), country, word, action, json.dumps(
            result["searchInformation"]["formattedTotalResults"]), query))
    else:
        print('    query: ', query)
    return result
