from boto3 import resource, client
from config import Config
import os
import boto3
import pandas as pd
import sys
import codecs
import csv

if sys.version_info[0] < 3: 
    from StringIO import StringIO # Python 2.x
else:
    from io import StringIO # Python 3.x


class s3Access():
    
    def __init__(self):
        # aws_id = os.environ['AWS_ID']
        # aws_secret = os.environ['AWS_SECRET']
        # self.client = client('s3' aws_access_key_id=aws_id,
            # aws_secret_access_key=aws_secret)
        self.client = client('s3')
        
    def readCsvFile(self,keyfile):
        csv_obj = self.client.get_object(Bucket=Config.bucket_name, Key=keyfile)
        body = csv_obj['Body']
        csv_string = body.read().decode('utf-8')
        df = pd.read_csv(StringIO(csv_string),names=['quote','author','category'])

        return df
