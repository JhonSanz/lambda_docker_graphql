import strawberry

@strawberry.type
class Money:
    id: str
    currency: str
