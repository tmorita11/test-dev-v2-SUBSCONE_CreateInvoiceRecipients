import os
import boto3
from lib.custom_exceptions import S3Error


class S3Accessor:
    def __init__(self, retail_type_cd):
        self.region = os.getenv('S3_REGION')
        self.bucket = os.getenv('S3_BUCKET')
        self.path = f"{retail_type_cd}/input/invoice/"

    def upload_json_data(self, file_name, json_data, tags):
        try:
            s3 = boto3.resource('s3', region_name=self.region)
            s3.Bucket(self.bucket).put_object(
                Key=f"{self.path}{file_name}",
                Body=json_data,
                ContentType='application/json',
                Tagging=tags
            )
        except Exception as ex:
            raise S3Error(f"S3アップロードで予期しないエラーが発生しました。: {ex}")
