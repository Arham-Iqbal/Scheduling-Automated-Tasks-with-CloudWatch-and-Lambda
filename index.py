import boto3
import zipfile
import os

# Initialize a session using Boto3
region_name = 'your-region'
lambda_client = boto3.client('lambda', region_name=region_name)
events_client = boto3.client('events', region_name=region_name)

# Define Lambda function code
lambda_code = """
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("Lambda function triggered by CloudWatch!")
    # Example logic: process an event or perform some actions
    # For demonstration, just returning a success message
    return {
        'statusCode': 200,
        'body': json.dumps('Lambda function executed successfully!')
    }
"""

# Save the Lambda function code to a file
lambda_code_path = 'lambda_function.py'
with open(lambda_code_path, 'w') as f:
    f.write(lambda_code)

# Create a zip file of the Lambda function code
zip_file_path = '/tmp/lambda_function.zip'
with zipfile.ZipFile(zip_file_path, 'w') as lambda_zip:
    lambda_zip.write(lambda_code_path, arcname='lambda_function.py')

# Read the zip file content
with open(zip_file_path, 'rb') as f:
    zip_content = f.read()

# Create Lambda function
lambda_function_name = 'ScheduledLambdaFunction'
iam_role_arn = 'arn:aws:iam::your-account-id:role/your-lambda-role'

response = lambda_client.create_function(
    FunctionName=lambda_function_name,
    Runtime='python3.8',
    Role=iam_role_arn,
    Handler='lambda_function.lambda_handler',
    Code=dict(ZipFile=zip_content),
    Timeout=10,
    MemorySize=128,
    Publish=True
)

print(f"Created Lambda Function: {response['FunctionArn']}")

# Create CloudWatch rule to trigger Lambda function every hour
rule_name = 'HourlyLambdaTrigger'
response = events_client.put_rule(
    Name=rule_name,
    ScheduleExpression='rate(1 hour)',  # Change this to your desired schedule
    State='ENABLED'
)

print(f"Created CloudWatch Rule: {response['RuleArn']}")

# Grant CloudWatch permission to invoke the Lambda function
statement_id = 'UniqueStatementID'
response = lambda_client.add_permission(
    FunctionName=lambda_function_name,
    StatementId=statement_id,
    Action='lambda:InvokeFunction',
    Principal='events.amazonaws.com',
    SourceArn=response['RuleArn']
)

print(f"Granted permission to CloudWatch: {response}")

# Associate the rule with the Lambda function
response = events_client.put_targets(
    Rule=rule_name,
    Targets=[
        {
            'Id': '1',
            'Arn': f"arn:aws:lambda:{region_name}:your-account-id:function:{lambda_function_name}"
        }
    ]
)

print("Associated Lambda function with CloudWatch rule")
