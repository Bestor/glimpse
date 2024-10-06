import threading
import whisper
from providers.broadcastify.broadcastify import BroadcastifyFeed, process
from core.writer import APIWriter

def process_streams(config):

    model_size = config["models"]["whisper"]["size"]
    model = whisper.load_model(model_size)


    feed_threads = []
    for feed in config['feeds']:
        if feed["provider"] == "broadcastify":
            writer = APIWriter(name=feed["name"], base_path=config["write_path"])
            bcast_feed = BroadcastifyFeed(url=feed["url"], 
                                          user=config["providers"]["broadcastify"]["user"],
                                          password=config["providers"]["broadcastify"]["password"])
            listener_thread = threading.Thread(target=process, args=(bcast_feed, model, writer))
            #listener_thread.daemon = True
            feed_threads.append(listener_thread)

    for feed_thread in feed_threads:
        feed_thread.start()
