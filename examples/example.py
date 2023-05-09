import requests
import json

API_GATEWAY_URL = 'https://example.com/{}' # or  'https://XXXXXXX.execute-api.us-east-1.amazonaws.com/prod/{}'

def signup(username, temporary_password, email):
    """
    Sign up a new user with a temporary password.
    
    :param username: The desired username.
    :param temporary_password: The temporary password for the new user.
    :param email: The email address for the new user.
    :return: The response from the /signup Endpoint.
    """
    headers = {'Content-Type': 'application/json'}
    payload = {
        'username': username,
        'email': email,
        'temporary_password': temporary_password
    }
    
    res = requests.post(API_GATEWAY_URL.format('signup'), params=payload, headers=headers)
    
    return json.loads(res.text)


def auth(username, password):
    """
    Authenticate a user with a given username and password.
    
    :param username: The user's username.
    :param password: The user's password.
    :return: The authentication response containing tokens and challenge data.
    """
    headers = {'Content-Type': 'application/json'}
    payload = {
        'username': username,
        'password': password
    }
    
    res = requests.post(API_GATEWAY_URL.format('login'), params=payload, headers=headers)
    
    return json.loads(res.text)
    
def challenge(username, temporary_password, new_password):
    """
    Complete the challenge for a user with a temporary password.
    
    :param username: The user's username.
    :param temporary_password: The user's temporary password.
    :param new_password: The new password for the user.
    :return: The response from the /challenge Endpoint.
    """
    auth_data = auth(username, temporary_password)
    
    if 'error' in auth_data:
        return auth_data
    
    challenge_name = auth_data['ChallengeName']
    session = auth_data['Session']
    
    headers = {'Content-Type': 'application/json'}
    payload = {
        'challenge_name': challenge_name,
        'session': session,
        'challenge_responses': json.dumps({
            'USERNAME': username,
            'NEW_PASSWORD': new_password
        })
    }
    
    res = requests.post(API_GATEWAY_URL.format('challenge'), params=payload, headers=headers)
    
    return json.loads(res.text)

def authenticated_request(username, password):
    """
    Send an authenticated request to the GPT API.
    
    :param username: The user's username.
    :param password: The user's password.
    :return: The response from the /gpt Endpoint.
    """
    auth_data = auth(username, password)
    auth_token = auth_data['id_token']
    
    api_key = '<OPENAI-KEY>'
    message = '<GPT PROMPT>'
    
    headers = {
        'Auth': auth_token,
        'Content-Type': 'application/json'
    }
    payload = {
        'key': api_key,
        'message': message
    }
    
    res = requests.post(API_GATEWAY_URL.format('gpt'), params=payload, headers=headers)
    
    return json.loads(res.text)
    
    
username = 'my-awesome-user5'
email = 'my@awesome.email'
temporary_password = 'MyTemp0raryPa33word!'
password = "MyAwesomePa33word!2"

if __name__ == '__main__':
    # Sign up a new user
    signup(username, temporary_password, email)
    
    # Complete the challenge for the new user
    challenge(username, temporary_password, password)
    
    # Send an authenticated request
    res = authenticated_request(username, password)
    
    print(res)