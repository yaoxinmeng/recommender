from loguru import logger
import bs4
from bs4._typing import _OneElement
from playwright.sync_api import sync_playwright

def scrape(url: str) -> str:
    """
    Call to scrape the contents of a web page. Retrieves only textual elements and images.

    :param str url: The URL of the web page to scrape.
    :return str: The content of the web page rendered in Markdown.
    """
    # scrape using Playwright
    content = _playwright_scrape(url)

    # extract relevent content using BeautifulSoup
    # we retain images in markup since the positions of embedded images are important
    html_content = _parse_html(content)

    # return only the first 10k tokens of the page content
    trunc_content = html_content[:10000]
    return trunc_content


def _playwright_scrape(url: str) -> str:
    """
    Scrape the contents of a page using the Playwright Sync API.
    """
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
        page = context.new_page()
        try:
            page.goto(url, wait_until='networkidle', timeout=3000)  # we wait at most 3 seconds for a page to render
        except Exception as e:
            logger.error(f"Error loading page: {e}") 
        try:    # attempts to retrieve page contents regardless
            content = page.content()
        except Exception as e:
            logger.error(f"Error retrieving page content: {e}") 
            content = ""
        browser.close()
    return content


def _parse_html(content: str, text_tags: list[str] = ["p", "h1", "h2", "h3", "h4", "li"], image_tags: str = ["img"]) -> str:
    """
    Custom parser for html. Retrieves all text contents as text, but retains information
    of embedded images in the page.

    :param str content: The html content to be parsed
    :param list[str] text_tags: The list of tags to retrieve text from
    :param list[str] image_tags: The list of tags that will be treated as images
    """
    soup = bs4.BeautifulSoup(content, "html.parser")
    html_content = []
    for element in soup.find_all():
        if element.name in image_tags:
            element = _recursively_remove_attrs(element, ["src"])
            # check if image url is valid
            if element.attrs.get("src", "").startswith("http"):
                html_content.append(str(element))
            element.decompose()
        elif element.name in text_tags:
            if element.name == "li":
                html_content.append("- " + element.get_text())
            elif element.name == "h1":
                html_content.append("# " + element.get_text())
            elif element.name == "h2":
                html_content.append("## " + element.get_text())
            elif element.name == "h3":
                html_content.append("### " + element.get_text())
            elif element.name == "h4":
                html_content.append("#### " + element.get_text())
            else:
                html_content.append(element.get_text())
            element.decompose()
    return "\n".join(html_content).strip(" \n")


def _recursively_remove_attrs(tag: _OneElement, attrs: list[str]) -> _OneElement:
    """
    Removes all attributes other than the specified ones from the element and its children, 
    and returns the modified tag

    :param _OneElement tag: The element to be stripped
    :param list[str] attrs: The list of attributes to keep
    """
    tag.attrs = {key: value for key, value in tag.attrs.items() if key in attrs}
    for element in tag.find_all():
        element.attrs = {key: value for key, value in element.attrs.items() if key in attrs}
    return tag