import strawberry
from type import Broker
from data import brokers

@strawberry.type
class Mutation:
    @strawberry.field
    def add_broker(self, name: str, website: str) -> Broker:
        new_broker = Broker.from_row(**{
            "id": len(brokers) + 1,
            "name": name,
            "website": website
        })
        brokers.append({
            "id": len(brokers) + 1,
            "name": name,
            "website": website
        })
        return new_broker

    @strawberry.field
    def delete_broker(self, id: str) -> Broker:
        to_delete = list(filter(lambda x: x["id"] == id, brokers))
        if not to_delete:
            raise Exception("Broker does not exist")
        to_delete = to_delete[0]
        brokers.remove(to_delete)
        return Broker.from_row({
            "id": to_delete["id"],
            "name": to_delete["name"],
            "website": to_delete["website"]
        })
