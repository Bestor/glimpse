from transformers import pipeline
from openai import OpenAI

import yaml
import json
# Napkin OpenAI math
# Num tokens per 30 sec audio ~340
# Num tokens per day = 2880 (30 second chunks per day) * 340 = 100k tokens per day
# gpt-4o-mini pricing ~$.6 per million tokens
#
# $.06 / day to listen and aggregate a single feed
# 10,000 feeds = $600/day = $200k/yr. The yearly cost for a single feed is ~$22 with this method
def valid_event_dict(event_dict):
    if "events" in event_dict:
        for event in event_dict["events"]:
            if "description" in event and "location" in event:
                continue
            else:
                return False
    else:
        return False 
    return True

def aggregate_events(config, text):

    client = OpenAI(
        project=config["openai"]["project"],
        api_key=config["openai"]["api_key"]
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"""
Return me a yaml string that contains the postal addresses in this text with a brief description of the event occuring. Only return the top choice that look the most like a postal addresses. Use the following format for the yaml:
```
events:
    - description: X
      location: Y
```

Text: {text}"""}],)
    
    # Print the response
    print(response)
    yaml_response = response.choices[0].message.content
    response_dict = {}
    MALFORMAT_ERR_TEXT = "The AI returned an invalid event format"
    try:
        response_dict = yaml.safe_load(yaml_response.removeprefix("```yaml").removesuffix("```"))
    except Exception as e:
        raise Exception(MALFORMAT_ERR_TEXT, e) 

    if not valid_event_dict(response_dict):
        raise Exception(MALFORMAT_ERR_TEXT)

    print(json.dumps(response_dict, indent=4))
    return response_dict
