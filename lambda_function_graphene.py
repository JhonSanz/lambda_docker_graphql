# from graphene import ObjectType, String, Field, Schema, List
# from gql_graphene.mutation import CreateBroker, UpdateBroker, DeleteBroker
# from gql_graphene.query import Query
# from gql_graphene.type import Broker

# class MyMutations(ObjectType):
#     create_broker = CreateBroker.Field()
#     update_broker = UpdateBroker.Field()
#     delete_broker = DeleteBroker.Field()

# class MyQuery(Query):
#     broker = Field(Broker)
#     get_broker = Field(Broker, id=String())
#     get_brokers = List(Broker)

# schema = Schema(query=MyQuery, mutation=MyMutations)


# def handler(event, context):
#     result = schema.execute(event['query'])
#     result = {
#         "data": result.data,
#         "errors": [err.formatted for err in result.errors] if result.errors else [],
#     }
#     return {
#         'statusCode': 200,
#         'body': result
#     }

import graphene
from graphene import Node, Connection, String, relay, Int, ID

SHIPS = ['Tug boat', 'Row boat', 'Canoe', 'Titanic']
SHIPS = [{"id": str(i+1), "ship_type": boat} for i, boat in enumerate(SHIPS)]

class Ship(graphene.ObjectType):
    id = ID(required=True)
    ship_type = String()

    def resolve_ship_type(self, info):
        return self.ship_type

    class Meta:
        interfaces = (Node,)


SHIPS = [Ship(id=boat["id"], ship_type=boat["ship_type"]) for boat in SHIPS]


class ShipConnection(Connection):
    count = Int()

    def resolve_count(self, info):
        return len(self.edges)

    class Meta:
        node = Ship


class Query(graphene.ObjectType):
    ships = relay.ConnectionField(ShipConnection)

    def resolve_ships(self, info, **kwargs):
        return SHIPS

schema = graphene.Schema(query=Query)


result = schema.execute(
    '''
        query{
            ships(first: 2, last: 3){
                count,
                edges{
                    cursor,
                    node {
                        id,
                        shipType
                    }
                }
            } 
        }
    '''
)

# result = schema.execute(
#     '''
#         query {
#             ships(first: 10){
#                 count
#             } 
#         }
#     '''
# )

print(result)