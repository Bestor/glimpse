# Glimpse

## Summary

The Glimpse project started when I was reading a reddit thread about a truck crash on a nearby freeway. A commenter was providing minute-by-minute reporting of what was happening on the scene. When asked where he was getting his information he responded that he was simply listening to the police scanner

This gave me the idea to create a project that could "listen" to radio feeds and transcribe them using OpenAI's whisper model. Using the transcribed audio we can summarize this data into events and use a geocoder to attempt to pinpoint the coordinates of these events

This is a hobby project where I often incorperate new or unfamiliar technologies that I don't get to work with in my day job. At the time of writing this is not published project and there is no support / SLAs around the tool.

## Architecture

Glimpse is divided into 4 services. You can view detailed documentation about each service in the README.md in each folder

Initially the 4 services were in seperate repos. If this was more than a hobby project I would have kept it that way but I found that managing everything seperately was too much work so I consolidated all the code into this single repo.

### API

Located in `glimpse-api` folder the API is written in golang. This is the connection point for the individual services to store data

### Listener

Located in `glimpse-listener` folder the Listener is python that runs the OpenAI whisper model. The listener handles transcribing the raw audio. It uploads the audio files it transcribed to S3 (minio) and sends the transcriptions and links to their audio files to the API

### Event Aggregator

Located in `glimpse-events` the event aggregator takes one or more transcriptions and attempts to use an LLM to aggregate events from that data. Currently it offloads events to OpenAIs gpt-4o-mini. I would like to run a model locally to support this (WIP)

The aggregator also uses Nominatim for geocoding the events.

It stores all events in the API

### UI

The UI is a simple map for displaying the events backed by leaflet. I would like to improve this to be a more functional UI using react to be able to browse through radio feeds/transcriptions
