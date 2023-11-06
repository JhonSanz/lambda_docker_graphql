# Strawberry endpoints + lambda + dynamodb

### Create endpoints

1. Create a dir named `currency`
2. Create `currency/type.py`
```python
import strawberry

@strawberry.type
class Currency:
    id: str
    name: str

```
3. run `python api_generator.py` like this
```python
from currency.type import Currency
# All the code in api_generator.py
Creator(Currency, "currency").run()
```
4. enjoy

### Create zip files
1. In `lambda_zip_generator.py` modify for statement according to your needs
```python
for item in [
    "currency",
]:
    install_dependencies(item)

```
2. enjoy

### Todo

- fix auto zip (check manual zipping)
- CDK grant access to dynamoDB via lambda rol


---

### Notes

It was necessary to add these headers in the lambda function response to avoid CORS error


```python
def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'headers': {
            "Content-Type": "application/json",
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,X-Amz-Security-Token,Authorization,X-Api-Key,X-Requested-With,Accept,Access-Control-Allow-Methods,Access-Control-Allow-Origin,Access-Control-Allow-Headers",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "X-Requested-With": "*"
        },
        'body': 'Test response without CORS'
    }
```