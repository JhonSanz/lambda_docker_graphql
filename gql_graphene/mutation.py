from graphene import String, Field, Mutation
from .type import Broker
from .data import brokers


class CreateBroker(Mutation):
    class Arguments:
        id = String()
        name = String()
        website = String()
    broker = Field(lambda: Broker)

    def mutate(root, info, id, name, website):
        broker = Broker(id=id, name=name, website=website)
        brokers.append({"id": id, "name": name, "website": website})
        return CreateBroker(broker=broker)


class UpdateBroker(Mutation):
    class Arguments:
        id = String()
        name = String()
        website = String()
    broker = Field(lambda: Broker)

    def mutate(root, info, id, name, website):
        broker = Broker(id=id, name=name, website=website)
        old_broker = list(filter(lambda x: x["id"] == id, brokers))[0]
        brokers.remove(old_broker)
        brokers.append({"id": id, "name": name, "website": website})
        return UpdateBroker(broker)


class DeleteBroker(Mutation):
    class Arguments:
        id = String()
    broker = Field(lambda: Broker)

    def mutate(root, info, id):
        old_broker = list(filter(lambda x: x["id"] == id, brokers))
        if not old_broker:
            raise Exception("Broker not found")
        old_broker = old_broker[0]
        broker = Broker(id=old_broker["id"], name=old_broker["name"], website=old_broker["website"])
        brokers.remove(old_broker)
        return DeleteBroker(broker=broker)
