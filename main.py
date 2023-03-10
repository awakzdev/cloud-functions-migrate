from googleapiclient.discovery import build
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
    project (str): The ID of the Google Cloud project.
    region (str): The region in which the functions are located.
    '''
    # Instantiate the client
    service = build('cloudfunctions', 'v1')

    # Retrieve the list of functions for the specified region
    functions = service.projects().locations().functions().list(parent=f"projects/{PROJECT}/locations/{REGION}").execute()

    # Initialize dictionary to store function information
    function_info = {}

    for function in functions['functions']:
        # Extract information about the function
        function_name = function['name'].split('/')[-1]

        # Extract environment variables
        env_vars = function.get('environmentVariables')
        build_env_vars = function.get('buildEnvironmentVariables')

        # Extract secrets
        secrets = {}
        if 'secretVolumes' in function:
            for secret_volume in function['secretVolumes']:
                secret = secret_volume['secret']
                secret_versions = secret_volume.get('versions', [])
                if secret_versions:
                    secrets[secret] = {
                        'version': secret_versions[0]['version'],
                        'mountPath': secret_volume['mountPath'],
                        'projectId': secret_volume['projectId']
                    }

        secret_env_vars = function.get('secretEnvironmentVariables')
        if secret_env_vars:
            for secret_env_var in secret_env_vars:
                secret = secret_env_var['secret']
                secrets[secret] = {
                    'version': secret_env_var['version'],
                    'projectId': secret_env_var['projectId']
                }

        # Extract trigger type and topic/url
        trigger_type = None
        trigger_topic_url = None
        if 'eventTrigger' in function:
            event_trigger = function['eventTrigger']
            trigger_type = 'Pub/Sub'
            trigger_topic_url = event_trigger.get('resource')
            failure_policy = event_trigger.get('failurePolicy', {})
            if failure_policy.get('retry'):
                failure_policy['retry'] = {'retryCount': 5, 'maxRetryDuration': '120s'}
        elif 'httpsTrigger' in function:
            trigger_type = 'httpsTrigger'
            trigger_topic_url = function['httpsTrigger']['url']
            failure_policy = None

        # Add function information to dictionary
        function_info[function_name] = {
            'environmentVariables': env_vars,
            'buildEnvironmentVariables': build_env_vars,
            'secret': secrets,
            trigger_type: {
                'topic': trigger_topic_url,
                'failurePolicy': failure_policy
            } if trigger_type else {}
        }

    # Write function information to JSON file
    with open('function_info.json', 'w') as f:
        json.dump(function_info, f, indent=2)

    print(functions)
    # Write function information to JSON file
    with open('function_info.json', 'w') as f:
        json.dump(function_info, f, indent=2)


if __name__ == '__main__':
    fetch(PROJECT, REGION)
