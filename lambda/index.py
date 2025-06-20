import boto3
from PIL import Image
import io
import os

s3 = boto3.client('s3')

def lambda_handler(event, context):
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    destination_bucket = os.environ['DEST_BUCKET']

    response = s3.get_object(Bucket=source_bucket, Key=key)
    image = Image.open(response['Body'])

    image = image.resize((300, 300))
    buffer = io.BytesIO()
    image.save(buffer, 'JPEG')
    buffer.seek(0)

    s3.put_object(Bucket=destination_bucket, Key=key, Body=buffer, ContentType='image/jpeg')

    return {
        'statusCode': 200,
        'body': f'Image resized and saved to {destination_bucket}'
    }
