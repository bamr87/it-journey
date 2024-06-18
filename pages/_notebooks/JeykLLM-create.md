---
title: "Chat GPT Text Generation"
description: "This notebook demonstrates how to use the Chat GPT model for text generation."
tags: ["NLP", "GPT", "Text Generation"]
libraries: 
  - openai
  - python-dotenv

---

## Introduction

This notebook demonstrates how to use the Chat GPT model for text generation. Chat GPT is a variant of the GPT model that is fine-tuned on conversational data. This makes it particularly well-suited for generating conversational text.


## Setup

First, we install the `openai` and `python-dotenv` libraries.

The `openai` library is an official Python client for the OpenAI API. We will use this library to interact with the Chat GPT model.

The `python-dotenv` library is used to load environment variables from a `.env` file. We will use this library to load our OpenAI API key from a `.env` file.



```python
# Pre-requisites
!pip show openai || pip install openai
!pip show python-dotenv || pip install python-dotenv
```

    Name: openai
    Version: 1.30.5
    Summary: The official Python library for the openai API
    Home-page: 
    Author: 
    Author-email: OpenAI <support@openai.com>
    License: 
    Location: /Users/bamr87/Library/Python/3.9/lib/python/site-packages
    Requires: anyio, distro, httpx, pydantic, sniffio, tqdm, typing-extensions
    Required-by: 
    Name: python-dotenv
    Version: 1.0.1
    Summary: Read key-value pairs from a .env file and set them as environment variables
    Home-page: https://github.com/theskumar/python-dotenv
    Author: Saurabh Kumar
    Author-email: me+github@saurabh-kumar.com
    License: BSD-3-Clause
    Location: /Users/bamr87/Library/Python/3.9/lib/python/site-packages
    Requires: 
    Required-by: 


## Setting up the OpenAI API Key

To use the OpenAI API, you need to sign up for an API key. You can get your API key by creating an account on the OpenAI website.

Once you have your API keys, create a `.env` file in the same directory as this notebook and add the following lines with your key values:

```shell
OPENAI_API_KEY=YOUR_API_KEY # should strat with 'sk-'
PROJECT_ID=YOUR_PROJECT_ID  # should start with 'pro-'
ORG_ID=YOUR_ORG_ID          # should start with 'org-'
```



```python
from dotenv import load_dotenv
import os

# Load environment variables from .env file
if load_dotenv():
    print("Environment variables loaded successfully.")
else:
    print("Failed to load environment variables.")

# Get API key from environment variables
api_key = os.getenv('OPENAI_API_KEY')
if api_key:
    print("OPENAI_API_KEY loaded successfully.")
else:
    print("Failed to load OPENAI_API_KEY.")

# Get project ID from environment variables
project_id = os.getenv('PROJECT_ID')
if project_id:
    print("PROJECT_ID loaded successfully.")
else:
    print("Failed to load PROJECT_ID.")

# Get organization ID from environment variables
org_id = os.getenv('ORG_ID')
if org_id:
    print("ORG_ID loaded successfully.")
else:
    print("Failed to load ORG_ID.")

```

    Environment variables loaded successfully.
    OPENAI_API_KEY loaded successfully.
    PROJECT_ID loaded successfully.
    ORG_ID loaded successfully.


## Checking the Environment Variables

To check if the environment variables are loaded correctly, we will print the API key's first and last 4 characters.


```python
# Print the loaded values with only a snippet for security
print("OPENAI_API_KEY: ", api_key[:4] + "..." + api_key[-4:])
print("PROJECT_ID: ", project_id[:4] + "..." + project_id[-4:])
print("ORG_ID: ", org_id[:4] + "..." + org_id[-4:])
```

    OPENAI_API_KEY:  sk-p...RbaA
    PROJECT_ID:  proj...OeP3
    ORG_ID:  org-...1j1N


## Test the connection with OpenAI API

We will test the connection with the OpenAI API by calling the `openai.ChatCompletion.create` method with a simple prompt.



```python
from openai import OpenAI
import yaml
from datetime import datetime

client = OpenAI(
  organization=os.getenv('ORG_ID'),
  project=os.getenv('PROJECT_ID'),
  api_key = os.getenv('OPENAI_API_KEY')
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
    model="gpt-3.5-turbo",
)

print(chat_completion.choices[0].message.content)
```

    This is a test.


## Define the function to create an Assistant

We will create a function to create an assistant by calling the `client.beta.assistants.create` method with instructions and a name as parameters.



```python
def create_assistant(name, instructions):
    assistant = client.beta.assistants.create(
        name=name,
        instructions=instructions,
        model="gpt-4o",
    )
    return assistant

```

## Invoke the function to create an Assistant

Finally, we will create an assistant by calling the `create_assistant` function with instructions and a name as parameters.


```python
# Define the name
assistant_name = "Title Generator"

# Define the instructions
instructions= "Your job is to take content and output a 4-word title that summarizes the content in a thought provoking manner. The title should be intriguing and attention getting for a reader. In other words, try to make it a worth while title for someone to be interested in."

# Create the assistant
assistant = create_assistant(assistant_name, instructions)

```

## Verify the Assistant

Print the assistant details to verify if the assistant is created successfully.


```python

# Print the assistant ID
print(assistant.id)
print(assistant.model)
print(assistant.instructions)
print(assistant.name)
```

    asst_7uR1GHSS13usMIdDxMZXP7tI
    gpt-4o
    Your job is to take content and output a 4-word title that summarizes the content in a thought provoking manner. The title should be intriguing and attention getting for a reader. In other words, try to make it a worth while title for someone to be interested in.
    Title Generator


## Define the function to send a message to the Assistant

We will create a function to send a message to the assistant by calling the `client.beta.assistants.message.create` method with the assistant id and message as parameters.


## Generating Text with Chat GPT

Next, we will create a function to generate text using the Chat GPT model by calling the `openai.ChatCompletion.create` method with a prompt.



```python
def generate_content(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": prompt,
            },
        ],
    )
    # Get the content of the last message in the response
    return response.choices[0].message.content.strip()
```

## Generate Text

Finally, we will generate text using the Chat GPT model by calling the `generate_content` function with a prompt as a parameter.


```python
# Get the prompt from the user
prompt = input("Please enter your prompt for the GPT: ")
content = generate_content(prompt)

# write me a satirical article about a company with good intentions to help poor countires irrigate their dessert land but only to have their equipment fail and polute the land that was intended to be used to grow wheat. Eventually, the cost to grow wheat increased and the water supply became polluted, which sparked a revolution and stance against western imperialism..
```

## Print the generated text

Print the generated text to see the output of the Chat GPT model.


```python
# Print the generated content
print(content)


```

    In a classic case of good intentions gone awry, the company "AquaAid" embarked on a mission to help impoverished desert countries irrigate their arid lands and transform them into fertile wheat fields. With grand promises of ending hunger and poverty, AquaAid brought in state-of-the-art irrigation equipment and set to work in the vast desert landscapes.
    
    But oh, how the tides turned against them! It was as if Murphy's Law had taken full effect - anything that could go wrong, did go wrong. The supposedly cutting-edge equipment malfunctioned almost immediately, causing vast stretches of once barren land to be tainted with pollutants and toxic chemicals. What was meant to be a beacon of hope for the struggling nations quickly turned into a nightmare, as the contaminated water and soil made it impossible to grow anything edible.
    
    As the cost of growing wheat skyrocketed and the promised abundance of food remained a distant dream, the people of the affected countries began to see AquaAid not as benevolent saviors, but as agents of destruction. Anti-western sentiment grew rampant as accusations of imperialism and exploitation were hurled at the now beleaguered company.
    
    Protests flared up, with angry mobs denouncing AquaAid and demanding immediate retribution for their ruined lands and shattered dreams. The once barren deserts were now teeming not with life-giving wheat, but with rebellion and dissent.
    
    In a tragic turn of events, what was meant to be a noble endeavor to aid the less fortunate had spiraled into a grotesque display of corporate greed and incompetence. AquaAid had unwittingly sown the seeds of revolution, leaving a legacy of polluted waters and broken promises in its wake.
    
    And so, as the sun set on the desolate desert lands, the tale of AquaAid served as a cautionary reminder of the perils of good intentions gone astray, and a sobering lesson on the dangers of playing god in foreign lands. May we all learn from their folly, and strive to do better in our efforts to aid those in need.


## Define the function to create a message for the Assistant 

This function will create a thread message for the assistant by calling the `client.beta.threads.create()` with the content as parameters.


```python
def create_message(content):
    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=content
    )
    return message

```

## Invoke the function to create a message for the Assistant

Finally, we will create a message for the assistant by calling the `create_message` function with the content as a parameter.


```python
message = create_message(content)
```

Print the message details to verify if the message is created successfully.


```python
print(message.thread_id)
print(message.id)
print(content)
```

    thread_hC5bIvln7hYrocJsAPBOlLfa
    msg_c6HwS5Qqeu3ARdEiyhUzqgVh
    In a classic case of good intentions gone awry, the company "AquaAid" embarked on a mission to help impoverished desert countries irrigate their arid lands and transform them into fertile wheat fields. With grand promises of ending hunger and poverty, AquaAid brought in state-of-the-art irrigation equipment and set to work in the vast desert landscapes.
    
    But oh, how the tides turned against them! It was as if Murphy's Law had taken full effect - anything that could go wrong, did go wrong. The supposedly cutting-edge equipment malfunctioned almost immediately, causing vast stretches of once barren land to be tainted with pollutants and toxic chemicals. What was meant to be a beacon of hope for the struggling nations quickly turned into a nightmare, as the contaminated water and soil made it impossible to grow anything edible.
    
    As the cost of growing wheat skyrocketed and the promised abundance of food remained a distant dream, the people of the affected countries began to see AquaAid not as benevolent saviors, but as agents of destruction. Anti-western sentiment grew rampant as accusations of imperialism and exploitation were hurled at the now beleaguered company.
    
    Protests flared up, with angry mobs denouncing AquaAid and demanding immediate retribution for their ruined lands and shattered dreams. The once barren deserts were now teeming not with life-giving wheat, but with rebellion and dissent.
    
    In a tragic turn of events, what was meant to be a noble endeavor to aid the less fortunate had spiraled into a grotesque display of corporate greed and incompetence. AquaAid had unwittingly sown the seeds of revolution, leaving a legacy of polluted waters and broken promises in its wake.
    
    And so, as the sun set on the desolate desert lands, the tale of AquaAid served as a cautionary reminder of the perils of good intentions gone astray, and a sobering lesson on the dangers of playing god in foreign lands. May we all learn from their folly, and strive to do better in our efforts to aid those in need.


## Define the function to run the thread for the Assistant

This function will run the thread for the assistant created earlier. It will call the `client.beta.threads.runs.create_and_poll()` with the assistant id and thread id as parameters.


```python
def create_and_poll_run(thread_id, assistant_id):
  run = client.beta.threads.runs.create_and_poll(
    thread_id=thread_id,
    assistant_id=assistant_id,
  )
  return run

```

## Run the thread for the Assistant

Finally, we will run the thread for the assistant by calling the `run_thread` function with the assistant id and thread id as parameters.


```python

thread_id = message.thread_id
assistant_id = assistant.id
run = create_and_poll_run(thread_id, assistant_id)

```

## Check the thread status

Print the thread details to verify if the thread is running successfully. and return the title.


```python
if run.status == 'completed': 
  messages = client.beta.threads.messages.list(
    thread_id=message.thread_id
  )
  text_message = messages.data[0].content[0].text.value
  title = text_message
  print(title)
else:
  print(run.status)
  
```

    AquaAid's Devastating Desert Mission


## Define the Markdown file generation function for Jekyll

Finally, we will generate the markdown file with the generated text and thread title. This markdown file can be used to display the generated text and thread title in Jekyll.


```python
def create_jekyll_post(title, content):
    front_matter = {
        'title': title,
        'layout': 'journals',
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'categories': 'gpt',
        'prompt': prompt,
        'assistant': assistant_name,
    }
    post_content = f"---\n{yaml.dump(front_matter)}---\n{content}"
    filename = f"../_posts/{datetime.now().strftime('%Y-%m-%d')}-{title.lower().replace(' ', '-')}.md"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as file:
        file.write(post_content)
    return filename
```

## Run the Markdown file generation function

Finally, we will run the `create_jekyll_post` function to generate the markdown file.


```python
file_path = create_jekyll_post(title, content)
print(f"The new file is created at: {file_path}")
```

    The new file is created at: ../_posts/2024-06-18-aquaaid's-devastating-desert-mission.md

