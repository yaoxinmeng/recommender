from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

from loguru import logger
import json
import re

from app.dependencies.bedrock import Bedrock, llm
from app.types.schema import LocationData


STRUCTURED_OUTPUT_PROMPT = """
Extract the relevant information from the document:

{text}

You MUST return your output in the following JSON format: {schema}
""".strip("\n")


class Scraper:
    def __init__(self):
        self.bs_transformer = BeautifulSoupTransformer()


    def scrape_with_playwright(self, url: str) -> LocationData:
        """
        Scrape the content of a web page using Playwright and BeautifulSoup, then extract structured data using LLM.

        :param str url: The URL of the web page to scrape.
        :return: The structured data extracted from the web page.
        """
        logger.info("Scraping documents with Playwright and BeautifulSoup")
        loader = AsyncChromiumLoader([url])
        docs = loader.load()
        bs_transformer = BeautifulSoupTransformer()
        docs_transformed = bs_transformer.transform_documents(
            docs, tags_to_extract=["span"]
        )
        logger.trace(docs_transformed)

        # Grab the first 1000 tokens of the site
        logger.info("Splitting documents into chunks")
        splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=1000, chunk_overlap=0
        )
        splits = splitter.split_documents(docs_transformed)
        content = splits[0].page_content
        logger.trace(content)

        # Process the first split
        logger.info(f"Extracting content with LLM")
        extracted_content = self.structured_output(content, retries=1)
        logger.trace(extracted_content)

        return extracted_content
    

    def structured_output(self, text: str, retries: int = 3) -> LocationData:
        """
        Generate a structured output from the input text using LLM.

        :param str text: The input text to process.
        :return: The structured output generated from the input text.
        """
        prompt = STRUCTURED_OUTPUT_PROMPT.format(text=text, schema=json.dumps(LocationData.model_json_schema()))
        logger.trace(prompt)
        for i in range(retries):
            try:
                raw_output = llm.invoke(prompt)
                matches = re.findall(r"(\{.+\})", raw_output, re.DOTALL)
                if not matches:
                    raise Exception("No JSON objects found in the output")
                structured_output = json.loads(matches[0])
                return LocationData.model_validate(structured_output, strict=False)
            except Exception as e:
                logger.error(f"Failed to generate structured output: {e}")
                logger.info(f"Retrying ({i + 1}/{retries})...")
        raise Exception("Unable to generate a structured output")
    
scraper = Scraper()