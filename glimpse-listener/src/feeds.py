import threading
import whisper
from providers.broadcastify.broadcastify import BroadcastifyFeed, process
from core.writer import APIWriter
import boto3


class Bucket():
    def __init__(self, s3_client, bucket_name):
        self.s3_client = s3_client
        self.bucket_name = bucket_name

    def write(self, bucket_path, local_path):
        self.s3_client.meta.client.upload_file(local_path, self.bucket_name, bucket_path)

    def create(self):
            self.s3_client.create_bucket(Bucket=self.bucket_name)

def process_streams(config):
    minio_endpoint = "http://minio:9000"  # Replace with your MinIO server endpoint
    access_key = "your-access-key"  # Replace with your MinIO access key
    secret_key = "your-secret-key"  # Replace with your MinIO secret key
    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )
    s3 = session.resource('s3', endpoint_url=minio_endpoint)
    bucket = Bucket(s3, "glimpse-audio")
    try:
        bucket.create()
    except Exception as e:
        print("WARN: Bucket creation failure")

    
    model_size = config["models"]["whisper"]["size"]
    model = whisper.load_model(model_size)


    feed_threads = []
    for feed in config['feeds']:
        if feed["provider"] == "broadcastify":
            writer = APIWriter(s3_bucket=bucket)
            bcast_feed = BroadcastifyFeed(url=feed["url"], 
                                          user=config["providers"]["broadcastify"]["user"],
                                          password=config["providers"]["broadcastify"]["password"])
            listener_thread = threading.Thread(target=process, args=(bcast_feed, model, writer))
            #listener_thread.daemon = True
            feed_threads.append(listener_thread)

    for feed_thread in feed_threads:
        feed_thread.start()
        feed_thread.join()
