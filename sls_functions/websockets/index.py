import json
import logging
import os
from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Any, Dict

import boto3

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if os.getenv("IS_OFFLINE"):
    dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")
else:
    dynamodb = boto3.resource("dynamodb")

WEBSOCKET_HTTP_URL = os.getenv("WEBSOCKET_HTTP_URL", "http://localhost:3001")

apigateway = boto3.client("apigatewaymanagementapi", endpoint_url=WEBSOCKET_HTTP_URL)


STAGE = os.getenv("STAGE")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

CONNECT = "CONNECT"
DISCONNECT = "DISCONNECT"
TABLE_NAME = "usersTable"


def get_response(status_code, body=None) -> Dict[str, Any]:
    response = {
        "isBase64Encoded": True,
        "statusCode": status_code.value,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
        },
    }
    if body:
        response["body"] = json.dumps(body)
    return response


def add_connection(connection_id: str) -> None:
    table = dynamodb.Table(TABLE_NAME)
    event_time = datetime.now()
    table.put_item(
        Item={
            "connection_id": connection_id,
            "created_at": event_time.strftime("%Y-%m-%d %H:%M:%S"),
            "expires_at": int((event_time + timedelta(days=2)).timestamp()),
            "email": "test@test.com",
        }
    )
    logger.info(f"Added new connnection `{connection_id}`.")


def remove_connection(connection_id: str) -> None:
    table = dynamodb.Table(TABLE_NAME)
    item = table.get_item(Key={"connection_id": connection_id})
    if "Item" in item:
        table.delete_item(Key={"connection_id": connection_id})
        logger.info(f"Removed connection `{connection_id}`.")
    else:
        logger.info(f"Not found connection `{connection_id}`.")


def connection_handler(event, *args, **kwargs):
    connection_id = event["requestContext"].get("connectionId")
    event_type = event["requestContext"]["eventType"]
    logger.info(event_type)
    if event_type == CONNECT:
        logger.info(f"Connect requested with id: {connection_id}")
        add_connection(connection_id)
        return get_response(HTTPStatus.OK)
    elif event_type == DISCONNECT:
        logger.info(f"Disconnect requested from {connection_id}")
        remove_connection(connection_id)
        return get_response(HTTPStatus.OK)
    else:
        logger.error(f"Connection manager received unrecognized eventType: {event}")
        return get_response(
            HTTPStatus.BAD_REQUEST, {"error": "unrecognized socket action"}
        )


def default_handler(event, *args, **kwargs):
    connection_id = event["requestContext"].get("connectionId")
    try:
        apigateway.post_to_connection(
            Data=json.dumps({"test": "test"}).encode("utf-8"),
            ConnectionId=connection_id,
        )
    except apigateway.exceptions.GoneException:
        remove_connection(connection_id)
    return get_response(HTTPStatus.OK)
