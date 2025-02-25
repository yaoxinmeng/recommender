CANDIDATE_LOCATIONS_PROMPT = """
Extract locations or events that are relevant to "{query}" from the following document. If no relevant locations or events are found, return an empty list.

{text}

```json
""".strip(" \n")


SEARCH_QUERY_PROMPT = """
You are an expert researcher who has been tasked to find detailed information on "{query}". Your first step is to craft a list of search queries to find the relevant information.

Currently you have gathered the following information:
{information}

The information that is required is in the following format: 
{schema}

If there is any missing information, return ONLY a list of Google search queries. DO NOT attempt to fill in the missing information yourself.

Search queries:
```json
""".strip(" \n")


STRUCTURED_OUTPUT_PROMPT = """
Extract only information relevant to "{name}" from this document:

{text}

```json
""".strip(" \n")


STRUCTURED_OUTPUT_SYSTEM_PROMPT = """
Your task is to precisely extract information from the text provided, and format it according to the given JSON schema delimited with triple backticks. Only include the JSON output in your response. Avoid including any other statements in the response.

```json
{json_schema}
```
""".strip(" \n")

STRUCTURED_RESPONSE_SYSTEM_PROMPT = """
Your task is to execute the instructions specified, and format your response according to the given JSON schema delimited with triple backticks. Only include the JSON output in your response. Avoid including any other statements in the response.

```json
{json_schema}
```
"""


IMAGE_CAPTION_PROMPT = """
Generate captions and hashtags for this image. For the caption, use the following examples to guide your tone. Keep the caption to less than 70 words. 

Example 1: An iconic staple of local cuisine, this dish is made with mud crab drenched in chilli sauce, with fried bread buns on the side to sop the leftovers.

Example 2: Made from flat rice noodles and cooked in a wok for a smoky flavour, this dish is stir-fried with garlic, soy sauce, Chinese sausage, bean sprouts and cockles.

Example 3: The Malays are the original inhabitants of Singapore and no other place reflects this better than Kampong Glam. Be awed by Sultan Mosque and explore the quaint little streets around it!

Example 4: Cycle through a first-of-its-kind indoor cycling path at Funan, a bicycle-friendly shopping mall that supports the car-lite movement in Singapore.

Example 5: The Civic district area holds the WW2 memorial for civilians. It is home to world-class museums and some of the country's most historic buildings.

Example 6: The heartbeat of Singapore, this bustling river is where everything started. Formerly lined with warehouses trading along the Singapore River, the only businesses you'll find here today are restaurants, clubs and bars.

Caption:
```json
""".strip(" \n")