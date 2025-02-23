from pydantic import BaseModel, Field

class OpeningHours(BaseModel):
    """
    The opening hours of each day is formatted as `<start>-<end>`, 
    where the start and end time is formatted as HHMM (e.g. `1030-2100`).
    """
    monday: str = Field(description="Opening hours on Monday")
    tuesday: str = Field(description="Opening hours on Tuesday")
    wednesday: str = Field(description="Opening hours on Wednesday")
    thursday: str = Field(description="Opening hours on Thursday")
    friday: str = Field(description="Opening hours on Friday")
    saturday: str = Field(description="Opening hours on Saturday")
    sunday: str = Field(description="Opening hours on Sunday")


class ImageData(BaseModel):
    caption: str = Field(description="Caption of the image")
    url: str = Field(description="URL of the image")
    hashtags: list[str] = Field(description="List of hashtags to be used when sharing the image")


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
