from boto3 import resource, client
from config import Config
import os
import boto3
import sys


if sys.version_info[0] < 3: 
    from StringIO import StringIO # Python 2.x
else:
    from io import StringIO # Python 3.x


class dynamoDBAccess():
    
    def __init__(self):
        # aws_id = os.environ['AWS_ID']
        # aws_secret = os.environ['AWS_SECRET']
        # self.client = client('s3' aws_access_key_id=aws_id,
            # aws_secret_access_key=aws_secret)
        self.resource = resource("dynamodb")
        self.table = self.resource.Table(table_name)
        
    def putRow(self,chat_id,date,first_name,username):   
        response = self.table.put_item(
            Item = {
                "chat_id": chat_id,
                "date": date,
                "first_name":first_name,
                "username":username,
            }
        )
    

    def scan_table(self):
        response = self.table.scan("chat_id,first_name")
        return response['Items']

    def filter_table(self,chat_id):
        # projection expression
        response = self.table.query("chat_id,first_name")
        return response['Items']
