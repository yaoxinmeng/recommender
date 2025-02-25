from pydantic import BaseModel, Field

class PreliminaryImageData(BaseModel):
    name: str = Field(description="Name of the image")
    url: str = Field(description="URL of the image")


class TimeInterval(BaseModel):
    start: str  = Field(description="Start time formatted as HH:MM")
    end: str  = Field(description="End time formatted as HH:MM")


class PreliminaryOpeningHours(BaseModel):
    monday: TimeInterval
    tuesday: TimeInterval
    wednesday: TimeInterval
    thursday: TimeInterval
    friday: TimeInterval
    saturday: TimeInterval
    sunday: TimeInterval


class Offering(BaseModel):
    name: str 
    price: str


class PreliminaryLocationData(BaseModel):
    name: str = Field(description="Name of the location")
    address: str  = Field(description="Physical address of the location or event")
    opening_hours: PreliminaryOpeningHours
    description: str  = Field(description="A 350-400 character description of the location")
    offerings: list[Offering] = Field(description="List of offerings saved as a mapping of {<offering>: <price}", default=[])
    contact: str  = Field(description="Contact number with the format '+65-1234-5678'")
    images: list[PreliminaryImageData] = Field(description="List of images", default=[])
