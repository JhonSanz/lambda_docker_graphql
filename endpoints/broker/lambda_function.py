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
			mutation {
				updateBroker(
					id: "dfb707c4-78c6-11ee-b781-790e436ee555"
					name: "Pepperstone :D"
					website: "https://pepperstone.com :D"
				) {
					id
					name
					website
				}
			}
	"""
)
print(result)

