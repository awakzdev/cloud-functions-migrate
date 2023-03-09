# Catalog Sync Cloud Functions
Utilizes Google Cloud SDK's to fetch all Cloud Functions and download their source code.

## Purpose

The purpose of this code is to automatically sync catalog data between multiple Google Cloud Functions into your local environment. 
The code retrieves catalog data from a source.

## Authentication

In order to use this code, you will need to authenticate with Google Cloud. You can do this by using the following command:
```
gcloud auth application-default login
```

Once you have completed authentication, you should be able to use this code to sync catalog data between different sources.

## Usage

To use this code, follow these steps:

1. Clone this repository to your local machine.
2. Install the necessary Python packages using `pip install -r requirements.txt`.
3. Set the `PROJECT_ID` and `REGION` environment variables to the ID of your Google Cloud project and the region where you want to deploy your functions.
4. Run `python main.py` to pull the Cloud Functions data.
