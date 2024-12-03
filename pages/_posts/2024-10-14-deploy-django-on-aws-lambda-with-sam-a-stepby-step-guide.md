---
title: "Deploy Django on AWS Lambda with SAM: A Step-by-Step Guide"
description: Learn how to deploy a serverless Django application on AWS Lambda using the Serverless Application Model (SAM).
author: null
excerpt: null
date: 2019-08-22T15:20:28.000Z
lastmod: 2024-10-14T15:53:39.822Z
draft: true
tags:
    - AWS
    - Django
    - Serverless
    - Lambda
    - SAM
categories:
    - Serverless
    - Django
    - AWS
meta: null
snippet: null
slug: null
---


## **How AWS SAM Fits into the Architecture**

By using AWS SAM, you can define all the components of your serverless Django application—including Lambda functions, API Gateway, RDS databases, VPC configurations, and other resources—in a single YAML or JSON template. This approach offers several benefits:

- **Infrastructure as Code (IaC):** Version control your infrastructure alongside your application code.
- **Simplified Deployment:** Use `sam build` and `sam deploy` commands to package and deploy your application.
- **Local Testing:** Test your Lambda functions and API Gateway integrations locally.
- **Compatibility with CloudFormation:** Since SAM templates are an extension of CloudFormation, you can leverage the full power of CloudFormation's resource definitions and functionalities.

---

## **Implementing the Architecture with AWS SAM**

Below is an expanded guide on how to implement the described architecture using AWS SAM.

### **1. Setup and Prerequisites**

- **AWS CLI Installed and Configured:** Ensure you have the AWS CLI installed and configured with appropriate credentials.
- **AWS SAM CLI Installed:** Install the SAM CLI for local development and deployment.
- **Docker Installed (Optional):** Required for local testing of Lambda functions.

### **2. Project Structure**

Organize your Django project to work within the Lambda execution environment:

```
my-django-app/
├── manage.py
├── my_app/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── requirements.txt
├── sam-template.yaml
└── src/
    └── lambda_function.py
```

- **`manage.py`, `my_app/`:** Standard Django project files.
- **`requirements.txt`:** List of Python dependencies.
- **`sam-template.yaml`:** AWS SAM template file defining the infrastructure.
- **`src/lambda_function.py`:** Entry point for the Lambda function.

### **3. AWS SAM Template**

Create a `sam-template.yaml` file to define your serverless application.

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: Serverless Django Application

Globals:
  Function:
    Timeout: 30  # Adjust as needed
    MemorySize: 1024  # Adjust as needed
    Runtime: python3.8
    Environment:
      Variables:
        DJANGO_SETTINGS_MODULE: my_app.settings
        PYTHONPATH: /var/task

Resources:
  DjangoFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: lambda_function.lambda_handler
      CodeUri: ./  # Points to the root of your project
      VpcConfig:
        SecurityGroupIds:
          - !Ref LambdaSecurityGroup
        SubnetIds:
          - subnet-xxxxxxxx
          - subnet-yyyyyyyy
      Policies:
        - AWSLambdaVPCAccessExecutionRole
        - AmazonRDSFullAccess  # Adjust permissions as needed
        - AmazonS3FullAccess
        - SecretsManagerReadWrite
      Events:
        ApiEvent:
          Type: Api
          Properties:
            Path: /{proxy+}
            Method: ANY

  LambdaSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Access to RDS
      VpcId: vpc-zzzzzzzz
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 5432  # For PostgreSQL
          ToPort: 5432
          CidrIp: 0.0.0.0/0  # Restrict in production
```

**Explanation:**

- **Globals:** Sets default properties for all Lambda functions.
- **DjangoFunction:** Defines the Lambda function that will run your Django application.
- **Handler:** Points to the `lambda_handler` function in `lambda_function.py`.
- **CodeUri:** Directory where the application code is located.
- **VpcConfig:** Specifies the VPC, subnets, and security groups for the Lambda function.
- **Policies:** Grants necessary permissions. Adjust these to follow the principle of least privilege.
- **Events:** Configures API Gateway to trigger the Lambda function.

### **4. Lambda Function Handler**

Create `src/lambda_function.py` as the entry point for your Lambda function.

```python
import os
import sys
from django.core.wsgi import get_wsgi_application

# Add your project directory to the system path
sys.path.append('/var/task')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_app.settings')
application = get_wsgi_application()

def lambda_handler(event, context):
    from mangum import Mangum  # AWS Lambda adapter for ASGI applications

    asgi_handler = Mangum(application)
    response = asgi_handler(event, context)
    return response
```

**Explanation:**

- **Mangum:** A library that allows running ASGI applications on AWS Lambda. Since Django 3.0+, it supports ASGI.
- **Adding Project Directory:** Ensures that the Lambda function can find your Django application.

### **5. Requirements File**

Update `requirements.txt` to include necessary dependencies:

```
django
mangum
psycopg2-binary
boto3
django-storages[boto3]
```

### **6. Database Configuration in Django**

Modify your `settings.py` to use environment variables and AWS Secrets Manager for database credentials.

```python
import os
import json
import boto3

def get_secret():
    secret_name = os.environ.get('SECRET_NAME')
    region_name = os.environ.get('AWS_REGION')

    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    secret = get_secret_value_response['SecretString']
    return json.loads(secret)

secrets = get_secret()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': secrets['DB_NAME'],
        'USER': secrets['DB_USER'],
        'PASSWORD': secrets['DB_PASSWORD'],
        'HOST': secrets['DB_HOST'],
        'PORT': secrets['DB_PORT'],
    }
}
```

**Note:** Ensure that `SECRET_NAME` and `AWS_REGION` are set in your environment variables or SAM template.

### **7. Configure Static and Media Files**

In `settings.py`, configure Django to use S3 for static and media files.

```python
INSTALLED_APPS += ['storages']

AWS_STORAGE_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
AWS_S3_REGION_NAME = os.environ.get('AWS_REGION')

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

STATIC_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/static/'
MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/media/'
```

### **8. Build and Deploy with AWS SAM**

#### **a. Build the Application**

```bash
sam build
```

- This command processes your SAM template and prepares your application for deployment, including installing dependencies.

#### **b. Package the Application**

```bash
sam package \
    --output-template-file packaged.yaml \
    --s3-bucket your-deployment-s3-bucket
```

- **`your-deployment-s3-bucket`:** An S3 bucket where SAM will upload your deployment package.

#### **c. Deploy the Application**

```bash
sam deploy \
    --template-file packaged.yaml \
    --stack-name your-stack-name \
    --capabilities CAPABILITY_IAM \
    --parameter-overrides \
        VpcId=vpc-zzzzzzzz \
        SubnetIds="subnet-xxxxxxxx,subnet-yyyyyyyy" \
        SecurityGroupIds="sg-zzzzzzzz" \
        DBHost=your-db-host \
        DBName=your-db-name \
        DBUser=your-db-user \
        DBPassword=your-db-password \
        S3BucketName=your-static-media-bucket \
        SecretName=your-secret-name \
        AWSRegion=your-aws-region
```

- **Parameters:** Replace placeholders with actual values.
- **Capabilities:** `CAPABILITY_IAM` is required to allow SAM to create IAM roles.

### **9. Running Database Migrations**

AWS SAM supports running CloudFormation custom resources, but for simplicity, you can run migrations manually.

#### **Option 1: Run Migrations Locally**

- Set up a VPN or SSH tunnel to your RDS instance.
- Run:

  ```bash
  python manage.py migrate
  ```

#### **Option 2: Create a Lambda Function for Migrations**

- Define a new Lambda function in your SAM template specifically for running migrations.

```yaml
MigrateFunction:
  Type: AWS::Serverless::Function
  Properties:
    Handler: manage.lambda_handler
    CodeUri: ./
    Runtime: python3.8
    Timeout: 900
    VpcConfig:
      SecurityGroupIds:
        - !Ref LambdaSecurityGroup
      SubnetIds:
        - subnet-xxxxxxxx
        - subnet-yyyyyyyy
    Policies:
      - AWSLambdaVPCAccessExecutionRole
      - AmazonRDSFullAccess
      - AmazonS3FullAccess
      - SecretsManagerReadWrite
    Environment:
      Variables:
        DJANGO_SETTINGS_MODULE: my_app.settings
        COMMAND: migrate
```

- **`manage.py` Modification:**

  ```python
  import os
  import sys

  def lambda_handler(event, context):
      os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_app.settings')
      from django.core.management import execute_from_command_line
      execute_from_command_line(['manage.py', os.environ.get('COMMAND')])
  ```

- **Invoke the Function:**

  ```bash
  aws lambda invoke \
      --function-name YourStackName-MigrateFunction-XXXXXXXXXXXX \
      response.json
  ```

### **10. Networking and VPC Configuration**

Ensure your Lambda functions are configured to access the VPC where your RDS instance is deployed.

- **VPC ID, Subnets, and Security Groups:** Provided as parameters in the SAM template.
- **Security Group Rules:** Configure security groups to allow traffic between Lambda functions and RDS.

### **11. Managing Secrets with AWS Secrets Manager**

- **Store Secrets:** In AWS Secrets Manager, create a secret containing your database credentials.
- **Access Policy:** Ensure your Lambda function's IAM role has permissions to access the secret.
- **Environment Variables:** Set `SECRET_NAME` and `AWS_REGION` to enable your application to retrieve secrets.

### **12. Testing Locally**

You can test your Lambda function locally using the SAM CLI.

```bash
sam local start-api
```

- This command starts a local API Gateway and Lambda environment.
- **Note:** You may need to adjust configurations or use local mocks for AWS services.

### **13. Monitoring and Logging**

- **CloudWatch Logs:** By default, Lambda writes logs to CloudWatch Logs.
- **X-Ray (Optional):** Use AWS X-Ray for distributed tracing.

### **14. Permissions and IAM Roles**

- Adjust IAM policies in your SAM template to follow the principle of least privilege.
- **Policies to Consider:**
  - `AWSLambdaVPCAccessExecutionRole`
  - `AWSSecretsManagerReadOnlyAccess`
  - Custom policies for S3 and RDS access.

---

## **Considerations and Best Practices**

### **a. Layer Dependencies**

- **AWS Lambda Layers:** Use layers to package dependencies separately from your code to reduce package size.

### **b. Optimizing Cold Starts**

- **Provisioned Concurrency:** Configure your Lambda function with provisioned concurrency to reduce cold start latency.

### **c. Security**

- **Restrict Security Group Access:** Limit ingress and egress rules to only necessary ports and IP ranges.
- **Encrypt Data:** Use SSL/TLS for connections to RDS and S3.

### **d. Scalability**

- **Database Connection Limits:** Be mindful of the maximum number of connections your RDS instance can handle.
- **Use RDS Proxy:** Implement RDS Proxy to manage connection pooling.

### **e. Environment Variables**

- Use the `Parameters` section in your SAM template to manage environment variables and make your template reusable.

---

## **Sample SAM Template with Parameters**

Here's an updated version of the SAM template using parameters:

```yaml
Parameters:
  VpcId:
    Type: String
    Description: VPC ID where resources are deployed
  SubnetIds:
    Type: CommaDelimitedList
    Description: Subnets for Lambda function
  SecurityGroupIds:
    Type: CommaDelimitedList
    Description: Security groups for Lambda function
  SecretName:
    Type: String
    Description: Name of the AWS Secrets Manager secret
  AWSRegion:
    Type: String
    Default: us-east-1
  S3BucketName:
    Type: String
    Description: S3 bucket for static and media files

Resources:
  DjangoFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: lambda_function.lambda_handler
      CodeUri: ./
      VpcConfig:
        SecurityGroupIds: !Ref SecurityGroupIds
        SubnetIds: !Ref SubnetIds
      Policies:
        - AWSLambdaVPCAccessExecutionRole
        - Version: '2012-10-17'
          Statement:
            - Effect: Allow
              Action:
                - s3:*
              Resource: "*"
            - Effect: Allow
              Action:
                - secretsmanager:GetSecretValue
              Resource: !Sub arn:aws:secretsmanager:${AWSRegion}:${AWS::AccountId}:secret:${SecretName}*
      Environment:
        Variables:
          DJANGO_SETTINGS_MODULE: my_app.settings
          SECRET_NAME: !Ref SecretName
          AWS_REGION: !Ref AWSRegion
          S3_BUCKET_NAME: !Ref S3BucketName
```

---

## **Using AWS SAM Accelerate**

AWS SAM Accelerate allows for rapid development and testing by syncing your code changes directly to the cloud.

- **Enable Accelerate:**

  ```bash
  sam sync --stack-name your-stack-name --watch
  ```

- **Benefits:**
  - Faster iterations during development.
  - Automatic detection of code changes.

---

## **Conclusion**

Implementing your serverless Django application using AWS SAM is not only feasible but also offers a structured and scalable approach to managing your infrastructure as code. AWS SAM integrates seamlessly with other AWS services, providing a cohesive environment for deploying and managing serverless applications.

**Key Benefits:**

- **Simplified Management:** Define and manage all AWS resources in a single template.
- **Local Development:** Test functions locally, reducing deployment cycles.
- **Extensibility:** Leverage the full range of AWS services and CloudFormation features.
- **Community Support:** As an AWS-supported framework, SAM has extensive documentation and community resources.

---

## **Next Steps**

- **Review AWS SAM Documentation:**
  - [AWS SAM Developer Guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html)
- **Explore Examples:**
  - Check out sample serverless applications using AWS SAM on [GitHub](https://github.com/aws-samples).
- **Optimize Your Application:**
  - Continuously monitor performance and costs.
  - Implement best practices for security and scalability.
