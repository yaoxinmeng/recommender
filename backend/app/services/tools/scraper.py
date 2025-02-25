from loguru import logger
import bs4
from playwright.sync_api import sync_playwright
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_core.documents import Document


def scrape(url: str, tags: list[str] = ["p", "h1", "h2", "h3", "h4", "img"]) -> str:
    """
    Call to scrape the contents of a web page. Retrieves only elements that match the provided tags.

    :param str url: The URL of the web page to scrape.
    :param list[str] tags: The list of relevant tags to retrieve.
    :return: The content of the web page.
    """
    # scrape using Playwright
    content = _playwright_scrape(url)

    # extract relevent content using BeautifulSoup
    # doc = Document(page_content=content, metadata={"source": url})
    # bs_transformer = BeautifulSoupTransformer()
    # docs_transformed = bs_transformer.transform_documents(
    #     [doc], tags_to_extract=["p", "img", "li", "span"],
    #     unwanted_tags=("nav", "script", "style")
    # )

    # extract relevent content using BeautifulSoup
    # we retain it in markup since the positions of embedded images are important
    soup = bs4.BeautifulSoup(content, "html.parser")
    html_content = ""
    KEEP_ATTRIBUTES = ["src"]
    for element in soup.find_all():
        if element.name in tags:
            element.attrs = {key: value for key, value in element.attrs.items() if key in KEEP_ATTRIBUTES}
            html_content += str(element.prettify())
            element.decompose()
    logger.trace(html_content)

    # return only the first 10k tokens of the page content
    trunc_content = html_content[:10000]
    return trunc_content


def _playwright_scrape(url: str) -> str:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
        page = context.new_page()
        try:
            page.goto(url)
            content = page.content()
        except Exception as e:
            logger.error(f"Error loading page: {e}") 
            content = ""
        browser.close()
    return content