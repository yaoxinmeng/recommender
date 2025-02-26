from app.types.model_outputs import PreliminaryLocationData, PreliminaryOpeningHours, TimeInterval, PreliminaryImageData, Offering
from app.types.schema import LocationData, ImageData, OpeningHours

def initialise_preliminary_locations(locations: list[str]) -> list[PreliminaryLocationData]:
    """
    Generate empty `PreliminaryLocationData` objects based on the list of location names.

    :param list[str] locations: List of location names
    :return list[PreliminaryLocationData]: List of objects with only the `name` field filled
    """
    return [PreliminaryLocationData(
        name=location,
        address="",
        opening_hours=PreliminaryOpeningHours(
            monday=TimeInterval(
                start="",
                end=""
            ),
            tuesday=TimeInterval(
                start="",
                end=""
            ),
            wednesday=TimeInterval(
                start="",
                end=""
            ),
            thursday=TimeInterval(
                start="",
                end=""
            ),
            friday=TimeInterval(
                start="",
                end=""
            ),
            saturday=TimeInterval(
                start="",
                end=""
            ),
            sunday=TimeInterval(
                start="",
                end=""
            )
        ),
        description="",
        offerings=[],
        contact="",
        images=[]
    ) for location in locations]


def preliminary_to_final_location_data(preliminary: PreliminaryLocationData, citations: list[str]) -> LocationData:
    """
    Convert a `PreliminaryLocationData` object to a `LocationData` object. Missing fields are left as either blank 
    strings or empty lists.

    :param PreliminaryLocationData preliminary: The `PreliminaryLocationData` object
    :param list[str] citations: The list of citations that were used to generate this object
    :return LocationData: The transformed object. The caption and hashtags of each image are left empty.
    """
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
        urls = []
        for i in images:
            if not i.name or not i.url:
                continue
            # remove duplicate images 
            if i.url in urls:
                continue
            urls.append(i.url)
            formatted[i.name] = ImageData(
                caption="",
                url=i.url,
                hashtags=[]
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