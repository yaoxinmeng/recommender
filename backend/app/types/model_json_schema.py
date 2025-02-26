# This file contains all the structured JSON formats based on the Pydantic models defined in `model_outputs.py`. 

PRELIMINARY_LOCATION_JSON_SCHEMA = """
{
    "name": "<name of location>",
    "address": "<address of the location>",
    "description": "<detailed description of the location>",
    "contact": "<contact number with the format '+65-1234-5678'>",
    "offerings": [
        {
            "name": "<name of product or service>",
            "price": "<price of product or service>"
        }
    ],
    "images": [
        {
            "name": "<image_name>",
            "url": "<image_url>"
        }
    ],
    "opening_hours": {
        "monday": {
            "start": "<start_time formatted as HH:MM>",
            "end": "<end_time formatted as HH:MM>"
        },
        "tuesday": {
            "start": "<start_time formatted as HH:MM>",
            "end": "<end_time formatted as HH:MM>"
        },
        "wednesday": {
            "start": "<start_time formatted as HH:MM>",
            "end": "<end_time formatted as HH:MM>"
        },
        "thursday": {
            "start": "<start_time formatted as HH:MM>",
            "end": "<end_time formatted as HH:MM>"
        },
        "friday": {
            "start": "<start_time formatted as HH:MM>",
            "end": "<end_time formatted as HH:MM>"
        },
        "saturday": {
            "start": "<start_time formatted as HH:MM>",
            "end": "<end_time formatted as HH:MM>"
        },
        "sunday": {
            "start": "<start_time formatted as HH:MM>",
            "end": "<end_time formatted as HH:MM>"
        }
    }
}
""".strip(" \n")


IMAGE_DETAILS_JSON_SCHEMA = """
{
    "caption": "image_caption",
    "hashtags": [
        "<image_hashtag>"
    ]
}
""".strip(" \n")