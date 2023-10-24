import strawberry
from query import Query


schema = strawberry.Schema(query=Query)
result = schema.execute_sync(
    '''
        query {
            brokers {
                name
                website
            } 
        }
    '''
)
print(result)
