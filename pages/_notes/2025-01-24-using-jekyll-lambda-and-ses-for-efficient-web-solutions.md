---
title: Using Jekyll, Lambda, and SES for Efficient Web Solutions
description: ""
date: 2025-01-24T17:04:43.040Z
preview: ""
tags: []
categories: []
sub-title: null
excerpt: null
snippet: null
author: ""
layout: null
keywords: {}
lastmod: 2025-01-25T03:52:35.049Z
permalink: null
attachments: ""
---

Below is a detailed walkthrough on how to create a **serverless** “Contact Us” form using **AWS Lambda**, **API Gateway**, and **Amazon SES**. This lets you keep your site static (e.g., generated via Jekyll), and offload email handling to AWS.

---

## Overview of Steps

1. **Set Up Amazon SES** to send email (domain or email verification, sandbox considerations).  
2. **Create an AWS Lambda Function** that will receive form data and send an email using SES.  
3. **Create an Amazon API Gateway Endpoint** to expose the Lambda function over HTTPS.  
4. **Update Your Jekyll Form** to POST data to the new API endpoint.  

---

## 1. Set Up Amazon SES

Amazon Simple Email Service (SES) can send emails on your behalf. By default, new AWS accounts start in the *SES sandbox*, which limits your ability to send emails only to verified addresses. You can either stay in the sandbox (and only accept form submissions if you send to verified emails) or request production access to send to unverified emails.

1. **Verify an Email or Domain**  
   - In the AWS Console, navigate to **Amazon SES**.  
   - Go to **Domains** or **Email Addresses** and verify the sender identity (e.g., `noreply@yourdomain.com`) or the whole domain (`yourdomain.com`).  
   - Follow the DNS instructions to verify and (optionally) set up DKIM.

2. **(Optional) Move Out of Sandbox**  
   - If you need to send emails to arbitrary recipients, open a **Service Quotas** or **Support** request to move SES from sandbox to production.  
   - Otherwise, in the sandbox, you can only send to verified email addresses.

---

## 2. Create an AWS Lambda Function

We’ll create a simple Lambda function (Node.js or Python). Below is an example **Node.js** version.

### a) Create Lambda Function
1. Go to the **AWS Lambda** console, click **Create function**.  
2. Choose **Author from scratch**.  
   - Name: `ContactUsFormHandler`  
   - Runtime: `Node.js 18.x` (or whichever LTS version is available)  
   - Permissions: Create a new or select an existing **Execution role**.  
3. Click **Create function**.

### b) Give Lambda Permission to Use SES

By default, your Lambda execution role does not have permission to send emails using SES. Attach a policy to allow sending email:

1. In the **Configuration** tab of your Lambda function, go to **Permissions** → **Execution role** → **Role name**.  
2. In the **IAM** console, click **Add permissions** → **Attach policies**.  
3. Search for **AmazonSESFullAccess** (or create a custom policy with least-privilege) and attach it.  

> **Tip**: For production, consider a more restrictive policy that only allows `ses:SendEmail` or `ses:SendRawEmail`, scoped to your region and verified identities.

### c) Add Code to Send Email

In the Lambda code editor, replace the default code with the following (example in Node.js):

```js
const AWS = require('aws-sdk');

// Make sure your Lambda is in the same region where SES is configured
// or specify the region explicitly:
AWS.config.update({ region: 'us-east-1' }); 

const ses = new AWS.SES();

exports.handler = async (event) => {
  try {
    // If using API Gateway with a standard integration, the request body will be in event.body.
    // The body can be JSON or form-encoded data depending on how you configure the request.
    
    // 1. Parse the incoming request
    //    For JSON form submissions:
    //    const data = JSON.parse(event.body);
    
    //    For URL-encoded form submissions, you have to parse manually or use a library.
    //    Example for simple URL-encoded:
    //    const qs = require('querystring');
    //    const data = qs.parse(event.body);

    const data = JSON.parse(event.body); // If you're sending JSON from your form

    const { name, email, message } = data;

    // 2. Construct the email parameters
    const params = {
      Source: 'noreply@yourdomain.com', // Verified in SES
      Destination: {
        ToAddresses: ['contact@yourbusiness.com'] // The recipient(s)
      },
      Message: {
        Subject: {
          Data: `New Contact Form Submission from ${name}`
        },
        Body: {
          Text: {
            Data: `
Name: ${name}
Email: ${email}
Message: ${message}
`
          }
          // Alternatively, use HTML data if needed
        }
      }
    };

    // 3. Send the email via SES
    await ses.sendEmail(params).promise();

    // 4. Return success response (with CORS headers if needed)
    return {
      statusCode: 200,
      headers: {
        "Access-Control-Allow-Origin": "*",  // or specify your domain
        "Access-Control-Allow-Headers": "Content-Type"
      },
      body: JSON.stringify({ status: 'success', message: 'Email sent successfully!' })
    };
  } catch (error) {
    console.error(error);
    return {
      statusCode: 500,
      headers: {
        "Access-Control-Allow-Origin": "*"
      },
      body: JSON.stringify({ status: 'error', message: 'Failed to send email.' })
    };
  }
};
```

> **Important**:  
> - Change the `Source` to the email address (or domain) you verified in SES.  
> - Change `Destination.ToAddresses` to the email address(es) you want to receive messages.  
> - If you’re using form-encoded data instead of JSON, parse accordingly.  

### d) Save & Test
- Use the **Test** function in the Lambda console.  
- Provide a test event body (JSON) with `name`, `email`, and `message`.  
- Check the logs (CloudWatch) for errors and verify you received the test email.

---

## 3. Create an Amazon API Gateway Endpoint

Now we expose our Lambda function via a public HTTPS endpoint using API Gateway.

1. Go to the **API Gateway** console, click **Create API**.  
2. Select **HTTP API** (the simpler option vs. REST API).  
3. Give it a name, e.g. `ContactUsAPI`.  
4. Under **Integrations**, choose **Add integration** → **Lambda**.  
   - Select your Lambda function (`ContactUsFormHandler`).  
5. Create a route, e.g. `POST /contact` pointing to that Lambda integration.  
6. Configure **CORS** to allow your domain (or `*` for testing) if your form is hosted on a different domain:
   - In API Gateway’s settings for the route or overall API, enable CORS and set allowed origins/headers.  
7. Click **Deploy** or **Save**. Note the **Invoke URL**, e.g. `https://abc123.execute-api.us-east-1.amazonaws.com/contact`.

---

## 4. Update Your Jekyll Contact Form

In your Jekyll site, you’ll have a `contact.html` (or `.md`) page. You can do one of two approaches:

### A) Plain HTML Form (Requires extra steps for form encoding)
1. **Form Markup** (URL-encoded approach):
   ```html
   <form id="contact-form" action="https://abc123.execute-api.us-east-1.amazonaws.com/contact" method="POST">
     <label for="name">Name</label>
     <input type="text" id="name" name="name" required>

     <label for="email">Email</label>
     <input type="email" id="email" name="email" required>

     <label for="message">Message</label>
     <textarea id="message" name="message" rows="5" required></textarea>

     <button type="submit">Submit</button>
   </form>
   ```
   - If you do a **direct form submit**, the browser will send data as `application/x-www-form-urlencoded`.  
   - In your Lambda, you’d parse `event.body` using `querystring.parse`.

2. **Add CORS** to your API Gateway so that the request from your domain doesn’t get blocked.  
3. **Handling Success/Failure**  
   - By default, the form will redirect to the API Gateway response. You may want to handle it more elegantly.  
   - Typically, you might do a JavaScript `fetch()` or `AJAX` to stay on the same page and show a message (see next approach).

### B) JavaScript Fetch (Recommended for a Better UX)
A more modern approach is to capture the form submission with JavaScript, build a JSON object, and post it to your endpoint:

```html
<form id="contact-form">
  <label for="name">Name</label>
  <input type="text" id="name" name="name" required>

  <label for="email">Email</label>
  <input type="email" id="email" name="email" required>

  <label for="message">Message</label>
  <textarea id="message" name="message" rows="5" required></textarea>

  <button type="submit">Submit</button>
</form>

<script>
  const form = document.getElementById('contact-form');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = {
      name: form.name.value,
      email: form.email.value,
      message: form.message.value
    };

    try {
      const response = await fetch('https://abc123.execute-api.us-east-1.amazonaws.com/contact', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });
      const result = await response.json();
      if (response.ok) {
        alert('Email sent successfully!');
      } else {
        alert('Error sending email: ' + result.message);
      }
    } catch (err) {
      console.error(err);
      alert('Error sending email.');
    }
  });
</script>
```

- This way you send JSON in the request body, which matches our Lambda code snippet (`JSON.parse(event.body)`).
- Make sure your **API Gateway CORS** settings allow `Content-Type: application/json`.

---

## Additional Considerations

1. **SES Sandbox**: If you’re still in the sandbox, you must verify the recipient email or request production access.  
2. **Spam / Bot Protection**: Add reCAPTCHA or honeypot fields to your form to reduce spam.  
3. **Rate Limits**: AWS Lambda and API Gateway have concurrency limits. For most small business forms, the free tier should be sufficient.  
4. **Cost**:  
   - **Lambda**: 1M free requests/month.  
   - **API Gateway**: 1M free requests/month for HTTP APIs (in many regions).  
   - **SES**: First 62,000 emails/month are free if your app is hosted in Amazon EC2; otherwise, it’s $0.10 per 1,000 emails. (Check AWS free tier specifics and region variations.)

---

## End-to-End Flow

1. **User visits** your Jekyll `Contact` page.  
2. **User fills out form**, clicks submit.  
3. A POST request is sent to the **API Gateway endpoint**.  
4. API Gateway **triggers the Lambda** function, passing the form data in the request body.  
5. **Lambda** uses the AWS SDK to call **Amazon SES** and send the email.  
6. **Response** from Lambda returns success or error.  
7. **User sees** a success message (or an error message) on the website.

---

## Summary

By combining **AWS Lambda**, **API Gateway**, and **Amazon SES**, you can add a contact form to a purely static Jekyll site without needing your own server. The steps above will get you up and running:

1. Configure SES (verify domain/email, handle sandbox).
2. Write a small Lambda function to receive form data and send mail via SES.
3. Create an API Gateway route to expose your Lambda function.
4. Update your Jekyll form to POST to the new endpoint (using URL-encoded or JSON + JavaScript fetch).

You’ll have a flexible, scalable, and cost-effective serverless contact form solution!