import json

from loguru import logger

from app.types.schema import LocationData
from app.types.model_outputs import PreliminaryLocationData
from app.services.tools.search import search_duckduckgo
from app.services.tools.scraper import scrape
from app.services.tools.structured_output import get_preliminary_location, get_candidate_locations, get_search_queries, update_location_data
from app.services.tools.image_processing import generate_caption_hashtags
from app.services.utils import initialise_preliminary_locations, preliminary_to_final_location_data

def extract_locations(query: str, n_results: int, n_iterations: int) -> list[LocationData]:
    """
    Identify the most relevant locations to the query and extract the required information 
    for these locations. 

    :param str query: The user query 
    :param int n_results: The number of locations to return
    :param int n_iterations: The number of iterations to run the agentic portion of the workflow. Larger
    number of iterations will yield more accurate results, at the cost of computation time.
    :return list[LocationData]: The list of location information 
    """
    # craft a list of candidate locations
    logger.info(f"Searching for pages relevant to '{query}'")
    sg_query = query + " Singapore"
    main_urls = search_duckduckgo(sg_query)
    locations: list[str] = []
    logger.info(f"Searching for information in these pages: {main_urls}")
    for result in main_urls:
        content = scrape(result)
        if not content:
            logger.warning(f"Failed to retrieve any content from {result}")
            continue
        candidate_locations = get_candidate_locations(content, sg_query)
        locations.extend([l for l in candidate_locations if l])

        logger.trace(locations)
        if len(locations) >= n_results:
            break

    # create an empty PreliminaryLocationData object for each location
    preliminary_locations = initialise_preliminary_locations(locations[:n_results])

    # attempt to fill in the details of each preliminary location using an iterative approach
    logger.info(f"Search for more information regarding: {locations}")
    results: list[LocationData] = []
    for i, location in enumerate(preliminary_locations):
        visited_urls = []
        citations = []
        for iter_count in range(n_iterations):  # iterate up to n times to refine the information of each candidate location
            search_queries = get_search_queries(location.name + " Singapore", preliminary_locations[i])
            logger.trace(f"Search queries: {search_queries}")
            if not search_queries:
                continue

            # extract data from first search query
            query = search_queries[0]
            urls = search_duckduckgo(query, max_results=5)
            logger.trace(f"URLs: {urls}")
            urls = [s for s in urls if s not in visited_urls]  # check if URL has been visited already
            if not urls:
                continue
            
            # limit search to top scrapable and unvisited URL
            content = ""
            for url in urls:
                logger.info(f"Attempting to retrieve relevant information from {url}")
                content = scrape(url)
                visited_urls.append(url)
                if content:
                    break
            if not content:
                logger.warning(f"No content could be scraped from these urls: {urls}")
                continue

            # attempt to extract information and parse into PreliminaryLocationData object
            location_data = get_preliminary_location(content, location.name)
            logger.trace(location_data.model_dump() if location_data else "No location data extracted")
            if not location_data:
                continue

            # Update previous location data with newly extracted information
            # save 1 LLM call if it's the first iteration
            if iter_count == 0:     
                preliminary_locations[i] = location_data
                citations.append(url)
                continue
            previous_json = preliminary_locations[i].model_dump_json()
            combined_data = update_location_data(preliminary_locations[i], location_data)
            changes = previous_json != combined_data.model_dump_json()
            if changes:
                preliminary_locations[i] = combined_data
                citations.append(url)

        transformed_data = preliminary_to_final_location_data(preliminary_locations[i], citations)
        logger.trace(transformed_data.model_dump())
        results.append(transformed_data)

    logger.debug(f"Pre-captioned data: {[r.model_dump() for r in results]}")
    # generate/refine captions for each image
    for i, r in enumerate(results):
        for name in r.images:
            caption, hashtags = generate_caption_hashtags(r.images[name].url)
            results[i].images[name].caption = caption
            results[i].images[name].hashtags = hashtags

    return results
