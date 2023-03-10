from google.cloud import pubsub_v1
from dotenv import load_dotenv
import sys
import time
import logging
import json
import os

"""
This script provides functions to list all Pub/Sub topics in a Google Cloud project and writes them to a JSON file.
It requires the user to set up the necessary environment variables in a .env file, such as the project ID and region.
The script uses the Google Cloud Pub/Sub client library and the dotenv library.

Usage:
    - Import the script and call the list_pubsub_topics() function to get a list of topic names.
    - Call the write_pubsub_topics_to_file(topics, file_path) function to write the list to a JSON file.
    - To execute the script, run it directly from the command line.

Example:
    - To get a list of topics and write them to a file named "pubsub_topics.json", call the following from the command line:
        `python pubsub_list_topics.py`
"""

# Set up logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    stream=sys.stderr,
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Record start time
start_time = time.monotonic()

# load environment variables from .env file
load_dotenv()

PROJECT = os.getenv('PROJECT')
REGION  = os.getenv('REGION')

def list_pubsub_topics():
    """
    Lists all Pub/Sub topics in a given Google Cloud project.

    Returns:
        List of Pub/Sub topic names (str)
    """
    publisher = pubsub_v1.PublisherClient()
    project_path = f"projects/{PROJECT}"
    topics = [topic.name.split('/')[-1] for topic in publisher.list_topics(request={"project": project_path})]
    return topics


def write_pubsub_topics_to_file(topics, file_path):
    """
    Writes a list of Pub/Sub topics to a JSON file.

    Args:
        topics: List of Pub/Sub topic names (str)
        file_path: File path of the output JSON file (str)

    Returns:
        None
    """
    with open(file_path, "w") as f:
        f.write(json.dumps(topics, indent=2))


if __name__ == "__main__":
    # list all pub/sub topics in the project
    pubsub_topics = list_pubsub_topics()

    # write topics to file
    file_path = "pubsub_topics.json"
    write_pubsub_topics_to_file(pubsub_topics, file_path)

    # log each topic written to file
    for topic in pubsub_topics:
        logger.info(f"Topic written to file: {topic}")

    # print confirmation message
    logger.info(f"Pub/Sub topics written to {file_path}")
