---
title: Building a VS Code Extension
description: A step-by-step guide to building a VS Code extension to save/publish/export Copilot conversations as markdown files.
excerpt: A step-by-step guide to building a VS Code extension to save/publish/export Copilot conversations as markdown files.
date: 2024-02-14
categories:
  - Programming
tags:
  - VS Code
  - Extension
  - GitHub Copilot
  - Markdown
type: Article
draft: true
lastmod: 2024-02-25T18:21:36.669Z
slug: building-code-extension
---

[VS Code API](https://code.visualstudio.com/api)

## Introduction

In this article, we'll walk through the process of building a Visual Studio Code (VS Code) extension to save/publish/export GitHub Copilot conversations as markdown files. GitHub Copilot is an AI-powered code completion tool that can generate code and provide suggestions based on natural language descriptions. By building an extension, we can automate the process of saving Copilot conversations as markdown files and publishing them to a GitHub repository.

## Prerequisites

Before we begin, make sure you have the following:

- [Node.js](https://nodejs.org/) and npm installed on your machine.
- [Visual Studio Code](https://code.visualstudio.com/) installed on your machine.
- [GitHub Copilot](https://copilot.github.com/) installed on your machine.
- [Ruby](https://www.ruby-lang.org/en/) installed on your machine.
- [Jekyll](https://jekyllrb.com/) installed on your machine.
- A GitHub account and a repository where you want to publish the markdown files.
- Basic knowledge of JavaScript and TypeScript.
- Basic knowledge of the VS Code extension API.
- A personal access token from GitHub to authenticate with the GitHub API.

## Getting Started

To build a VS Code extension, we'll need to set up a new extension project, write the code to interact with the VS Code API, and test the extension in a local development environment. Here are the high-level steps we'll follow:

1. Set up a new VS Code extension project.
2. Write the code to interact with the VS Code API.
3. Test the extension in a local development environment.
4. Publish the extension to the VS Code Marketplace.
5. Deploy the extension to a production environment.

Let's get started!



## Step 1: Set Up the Extension

The first step is to set up a new VS Code extension project. We'll use the VS Code Extension Generator to create the basic structure of the extension.



bamr87: I want to build an online app that publishes these conversations.

GitHub Copilot: Sure, I can help you with that. Here's a high-level plan for building such an application:

1. **Frontend**: Create a user interface where users can input their conversations. This could be a simple form with text input fields. You can use HTML, CSS, and JavaScript for this. If you prefer a framework, consider using React or Vue.js.

2. **Backend**: Create a server that will receive the conversations from the frontend, process them, and store them in a database. You can use Node.js with Express.js for this. For the database, consider using MongoDB or PostgreSQL.

3. **API**: Create an API endpoint that the frontend can call to send the conversations to the backend. This could be a POST request to a /conversations endpoint.

4. **Database**: Store the conversations in a database. Each conversation could be a document or a row in the database, with fields for the user's name, the conversation, and the timestamp.

5. **Display Conversations**: Create another API endpoint that the frontend can call to get the conversations from the database and display them. This could be a GET request to a /conversations endpoint.

6. **Deployment**: Once everything is working locally, deploy your application to the internet. You can use services like Heroku, Vercel, or Netlify for this.

Here's a basic example of how you could structure your backend with Node.js and Express.js:

```javascript
const express = require('express');
const app = express();
app.use(express.json());

let conversations = [];

app.post('/conversations', (req, res) => {
  const conversation = req.body;
  conversations.push(conversation);
  res.status(201).send();
});

app.get('/conversations', (req, res) => {
  res.send(conversations);
});

app.listen(3000, () => console.log('Server is running on port 3000'));
```

This is a very basic example and a real application would need more features like error handling, user authentication, and a connection to a real database. But it should give you a starting point.

bamr87: I want to build this using Jekyll and github pages.

GitHub Copilot: Building a static site with Jekyll and GitHub Pages is a great choice for publishing content. However, it's important to note that Jekyll and GitHub Pages are designed for static websites and don't support server-side processing or databases. This means you won't be able to store conversations directly on the server as in a traditional web application.

However, you can use third-party services to store and retrieve data. Here's a high-level plan:

1. **Jekyll Setup**: Install Jekyll and create a new Jekyll site. Customize the layout and design as needed.

2. **Form Handling**: Use a third-party service like Formspree, Netlify Forms, or Google Forms to handle form submissions. You can create a form on your Jekyll site where users can enter their conversations, and when they submit the form, the data will be sent to the third-party service.

3. **Data Storage**: The third-party form handling service will store the form submissions. Some services may allow you to access this data via an API.

4. **Display Conversations**: To display the conversations on your site, you could manually add them to your site's content. If the form handling service has an API, you could also use JavaScript to fetch the data and dynamically generate the content.

Here's a basic example of how you could create a form with Jekyll and Formspree:

```html
---
layout: page
title: Submit Conversation
---

<form action="https://formspree.io/YOUREMAIL" method="POST">
    <label for="name">Your Name:</label>
    <input type="text" id="name" name="name">

    <label for="conversation">Conversation:</label>
    <textarea id="conversation" name="conversation"></textarea>

    <button type="submit">Submit</button>
</form>
```

Replace `YOUREMAIL` with your email. When a user submits the form, Formspree will send you an email with the form data.

Remember to add a privacy policy to your site informing users how their data will be used and stored.

bamr87: I would like the data storage to be a markdown file instead of a third party.

GitHub Copilot: If you want to store the conversations as markdown files in your Jekyll site, you'll need to manually create a new markdown file for each conversation. Jekyll and GitHub Pages don't support server-side processing, so this process can't be automated directly within the Jekyll site.

However, you can use GitHub's API to programmatically create new files (including markdown files) in your repository. You could create a separate application (for example, a Node.js application) that receives the form submissions, and then uses the GitHub API to create a new markdown file in your repository for each submission.

Here's a high-level plan:

1. **Form Handling**: As before, use a third-party service like Formspree or Netlify Forms to handle form submissions.

2. **Server Application**: Create a separate server application that receives the form submissions from the form handling service. This application could be built with Node.js and Express.js.

3. **GitHub API**: In the server application, use the GitHub API to create a new markdown file in your repository for each form submission. You'll need to authenticate with the GitHub API using a personal access token.

4. **Jekyll Site**: In your Jekyll site, create a page that lists all the markdown files (i.e., all the conversations). You can use Jekyll's `site.posts` variable to access all the markdown files.

Here's a basic example of how you could use the GitHub API to create a new file in your repository:

```javascript
const axios = require('axios');
const base64 = require('js-base64').Base64;

const githubToken

 =

 'YOUR_GITHUB_TOKEN';
const repoOwner = 'YOUR_GITHUB_USERNAME';
const repoName = 'YOUR_REPOSITORY_NAME';

const createFile = async (filename, content) => {
  const encodedContent = base64.encode(content);

  const response = await axios.put(`https://api.github.com/repos/${repoOwner}/${repoName}/contents/_posts/${filename}.md`, {
    message: `Add conversation: ${filename}`,
    content: encodedContent
  }, {
    headers: {
      'Authorization': `token ${githubToken}`
    }
  });

  return response.data;
};

createFile('conversation1', 'This is the content of the conversation');
```

Replace `'YOUR_GITHUB_TOKEN'`, `'YOUR_GITHUB_USERNAME'`, and `'YOUR_REPOSITORY_NAME'` with your actual GitHub token, username, and repository name. This script creates a new markdown file in the `_posts` directory of your repository.

Remember to secure your GitHub token and don't expose it in your client-side code.

bamr87: the form handling and the server application should be the vscode. From within VS Code, i would like the option to save/publish/export the co-pilot conversation as an markdown file that can be pushed into a github repository. 

GitHub Copilot: To save/publish/export the Copilot conversation as a markdown file from within VS Code, you can follow these steps:

1. **Save the Conversation**: As you're interacting with Copilot, you can copy the conversation and paste it into a new file in VS Code.

2. **Format as Markdown**: Format the conversation as markdown. For example, you could make each user input a heading and each Copilot response a paragraph.

3. **Save as Markdown**: Save the file with a `.md` extension. This tells VS Code (and other tools) that the file is a markdown file.

4. **Push to GitHub**: Use VS Code's built-in Git support to commit the new file and push it to your GitHub repository.

Here's an example of how you might format a Copilot conversation as markdown:

```markdown
# User

I want to build an online app that publishes these conversations.

# GitHub Copilot

Sure, I can help you with that. Here's a high-level plan for building such an application...

# User

I want to build this using Jekyll and github pages.

# GitHub Copilot

Building a static site with Jekyll and GitHub Pages is a great choice for publishing content...
```

Unfortunately, there's currently no built-in way to automate this process in VS Code. You would need to manually copy the conversation, format it as markdown, and save it as a markdown file. However, you could potentially automate some of these steps using a VS Code extension or a script.

bamr87: Help me write a script to acomplish this.

GitHub Copilot: Creating a script to automate this process within VS Code would involve creating a VS Code extension. This extension would need to interact with the VS Code API to access the current editor content, format it as markdown, and save it as a markdown file.

Here's a basic example of how you might create such an extension:

1. **Set up the extension**: First, you'll need to set up a new VS Code extension. You can do this by following the [VS Code extension tutorial](https://code.visualstudio.com/api/get-started/your-first-extension).

2. **Access the editor content**: Use the VS Code API to access the current editor content. You can do this with `vscode.window.activeTextEditor.document.getText()`.

3. **Format as markdown**: Write a function to format the text as markdown. This could be as simple as adding `# ` before each line to make each line a heading.

4. **Save as markdown**: Use the VS Code API to create a new file and write the formatted text to it. You can do this with `vscode.workspace.openTextDocument` and `vscode.window.showTextDocument`.

Here's a basic example of how you might implement this in your extension's `activate` function:

```javascript
const vscode = require('vscode');

function activate(context) {
    let disposable = vscode.commands.registerCommand('extension.saveAsMarkdown', async function () {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage('No active editor!');
            return;
        }

        const text = editor.document.getText();
        const markdown = text.split('\n').map(line => '# ' + line).join('\n');

        const newFile = await vscode.workspace.openTextDocument({ content: markdown, language: 'markdown' });
        await vscode.window.showTextDocument(newFile);
    });

    context.subscriptions.push(disposable);
}
exports.activate = activate;
```

This script creates a new command `extension.saveAsMarkdown` that you can run from the Command Palette (Ctrl+Shift+P) to save the current editor content as a markdown file.

Please note that this is a very basic example and might not work perfectly for your use case. You might need to adjust the markdown formatting function to better match your desired output. Also, this script doesn't automatically commit and push the new file to GitHub. You would need to do that manually, or add additional code to automate it.

bamr87: provide step by step instructions to set up the extension.

GitHub Copilot: Sure, here are the step-by-step instructions to set up a VS Code extension:

1. **Install Node.js and npm**: VS Code extensions are written in JavaScript or TypeScript, so you'll need to have Node.js and npm installed. You can download Node.js from the [official website](https://nodejs.org/), which also includes npm.

2. **Install Yeoman and VS Code Extension Generator**: Yeoman helps to scaffold out new projects quickly, and the VS Code Extension Generator creates the basic structure of a VS Code extension. Install them by running the following command in your terminal:

```bash
npm install -g yo generator-code
```

3. **Generate a new extension**: Run the following command to start the generator:

```bash
yo code
```

4. **Fill out the prompts**: The generator will ask you a series of questions about your extension. For the purpose of this example, you can choose "New Extension (JavaScript)" when asked about the type of extension, and fill out the other fields as you see fit.

5. **Navigate to the new extension directory**: The generator will create a new directory with the same name as your extension. Navigate into it with:

```bash
cd my-extension
```

Replace "my-extension" with the name of your extension.

6. **Open the extension in VS Code**: Open the new extension directory in VS Code by running:

```bash
code .
```

7. **Modify the extension**: In the `src/extension.js` file, you'll see a function named `activate`. This is where you can put the code for your extension. You can replace the existing code with the code provided in the previous response.

8. **Run the extension**: Press F5 to start debugging the extension. This will open a new VS Code window where your extension is loaded. You can test your extension in this window.

9. **Publish the extension**: Once you're happy with your extension, you can publish it to the VS Code marketplace. You'll need to create a publisher, generate a Personal Access Token from GitHub, and use the `vsce` tool to package and publish your extension. You can find more details in the [VS Code extension publishing guide](https://code.visualstudio.com/api/working-with-extensions/publishing-extension).

Remember to replace the placeholder code in the `activate` function with the actual code for your extension.