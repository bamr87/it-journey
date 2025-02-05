---
title: Set Up Azure for Jekyll Contact Us Form
description: Learn how to easily set up Azure for your Jekyll Contact Us form and enhance user engagement on your website.
date: 2025-01-24T18:06:04.177Z
preview: ""
tags:
    - Azure
    - Contact Form
    - GitHub Pages
    - Jekyll
    - Tutorial
categories:
    - Development
    - Guides
    - Jekyll
    - Programming
    - Web Development
sub-title: null
excerpt: null
snippet: null
author: ""
layout: null
keywords: {}
lastmod: 2025-01-25T03:52:33.559Z
permalink: null
attachments: ""
---

Below is a step-by-step guide on how to build a serverless “Contact Us” form using **Azure Functions** and a **Microsoft Exchange** server (on-premises or Exchange Online) to send emails. This approach keeps your Jekyll site static and offloads the email-sending logic to Azure. We’ll focus on a **cost-effective** setup, leveraging Azure’s consumption-based pricing for Functions.

---

## High-Level Steps

1. **Create an Azure Function App** (HTTP-triggered) to handle form submissions.  
2. **Send emails via Exchange**, either by:
   - **SMTP** (simplest if Exchange allows SMTP connections), or
   - **Microsoft Graph API** (if you’re on Office 365/Exchange Online and want modern authentication).
3. **Update your Jekyll form** to POST data to the Azure Function endpoint.

---

## 1. Create an Azure Function App

1. **Sign in to the Azure Portal** ([portal.azure.com](https://portal.azure.com))  
2. Click **Create a resource** → **Compute** → **Function App**.  
3. Enter the required details:  
   - **Subscription**: Your Azure subscription.  
   - **Resource Group**: Create or use an existing one (e.g., “ContactFormResourceGroup”).  
   - **Function App name**: e.g., “ContactUsFunctionApp”.  
   - **Runtime stack**: Choose Node.js, Python, or .NET — whichever you prefer.  
   - **Region**: Pick a region close to your users (or to your Exchange server if on-prem).  
   - **Hosting**:  
     - **Plan type**: Choose **Consumption** for a pay-per-use model (most cost-effective for low-volume contact forms).  
4. Click **Review + create**, then **Create**.

Within a minute or so, your Function App will be provisioned.

---

## 2. Create the Function (HTTP Trigger)

We’ll use a simple **HTTP-triggered** function to receive form data. The steps differ slightly depending on your chosen runtime.

Below is an example in **Node.js** (using the Azure Portal “In-portal” editor or local development with Azure CLI).

### Option A: Quick In-Portal Creation

1. Go to **Function App** → **Functions** → **Create**.  
2. Select **HTTP trigger** → Provide a function name (e.g. `ContactFormHandler`).  
3. Authorization level: choose **Anonymous** (so your form can POST without keys).

A code editor will appear with a sample `index.js` (and possibly `function.json`).

### Option B: Local Development (VS Code)

If you prefer local dev, install the [Azure Functions VS Code extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions). Then create a new HTTP-triggered function. You’ll eventually deploy it to Azure.

---

## 3. Sending Email via Exchange

Depending on your environment, you have two main ways to send email to your Exchange server:

1. **SMTP** (traditional).  
2. **Microsoft Graph API** (if you have Exchange Online/Office 365 and want modern auth).

### 3.1 SMTP Approach (Simpler if allowed)

**Requirements**:  
- Your Exchange server or Exchange Online is configured to allow SMTP connections (e.g., port 587, TLS).  
- You have credentials for an account with permission to send mail.

**Node.js Example with Nodemailer**

In your `index.js` for the Azure Function:

```js
const nodemailer = require('nodemailer');

module.exports = async function (context, req) {
  try {
    // 1. Extract form data (assumes JSON payload)
    const { name, email, message } = req.body;

    // 2. Configure transport
    // Replace with your actual Exchange server details
    // For on-prem Exchange:
    //   host: 'mail.yourdomain.com',
    //   port: 587,
    //   secure: false, // or true if using SSL/TLS on port 465
    // For Exchange Online (Office 365):
    //   host: 'smtp.office365.com',
    //   port: 587,
    //   secure: false
    const transporter = nodemailer.createTransport({
      host: 'smtp.office365.com', // or your on-prem Exchange host
      port: 587,
      secure: false, 
      auth: {
        user: 'contactform@yourdomain.com', // Service account or mailbox
        pass: 'YOUR_PASSWORD'
      },
      tls: {
        ciphers: 'TLSv1.2'
      }
    });

    // 3. Craft the email
    const mailOptions = {
      from: 'contactform@yourdomain.com',   // Must be a valid, permitted sender
      to: 'recipient@yourdomain.com',       // Where you want to receive the email
      subject: `New Contact Form Submission from ${name}`,
      text: `
Name: ${name}
Email: ${email}
Message:
${message}
`
    };

    // 4. Send the email
    await transporter.sendMail(mailOptions);

    // 5. Return success
    context.res = {
      status: 200,
      body: { status: 'success', message: 'Email sent successfully!' }
    };
  } catch (err) {
    context.log.error('Error sending email:', err);
    context.res = {
      status: 500,
      body: { status: 'error', message: 'Failed to send email.' }
    };
  }
};
```

**Notes**:  
- Make sure to install **nodemailer** in your function. If using the **In-portal** editor, you’ll need a `package.json` specifying `"nodemailer": "^x.x.x"`.  
- If your Exchange server requires additional security (self-signed SSL, etc.), you may need to adjust the `tls` options or ensure your function can reach the server.  
- For **Exchange Online**, typical SMTP endpoint is `smtp.office365.com`, port `587`, TLS required.

### 3.2 Using Microsoft Graph API (Office 365 / Exchange Online Only)

If you prefer modern OAuth-based authentication and you have a mailbox in Office 365:

1. **Register an Azure AD app** to get a Client ID and Client Secret.  
2. **Grant Mail.Send or related permissions** to your app (application permission or delegated permission with a user’s consent).  
3. **Acquire an access token** from Azure AD in your Azure Function.  
4. **Use the Graph endpoint** (`/v1.0/me/sendMail`) or (`/v1.0/users/{id|userPrincipalName}/sendMail`) to send mail.

This is more complex, so unless you specifically require token-based auth and have set up Graph, the SMTP approach is often simpler.

---

## 4. Configure CORS (If Needed)

By default, the Azure Function’s HTTP endpoint does not restrict CORS. If your Jekyll site is hosted on the same domain, you’re fine. If it’s on a different domain (e.g., GitHub Pages or Netlify), you need to ensure the function returns appropriate **Access-Control-Allow-Origin** headers.

You can manually set CORS in the function response or use the **Azure Portal** → **Function App** → **API** → **CORS** settings to add your site’s domain.

Example in Node.js:

```js
context.res = {
  status: 200,
  headers: {
    'Access-Control-Allow-Origin': '*', // or your domain
    'Access-Control-Allow-Headers': 'Content-Type'
  },
  body: ...
};
```

---

## 5. Connect Jekyll Form to Azure Function

In your Jekyll `contact.html` (or `.md`), create a form that POSTs data to the Function URL. Let’s assume you’ll do a modern JavaScript approach:

```html
<form id="contact-form">
  <label for="name">Name:</label>
  <input type="text" name="name" id="name" required>

  <label for="email">Email:</label>
  <input type="email" name="email" id="email" required>

  <label for="message">Message:</label>
  <textarea name="message" id="message" rows="5" required></textarea>

  <button type="submit">Send</button>
</form>

<script>
  const form = document.getElementById('contact-form');
  form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const formData = {
      name: form.name.value,
      email: form.email.value,
      message: form.message.value
    };

    try {
      const response = await fetch('https://YOUR-FUNCTION-APP-NAME.azurewebsites.net/api/ContactFormHandler', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      const result = await response.json();
      
      if (response.ok) {
        alert('Your message has been sent!');
      } else {
        alert('Error sending message: ' + result.message);
      }
    } catch (error) {
      console.error(error);
      alert('An error occurred while sending your message.');
    }
  });
</script>
```

- Replace the **fetch URL** with your actual function endpoint (`https://<functionapp>.azurewebsites.net/api/<functionName>`).  
- Ensure your function is set to **Anonymous** auth so it can be called without additional headers.

---

## 6. Cost Considerations

### Azure Functions
- **Consumption Plan**: You only pay for execution time and resources used. For a low-volume contact form (a few hundred or thousand submissions per month), you’ll likely stay within the **free grant**.  
- If usage grows, you pay for additional calls and execution time, which is still typically very low cost.

### Exchange
- If you already have an on-prem or hosted Exchange environment (or Office 365 license), there’s no extra cost for sending emails via SMTP or Graph unless you hit large volumes.

### Overall
- This approach is highly cost-effective for small or medium businesses.  
- The biggest overhead is setting up and configuring your Exchange or Office 365 environment to allow SMTP or Graph access.

---

## Putting It All Together

1. **Create an Azure Function App** on the Consumption plan.  
2. **Create an HTTP-triggered function** that:  
   - Parses the form data from the request.  
   - Uses SMTP (nodemailer) or the Graph API to send the email via Exchange.  
3. **Handle CORS** if needed (especially if your Jekyll site is on a different domain).  
4. **Update your Jekyll form** to POST to the Azure Function endpoint.  
5. **Test** by submitting a form and verifying that you receive the email.

You now have a fully serverless, cost-effective **Contact Us** form integration that uses **Azure** + **Exchange** behind the scenes!