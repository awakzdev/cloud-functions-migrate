from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
import json
import os

'''
Utilizes Google Cloud SDK's to fetch all Google Cloud Functions topics.
Authentication is applied using the following command - **`gcloud auth application-default login`**.
This code uses the .env variable to set your PROJECT / REGION.
'''

# Load environment variables
load_dotenv()

PROJECT = os.getenv('PROJECT')
REGION  = os.getenv('REGION')

def fetch(project, region):
    '''
    Fetches information about all Cloud Functions in the given project and region.
    Stores the function information in a dictionary, and writes it to a JSON file.
    
    Parameters:
    PROJECT (str): The ID of the Google Cloud project.
    REGION (str): The region in which the functions are located.
    '''
    # Instantiate the client
    service = build('cloudfunctions', 'v1')

    # Retrieve the list of functions for the specified region
    parent = os.path.join("projects", PROJECT, "locations", REGION).replace('\\', '/')
    try:
        functions = service.projects().locations().functions().list(parent=parent).execute()
    except HttpError as err:
        resp = json.loads(err.content)
        if resp.get('error', {}).get('code') == 403:
            print("User doesn't have permissions to %s or it doesn't exist" % (parent))
            return
        else:
            raise

    # Initialize dictionary to store function information
    function_info = {}
    try:
        for function in functions['functions']:
            # Extract information about the function
            function_name = function['name'].split('/')[-1]

            # Extract environment variables
            env_vars = function.get('environmentVariables')
            build_env_vars = function.get('buildEnvironmentVariables')

            # Extract secrets
            secrets = {}
            secret_env_vars = function.get('secretEnvironmentVariables')
            if secret_env_vars:
                secrets['secretEnvironmentVariables'] = [{'key': sev['key'], 'projectId': sev['projectId'], 'secret': sev['secret'], 'version': sev['version']} for sev in secret_env_vars]

            if 'secretVolumes' in function:
                secrets['secretVolumes'] = [{'mountPath': sv['mountPath'], 'projectId': sv['projectId'], 'secret': sv['secret'], 'versions': [{'version': v['version'], 'path': v.get('path')} for v in sv.get('versions', [])]} for sv in function['secretVolumes']]

            # Extract trigger type and topic/url
            trigger_type = None
            trigger_topic_url = None
            if 'eventTrigger' in function:
                event_trigger = function['eventTrigger']
                trigger_type = 'eventTrigger'
                trigger_topic_url = event_trigger.get('resource')
                eventType = event_trigger.get('eventType')
                failure_policy = event_trigger.get('failurePolicy', {})
            elif 'httpsTrigger' in function:
                trigger_type = 'httpsTrigger'
                trigger_topic_url = function['httpsTrigger']['url']
                failure_policy = None

            # Extact additional information
            runtime = function.get('runtime')
            entry_point = function.get('entryPoint')
            timeout = function.get('timeout').strip('s')
            available_memory_mb = function.get('availableMemoryMb')

            # Extract additional function settings
            function_info[function_name] = {
                'runtime': runtime,
                'entryPoint': entry_point,
                'timeout': timeout,
                'available_memory_mb': available_memory_mb,
                'environmentVariables': env_vars,
                'buildEnvironmentVariables': build_env_vars,
                'secrets': secrets,
                trigger_type: {
                    "resource": trigger_topic_url,
                    "eventType": eventType,
                    'failurePolicy': failure_policy
                } if trigger_type == 'eventTrigger' else {'url': trigger_topic_url}
            }

            # Log the function information
            print(f"Function '{function_name}' found and added to function_info")
    except KeyError:
        print('No functions found in project', project, 'and region', region)

    # Write function information to JSON file
    with open('function_info.json', 'w') as f:
        json.dump(function_info, f, indent=2)


if __name__ == '__main__':
    fetch(PROJECT, REGION)
