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