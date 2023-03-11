from google.cloud import pubsub_v1
import google.api_core.exceptions
from dotenv import load_dotenv
import logging
import json
import sys
import os

# Set up logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    stream=sys.stderr,
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# load environment variables from .env file
load_dotenv()

PROJECT = os.getenv('PROJECT')
REGION  = os.getenv('REGION')


def list_pubsub_topics():
    """
    Lists all Pub/Sub topics in a given Google Cloud project and writes them to a JSON file.
    """
    # list all pub/sub topics in the project
    try:
        publisher = pubsub_v1.PublisherClient()
        project_path = f"projects/{PROJECT}"
        topics = [topic.name.split('/')[-1] for topic in publisher.list_topics(request={"project": project_path})]

        # Break if no topics exist
        if topics == []:
            logger.info("No Topics were found in %s Project", PROJECT)
            return

        # write topics to file
        file_path = "pubsub_topics.json"
        with open(file_path, "w") as f:
            f.write(json.dumps(topics, indent=2))

        # log each topic written to file
        for topic in topics:
            logger.info(f"Topic written to file: {topic}")

        # print confirmation message
        logger.info(f"Pub/Sub Topics written to {file_path}")

        # return list of pub/sub topics
        return topics

    # Catch an error with permissions or project set incorrectly.
    except google.api_core.exceptions.NotFound:
        logger.error(f"Could not find project {PROJECT}. Please check the project ID and make sure the user has access to it.")
        return None
    
if __name__ == "__main__":
    list_pubsub_topics()
