CANDIDATE_LOCATIONS_PROMPT = """
Extract locations or events that are relevant to "{query}" from the following document. If no relevant locations or events are found, return an empty list.

{text}
""".strip(" \n")


SEARCH_QUERY_PROMPT = """
You are an expert researcher who has been tasked to find detailed information on "{query}". Your first step is to craft a list of search queries to find the relevant information.

Currently you have gathered the following information:
{information}

The information that is required is in the following format: {schema}

If there is any missing information, return a list of Google search queries as a JSON list of string. DO NOT attempt to fill in the missing information yourself.
If there is no more missing information, return an empty list.
""".strip(" \n")


STRUCTURED_OUTPUT_PROMPT = """
Extract only information relevant to "{name}" from this document:

{text}
""".strip(" \n")


STRUCTURED_OUTPUT_SYSTEM_PROMPT = """
Your task is to precisely extract information from the text provided, and format it according to the given JSON schema delimited with triple backticks. Only include the JSON output in your response. If a specific field has no available data, indicate this by writing `null` as the value for that field in the output JSON. Avoid including any other statements in the response.

```json
{json_schema}
```
""".strip(" \n")

STRUCTURED_RESPONSE_SYSTEM_PROMPT = """
Your task is to perform the task specified, and format your response according to the given JSON schema delimited with triple backticks. Only include the JSON output in your response.

```json
{json_schema}
```
"""


IMAGE_CAPTION_PROMPT = """
Caption this image in less than 70 words.
""".strip(" \n")