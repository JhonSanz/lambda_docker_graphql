import strawberry

@strawberry.type
class Broker:
    id: int
    name: str
    website: str