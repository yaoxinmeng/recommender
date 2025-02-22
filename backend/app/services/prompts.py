DETAILED_LOCATION_PROMPT = """
Extract the relevant information from the document:

{text}

You MUST return your output in the following JSON format: {schema}

If the information of any property is not available, return an empty string for that property.
""".strip(" \n")

BASIC_LOCATIONS_PROMPT = """
Extract the relevant information from the document:

{text}

You MUST return your output as a JSON list of objects with the following format: {schema}

If no relevant locations are found, return an empty list.
""".strip(" \n")