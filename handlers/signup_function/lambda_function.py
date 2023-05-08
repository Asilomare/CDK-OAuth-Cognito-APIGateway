import json
from os import environ
import boto3
import datetime

# Custom JSON serializer to handle datetime objects
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super(CustomJSONEncoder, self).default(obj)

def lambda_handler(event, context):
    
    payload = event['queryStringParameters']
    
    user_pool_id = environ['USER_POOL_ID']
    username = payload['username']
    email = payload['email']
    temporary_password = payload['temporary_password']
    
    # Initialize the Cognito client
    cognito_client = boto3.client('cognito-idp')

    # Create the user
    try:
        response = cognito_client.admin_create_user(
            UserPoolId=user_pool_id,
            Username=username,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': email
                },
                {
                    'Name': 'email_verified',
                    'Value': 'true'
                }
            ],
            TemporaryPassword=temporary_password,
            MessageAction='SUPPRESS'  # Suppress the default welcome email
        )
        
        # Properly format the response for API Gateway
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(response, cls=CustomJSONEncoder)
        }

    except cognito_client.exceptions.UsernameExistsException as e:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'User already exists'})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
