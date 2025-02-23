PRELIMINARY_LOCATION_JSON_SCHEMA = """
{
    "name": "<name of location>",
    "address": "<address of the location>",
    "description": "<description of the location>",
    "contact": "<contact_number with the format '+65-1234-5678'>",
    "offerings": [
        {
            "name": "<offering_name>",
            "price": "<offering_price>"
        }
    ],
    "images": [
        {
            "name": "<image_name>",
            "url": "<image_url>",
            "hashtags": [
                "<image_hashtag>"
            ]
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