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
        listofitems = list()
        response = self.table.scan(ProjectionExpression="chat_id,first_name")

        listofitems.extend(response['Items'])

        while 'LastEvaluatedKey' in response:
            response = self.table.scan(ProjectionExpression="chat_id,first_name",
                    ExclusiveStartKey=response['LastEvaluatedKey'])
            listofitems.extend(response['Items'])

        return listofitems 

    def compare_chat_id(self,chat_id):
        response = self.table.query(
            KeyConditionExpression=Key('chat_id').eq(chat_id)
        )
        if len(response['Items']) == 0:
            return False
        return True