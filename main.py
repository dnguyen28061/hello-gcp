import os
from flask import Flask
from google.cloud import storage, pubsub_v1, bigquery
import redis

app = Flask(__name__)
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
REDIS_IP = os.environ.get("REDISHOST", "localhost")

@app.route("/")
def hello_world():
    # Redis Cache: Increment visitor count
    r = redis.Redis(host=REDIS_IP, port=6379)
    count = r.incr('visitor_count')

    # Pub/Sub: Publish 'User Visited' event
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, "hello-topic")
    publisher.publish(topic_path, b"User Visited")

    # Cloud Storage: Save log as text file
    storage_client = storage.Client()
    bucket = storage_client.bucket(f"hello-world-{PROJECT_ID}")
    bucket.blob(f"visit_{count}.txt").upload_from_string(f"Visitor {count}")

    # BigQuery: Insert visit record into analytics table
    bq_client = bigquery.Client()
    query = f"INSERT INTO `{PROJECT_ID}.hello_dataset.logs` (msg) VALUES ('Visit {count}')"
    bq_client.query(query).result()

    return f"Hello GCP! Visitor #{count} logged across the stack."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

