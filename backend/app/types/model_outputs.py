from pydantic import BaseModel, Field

class BasicLocationData(BaseModel):
    name: str = Field(description="Name of the location")
    address: str = Field(description="Physical address of the location or event. If this information is not available, return an empty string")
    description: str = Field(description="A 350-400 character description of the location. If this information is not available, return an empty string")
    contact: str = Field(description="Contact number with the format '+65-1234-5678'. If this information is not available, return an empty string")


class OpeningHours(BaseModel):
    monday: str = Field(description="Opening hours on Monday")
    tuesday: str = Field(description="Opening hours on Tuesday")
    wednesday: str = Field(description="Opening hours on Wednesday")
    thursday: str = Field(description="Opening hours on Thursday")
    friday: str = Field(description="Opening hours on Friday")
    saturday: str = Field(description="Opening hours on Saturday")
    sunday: str = Field(description="Opening hours on Sunday")


class ImageData(BaseModel):
    url: str = Field(description="URL of the image")
    caption: str = Field(description="Caption of the image")
    hashtags: list[str] = Field(description="List of hashtags to be used when sharing the image")


class DetailedLocationData(BaseModel):
    opening_hours: OpeningHours
    address: str = Field(description="Physical address of the location or event.")
    description: str = Field(description="A 350-400 character description of the location")
    offerings: dict[str, str] = Field(description="List of offerings saved as a mapping of {<offering>: <price}")
    contact: str = Field(description="Contact number with the format '+65-1234-5678'")
    images: dict[str, ImageData] = Field(description="Dictionary of images saved as a mapping of {<image_name>: <ImageData>}")