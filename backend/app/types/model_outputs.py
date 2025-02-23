from typing import Optional
from pydantic import BaseModel, Field

class PreliminaryImageData(BaseModel):
    name: str = Field(description="Name of the image")
    url: str = Field(description="URL of the image")
    hashtags: list[str] = Field(description="List of hashtags to be used when sharing the image")


class TimeInterval(BaseModel):
    start: str | None  = Field(description="Start time formatted as HH:MM")
    end: str | None  = Field(description="End time formatted as HH:MM")


class PreliminaryOpeningHours(BaseModel):
    monday: TimeInterval
    tuesday: TimeInterval
    wednesday: TimeInterval
    thursday: TimeInterval
    friday: TimeInterval
    saturday: TimeInterval
    sunday: TimeInterval


class Offering(BaseModel):
    name: str | None 
    price: str | None 


class PreliminaryLocationData(BaseModel):
    name: str | None = Field(description="Name of the location")
    address: str | None  = Field(description="Physical address of the location or event")
    opening_hours: PreliminaryOpeningHours
    description: str | None  = Field(description="A 350-400 character description of the location")
    offerings: list[Offering] = Field(description="List of offerings saved as a mapping of {<offering>: <price}")
    contact: str | None  = Field(description="Contact number with the format '+65-1234-5678'")
    images: list[PreliminaryImageData] = Field(description="List of images")
