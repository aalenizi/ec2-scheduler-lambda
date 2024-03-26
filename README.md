# Auto Start/Stop EC2 Instances

## Overview

The `ec2-scheduler-lambda` AWS Lambda function is designed to automatically start and stop EC2 instances based on a predefined schedule. This schedule is defined using tags in the AWS Management Console, enabling cost-effective management of EC2 resources by ensuring they run only when needed.

## Requirements

- AWS Account
- Python 3.7
- Boto3 library
- Pytz library

## Setup

1. **IAM Role Creation**: Create an IAM role `ec2-scheduler-lambda-role` with EC2 access and Lambda execution policies.
2. **Schedule Tag**: Tag your EC2 instances with the `Schedule` key and value in the format `Day1,Day2,Day3 hh:mm-hh:mm`.
3. **Deploy Lambda Function**: Upload the `lambda_function.py` as your Lambda function code.
4. **EventBridge Rule**: Set up an Amazon EventBridge (formerly CloudWatch Events) rule to trigger the Lambda function every 5 minutes using the expression `rate(5 minutes)`.

## Function Policy and Role

Ensure the Lambda function has the following policy attached:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeInstances",
        "ec2:StartInstances",
        "ec2:StopInstances"
      ],
      "Resource": "*"
    }
  ]
}
```
This policy enables the function to describe, start, and stop instances.
## Usage
##Usage
Once set up, the Lambda function will check the tagged EC2 instances and start or stop them based on the current day and time matching the Schedule tag.

##Contributing
Feel free to fork the repository and submit pull requests to contribute to the development of this function.
