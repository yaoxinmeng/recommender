import json

from loguru import logger

from app.types.schema import LocationData, OpeningHours, ImageData
from app.types.model_outputs import PreliminaryLocationData, TimeInterval, Offering, PreliminaryImageData
from app.services.tools.search import search_duckduckgo
from app.services.tools.scraper import scrape
from app.services.tools.structured_output import get_preliminary_location, get_candidate_locations, get_search_queries
from app.services.tools.image_caption import generate_caption
from app.services.utils import initialise_preliminary_locations

def venue_agent(query: str, n_results: int) -> list[LocationData]:
    # craft a list of candidate locations
    sg_query = query + " Singapore"
    urls = search_duckduckgo(sg_query)
    locations: list[str] = []
    for result in urls:
        content = scrape(result)
        candidate_locations = get_candidate_locations(content, sg_query, n_results)
        locations.extend([l for l in candidate_locations if l])

        logger.trace(locations)
        if len(locations) >= n_results:
            break

    # create an empty PreliminaryLocationData object for each location
    preliminary_locations = initialise_preliminary_locations(locations[:n_results])

    # attempt to fill in the details of each preliminary location
    results: list[LocationData] = []
    for i, location in enumerate(preliminary_locations):
        citations = [*urls]
        for _ in range(2):  # iterate up to n times to refine the information of each candidate location
            search_queries = get_search_queries(location.name + " Singapore", location)
            logger.trace(search_queries)
            if not search_queries:
                continue

            # extract data from first search query
            query = search_queries[0]
            urls = search_duckduckgo(query)
            logger.trace(urls)
            urls = [s for s in urls if s not in citations]  # check if URL has been visited already
            for url in urls[:2]:  # limit search to top 2 each time
                logger.info(f"Attempting to retrieve relevant information from {url}")
                content = scrape(url)
                logger.trace(content)

                # attempt to parse into PreliminaryLocationData and update location
                location_data = get_preliminary_location(content, location.name)
                logger.trace(location_data)
                updated, preliminary_locations[i] = _update_location_data(preliminary_locations[i], location_data)
                if updated:
                    citations.append(url)

        transformed_data = _preliminary_to_final_location_data(preliminary_locations[i], citations)
        logger.trace(transformed_data)
        results.append(transformed_data)

    # generate captions for each image
    for i, r in enumerate(results):
        for name in r.images:
            caption = generate_caption(r.images[name])
            results[i].images[name].caption = caption

    return results


def _update_location_data(old_data: PreliminaryLocationData, new_data: PreliminaryLocationData | None) -> tuple[bool, PreliminaryLocationData]:
    """
    Update the old data with newly scraped data. We make the assumption that the new data is more relevant to the old data,
    but this can be formally implemented in the future with a LLM call.

    Returns a tuple containing a flag of whether any updates were made, and the updated model.
    """
    if not new_data:
        return False, old_data
    
    # convert to dictionary for easier iteration
    new_dict = new_data.model_dump()
    old_dict = old_data.model_dump()
    old_dict_json = json.dumps(old_dict)

    # update fields individually
    for key in new_dict:
        if key == "opening_hours":
            for day in new_dict[key]:
                if new_dict[key][day]["start"]:
                    old_dict[key][day]["start"] = new_dict[key][day]["start"]
                if new_dict[key][day]["end"]:
                    old_dict[key][day]["end"] = new_dict[key][day]["end"]
        elif key == "offerings" or key == "images":
            old_dict[key].extend(new_dict[key])
        else:
            if new_dict[key]:
                old_dict[key] = new_dict[key]

    # check if any updates were made
    changes = old_dict_json != json.dumps(old_dict)

    return changes, PreliminaryLocationData.model_validate(old_dict)


def _preliminary_to_final_location_data(preliminary: PreliminaryLocationData, citations: list[str]) -> LocationData:
    def format_opening_hours(interval: TimeInterval) -> str:
        start = "".join(interval.start.split(":"))
        end = "".join(interval.end.split(":"))
        return f"{start}-{end}"
    
    def format_offerings(offerings: list[Offering]) -> dict[str, str]:
        return {
            k.name: k.price for k in offerings if k.name is not None and k.price is not None
        }
    
    def format_images(images: list[PreliminaryImageData]) -> dict[str, ImageData]:
        formatted = {}
        for i in images:
            if not i.name or not i.url:
                continue
            formatted[i.name] = ImageData(
                caption="",
                url=i.url,
                hashtags=i.hashtags
            )
        return formatted

    return LocationData(
            name=preliminary.name,
            address=preliminary.address,
            opening_hours=OpeningHours(
                monday=format_opening_hours(preliminary.opening_hours.monday),
                tuesday=format_opening_hours(preliminary.opening_hours.tuesday),
                wednesday=format_opening_hours(preliminary.opening_hours.wednesday),
                thursday=format_opening_hours(preliminary.opening_hours.thursday),
                friday=format_opening_hours(preliminary.opening_hours.friday),
                saturday=format_opening_hours(preliminary.opening_hours.saturday),
                sunday=format_opening_hours(preliminary.opening_hours.sunday),
            ),
            description=preliminary.description,
            offerings=format_offerings(preliminary.offerings),
            contact=preliminary.contact,
            images=format_images(preliminary.images),
            citation=citations
        )