# Scheduling Automated Tasks with CloudWatch and Lambda

## Project Overview

This project demonstrates how to schedule automated tasks using AWS CloudWatch and AWS Lambda. AWS Lambda allows you to run code without provisioning or managing servers, while CloudWatch enables you to set up event-based rules to trigger Lambda functions at specified times or intervals. In this project, you will:

1. **Create a Lambda Function**: Write and deploy a simple Lambda function.
2. **Create a CloudWatch Rule**: Set up a CloudWatch rule to trigger the Lambda function on a schedule.
3. **Manage Permissions**: Allow CloudWatch to invoke the Lambda function.
4. **Verify**: Ensure that the Lambda function is triggered according to the schedule.

## Prerequisites

Before running the scripts, make sure you have:

- **AWS Account**: An active AWS account to create and manage Lambda functions and CloudWatch rules.
- **IAM Role with Lambda Permissions**: An IAM role with the `AWSLambdaBasicExecutionRole` policy.
- **AWS CLI Configured**: Ensure the AWS CLI is installed and configured with your credentials.
- **Python Installed**: Python 3.x should be installed on your machine.
- **Boto3 Installed**: Boto3, the AWS SDK for Python, should be installed. Install Boto3 using:

  ```bash
  pip install boto3
  ```

## Project Steps

### 1. Create a Lambda Function

The following script creates a Lambda function that prints a message when triggered:

```python
import boto3
import zipfile

# Initialize a session using Boto3
region_name = 'your-region'
lambda_client = boto3.client('lambda', region_name=region_name)

# Define Lambda function code
lambda_code = """
import json

def lambda_handler(event, context):
    print("Lambda function triggered by CloudWatch!")
    # Add your logic here
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
```

### 2. Create a CloudWatch Rule

Create a CloudWatch rule to trigger the Lambda function every hour:

```python
import boto3

# Initialize a session using Boto3
events_client = boto3.client('events', region_name='your-region')

# Create CloudWatch rule
rule_name = 'HourlyLambdaTrigger'
response = events_client.put_rule(
    Name=rule_name,
    ScheduleExpression='rate(1 hour)',  # Change this to your desired schedule
    State='ENABLED'
)

print(f"Created CloudWatch Rule: {response['RuleArn']}")

# Grant CloudWatch permission to invoke the Lambda function
lambda_client.add_permission(
    FunctionName='ScheduledLambdaFunction',
    StatementId='UniqueStatementID',
    Action='lambda:InvokeFunction',
    Principal='events.amazonaws.com',
    SourceArn=response['RuleArn']
)

# Associate the rule with the Lambda function
response = events_client.put_targets(
    Rule=rule_name,
    Targets=[
        {
            'Id': '1',
            'Arn': 'arn:aws:lambda:your-region:your-account-id:function:ScheduledLambdaFunction'
        }
    ]
)

print("Associated Lambda function with CloudWatch rule")
```

### 3. Test and Verify

- **Deploy**: Ensure that both the Lambda function and CloudWatch rule are deployed.
- **Monitor**: Check CloudWatch Logs to verify that the Lambda function is triggered as scheduled.

## Explanation

- **Create Lambda Function**: Deploy a Lambda function that executes code whenever it's triggered.
- **Create CloudWatch Rule**: Set up a rule to trigger the Lambda function based on a schedule.
- **Manage Permissions**: Allow CloudWatch to invoke the Lambda function.
- **Associate Rule**: Link the CloudWatch rule to the Lambda function.

## Real-Life Use Cases

- **Scheduled Maintenance**: Automate regular maintenance tasks for AWS resources.
- **Periodic Data Processing**: Automatically process data at set intervals.
- **Automated Notifications**: Send notifications or alerts on a regular schedule.

## Conclusion

This project introduces you to scheduling and automating tasks using AWS Lambda and CloudWatch. By creating and managing Lambda functions and scheduling them with CloudWatch, you'll gain valuable experience with serverless computing and automated task scheduling in AWS.

Feel free to modify the scripts to suit your needs and explore further use cases for Lambda and CloudWatch.

```

This README provides a clear and detailed overview of the project, including setup instructions, code examples, and explanations for each step, ensuring you can implement and understand AWS Lambda scheduling and automation effectively.