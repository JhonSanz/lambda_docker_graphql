import typing
import strawberry
from type import Broker
from data import brokers


def get_books():
    return [Broker(
        id=broker["id"],
        name=broker["name"],
        website=broker["website"],
    ) for broker in brokers]

@strawberry.type
class Query:
    brokers: typing.List[Broker] = strawberry.field(resolver=get_books)
