import json
import strawberry
from query import Query
from mutations import Mutation

def lambda_handler(event, context):
	body = json.loads(event['body'])
	if not body.get('query'):
		return {
			'statusCode': 400,
			'body': 'Bad body bro'
		}
	schema = strawberry.Schema(query=Query, mutation=Mutation)
	result = schema.execute_sync(body['query'])
	return {
		'statusCode': 200,
		'body': json.dumps(
			{
				'data': result.data,
				'errors': [
					{
						'msg': err.message,
						'location': [
							{'line': loc.line, 'column': loc.column}
							for loc in err.locations
						]
					}
					for err in result.errors
				] if result.errors else []
			}
		)
	}


schema = strawberry.Schema(query=Query, mutation=Mutation)
result = schema.execute_sync(
	"""
		{
			accounts(
				orderBy: "id", offset: 0, limit: 5,
				query: {
					name: {
						exact: "account 1"
					},
					brokerId: {
						exact: "1"
					}
				}
			) {
				items {
					id
					name
					details
					leverage
				}
				totalItemsCount
			}
		}
	"""
)
print(result)
