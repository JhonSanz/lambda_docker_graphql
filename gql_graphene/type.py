from graphene import ObjectType, String

class Broker(ObjectType):
    id = String()
    name = String()
    website = String()
