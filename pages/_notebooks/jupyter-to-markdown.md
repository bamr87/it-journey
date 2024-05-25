---
title: Jupyter Notebook to Markdown Converter
description: Convert Jupyter Notebooks to Markdown
author: "Amr Abdel-Motaleb"
date: "2024-05-24"
---


```python
%pip install nbconvert
```

    Defaulting to user installation because normal site-packages is not writeable
    Requirement already satisfied: nbconvert in /Users/bamr87/Library/Python/3.9/lib/python/site-packages (7.16.4)
    Requirement already satisfied: beautifulsoup4 in /Users/bamr87/Library/Python/3.9/lib/python/site-packages (from nbconvert) (4.12.3)
    Requirement already satisfied: bleach!=5.0.0 in /Users/bamr87/Library/Python/3.9/lib/python/site-packages (from nbconvert) (6.1.0)
    Requirement already satisfied: defusedxml in /Users/bamr87/Library/Python/3.9/lib/python/site-packages (from nbconvert) (0.7.1)
    Requirement already satisfied: importlib-metadata>=3.6 in /Users/bamr87/Library/Python/3.9/lib/python/site-packages (from nbconvert) (7.1.0)
    Requirement already satisfied: jinja2>=3.0 in /Users/bamr87/Library/Python/3.9/lib/python/site-packages (from nbconvert) (3.1.4)
    Requirement already satisfied: jupyter-core>=4.7 in /Users/bamr87/Library/Python/3.9/lib/python/site-packages (from nbconvert) (5.7.2)
    Requirement already satisfied: jupyterlab-pygments in /Users/bamr87/Library/Python/3.9/lib/python/site-packages (from nbconvert) (0.3.0)
    Requirement already satisfied: markupsafe>=2.0 in /Users/bamr87/Library/Python/3.9/lib/python/site-packages (from nbconvert) (2.1.5)
    Requirement already satisfied: mistune<4,>=2.0.3 in /Users/bamr87/Library/Python/3.9/lib/python/site-packages (from nbconvert) (3.0.2)
    Requirement already satisfied: nbclient>=0.5.0 in /Users/bamr87/Library/Python/3.9/lib/python/site-packages (from nbconvert) (0.10.0)
    Requirement already satisfied: nbformat>=5.7 in /Users/bamr87/Library/Python/3.9/lib/python/site-packages (from nbconvert) (5.10.4)
    Requirement already satisfied: packaging in /Users/bamr87/Library/Python/3.9/lib/python/site-packages (from nbconvert) (24.0)
    Requirement already satisfied: pandocfilters>=1.4.1 in /Users/bamr87/Library/Python/3.9/lib/python/site-packages (from nbconvert) (1.5.1)
    Requirement already satisfied: pygments>=2.4.1 in /Users/bamr87/Library/Python/3.9/lib/python/site-packages (from nbconvert) (2.17.2)
    Requirement already satisfied: tinycss2 in /Users/bamr87/Library/Python/3.9/lib/python/site-packages (from nbconvert) (1.3.0)
    Requirement already satisfied: traitlets>=5.1 in /Users/bamr87/Library/Python/3.9/lib/python/site-packages (from nbconvert) (5.14.2)
    Requirement already satisfied: six>=1.9.0 in /Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/site-packages (from bleach!=5.0.0->nbconvert) (1.15.0)
    Requirement already satisfied: webencodings in /Users/bamr87/Library/Python/3.9/lib/python/site-packages (from bleach!=5.0.0->nbconvert) (0.5.1)
    Requirement already satisfied: zipp>=0.5 in /Users/bamr87/Library/Python/3.9/lib/python/site-packages (from importlib-metadata>=3.6->nbconvert) (3.18.1)
    Requirement already satisfied: platformdirs>=2.5 in /Users/bamr87/Library/Python/3.9/lib/python/site-packages (from jupyter-core>=4.7->nbconvert) (4.2.0)
    Requirement already satisfied: jupyter-client>=6.1.12 in /Users/bamr87/Library/Python/3.9/lib/python/site-packages (from nbclient>=0.5.0->nbconvert) (8.6.1)
    Requirement already satisfied: fastjsonschema>=2.15 in /Users/bamr87/Library/Python/3.9/lib/python/site-packages (from nbformat>=5.7->nbconvert) (2.19.1)
    Requirement already satisfied: jsonschema>=2.6 in /Users/bamr87/Library/Python/3.9/lib/python/site-packages (from nbformat>=5.7->nbconvert) (4.22.0)
    Requirement already satisfied: soupsieve>1.2 in /Users/bamr87/Library/Python/3.9/lib/python/site-packages (from beautifulsoup4->nbconvert) (2.5)
    Requirement already satisfied: attrs>=22.2.0 in /Users/bamr87/Library/Python/3.9/lib/python/site-packages (from jsonschema>=2.6->nbformat>=5.7->nbconvert) (23.2.0)
    Requirement already satisfied: jsonschema-specifications>=2023.03.6 in /Users/bamr87/Library/Python/3.9/lib/python/site-packages (from jsonschema>=2.6->nbformat>=5.7->nbconvert) (2023.12.1)
    Requirement already satisfied: referencing>=0.28.4 in /Users/bamr87/Library/Python/3.9/lib/python/site-packages (from jsonschema>=2.6->nbformat>=5.7->nbconvert) (0.35.1)
    Requirement already satisfied: rpds-py>=0.7.1 in /Users/bamr87/Library/Python/3.9/lib/python/site-packages (from jsonschema>=2.6->nbformat>=5.7->nbconvert) (0.18.1)
    Requirement already satisfied: python-dateutil>=2.8.2 in /Users/bamr87/Library/Python/3.9/lib/python/site-packages (from jupyter-client>=6.1.12->nbclient>=0.5.0->nbconvert) (2.9.0.post0)
    Requirement already satisfied: pyzmq>=23.0 in /Users/bamr87/Library/Python/3.9/lib/python/site-packages (from jupyter-client>=6.1.12->nbclient>=0.5.0->nbconvert) (26.0.0)
    Requirement already satisfied: tornado>=6.2 in /Users/bamr87/Library/Python/3.9/lib/python/site-packages (from jupyter-client>=6.1.12->nbclient>=0.5.0->nbconvert) (6.4)
    Note: you may need to restart the kernel to use updated packages.



```python
import os
import subprocess
import tempfile
from datetime import datetime
from glob import glob

# Define the path to your Jekyll site's _posts directory
POSTS_DIR = "/_posts/notebooks"

# Get the current date in the format required by Jekyll
DATE = datetime.now().strftime("%Y-%m-%d")

# Loop over all .ipynb files in the current directory and its subdirectories
for notebook in glob("**/*.ipynb", recursive=True):
    # Convert the Jupyter notebook to a markdown file
    subprocess.run(["jupyter", "nbconvert", "--to", "markdown", notebook])

    # Get the name of the markdown file
    md_file = f"{os.path.splitext(notebook)[0]}.md"

    # Rename the markdown file to match Jekyll's naming convention
    jekyll_md_file = f"{DATE}-{md_file}"

    # Extract the front matter from the Jupyter notebook
    front_matter = subprocess.run(["jq", "-r", "'.cells[0].source | join(\"\\n\")'", notebook], capture_output=True, text=True).stdout

    # Create a temporary file
    temp_file = tempfile.mktemp()

    # Write the front matter to the temporary file
    with open(temp_file, 'w') as f:
        f.write(front_matter)
```

    [NbConvertApp] Converting notebook jupyter-to-markdown.ipynb to markdown
    [NbConvertApp] Writing 14368 bytes to jupyter-to-markdown.md
    [NbConvertApp] Converting notebook html_md_doc_scrapper.ipynb to markdown
    [NbConvertApp] Writing 42513 bytes to html_md_doc_scrapper.md


Success! You have converted a Jupyter Notebook to Markdown.

but the output is not labeled as such. 

Now we need to update the script to tag the output with codeblocks and tags. for example:

```jupyter_output
 Output here
```


