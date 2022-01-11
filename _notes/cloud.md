---
title: cloud
author: null
excerpt: null
description: null
snippet: null
categories:
    - notes
tags:
    - notes
meta: null
draft: true
slug: /cloud/
lastmod: '2022-01-10T23:19:02.724Z'
---

[AWS vs Azure vs GCP](https://www.bmc.com/blogs/aws-vs-azure-vs-google-cloud-platforms/)

[AWS Training](https://explore.skillbuilder.aws/learn)

[AWS Certification](https://www.aws.training/Certification)

[AWS Study Guides](https://aws.amazon.com/certification/certification-prep/)

[AWS Test Questions](https://amazonwebservices.benchprep.com/)

## AWS Certified Cloud Practitioner Official Practice Question Set

## 1.1 Define the AWS Cloud and its value proposition

### Question 1

**Which of the following are benefits of the AWS Cloud? (Select TWO.)**

A - Companies need increased IT staff.

Incorrect. With the AWS Cloud, you can focus on your customers, rather than on the acquisition, installation, and management of infrastructure. Although the use of AWS services might offload some of the work your IT staff performs, it will not directly increase your IT staff.

B - Capital expenses are replaced with variable expenses.

Correct. With the AWS Cloud, you benefit from Amazon's global purchasing of compute resources. You do not need to invest heavily in data centers.

C - Customers receive the same monthly bill regardless of which resources they use.

Incorrect. With the AWS Cloud, you pay only for the individual services that you need, for as long as you use them. You are not required to commit to a long-term contract.

For more information about flexible pricing on the AWS platform, see AWS Pricing.

D - Companies gain increased agility.

Correct. With the AWS Cloud, you make IT resources available to developers in minutes instead of weeks. The result is reduced cost and time for development, which increases agility.

For more information about agility, see Six Advantages of Cloud Computing.

E - AWS holds responsibility for security in the cloud.

Incorrect. The customer is responsible for security in the AWS Cloud as part of the AWS shared responsibility model.

For more information about security in the AWS Cloud, see Shared Responsibility Model.

#### Question 2

**Which of the following are advantages of the AWS Cloud? (Select TWO.)**

A - AWS manages the maintenance of the cloud infrastructure.

Correct. This solution is an example of security "of" the cloud. AWS is responsible for protecting the infrastructure that runs all of the services offered in the AWS Cloud. This infrastructure is composed of the hardware, software, networking, and facilities that run AWS Cloud services.

For more information about the AWS shared responsibility model, see Shared Responsibility Model.

B - AWS manages the security of applications built on AWS.

Incorrect. This solution is an example of security "in" the cloud. Application security is the customer's responsibility.

For more information about the AWS shared responsibility model, see Shared Responsibility Model.

C - AWS manages capacity planning for physical servers.

Correct. This solution is an example of security "of" the cloud. Capacity planning of the cloud is an inherited control from AWS. AWS purchases additional servers as needed, based on overall customer demand.

For more information about the AWS shared responsibility model, see Shared Responsibility Model.

D - AWS manages the development of applications on AWS.

Incorrect. This solution is an example of security "in" the cloud. AWS does not manage application development.

For more information about the AWS shared responsibility model, see Shared Responsibility Model.

E - AWS manages cost planning for virtual servers.

Incorrect. AWS offers tools to help customers visualize, understand, and manage costs. Customers are responsible for cost planning for their virtual servers.

For more information about cost planning tools, see AWS Cost Explorer.

## 1.2 Identify aspects of AWS Cloud economics

### Question 3

**A company requires physical isolation of its Amazon EC2 instances from the instances of other customers.**

**Which instance purchasing option meets this requirement?**

A - Dedicated Hosts

Correct. With Dedicated Hosts, a physical server is dedicated for your use. Dedicated Hosts provide visibility and the option to control how you place your instances on an isolated, physical server.

For more information about Dedicated Hosts, see Amazon EC2 Dedicated Hosts.

B - Reserved Instances

Incorrect. Reserved Instances are not physical instances. Reserved Instances are a billing discount applied to the use of On-Demand Instances in your account. Reserved Instances do not provide physical workload isolation.

For more information about Reserved Instances, see Reserved Instances.

C - On-Demand Instances

Incorrect. With On-Demand Instances, you pay for compute capacity by the second with no long-term commitments. On-Demand Instances do not provide physical workload isolation.

For more information about On-Demand Instances, see On-Demand Instances.

D - Spot Instances

Incorrect. With Spot Instances, you can take advantage of unused EC2 capacity in the AWS Cloud. Spot Instances do not provide physical workload isolation.

For more information about Spot Instances, see Amazon EC2 Spot Instances.

## 1.3 Explain the different cloud architecture design principles

### Question 4

**Which AWS Cloud architecture principle states that systems should reduce interdependencies?**

A - Scalability

Incorrect. Systems that are scalable can react to increases and decreases in load. Scalability does not reduce interdependencies between system components.

For more information about AWS Cloud best practices, see AWS Well-Architected Framework.

B - Services, not servers

Incorrect. This solution does not reduce interdependencies between system components in an application deployment. However, you still need to design features that are decoupled within the application to reduce single endpoints that can become failures.

For more information about AWS Cloud best practices, see AWS Well-Architected Framework.

C - Automation

Incorrect. Automation can improve stability, efficiency during deployments, and the response to events. However, you still need to design architecture that reduces tight dependencies between the layers of the application.

For more information about AWS Cloud best practices, see AWS Well-Architected Framework.

D - Loose coupling

Correct. Loose coupling helps isolate behavior of a component from other components that depend on it, increasing resiliency and agility. A change or a failure in one of the components should not affect the other components.

For more information about AWS Cloud best practices, see AWS Well-Architected Framework.

### Question 5

Which AWS Cloud architecture design principle supports the distribution of workloads across multiple Availability Zones?

A - Implement automation.

Incorrect. You can use automation services, such as AWS CloudFormation, to deploy resources into one or more Availability Zones. However, the implementation of automation is not directly tied to, or limited to, the distribution of workloads across multiple Availability Zones.

For more information about CloudFormation, see AWS CloudFormation FAQs.

B - Design for agility.

Incorrect. When you design for agility, you can provision resources more quickly. Agility is not related to the number of Availability Zones.

For more information about agility, see Risk is Lack of Agility.

C - Design for failure.

Correct. AWS recommends that you distribute workloads across multiple Availability Zones. This distribution will ensure continuous availability of your application, even if the application is unavailable in one single Availability Zone.

For more information about the performance efficiency pillar, see Performance Efficiency Pillar - AWS Well-Architected Framework.

D - Implement elasticity.

Incorrect. Elasticity is the ability to activate resources as you need them and return resources when you no longer need them. Elasticity is not related to the number of Availability Zones.

For more information about elasticity, see Elasticity.

## 2.1 Define the AWS shared responsibility model

### Question 6

**Which of the following is a responsibility of AWS under the AWS shared responsibility model?**

A - Design a customer's application for disaster recovery.

Incorrect. AWS offers many services to help with disaster recovery and business continuity planning. However, according to the shared responsibility model, it is the customer’s responsibility to decide which services it needs.

For more information about the shared responsibility model, see Shared Responsibility Model.

B - Update the guest operating systems on deployed Amazon EC2 instances.

Incorrect. The customer must manage its own updates on its provisioned infrastructure.

For more information about the shared responsibility model, see Shared Responsibility Model.

C - Configure new resources within an AWS account.

Incorrect. The customer decides which services to use and how to use them.

For more information about the shared responsibility model, see Shared Responsibility Model.

D  - Secure the physical infrastructure.

Correct. AWS fully maintains the physical controls.

For more information about the shared responsibility model, see Shared Responsibility Model.

## 2.2 Define AWS Cloud security and compliance concepts

### Question 7

**Which of the following describes a security best practice that can be implemented by using AWS Identity and Access Management (IAM)?**

A - Turn off AWS Management Console access for all users.

Incorrect. There could be legitimate requirements for certain IAM users to have access to the console. Consequently, to turn off access for all users is not the correct solution.

For more information about best practices for securing an AWS account, see What are some best practices for securing my AWS account and its resources?

B - Generate secret keys for every IAM user.

Incorrect. This solution would generate secret keys for IAM users and would require them to access their applications through programmatic access.

For more information about best practices for securing an AWS account, see What are some best practices for securing my AWS account and its resources?

C - Grant permissions to users who are required to perform a specific task only.

Correct. Through the security recommendation of least privilege, an IAM best practice is to grant granular permissions to users by using IAM roles.

For more information about IAM best practices and least privilege, see Grant least privilege.

For more information about best practices for securing an AWS account, see What are some best practices for securing my AWS account and its resources?

D - Store AWS credentials within Amazon EC2 instances.

Incorrect. The solution to store credentials within EC2 instances is not a security best practice. It would be a better security practice to use IAM roles to grant permissions to EC2 instances, because the IAM roles will rotate the credentials automatically.

For more information about best practices for securing an AWS account, see What are some best practices for securing my AWS account and its resources?

### Question 8

A company needs to monitor and receive alerts about AWS Management Console sign-in events that involve the AWS account root user.

Which AWS service can the company use to meet these requirements?

A - Amazon CloudWatch

Correct. CloudWatch monitors your AWS resources and the applications that you run on AWS in real time. You can use CloudWatch to monitor and receive alerts about console sign-in events that involve the AWS account root user.

For more information about CloudWatch, see What is Amazon CloudWatch?

B - AWS Config

Incorrect. You can use AWS Config to assess, audit, and evaluate the configurations of your AWS resources. AWS Config cannot alert you about console sign-in events that involve the AWS account root user.

For more information about AWS Config, see What is AWS Config?

C - AWS Trusted Advisor

Incorrect. You can use Trusted Advisor for real-time guidance to help you provision your resources according to AWS best practices. Trusted Advisor cannot alert you about console sign-in events that involve the AWS account root user.

For more information about Trusted Advisor, see AWS Trusted Advisor.

D - AWS Identity and Access Management (IAM)

Incorrect. With IAM, you can manage access to AWS services and resources securely. IAM cannot alert you about console sign-in events that involve the AWS account root user.

For more information about IAM, see AWS Identity and Access Management (IAM).

## 2.3 Identify AWS access management capabilities

### Question 9

**A company has an application server that runs on an Amazon EC2 instance. The application server needs to access contents within a private Amazon S3 bucket.**

**What is the recommended approach to meet this requirement?**

A - Create an IAM role with the appropriate permissions. Associate the role with the EC2 instance.

Correct. IAM roles are temporary credentials that expire. IAM roles are more secure than long-term access keys because they reduce risk if credentials are accidentally exposed.

For more information about IAM roles, see Using an IAM role to grant permissions to applications running on Amazon EC2 instances.

B - Configure a VPC peering connection to allow private communication between the EC2 instance and the S3 bucket.

Incorrect. A VPC peering connection is a networking connection between two VPCs that enables you to route traffic between them by using private IPv4 addresses or IPv6 addresses. VPC peering connections cannot connect a VPC and an S3 bucket.

For more information about VPC peering, see What is VPC peering?

C - Create a shared access key. Configure the EC2 instance to use the hardcoded key.

Incorrect. The creation of a shared key is not a best practice because this reduces the value of auditing AWS resource access. It is not a best practice to embed access keys into the application code because application code can become compromised.

For more information about managing access keys, see Best practices for managing AWS access keys.

D - Configure the application to read an access key from a secured source.

Incorrect. It is a best practice to use IAM roles instead of long-term access keys. Long-term access keys, such as those associated with IAM users and AWS account root users, remain valid until you manually revoke them. However, temporary security credentials that are obtained through IAM roles and other features of AWS Security Token Service (AWS STS) expire after a short period of time. Use temporary security credentials to help reduce the risk in case credentials are accidentally exposed.

For more information about managing access keys, see Best practices for managing AWS access keys.

## 2.4 Identify resources for security support

### Question 10

Which security-related services or features does AWS offer? (Select TWO.)

A - Complete PCI compliance for customer applications that run on AWS

Incorrect. Customers are responsible for the certification of PCI compliance of their applications. Some AWS services are certified to be PCI compliant.

For more information about AWS Security Competency Partners, see AWS Security Competency Partners.

B - AWS Trusted Advisor security checks

Correct. Trusted Advisor draws upon best practices learned from serving hundreds of thousands of AWS customers. These best practices include security checks.

For more information about Trusted Advisor, see AWS Trusted Advisor.

For more information about Trusted Advisor security checks, see AWS Trusted Advisor best practice checklist.

C - Data encryption

Correct. Many AWS services support data encryption, including Amazon Elastic Block Store (Amazon EBS) and Amazon S3.

For more information about data encryption on Amazon S3, see Protecting data using encryption.

For more information about data encryption on Amazon EBS, see Amazon EBS encryption.

D - Automated penetration testing

Incorrect. AWS does not provide automated penetration testing. AWS customers can carry out security assessments or penetration tests on their AWS infrastructure without prior approval for some services.

For more information about penetration testing, see Penetration Testing.

E - Amazon S3 copyrighted content detection

Incorrect. AWS provides copyrighted content detection.

### Question 11

**Which recommendations are included in the AWS Trusted Advisor checks? (Select TWO.)**

A - Amazon S3 bucket permissions

Correct. Trusted Advisor checks for S3 bucket permissions in Amazon S3 with open access permissions. Bucket permissions that grant list access to everyone can result in higher than expected charges if objects in the bucket are listed by unintended users at a high frequency. Bucket permissions that grant upload and delete access to all users create potential security vulnerabilities by allowing anyone to add, modify, or remove items in a bucket. This Trusted Advisor check examines explicit bucket permissions and associated bucket policies that might override the bucket permissions.

For more information about S3 bucket permissions, see AWS Trusted Advisor best practice checklist.

B - AWS service outages for services

Incorrect. Trusted Advisor does not provide notifications for service outages. You can use the AWS Personal Health Dashboard to learn about AWS Health events that can affect your AWS services or account.

For more information about the Personal Health Dashboard, see Getting started with the AWS Personal Health Dashboard.

C - Multi-factor authentication (MFA) use on the AWS account root user

Correct. Trusted Advisor checks the root account and warns if MFA is not enabled.

For more information about Trusted Advisor, see AWS Trusted Advisor best practice checklist.

D - Available software patches for Amazon EC2 instances

Incorrect. Trusted Advisor does not provide notifications about software patches for EC2 instances.

E - Number of users in the account

Incorrect. Trusted Advisor does not provide information about the number of users in an AWS account.

## 3.1 Define methods of deploying and operating in the AWS Cloud

### Question 12

**A company wants a dedicated private connection to the AWS Cloud from its on-premises operations.**

**Which AWS service or feature will provide this connection?**

A - AWS VPN

Incorrect. AWS VPN establishes secure connections between your on-premises networks, remote offices, client devices, and the AWS global network. AWS VPN is not a dedicated connection.

For more information about AWS VPN, see .

B - AWS PrivateLink

Incorrect. You use PrivateLink when you want to use services offered by another VPC securely within the AWS network. With PrivateLink, all network traffic stays on the global AWS backbone and never traverses the public internet. PrivateLink does not connect to on-premises operations.

For more information about PrivateLink, see AWS PrivateLink.

C - VPC endpoint

Incorrect. A VPC endpoint enables private connections between your VPC and supported AWS services and VPC endpoint services powered by PrivateLink. A VPC endpoint does not connect to on-premises operations.

For more information about VPC endpoints, see VPC endpoints.

D - AWS Direct Connect

Correct. Direct Connect provides a dedicated private connection from your premises to the AWS Cloud. Direct Connect is an alternative to using the internet to access AWS Cloud services.

For more information about Direct Connect, see AWS Direct Connect.

## 3.2 Define the AWS global infrastructure

### Question 13

**Which aspect of AWS infrastructure provides global deployment of compute and storage?**

A - Multiple Availability Zones in an AWS Region

Incorrect. Availability Zones are one or more discrete data centers with redundant power, networking, and connectivity in a Region. When infrastructure is deployed across multiple Availability Zones, you can achieve a highly available deployment within the geographical location of the Region. However, this solution does not provide global deployments.

For more information about Availability Zones, see Global Infrastructure.

B - Multiple AWS Regions

Correct. A Region is a physical location where there are clusters of AWS data centers. AWS offers many different Regions where you can deploy infrastructure around the world. With the use of multiple Regions, you can achieve a global deployment of compute, storage, and databases.

For more information about Regions, see Global Infrastructure.

C - Tags

Incorrect. Tags are metadata that you can associate with AWS resources. Tags are user-defined data in the form of key-value pairs. You can use tags to manage, identify, organize, search for, and filter resources. Tags do not provide global deployments of applications and solutions.

For more information about tags, see Tagging AWS resources.

D - Resource groups

Incorrect. AWS Resource Groups is a service that you can use to manage and automate tasks on many resources at the same time. Resources in AWS are entities such as Amazon EC2 instances and Amazon S3 buckets. With Resource Groups, you can filter resources based on tags or AWS CloudFormation stacks and then perform an action against a group of resources. You do not use Resource Groups to deploy AWS resources globally.

For more information about resource groups, see What are AWS Resource Groups?

### Question 14

**Which AWS services or features support data replication across AWS Regions? (Select TWO.)**

A - Amazon S3

Correct. Amazon S3 supports Cross-Region Replication. With Cross-Region Replication, you designate a destination S3 bucket in another Region. When Cross-Region Replication is turned on, any new object that is uploaded will be replicated to the destination S3 bucket.

For more information about Amazon S3, see Replicating objects.

B - Amazon Elastic Block Store (Amazon EBS)

Incorrect. Amazon EBS automatically replicates data within an Availability Zone. Amazon EBS does not support Cross-Region Replication.

For more information about Amazon EBS, see Amazon Elastic Block Store.

C - Amazon EC2 instance store

Incorrect. An EC2 instance store is block storage that is attached to an EC2 instance. This storage is located on disks that are physically attached to the host computer. An instance store is ideal for temporary storage of information that changes frequently. The data that is stored on an instance store is temporary. There is no built-in mechanism to replicate data across Regions.

For more information about EC2 instance stores, see Amazon EC2 instance store.

D - AWS Storage Gateway

Incorrect. Storage Gateway connects an on-premises software appliance with cloud-based storage. Storage Gateway provides integration with data security features between your on-premises IT environment and AWS storage infrastructure such as Amazon S3. Storage Gateway does not directly support Cross-Region Replication.

For more information about Storage Gateway, see What is AWS Storage Gateway?

E - Amazon RDS

Correct. You can use Amazon RDS to host relational databases on AWS. One RDS DB instance resides in a single Region. With Amazon RDS, you can create read replicas across Regions. Amazon RDS replicates any data from the primary DB instance to the read replica across Regions.

For more information about Amazon RDS, see Working with read replicas.

## 3.3 Identify the core AWS services

### Question 15

**A company is hosting a static website from a single Amazon S3 bucket.**

**Which AWS service will achieve lower latency and high transfer speeds?**

A - AWS Elastic Beanstalk

Incorrect. Elastic Beanstalk is a service to deploy and scale web applications and services developed with common programming languages on automatically deployed infrastructure with capacity management, load balancing, auto scaling, and monitoring. Elastic Beanstalk makes it easier to provision and support an application. Elastic Beanstalk does not reduce website latency.

For more information about Elastic Beanstalk, see What is AWS Elastic Beanstalk?

B - Amazon DynamoDB Accelerator (DAX)

Incorrect. DAX is used to reduce response times from a DynamoDB table from single-digit milliseconds to microseconds. DynamoDB tables cannot host static websites.

For more information about DAX, see In-Memory Acceleration with DynamoDB Accelerator (DAX).

C - Amazon Route 53

Incorrect. Route 53 is a highly available and scalable DNS web service. The three main functions of Route 53 are registering domain names, routing internet traffic to the resources for your domain, and checking the health of those resources. Route 53 can direct traffic to S3 buckets. But because the question describes only one S3 bucket, Route 53 would have only one potential route and could not reduce latency.

For more information about Route 53, see What is Amazon Route 53?

For more information about routing to S3 buckets by using Route 53, see Routing traffic to a website that is hosted in an Amazon S3 bucket.

D - Amazon CloudFront

Correct. CloudFront is a web service that speeds up the distribution of your static and dynamic web content, such as .html, .css, .js, and image files, to your users. Content is cached in edge locations. Content that is repeatedly accessed can be served from the edge locations instead of the source S3 bucket.

For more information about CloudFront, see Accelerate static website content delivery.

### Question 16

**Which AWS service provides a simple and scalable shared file storage solution for use with Linux-based Amazon EC2 instances and on-premises servers?**

A - AWS Managed Services (AMS)

Incorrect. AMS helps you to operate your AWS infrastructure more efficiently and securely. By using AWS services and a growing library of automations, configurations, and run books, AMS can augment and optimize your operational capabilities in both new and existing AWS environments. However, AMS is not a storage service.

For more information about AMS, see AWS Managed Services.

B - Amazon S3 Glacier

Incorrect. S3 Glacier is an object store used for archiving purposes. It is not suitable for one time access.

For more information about S3 Glacier, see What Is Amazon S3 Glacier?

C - Amazon Elastic Block Store (Amazon EBS)

Incorrect. Amazon EBS provides block-level storage volumes for use with EC2 instances. EBS volumes behave like raw, unformatted block devices. However, EBS volumes cannot be shared between on-premises servers and EC2 instances.

For more information about Amazon EBS, see Amazon Elastic Block Store (Amazon EBS).

D - Amazon Elastic File System (Amazon EFS)

Correct. Amazon EFS provides an elastic file system that lets you share file data without the need to provision and manage storage. It can be used with AWS Cloud services and on-premises resources, and is built to scale on demand to petabytes without disrupting applications. With Amazon EFS, you can grow and shrink your file systems automatically as you add and remove files, eliminating the need to provision and manage capacity to accommodate growth.

For more information about using Amazon EFS, see Walkthrough: Create and mount a file system on premises with AWS Direct Connect and VPN.

## 3.4 Identify resources for technology support

### Question 17

**A company needs phone, email, and chat access 24 hours a day, 7 days a week. The response time must be less than 1 hour if a production system has a service interruption.**

**Which AWS Support plan meets these requirements at the LOWEST cost?**

A - AWS Basic Support

Incorrect. The Basic Support plan does not include chat access and phone calls.

For more information about AWS Support plans, see Compare AWS Support Plans.

B - AWS Developer Support

Incorrect. The Developer Support plan does not include chat access and phone calls. It provides email support during business hours only.

For more information about AWS Support plans, see Compare AWS Support Plans.

C - AWS Business Support

Correct. The Business Support plan provides phone, email, and chat access 24 hours a day, 7 days a week. The Business Support plan has a response time of less than 1 hour if a production system has a service interruption.

For more information about AWS Support plans, see Compare AWS Support Plans.

D - AWS Enterprise Support

Incorrect. The Enterprise Support plan provides phone, email, and chat access 24 hours a day, 7 days a week. The Enterprise Support plan has a response time of less than 15 minutes if a production system has a service interruption. However, the Enterprise Support plan is more expensive than the Business Support plan.

For more information about AWS Support plans, see Compare AWS Support Plans.

## 4.1 Compare and contrast the various pricing models for AWS (for example, On-Demand Instances, Reserved Instances, and Spot Instance pricing)

### Question 18

**Which Amazon EC2 pricing model adjusts based on supply and demand of EC2 instances?**

A - On-Demand Instances

Incorrect. On-Demand Instances are offered at a set price by AWS Region.

For more information about On-Demand Instances, see Amazon EC2 On-Demand Pricing.

B - Reserved Instances

Incorrect. Reserved Instances reserve capacity at a discounted rate. The customer commits to purchase a certain amount of compute.

For more information about Reserved Instances, see Amazon EC2 Reserved Instances.

C - Spot Instances

Correct. Spot Instances are discounted more heavily when there is more capacity available in the Availability Zones.

For more information about Spot Instances, see Amazon EC2 Spot Instances.

D - Convertible Reserved Instances

Incorrect. Reserved Instances reserve capacity at a discounted rate. The customer commits to purchase a certain amount of compute. With Convertible Reserved Instances, you can change the instance family, operating system, and tenancies.

For more information about Reserved Instances, see Amazon EC2 Reserved Instances.

## 4.2 Recognize the various account structures in relation to AWS billing and pricing

### Question 19

**Which of the following is an advantage of consolidated billing on AWS?**

A - Volume pricing qualification

Correct. Consolidated billing is a feature of AWS Organizations. You can combine the usage across all accounts in your organization to share volume pricing discounts, Reserved Instance discounts, and Savings Plans. This solution can result in a lower charge compared to the use of individual standalone accounts.

For more information about consolidated billing, see Consolidated billing for AWS Organizations.

B - Shared access permissions

Incorrect. Shared access permissions is a feature of roles that are developed in AWS Identity and Access Management (IAM). This solution is not related to consolidated billing.

For more information about IAM, see What is IAM?

C - Multiple bills for each account

Incorrect. The goal of consolidated billing is to have one bill for multiple accounts.

For more information about consolidated billing, see Consolidated billing for AWS Organizations.

D - Elimination of the need to tag resources

Incorrect. In consolidated billing, you can apply tags that represent business categories. This functionality helps you organize your costs across multiple services within consolidated billing.

For more information about how tagging relates to billing, see Using Cost Allocation Tags.

## 4.3 Identify resources available for billing support

### Question 20

**Which AWS service can create an alarm that sends a notification when a billing threshold is exceeded?**

A - AWS Trusted Advisor

Incorrect. Trusted Advisor draws upon best practices learned from serving hundreds of thousands of AWS customers. Trusted Advisor inspects your AWS environment and then makes recommendations when opportunities exist to save money, improve system availability and performance, or help close security gaps. However, Trusted Advisor cannot create a billing alarm.

For more information about Trusted Advisor, see AWS Trusted Advisor.

B - AWS CloudTrail

Incorrect. CloudTrail is an AWS service that helps you enable governance, compliance, and operational and risk auditing of your AWS account. CloudTrail records actions taken by a user, role, or an AWS service as events. However, CloudTrail cannot create a billing alarm.

For more information about CloudTrail, see What Is AWS CloudTrail?

C - Amazon CloudWatch

Correct. You can monitor your estimated AWS charges by using CloudWatch. When you enable the monitoring of estimated charges for your AWS account, the estimated charges are calculated and sent several times daily to CloudWatch as metric data.

For more information about CloudWatch, see Creating a billing alarm to monitor your estimated AWS charges.

D - Amazon QuickSight

Incorrect. QuickSight is a cloud-scale business intelligence (BI) service that you can use to deliver easy-to-understand insights. QuickSight connects to your data in the cloud and combines data from many different sources. However, QuickSight is a data visualization tool, not a tool for creating alarms.

For more information about QuickSight, see What Is Amazon QuickSight?

![Scores](/assets/images/aws-cloud-pract-practice-test-domain.png)
