import requests
import json
import os


def getCreds():
    creds = dict()
    creds['access_token'] = os.environ.get('IG_ACCESS_TOKEN')
    creds['client_id'] = os.environ.get('IG_CLIENT_ID') #ig app id
    creds['graph_domain'] = 'https://graph.facebook.com/'
    creds['graph_version'] = 'v15.0'
    creds['endpoint_base'] = creds['graph_domain'] + creds['graph_version'] + '/'
    creds['debug'] = 'no'
    creds['page_id'] = os.environ.get('FB_PAGE_ID') # users page id
    creds['instagram_account_id'] = os.environ.get('IG_ACCOUNT_ID') # users instagram account id
    creds['ig_username'] = 'legoholka' # ig username

    return creds


def makeApiCall(url, endpointParams, debug='no'):
    data = requests.get(url, endpointParams)

    response = dict()
    response['url'] = url
    response['endpoint_params'] = endpointParams
    response['endpoint_params_pretty'] = json.dumps(endpointParams, indent = 4)
    response['json_data'] = json.loads(data.content)
    response['json_data_pretty'] = json.dumps(response['json_data'], indent = 4)

    if ('yes' == debug):
        displayApiCallData(response)

    return response


def displayApiCallData(response):
    print("URL:\n")
    print(response['url'])
    print("\nEndpoint Params: \n")
    print(response['endpoint_params_pretty'])
    print("\nResponse:\n")
    print(response['json_data_pretty'])
    return response
