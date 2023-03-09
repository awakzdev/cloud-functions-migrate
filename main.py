from googleapiclient.discovery import build
from google.cloud import storage
from dotenv import load_dotenv
import os

'''
Utilizes Google Cloud SDK's to fetch all Cloud Functions and download their source code.
Authentication is applied using the following command - **`gcloud auth application-default login`**.
This code uses the .env variable to set your PROJECT / REGION.
'''

# Load environment variables
load_dotenv()

# Instantiate the client
client = storage.Client()

PROJECT = os.getenv('PROJECT')
REGION  = os.getenv('REGION')

'''
Snippet below will grab cloud-functions API and print the following:
1. File name
2. Function name
3. Bucket name
And download the contents into the current directory
'''
def fetch(project, region):
    service = build('cloudfunctions', 'v1')

    # Retrieve the list of functions for the specified region
    functions = service.projects().locations().functions().list(parent=f"projects/{PROJECT}/locations/{REGION}").execute()
    # print(functions) Will print complete dictionary of cloud function

    for function in functions['functions']:
        # Extract information about the function
        function_name = function['name'].split('/')[-1]
        bucket_name   = function['sourceArchiveUrl'].split('/')[2]
        file_name     = function['sourceArchiveUrl'].split('/')[3]
        print(f"\nBucket name - {bucket_name}")
        print(f"Function name - {function_name}")
        print(f"File - {file_name}")

        # Create a new directory with the buckets name
        current = os.getcwd()
        bucket_dir = os.path.join(os.getcwd(), bucket_name)
        os.makedirs(bucket_dir, exist_ok=True)
        os.chdir(bucket_dir)

        # Download the file
        bucket = client.bucket(bucket_name)
        blob   = bucket.blob(file_name)
        file_content = blob.download_as_bytes()

        # Save the file to disk
        with open(file_name, 'wb') as f:
            f.write(file_content)

        # Create a text file containing the function our code belongs to
        with open("functions.txt", 'a') as f:
            f.write(f"{function_name}\n")

        # Return to original directory
        os.chdir(current)

if __name__ == '__main__':
    project_id = os.getenv('PROJECT')
    region = os.getenv('REGION')
    fetch(project_id, region)
