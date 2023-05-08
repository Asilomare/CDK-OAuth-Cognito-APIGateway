# CDK-Cognito-API

This application seamlessly integrates AWS services such as API Gateway, Cognito, Boto3, and Lambda to establish a robust and efficient API. The API facilitates seamless provisioning and interaction with a Cognito backend. By leveraging these powerful AWS services, the application ensures a scalable, secure, and high-performance solution for user authentication and management.

## Methods

Signup and Auth methods use boto3 to interact with the Cognito UserPool

### Signup

This endpoint, accessible at awesome-domain.com/auth, is designed to initiate the creation of a new user.
The Cognito stack contains commented-out custom configurations of password requirements, multi-factor authentication (MFA), and custom onboarding or authentication Lambda functions for you to tailor to your needs.

Example Usage
```
import requests

headers = {'Content-Type': 'application/json'}

payload = {
    'username': 'awesome-user',
    'email': 'test@test.test',
    'temporary_password': 'Password123!@#'
}

res = requests.post("awesome-domain.com/auth", params=payload, headers=headers)
```

### Auth

The endpoint located at awesome-domain.com/auth is designed to handle user authentication and guide them through any necessary additional steps, in line with AWS Cognito standards. Upon successful authentication or initiation of a challenge, such as email verification or password reset, the function returns a session token that is valid for up to one day.

AWS Cognito follows a secure and flexible authentication flow, allowing developers to implement multiple authentication steps, such as MFA or custom challenge verification. With this endpoint, users can easily navigate the authentication process while ensuring a high level of security and compliance with AWS Cognito best practices.

Example Usage:
```
import requests

headers = {'Content-Type': 'application/json'}

payload = {
    'username': 'awesome-user',
    'password': 'Password123!@#'
}

res = requests.post("awesome-domain.com/login", params=payload, headers=headers)
```

### GPT

Please note that the final method included is a remnant from a previous project that involved ChatGPT. It may not be directly relevant to the current implementation and can be safely removed or disregarded

```
key = '<API KEY'
m = '<GPT PROMPT>' #E.g 'write a five line poem'

headers = {'Content-Type': 'application/json'}

payload = {
    'key': key,
    "message": m
}

res = requests.get("awesome-domain.com/gpt", params=payload, headers=headers)
```

## Configuration

Domain Name: To configure the domain name, navigate to stacks/api_stack.py and locate the definition of the 'api' variable. A valid SSL/TLS certificate for the website, stored in AWS Certificate Manager, is required for this configuration.

Authentication Options: During instantiation, you can customize the authentication process to fit your requirements. This includes defining custom onboarding/authentication Lambdas, enabling Multi-Factor Authentication (MFA), customizing SMS messages, and setting password requirements. Fine-grained control over the authentication flow allows for a tailored and secure user experience.