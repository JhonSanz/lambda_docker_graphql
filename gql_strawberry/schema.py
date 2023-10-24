import strawberry
from query import Query
from mutations import Mutation


schema = strawberry.Schema(query=Query, mutation=Mutation)
result = schema.execute_sync(
    '''
        {
            brokers(orderBy: "name", offset: 0, limit: 3) {
                items {
                    name
                    website
                }
                totalItemsCount
            }
        }
    '''
)
print(result)
print("\n"*2)

# print("\n"*2)
# print(result)
# print("\n"*2)
# result = schema.execute_sync(
#     '''
#         mutation {
#             addBroker(name: "test", website: "test.com") {
#                 name
#                 website
#             } 
#         }
#     '''
# )
# print(result)
# print("\n"*2)
# result = schema.execute_sync(
#     '''
#         query {
#             brokers {
#                 name
#                 website
#             } 
#         }
#     '''
# )
# print(result)

result = schema.execute_sync(
    '''
        mutation {
            deleteBroker(id: "123") {
                name
                website
            } 
        }
    '''
)
print(result)
print("\n"*2)


result = schema.execute_sync(
    '''
        {
            brokers(orderBy: "name", offset: 0, limit: 3) {
                items {
                    name
                    website
                }
                totalItemsCount
            }
        }
    '''
)
print(result)
print("\n"*2)