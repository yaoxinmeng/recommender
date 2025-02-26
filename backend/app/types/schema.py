from pydantic import BaseModel, Field

class OpeningHours(BaseModel):
    """
    The opening hours of each day formatted as `<start>-<end>`, 
    where the start and end time is formatted as HHMM (e.g. `1030-2100`).

    :param str monday: Opening hours on Monday
    :param str tuesday: Opening hours on Tuesday
    :param str wednesday: Opening hours on Wednesday
    :param str thursday: Opening hours on Thursday
    :param str friday: Opening hours on Friday
    :param str saturday: Opening hours on Saturday
    :param str sunday: Opening hours on Sunday
    """
    monday: str
    tuesday: str
    wednesday: str
    thursday: str
    friday: str
    saturday: str
    sunday: str


class ImageData(BaseModel):
    """
    The relevant information of each image.

    :param str caption: The caption of the image in less than 70 words
    :param str url: The URL of the image
    :param list[str] hashtags: A list of hashtags to be used when sharing the image
    """
    caption: str
    url: str
    hashtags: list[str]


class LocationData(BaseModel):
    """
    Saves the relevant information of a single location.

    :param str name: Name of the location
    :param str address: Physical address of the location or event
    :param OpeningHours opening_hours: Opening hours in the 2400 format
    :param str description: A 350-400 character description of the location
    :param dict[str, str] offerings: List of offerings saved as a mapping of {<offering>: <price>}
    :param str contact: Contact number with the format "+65-1234-5678"
    :param dict[str, ImageData] images: Dictionary of images saved as a mapping of {<image_name>: <ImageData>}
    :param list[str] citation: List of sources used to generate this data
    """
    name: str
    address: str
    opening_hours: OpeningHours
    description: str
    offerings: dict[str, str]
    contact: str
    images: dict[str, ImageData]
    citation: list[str]
