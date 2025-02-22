from typing import Any
import json
import re

from loguru import logger
from playwright.sync_api import sync_playwright
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from app.dependencies.llm import llm
from app.types.model_outputs import BasicLocationData, DetailedLocationData
from app.services.prompts import BASIC_LOCATIONS_PROMPT, DETAILED_LOCATION_PROMPT


class Scraper:
    def __init__(self):
        self.bs_transformer = BeautifulSoupTransformer()


    def scrape_basic_location(self, url: str) -> list[BasicLocationData]:
        """
        Scrape the content of a web page using Playwright and BeautifulSoup, then extract structured data using LLM.

        :param str url: The URL of the web page to scrape.
        :return: The structured data extracted from the web page.
        """
        logger.info("Scraping documents with Playwright and BeautifulSoup")
        docs = [self._scrape(url)]
        bs_transformer = BeautifulSoupTransformer()
        docs_transformed = bs_transformer.transform_documents(
            docs, tags_to_extract=["span"]
        )
        logger.trace(docs_transformed)

        # Chunk the documents into smaller parts
        logger.info("Splitting documents into chunks")
        splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=1000, chunk_overlap=0
        )
        splits = splitter.split_documents(docs_transformed)

        # process each chunk
        locations: list[BasicLocationData] = []
        for split in splits:
            logger.trace(split.page_content)
            logger.info(f"Extracting content with LLM")
            extracted_content = self._extract_basic_locations(split.page_content)
            logger.trace(extracted_content)
            locations.extend(extracted_content)

        return locations
    

    def scrape_detailed_locations(self, urls: list[str]) -> DetailedLocationData:
        """
        Scrape the content of a web page using Playwright and BeautifulSoup, then extract structured data using LLM.

        :param str url: The URL of the web page to scrape.
        :return: The structured data extracted from the web page.
        """
        logger.info("Scraping documents with Playwright and BeautifulSoup")
        docs = [self._scrape(urls)]
        bs_transformer = BeautifulSoupTransformer()
        docs_transformed = bs_transformer.transform_documents(
            docs, tags_to_extract=["span"]
        )
        logger.trace(docs_transformed)

        # Chunk the documents into smaller parts
        logger.info("Splitting documents into chunks")
        splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=1000, chunk_overlap=0
        )
        splits = splitter.split_documents(docs_transformed)

        # process each chunk
        locations: list[BasicLocationData] = []
        for split in splits:
            logger.trace(split.page_content)
            logger.info(f"Extracting content with LLM")
            extracted_content = self._extract_basic_locations(split.page_content)
            logger.trace(extracted_content)
            locations.extend(extracted_content)

        return locations
    

    def _extract_basic_locations(self, text: str, retries: int = 0) -> list[BasicLocationData]:
        """
        Generate a structured output from the input text using LLM.

        :param str text: The input text to process.
        :param int retries: The number of retries to attempt if the structured output cannot be generated. Default is 0.
        :return: The structured output generated from the input text.
        """
        schema = json.dumps(BasicLocationData.model_json_schema())
        prompt = BASIC_LOCATIONS_PROMPT.format(text=text, schema=schema)
        logger.trace(prompt)
        for i in range(retries+1):
            try:
                raw_output = llm.invoke(prompt)
                matches = re.findall(r"(\[[\r\n\s]*\{.+\}[\r\n\s]*\])", raw_output, re.DOTALL)
                if not matches:
                    raise Exception("No JSON objects found in the output")
                structured_outputs = json.loads(matches[0])
                return [self._parse_basic_location(o) for o in structured_outputs]
            except Exception as e:
                logger.error(f"Failed to generate structured output: {e}")
                if i == retries:
                    break
                logger.info(f"Retrying ({i + 1}/{retries})...")
        logger.error(f"Failed to generate structured output after {retries} retries")
        return []
    

    def _extract_detailed_locations(self, text: str, retries: int = 0) -> DetailedLocationData:
        """
        Generate a structured output from the input text using LLM.

        :param str text: The input text to process.
        :param int retries: The number of retries to attempt if the structured output cannot be generated. Default is 0.
        :return: The structured output generated from the input text.
        """
        schema = json.dumps(DetailedLocationData.model_json_schema())
        prompt = DETAILED_LOCATION_PROMPT.format(text=text, schema=schema)
        logger.trace(prompt)
        for i in range(retries+1):
            try:
                raw_output = llm.invoke(prompt)
                matches = re.findall(r"(\{.+\})", raw_output, re.DOTALL)
                if not matches:
                    raise Exception("No JSON objects found in the output")
                structured_output = json.loads(matches[0])
                return self._parse_detailed_location(structured_output)
            except Exception as e:
                logger.error(f"Failed to generate structured output: {e}")
                if i == retries:
                    break
                logger.info(f"Retrying ({i + 1}/{retries})...")
        logger.error(f"Failed to generate structured output after {retries} retries")
        return []
        

    def _scrape(self, url: str) -> Document:
        """
        Our own synchronous scraping function using Playwright that avoids using `asyncio.run()`.
        """
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            page.goto(url)
            metadata = {"source": url}
            content = page.content()
            browser.close()
        return Document(page_content=content, metadata=metadata)


    def _parse_basic_location(self, location: dict[str, Any]) -> BasicLocationData | None:
        """
        Parse the location data into a basic location data object.

        :param LocationData location: The location data to parse.
        :return: The basic location data object.
        """
        if "properties" not in location:
            logger.error("Location data does not contain properties")
            return None
        location = location["properties"]

        if "name" not in location or "description" not in location["name"] or location["name"]["description"] == "":
            logger.error("Location data does not contain a name")
            return None
        name = location["name"]["description"]

        if "address" not in location or "description" not in location["address"]:
            address = ""
        else:
            address = location["address"]["description"]

        if "description" not in location or "description" not in location["description"]:
            description = ""
        else:
            description = location["description"]["description"]

        if "contact" not in location or "description" not in location["contact"]:
            contact = ""
        else:
            contact = location["contact"]["description"]
        
        return BasicLocationData(
            name=name,
            address=address,
            description=description,
            contact=contact
        )
    

    def _parse_detailed_location(self, location: dict[str, Any]) -> DetailedLocationData | None:
        """
        Parse the location data into a detailed location data object.

        :param LocationData location: The location data to parse.
        :return: The detailed location data object.
        """
        if "properties" not in location:
            logger.error("Location data does not contain properties")
            return None
        location = location["properties"]
        if "name" not in location or "description" not in location["name"] or location["name"]["description"] == "":
            logger.error("Location data does not contain a name")
            return None
        name = location["name"]["description"]
        if "address" not in location or "description" not in location["address"]:
            address = ""
        else:
            address = location["address"]["description"]
        if "description" not in location or "description" not in location["description"]:
            description = ""
        else:
            description = location["description"]["description"]
        if "offerings" not in location or "description" not in location["offerings"]:
            offerings = {}
        else:
            offerings = location["offerings"]["description"]
        if "contact" not in location or "description" not in location["contact"]:
            contact = ""
        else:
            contact = location["contact"]["description"]
        if "images" not in location or "description" not in location["images"]:
            images = {}
        else:
            images = location["images"]["description"]
        
        return DetailedLocationData(
            name=name,
            address=address,
            description=description,
            offerings=offerings,
            contact=contact,
            images=images
        )
    
scraper = Scraper()