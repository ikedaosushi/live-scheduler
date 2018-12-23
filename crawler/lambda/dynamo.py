import os, sys, re, datetime, time
from boto3.session import Session

def put_items(items):
    dynamodb = Session().resource('dynamodb', region_name='ap-northeast-1')
    table_name = os.environ.get('DYNAMODB_TABLE')
    table = dynamodb.Table(table_name)

    for item in items:
      item = {k: v for k, v in item.items() if v}
      table.put_item(Item=item)

