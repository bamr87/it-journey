---
title: Jupyter Notebook to Markdown Converter
description: Convert Jupyter Notebooks to Markdown
author: "Amr Abdel-Motaleb"
featured: true
tags: ["jupyter", "markdown", "converter", "jekyll"]
date: "2024-05-24"
---


```python
# prerequisites

%pip install nbconvert
```


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

    [NbConvertApp] Converting notebook JeykLLM-create.ipynb to markdown
    [NbConvertApp] Writing 5094 bytes to JeykLLM-create.md
    [NbConvertApp] Converting notebook jupyter-to-markdown.ipynb to markdown
    [NbConvertApp] Writing 6839 bytes to jupyter-to-markdown.md
    [NbConvertApp] Converting notebook html_md_doc_scrapper.ipynb to markdown
    [NbConvertApp] Writing 42579 bytes to html_md_doc_scrapper.md
    [NbConvertApp] Converting notebook markdown-to-script.ipynb to markdown
    [NbConvertApp] Writing 2109 bytes to markdown-to-script.md


Success! You have converted a Jupyter Notebook to Markdown.

but the output is not labeled as such. 

Now we need to update the script to tag the output with codeblocks and tags. for example:

```jupyter_output
 Output here
```


