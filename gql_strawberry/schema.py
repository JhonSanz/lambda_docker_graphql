import typing
import strawberry


@strawberry.type
class Book:
    title: str
    author: str

def get_books():
    # return [
    #     Book(
    #         title="The Great Gatsby",
    #         author="F. Scott Fitzgerald",
    #     ),
    #     Book(
    #         title="Test",
    #         author="Me",
    #     ),
    # ]

    return [
        {
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
        },
        {
            "title": "test",
            "author": "Me",
        }

    ]

@strawberry.type
class Query:
    books: typing.List[Book] = strawberry.field(resolver=get_books)


schema = strawberry.Schema(query=Query)
result = schema.execute_sync(
    '''
        query {
            books{
                title
                author
            } 
        }
    '''
)
print(result)