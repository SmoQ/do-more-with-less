try:
    import config_local  # noqa: F401
except ImportError:
    pass
import json
import os
from datetime import datetime, timedelta

import boto3
import django_setup  # noqa: F401
from todo.models import Item, ToDo

WEBSOCKET_HTTP_URL = os.getenv("WEBSOCKET_HTTP_URL", "http://localhost:3001")
TABLE_NAME = "usersTable"
if os.getenv("IS_OFFLINE"):
    dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")
else:
    dynamodb = boto3.resource("dynamodb")

apigateway = boto3.client("apigatewaymanagementapi", endpoint_url=WEBSOCKET_HTTP_URL)


def handler(event, *args, **kwargs):
    title = event.get("title")
    obj, _ = ToDo.objects.get_or_create(title=title)
    number = obj.item_set.all().count() + 1
    item = Item.objects.create(
        title=f"Title {number}",
        description=f"Description {number}",
        due_date=datetime.now() + timedelta(days=number),
        todo_list=obj,
    )
    table = dynamodb.Table(TABLE_NAME)
    items = table.scan()["Items"]
    for _item in items:
        msg = f"{item.title} {item.description}"
        data = json.dumps({"msg": msg, "todo_id": obj.id, "title": obj.title}).encode(
            "utf-8"
        )
        connection_id = _item["connection_id"]
        try:
            apigateway.post_to_connection(Data=data, ConnectionId=connection_id)
        except apigateway.exceptions.GoneException:
            pass
    print(f"Successfully created item {item}.")
