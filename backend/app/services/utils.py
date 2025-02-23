from app.types.model_outputs import PreliminaryLocationData, PreliminaryOpeningHours, TimeInterval

def intialise_preliminary_locations(locations: list[str]) -> list[PreliminaryLocationData]:
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