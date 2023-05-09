import json
import boto3
from os import environ

def lambda_handler(event, context):
    payload = event['queryStringParameters']
    
    username = payload['username']
    password = payload['password']
        
    # Initialize Cognito client
    cognito_client = boto3.client("cognito-idp")

    app_client_id = environ.get('APP_CLIENT_ID')

    # Attempt to authenticate the user
    try:
        response = cognito_client.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            },
            ClientId=app_client_id
        )

        if response.get('AuthenticationResult'):
            id_token = response['AuthenticationResult']['IdToken']
            access_token = response['AuthenticationResult']['AccessToken']
            refresh_token = response['AuthenticationResult']['RefreshToken']
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'id_token': id_token,
                    'access_token': access_token,
                    'refresh_token': refresh_token
                })
            }
        else:
            return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(response)
        }

    except cognito_client.exceptions.NotAuthorizedException as e:
        return {
            'statusCode': 401,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Incorrect username or password'})
        }
    except cognito_client.exceptions.UserNotFoundException as e:
        return {
            'statusCode': 404,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': f'User: {username} does not exist'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }