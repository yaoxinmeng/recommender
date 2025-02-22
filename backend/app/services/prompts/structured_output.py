STRUCTURED_OUTPUT_PROMPT = """
Extract the relevant information from the document:

{text}

You MUST return your output in the following JSON format: {schema}
""".strip("\n")