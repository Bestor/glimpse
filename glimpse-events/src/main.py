import argparse
from config import load_config
from core import aggregate, geocode
from api_handler import API
import json
from datetime import datetime, timezone
from glimpse_api_client.glimpse_api_client import Client, models
from glimpse_api_client.glimpse_api_client.api.default import post_events

import time
import requests

API_ENDPOINT = "localhost:8080/transcriptions"  # Replace with your API URL
POLLING_INTERVAL = 10 # Time in seconds between each poll


def fetch_transcriptions():
    try:
        return API().get_transcriptions()
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching events: {e}")
        return None
    
def get_latest_trancription(transcriptions):
    #return transcriptions[-1]
    newest_timestamp = datetime(1970, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    newest_transcription = None
    for transcription in transcriptions:
        if transcription.timestamp > newest_timestamp:
            newest_timestamp = transcription.timestamp
            newest_transcription = transcription
    
    return newest_transcription

TRANSCRIPTION_BATCH_SIZE = 200
def main(args):
    config = load_config(args.config_path)

    client = Client(base_url="http://localhost:8080")

    last_transcription_processed = models.Transcription(content="DUMMY", audio="", timestamp=datetime(1970, 1, 1, 0, 0, 0, tzinfo=timezone.utc))
    current_block_to_check = ""

    NEW_EVENT = models.Event(description="DUMMY", timestamp=datetime(1970, 1, 1, 0, 0, 0, tzinfo=timezone.utc))
    event = NEW_EVENT
    while True:
        print("Checking for new transcriptions...")
        transcriptions = fetch_transcriptions()

        # newest_transcription = get_latest_trancription(transcriptions=transcriptions)
        # process_transcription(newest_transcription, config)

        if transcriptions:
            newest_transcription = get_latest_trancription(transcriptions=transcriptions)
            if newest_transcription.timestamp > last_transcription_processed.timestamp:
                # If we are in this block there is a new transcription to process
                if event.transcriptions:
                    event.transcriptions.append(newest_transcription)
                else:
                    event.transcriptions = [newest_transcription]

                current_block_to_check = f"{current_block_to_check}. {newest_transcription.content}"
                print(f"current block length = {len(current_block_to_check)}")
                if len(current_block_to_check) > TRANSCRIPTION_BATCH_SIZE:
                    print(f"Processing transcription: {current_block_to_check}")
                    events = aggregate.aggregate_events(config, current_block_to_check)
                    for event_dict in events["events"]:
                        event.timestamp = datetime.now(timezone.utc)
                        print(event)
                        location_to_search = f'{event_dict["location"]}, indianapolis'
                        location = geocode.search_address(location_to_search)
                        if location:
                            event.location = models.Location(text=location.address, latitude=location.latitude, longitude=location.longitude)
                        event.description = event_dict["description"]
                        response = post_events.sync_detailed(
                            client=client,
                            body=event
                        )
                        print(f"RESPONSE: {event.transcriptions}")
                        event = NEW_EVENT

                    current_block_to_check = ""
                    event.timestamp = datetime.now(timezone.utc)
                last_transcription_processed = newest_transcription
                print(last_transcription_processed.timestamp)
        
        print(f"Waiting for {POLLING_INTERVAL} seconds before next check...")
        time.sleep(POLLING_INTERVAL)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="An app to analyze sentences")

    parser.add_argument("--config-path", required=False, default="./config/config.yaml", help="Path to the output file")

    args = parser.parse_args()

    main(args)

# def main(args):
#     config = load_config(args.config_path)
#     sentence = "I'll take that. 128 tonight and I'll go. Edward 123, Edward 128 at 1133, Edward 121 at 131. Downtown 21, suffering overdose 20 North Pennsylvania Street, 50 North 100 East. 20 North Pennsylvania Street, 50 North 100 East. Edward 131 for overdose 20 North Pennsylvania Street in front of Wingstop for male overdosing in us and out. 131. 131."
#     sentences = API().get_transcription()
#     print(sentences)
#     text = ""
#     # for sentence in sentences:
#     #     text += f" {sentence}"
#     #     if len(text) > 500:
#     #         events = aggregate.aggregate_events(config, text) #

#     #         for event in events:
#     #             geocode.geocode(event["location"])
#     #             break

