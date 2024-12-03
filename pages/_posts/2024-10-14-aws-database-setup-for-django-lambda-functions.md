---
title: AWS Database Setup for Django Lambda Functions
description: null
author: null
excerpt: null
date: 2019-08-22T15:20:28.000Z
lastmod: 2024-10-14T16:00:26.339Z
draft: true
tags: []
categories: []
meta: null
snippet: null
slug: null
---

## **Overview**

We will:

1. **Choose a Database Engine**
2. **Create an AWS RDS Database Instance**
3. **Configure Network Settings and Security Groups**
4. **Set Up AWS RDS Proxy (Optional but Recommended)**
5. **Store Database Credentials Securely with AWS Secrets Manager**
6. **Update Lambda Function Configuration**
7. **Configure Django to Use the Database**
8. **Test the Database Connection**
9. **Run Database Migrations**
10. **Best Practices and Considerations**

---

## **Prerequisites**

- An AWS account with necessary permissions to create and manage RDS instances, Lambda functions, and IAM roles.
- AWS CLI installed and configured (optional but helpful).
- Basic knowledge of AWS services and Django applications.

---

## **Step 1: Choose a Database Engine**

AWS RDS supports several database engines compatible with Django:

- **PostgreSQL**
- **MySQL**
- **MariaDB**
- **Amazon Aurora (MySQL or PostgreSQL compatible)**

For this guide, we'll use **Amazon RDS for PostgreSQL**.

---

## **Step 2: Create an AWS RDS Database Instance**

### **Option A: Using AWS Management Console**

1. **Navigate to RDS Service:**

   - Log in to the AWS Management Console.
   - Search for and select **RDS**.

2. **Create a Database:**

   - Click on **Databases** in the left navigation pane.
   - Click on **Create database**.

3. **Choose a Database Creation Method:**

   - **Standard Create:** Allows full control over configuration options.

4. **Select Engine Options:**

   - **Engine Type:** Choose **PostgreSQL**.
   - **Version:** Select the latest supported version.

5. **Specify Templates:**

   - Choose **Free tier** for testing or **Production** for live applications.

6. **Settings:**

   - **DB Instance Identifier:** A unique name for your database instance (e.g., `my-django-db`).
   - **Master Username:** Enter a username (e.g., `dbadmin`).
   - **Master Password:** Enter and confirm a strong password.

7. **Instance Configuration:**

   - **DB Instance Class:** Select an appropriate instance size (e.g., `db.t3.micro` for testing).
   - **Storage:** Set the allocated storage (e.g., 20 GiB).
   - **Storage Autoscaling:** Enable if desired.

8. **Availability & Durability:**

   - For production, consider **Multi-AZ deployment** for high availability.

9. **Connectivity:**

   - **Virtual Private Cloud (VPC):** Choose the VPC where your Lambda function resides.
   - **Subnet Group:** Leave as default or select specific subnets.
   - **Public Access:** Set to **No** to keep the database private.
   - **VPC Security Group:** Create a new security group or select an existing one.
     - **New Security Group:** Will allow you to define inbound/outbound rules.

10. **Additional Configuration:**

    - **Database Port:** Default is `5432` for PostgreSQL.
    - **DB Parameter Group & Option Group:** Leave as default unless specific configurations are needed.
    - **Encryption:** Enable if required.

11. **Backup and Maintenance:**

    - **Automatic Backups:** Enable and set retention period.
    - **Backup Window:** Specify or leave as default.
    - **Maintenance Window:** Specify or leave as default.

12. **Monitoring:**

    - Enable enhanced monitoring if needed.

13. **Log Exports:**

    - Enable PostgreSQL logs for auditing and troubleshooting.

14. **Delete Protection:**

    - Enable **Deletion Protection** to prevent accidental deletion.

15. **Create Database:**

    - Review your settings.
    - Click **Create database**.

### **Option B: Using AWS CLI**

```bash
aws rds create-db-instance \
    --db-instance-identifier my-django-db \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --allocated-storage 20 \
    --master-username dbadmin \
    --master-user-password YourStrongPassword \
    --vpc-security-group-ids sg-xxxxxxxx \
    --db-subnet-group-name my-subnet-group \
    --no-publicly-accessible
```

**Note:** Replace placeholders with your actual values.

---

## **Step 3: Configure Network Settings and Security Groups**

### **1. Security Group for RDS**

- **Inbound Rules:**
  - **Type:** PostgreSQL
  - **Protocol:** TCP
  - **Port Range:** 5432
  - **Source:** Security group of your Lambda function (recommended) or specific IP ranges.

### **2. Security Group for Lambda Function**

- Ensure the Lambda function's security group allows outbound traffic to the database's security group on port 5432.

### **3. VPC and Subnets**

- Both the Lambda function and RDS instance should be in the **same VPC**.
- Use **private subnets** for enhanced security.

---

## **Step 4: Set Up AWS RDS Proxy (Optional but Recommended)**

**Benefits:**

- Manages database connections efficiently.
- Improves application scalability.
- Enhances security by integrating with IAM and Secrets Manager.

### **1. Create RDS Proxy**

1. **Navigate to RDS Proxies:**

   - In the AWS RDS console, click on **Proxies** in the left navigation pane.
   - Click **Create proxy**.

2. **Configure Proxy Settings:**

   - **Proxy Identifier:** A unique name for your proxy (e.g., `my-django-proxy`).
   - **Engine Compatibility:** Select **PostgreSQL**.
   - **Require IAM Authentication:** Enable for enhanced security (optional).

3. **Target Group:**

   - **Select RDS DB Instance:** Choose your RDS instance created earlier.
   - **Connection Settings:** Configure as needed.

4. **Connectivity:**

   - **VPC:** Should be the same as your Lambda function and RDS instance.
   - **Subnets:** Select the same subnets used by your Lambda function.
   - **Security Groups:** Assign a security group that allows traffic between the Lambda function and the RDS Proxy.

5. **IAM Role:**

   - **Create New Role:** Allow the proxy to access Secrets Manager and authenticate with the database.

6. **Encryption:** Enable if required.

7. **Create Proxy:**

   - Review settings and click **Create proxy**.

### **2. Update Security Groups**

- Ensure that the Lambda function's security group allows outbound traffic to the RDS Proxy's security group on port 5432.

### **3. Adjust Database Connection Settings**

- When using RDS Proxy, you'll connect to the proxy endpoint instead of the database endpoint.

---

## **Step 5: Store Database Credentials Securely with AWS Secrets Manager**

### **1. Create a Secret**

1. **Navigate to Secrets Manager:**

   - In the AWS Management Console, search for and select **Secrets Manager**.

2. **Store a New Secret:**

   - Click **Store a new secret**.
   - **Secret Type:** Choose **Credentials for RDS database**.
   - **Credentials:**
     - **Username:** Database master username (e.g., `dbadmin`).
     - **Password:** Database master password.

3. **Select Database**

   - **Encryption Key:** Use the default or a custom KMS key.
   - **Select the Database:** Choose the RDS database you created.

4. **Secret Name and Description:**

   - **Secret Name:** Give a meaningful name (e.g., `my-django-db-secret`).

5. **Configure Rotation (Optional):**

   - Enable automatic rotation if desired.

6. **Review and Store:**

   - Review the settings and click **Store**.

### **2. IAM Permissions**

- Ensure your Lambda function's execution role has permissions to access the secret.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "secretsmanager:GetSecretValue",
      "Resource": "arn:aws:secretsmanager:region:account-id:secret:my-django-db-secret"
    }
  ]
}
```

---

## **Step 6: Update Lambda Function Configuration**

### **1. Configure VPC Access**

- In the AWS Lambda console:

  - Navigate to your Lambda function.
  - Click on **Configuration** > **VPC**.
  - Select the same **VPC**, **subnets**, and **security groups** as your RDS instance.

### **2. Set Environment Variables**

- Add the following environment variables to your Lambda function:

  - **SECRET_NAME:** Name of your secret in Secrets Manager (e.g., `my-django-db-secret`).
  - **AWS_REGION:** Region where your secret is stored (e.g., `us-east-1`).

### **3. Update IAM Role**

- Ensure the Lambda function's execution role includes:

  - Permissions to access AWS Secrets Manager.
  - Permissions to access AWS RDS Proxy (if used).

### **4. Adjust Timeout and Memory Settings**

- **Timeout:** Increase to at least 30 seconds to allow for database connections.
- **Memory:** Allocate sufficient memory (e.g., 1024 MB) to improve performance.

---

## **Step 7: Configure Django to Use the Database**

### **1. Install Database Driver**

- For PostgreSQL:

  ```bash
  pip install psycopg2-binary
  ```

### **2. Update `settings.py`**

```python
import os
import json
import boto3
from botocore.exceptions import ClientError

def get_secret():
    secret_name = os.environ.get('SECRET_NAME')
    region_name = os.environ.get('AWS_REGION')

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise e
    else:
        # Secrets Manager returns the secret as a string
        secret = get_secret_value_response['SecretString']
        return json.loads(secret)

secrets = get_secret()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': secrets['dbname'],
        'USER': secrets['username'],
        'PASSWORD': secrets['password'],
        'HOST': secrets['host'],  # Use RDS Proxy endpoint if using proxy
        'PORT': secrets.get('port', '5432'),
    }
}
```

**Notes:**

- **`secrets['host']`:** If using RDS Proxy, use the proxy endpoint.
- **Ensure** that `boto3` is included in your Lambda function's deployment package.

---

## **Step 8: Test the Database Connection**

### **1. Verify Lambda Function Connectivity**

- **Test Event:**

  - In the Lambda console, create a test event.
  - Invoke the Lambda function and check for any connection errors.

### **2. Check CloudWatch Logs**

- Look for any errors related to database connectivity in the logs.

### **3. Common Issues**

- **Timeout Errors:** May indicate networking issues or incorrect VPC configurations.
- **Authentication Errors:** Check that credentials are correct and Secrets Manager is returning the expected values.

---

## **Step 9: Run Database Migrations**

### **Option 1: Run Migrations via Lambda Function**

- **Create a Migration Function:**

  - Use the same Lambda function or create a separate one specifically for migrations.
  - Set an environment variable `COMMAND` with the value `migrate`.

- **Modify `lambda_function.py`:**

  ```python
  import os
  import sys
  from django.core.management import execute_from_command_line

  def lambda_handler(event, context):
      os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_app.settings')
      execute_from_command_line(['manage.py', os.environ.get('COMMAND', 'migrate')])
  ```

- **Invoke the Function:**

  - Manually invoke the Lambda function to run migrations.

### **Option 2: Run Migrations Locally**

- **Set Up SSH Tunnel (if necessary):**

  - If your database is not publicly accessible, establish an SSH tunnel through a bastion host or VPN.

- **Run Migrations:**

  ```bash
  python manage.py migrate
  ```

**Note:** Ensure your local environment can access the database.

---

## **Step 10: Best Practices and Considerations**

### **1. Database Connection Management**

- **Use RDS Proxy:** Helps manage and pool connections, reducing overhead.
- **Set `CONN_MAX_AGE` in Django:**

  ```python
  DATABASES['default']['CONN_MAX_AGE'] = 600  # Keep connections open for 10 minutes
  ```

### **2. Security**

- **IAM Authentication (Optional):** Use IAM roles to authenticate to the database instead of static credentials.
- **Restrict Security Group Access:** Limit inbound rules to necessary sources.
- **Encryption:** Enable encryption at rest and in transit.

### **3. Performance Optimization**

- **Lambda Function Memory and Timeout:**

  - Allocate more memory to increase CPU allocation.
  - Set appropriate timeout values.

- **VPC Endpoint (Optional):**

  - Use VPC endpoints for AWS services to reduce latency.

### **4. Monitoring and Logging**

- **Enable Enhanced Monitoring:** In RDS for detailed performance metrics.
- **Use CloudWatch Alarms:** Set up alarms for key metrics (e.g., CPU utilization, connections).

### **5. Cost Management**

- **Right-Size RDS Instances:** Choose instance types that match your workload.
- **Use Serverless Database Options:** Consider Amazon Aurora Serverless for variable workloads.

---

## **Additional Tips**

- **Testing in Development:**

  - Use a separate RDS instance for development and testing.
  - Ensure configurations mirror production as closely as possible.

- **Automate Deployment:**

  - Use AWS SAM, CloudFormation, or Terraform to automate infrastructure provisioning.

- **Stay Updated:**

  - Regularly update your database engine version and apply patches.

---

## **Conclusion**

By following these steps, you've set up an AWS RDS database instance configured to work with your Lambda function running a Django application. This setup ensures secure, scalable, and efficient database connectivity in a serverless environment.

