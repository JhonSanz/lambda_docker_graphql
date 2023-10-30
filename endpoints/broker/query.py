import strawberry
import boto3
from boto3.dynamodb.conditions import Key
from type import Broker
from utils import PaginationWindow, get_pagination_window


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('broker')

@strawberry.type
class Query:
	@strawberry.field(description='Get a list of broker')
	def brokers(
		self,
		order_by: str,
		limit: int,
		offset: int = 0,
		name: str | None = None,
	) -> PaginationWindow[Broker]:
		response = table.scan()
		brokers = response['Items']

		while 'LastEvaluatedKey' in response:
			response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
			brokers.extend(response['Items'])

		filters = {}
		if name:
			filters['name'] = name
		return get_pagination_window(
			dataset=brokers,
			ItemType=Broker,
			order_by=order_by,
			limit=limit,
			offset=offset,
			filters=filters,
		)

	@strawberry.field(description='Get a broker record.')
	def broker(self, id: str) -> Broker:
		broker = table.query(
			KeyConditionExpression=Key('id').eq(id)
		)['Items']
		if not broker:
			raise Exception('broker not found')
		broker = broker[0]
		return Broker.from_row(broker)
