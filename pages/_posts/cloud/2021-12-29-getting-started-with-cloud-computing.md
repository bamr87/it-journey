---
title: Getting Started with Cloud Computing
author: null
layout: default
description: null
categories:
    - Posts
lastmod: '2021-12-29T18:18:38.884Z'
draft: true
---

## Getting Started with Cloud Computing

There are 3 main providers of cloud computing services:

    - [Amazon Web Services](https://docs.aws.amazon.com/) (AWS)
    - Google Cloud Platform (GCP)
    - Microsoft Azure

Each one of these providers has its own set of services and features. however, they all have a common goal: to provide a platform for developers to build and deploy applications. in this post, I will show you how to get started with AWS, GCP, and Azure, but I will explain the core concepts of each of these providers.

## Account Setup

This is self explanatory. Make sure you have an account with each of these providers.

## Installing AWS CLI

### Installing on Linux

Install the AWS CLI using the following command:

```bash
pip install awscli --upgrade --user
```

### Installing on Windows

Install the AWS CLI using the following command:

```bash
pip install awscli --upgrade --user
```

## installing GCP CLI 

### Installing on Linux

Install the GCP CLI using the following command:

```bash
pip install google-cloud-sdk --upgrade --user
```

### Installing on Windows

Install the GCP CLI using the following command:

```bash
pip install google-cloud-sdk --upgrade --user
```

## installing Azure CLI 

### Installing on Linux

Install the Azure CLI using the following command:

```bash
pip install azure-cli --upgrade --user
```

### Installing on Windows

Install the Azure CLI using the following command:

```bash
pip install azure-cli --upgrade --user
```

## AWS CLI

### AWS CLI

### AWS CLI - Login

To login to AWS, use the following command:

```bash
aws configure
```

### AWS CLI - Configure

To configure your AWS CLI, use the following command:

```bash
aws configure
```

### AWS CLI - List Regions

To list the regions that AWS offers, use the following command:

```bash
aws ec2 describe-regions
```

### AWS CLI - List Instances

To list the instances that are running, use the following command:

```bash
aws ec2 describe-instances
```

### AWS CLI - Start Instance

To start an instance, use the following command:

```bash
aws ec2 start-instances --instance-ids <instance_id>
```

### AWS CLI - Stop Instance

To stop an instance, use the following command:

```bash
aws ec2 stop-instances --instance-ids <instance_id>
```

### AWS CLI - Reboot Instance

To reboot an instance, use the following command:

```bash
aws ec2 reboot-instances --instance-ids <instance_id>
