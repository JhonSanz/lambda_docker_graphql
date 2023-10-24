from graphene import ObjectType
from .data import brokers


class Query(ObjectType):
    def resolve_get_broker(root, info, id):
        broker = list(filter(lambda x: x["id"] == id, brokers))
        if not broker:
            raise Exception("Broker not found")
        return broker[0]
    
    def resolve_get_brokers(root, info):
        return brokers
