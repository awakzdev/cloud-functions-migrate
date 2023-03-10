## Purpose and use case

- The purpose of this code is to automatically sync Pub\Sub and Google Cloud Function to your local environment. 
- Aid in the process of migration from one GCP environment to another using Terraform.


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
3. Wthin '.env' set the `PROJECT` and `REGION` environment variables to the ID of your Google Cloud project and the region where you want to deploy your functions.


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
]
```
Running main.py will create a JSON with the following structure :
```
{
  "AuthenticatedFunction": {
    "entryPoint": "helloWorld",
    "timeout": "60",
    "available_memory_mb": 256,
    "environmentVariables": {
      "RUN": "VALUE",
      "RUNAGAIN": "VALUEAGAIN"
    },
    "buildEnvironmentVariables": {
      "BUILDATMAX": "50",
      "BUILDATMIN": "1"
    },
    "secrets": {
      "secretEnvironmentVariables": [
        {
          "key": "RandomVariable",
          "projectId": "1001384248257",
          "secret": "password",
          "version": "1"
        }
      ],
      "secretVolumes": [
        {
          "mountPath": "/secret",
          "projectId": "1001384248257",
          "secret": "mysecret",
          "versions": [
            {
              "version": "latest",
              "path": "/mysecret"
            }
          ]
        }
      ]
    },
    "httpsTrigger": {
      "url": "https://us-central1-cc-s2s-vpn-test.cloudfunctions.net/function-1"
    }
  },
  "AllocatedFunction": {
    "entryPoint": "helloPubSub",
    "timeout": "60",
    "available_memory_mb": 256,
    "environmentVariables": null,
    "buildEnvironmentVariables": null,
    "secrets": {},
    "eventTrigger": {
      "resource": "projects/cc-s2s-vpn-test/topics/elazar-asdasdx",
      "eventType": "google.pubsub.topic.publish",
      "failurePolicy": {
        "retry": {}
      }
    }
  }
}
```

## Terraform Iteration
An additional terraform file has been added with the resources this is supposed to iterate on.

You may create a `terraform.tfvars` file using the following command :
```
cat << EOF > terraform.tfvars
gcp_project = "my-project"
gcp_region = "my-region"
name_prefix = "my-prefix"
EOF
```
