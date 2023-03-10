## Purpose

The purpose of this code is to automatically sync Pub\Sub and Google Cloud Function into your local environment. 

## Authentication

In order to use this code, you will need to authenticate with Google Cloud. You can do this by using the following command:
```
gcloud auth application-default login
```

Once you have completed authentication, you should be able to use this code to sync data between different sources.

## Usage

To use this code, follow these steps:

1. Clone this repository to your local machine.
2. Install the necessary Python packages using `pip install -r requirements.txt`.
3. Set the `PROJECT_ID` and `REGION` environment variables to the ID of your Google Cloud project and the region where you want to deploy your functions.


## Results
Running pubsub.py will create a JSON that holds a list with the following strcuture :
```
[
    "agencies-filter",
    "agencies",
    "allocate",
    "auto-reply",
    "backup",
    "gallery",
    "bq-to",
    "plate-data",
    "bq-to-pg",
    "details-filter",
    "details",
    "classification",
    "interaction-to-mimun",
    "interactions",
    "mimun_sender",
    "catalog",
    "create-mimun-lead",
    "data-gov-fetch",
```
Running main.py will create a JSON with the following structure :
```
{
  "AuthenticatedFunction": { # Your function name
    "environmentVariables": null,
    "buildEnvironmentVariables": null,
    "secret": {},
    "Pub/Sub": { # Your function Trigger type
      "topic": "projects/cc-s2s-vpn-test/topics/asdasdx",
      "failurePolicy": {}
    }
  },
  "HelloWorld": { # Your function name
    "environmentVariables": { # Your function environment variables
      "RUNTIME": "HELLO",
      "RUNTIMEE": "HELLOO"
    },
    "buildEnvironmentVariables": { # Your function build variables
      "BUILD": "TEST",
      "BUILDD": "TEST-2"
    },
    "secret": { # Your function secret
      "mysecret": {
        "version": "latest",
        "mountPath": "/path",
        "projectId": "1001384248257"
      },
      "mysecret-2": {
        "version": "latest",
        "projectId": "1001384248257"
      }
    },
    "httpsTrigger": { # Your function Trigger type
      "topic": "https://us-central1-cc-s2s-vpn-test.cloudfunctions.net/function-2",
      "failurePolicy": null
    }
  }
```
