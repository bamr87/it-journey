---
title: Markdown Code to Scripts
description: null
date: 2024-06-02T21:11:39.440Z
preview: null
draft: true
tags: []
categories: []
sub-title: null
excerpt: null
snippet: null
author: bamr87
layout: null
keywords: {}
lastmod: 2024-06-02T21:11:53.991Z
slug: null
permalink: null
attachments: ""
type: posts
---

bamr87: how would i convert a markdown file into a bash script? essentially, i just want all the text outside of the "```shell" code blocks to be commented out in the shell script.

GitHub Copilot: You can use a Python script to parse the markdown file and convert it into a bash script. Here's a step-by-step plan:

1. Open the markdown file for reading.
2. Open a new bash file for writing.
3. Read the markdown file line by line.
4. If a line contains "```shell", switch to shell script mode.
5. If a line contains "```" and we are in shell script mode, switch back to markdown mode.
6. If we are in shell script mode, write the line to the bash file as is.
7. If we are in markdown mode, write the line to the bash file as a comment.

Here's the Python code that implements this plan:

```python
def convert_md_to_bash(md_file_path, bash_file_path):
    with open(md_file_path, 'r') as md_file, open(bash_file_path, 'w') as bash_file:
        shell_script_mode = False
        for line in md_file:
            if '```shell' in line:
                shell_script_mode = True
                continue
            elif '```' in line and shell_script_mode:
                shell_script_mode = False
                continue
            if shell_script_mode:
                bash_file.write(line)
            else:
                bash_file.write(f'# {line}')

convert_md_to_bash('zer0.md', 'zer0.sh')
```

This script reads a markdown file named 'zer0.md' and writes the converted bash script to 'zer0.sh'. You can replace these file names with your actual file names.

bamr87: don't you need to add the shebang line at the top?

GitHub Copilot: Yes, you're correct. The shebang line is important in a bash script. It tells the system that this file is a set of commands to be fed to the command interpreter indicated. For a bash script, the shebang line is `#!/bin/bash`.

You can modify the Python script to add the shebang line at the top of the bash script:

```python
def convert_md_to_bash(md_file_path, bash_file_path):
    with open(md_file_path, 'r') as md_file, open(bash_file_path, 'w') as bash_file:
        bash_file.write('#!/bin/bash\n')  # add shebang line
        shell_script_mode = False
        for line in md_file:
            if '```shell' in line:
                shell_script_mode = True
                continue
            elif '```' in line and shell_script_mode:
                shell_script_mode = False
                continue
            if shell_script_mode:
                bash_file.write(line)
            else:
                bash_file.write(f'# {line}')

convert_md_to_bash('zer0.md', 'zer0.sh')
```

This will add `#!/bin/bash` at the top of the 'zer0.sh' file.

bamr87: update the script to pars the code block and create the files based on the language used in the code block. for example, if there are python code blocks, the output file will be a .py file with all the non-python code blocks commented out. at the same time, if there's a shell code block, the same logic applies and a .sh file it produced. the number of files is determined by the number of different languages in the markdown file. 

GitHub Copilot: Here's a step-by-step plan:

1. Open the markdown file for reading.
2. Read the markdown file line by line.
3. If a line contains "```" followed by a language name, switch to that language mode and open a new file for that language.
4. If a line contains "```" and we are in a language mode, switch back to markdown mode and close the current language file.
5. If we are in a language mode, write the line to the current language file as is.
6. If we are in markdown mode, write the line to the current language file as a comment.

Here's the Python code that implements this plan:

```python
def convert_md_to_files(md_file_path):
    language_file = None
    language_mode = None
    language_extensions = {'python': '.py', 'shell': '.sh'}
    shebang_lines = {'python': '#!/usr/bin/env python3\n', 'shell': '#!/bin/bash\n'}

    with open(md_file_path, 'r') as md_file:
        for line in md_file:
            if '```' in line:
                if language_mode:
                    # End of a language block, close the file and switch back to markdown mode
                    language_file.close()
                    language_mode = None
                else:
                    # Start of a language block, open a new file for this language
                    language = line.strip('`\n')
                    if language in language_extensions:
                        language_mode = language
                        language_file = open(md_file_path.replace('.md', language_extensions[language]), 'w')
                        language_file.write(shebang_lines.get(language, ''))
                continue

            if language_mode:
                language_file.write(line)
            else:
                if language_file:
                    language_file.write(f'# {line}')

    if language_file:
        language_file.close()

convert_md_to_files('zer0.md')
```

This script reads a markdown file named 'zer0.md' and writes the converted scripts to files with the appropriate extensions for each language block found in the markdown file. The shebang line is added at the top of each script file. You can replace 'zer0.md' with your actual file name.

bamr87: ---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
Cell In[9], line 32
     29     if language_file:
     30         language_file.close()
---> 32 convert_md_to_files('zer0.md')

Cell In[9], line 27
     25         else:
     26             if language_file:
---> 27                 language_file.write(f'# {line}')
     29 if language_file:
     30     language_file.close()

ValueError: I/O operation on closed file.

GitHub Copilot: The error is due to the fact that the script is trying to write to a file that has been closed. This happens when the script encounters a markdown line after closing a language block but before starting a new one. 

To fix this, we need to only write to the language file when we're in language mode. If we're not in language mode, we should skip the line because it's markdown and doesn't belong in any of the language files.

Here's the corrected code:

```python
def convert_md_to_files(md_file_path):
    language_file = None
    language_mode = None
    language_extensions = {'python': '.py', 'shell': '.sh'}
    shebang_lines = {'python': '#!/usr/bin/env python3\n', 'shell': '#!/bin/bash\n'}

    with open(md_file_path, 'r') as md_file:
        for line in md_file:
            if '```' in line:
                if language_mode:
                    # End of a language block, close the file and switch back to markdown mode
                    language_file.close()
                    language_mode = None
                else:
                    # Start of a language block, open a new file for this language
                    language = line.strip('`\n')
                    if language in language_extensions:
                        language_mode = language
                        language_file = open(md_file_path.replace('.md', language_extensions[language]), 'w')
                        language_file.write(shebang_lines.get(language, ''))
                continue

            if language_mode:
                language_file.write(line)

    if language_file:
        language_file.close()

convert_md_to_files('zer0.md')
```

This version of the script will not attempt to write to the language file unless it's in language mode.

bamr87: it's not worrking correctly. it's adding the shebang line for the python file, and it's failing to copy all the lines respectively.

GitHub Copilot: I apologize for the confusion. Let's modify the script to handle the shebang line correctly and ensure all lines are copied as expected. 

Here's the updated plan:

1. Open the markdown file for reading.
2. Read the markdown file line by line.
3. If a line contains "```" followed by a language name, switch to that language mode and open a new file for that language.
4. If a line contains "```" and we are in a language mode, switch back to markdown mode and close the current language file.
5. If we are in a language mode, write the line to the current language file as is.
6. If we are in markdown mode, skip the line as it's markdown and doesn't belong in any of the language files.

Here's the Python code that implements this plan:

```python
def convert_md_to_files(md_file_path):
    language_file = None
    language_mode = None
    language_extensions = {'python': '.py', 'shell': '.sh'}
    shebang_lines = {'python': '#!/usr/bin/env python3\n', 'shell': '#!/bin/bash\n'}

    with open(md_file_path, 'r') as md_file:
        for line in md_file:
            if '```' in line:
                if language_mode:
                    # End of a language block, close the file and switch back to markdown mode
                    language_file.close()
                    language_mode = None
                else:
                    # Start of a language block, open a new file for this language
                    language = line.strip('`\n')
                    if language in language_extensions:
                        language_mode = language
                        language_file = open(md_file_path.replace('.md', language_extensions[language]), 'w')
                        if language in shebang_lines:
                            language_file.write(shebang_lines[language])
                continue

            if language_mode:
                language_file.write(line)

    if language_file:
        language_file.close()

convert_md_to_files('zer0.md')
```

This version of the script will only add the shebang line if the language is in the `shebang_lines` dictionary, and it will skip markdown lines when not in language mode.

bamr87: still not working. 

GitHub Copilot: I apologize for the confusion earlier. Let's try a different approach. We'll use a dictionary to keep track of the open files for each language. This way, we can handle multiple language blocks for the same language.

Here's the updated plan:

1. Open the markdown file for reading.
2. Initialize an empty dictionary to keep track of the open files for each language.
3. Read the markdown file line by line.
4. If a line contains "```" followed by a language name, switch to that language mode and open a new file for that language if it's not already open.
5. If a line contains "```" and we are in a language mode, switch back to markdown mode.
6. If we are in a language mode, write the line to the corresponding language file as is.
7. If we are in markdown mode, skip the line as it's markdown and doesn't belong in any of the language files.
8. After reading all lines, close all open language files.

Here's the Python code that implements this plan:

```python
def convert_md_to_files(md_file_path):
    language_files = {}
    language_mode = None
    language_extensions = {'python': '.py', 'shell': '.sh'}
    shebang_lines = {'python': '#!/usr/bin/env python3\n', 'shell': '#!/bin/bash\n'}

    with open(md_file_path, 'r') as md_file:
        for line in md_file:
            if '```' in line:
                if language_mode:
                    # End of a language block, switch back to markdown mode
                    language_mode = None
                else:
                    # Start of a language block, open a new file for this language if not already open
                    language = line.strip('`\n')
                    if language in language_extensions:
                        language_mode = language
                        if language not in language_files:
                            language_file = open(md_file_path.replace('.md', language_extensions[language]), 'w')
                            if language in shebang_lines:
                                language_file.write(shebang_lines[language])
                            language_files[language] = language_file
                continue

            if language_mode:
                language_files[language_mode].write(line)

    # Close all open language files
    for language_file in language_files.values():
        language_file.close()

convert_md_to_files('zer0.md')
```

This version of the script should correctly handle multiple language blocks for the same language and add the shebang line only once for each language file.

bamr87: ok. it's working now. but update the logic so that it sets the mode only if the first three characters of the line are "```". right now it does not work for code blocks where there's a "```" elsewhere on the line.

GitHub Copilot: I understand your requirement. We need to modify the script to only switch modes when the line starts with "```". Here's the updated plan:

1. Open the markdown file for reading.
2. Initialize an empty dictionary to keep track of the open files for each language.
3. Read the markdown file line by line.
4. If a line starts with "```" followed by a language name, switch to that language mode and open a new file for that language if it's not already open.
5. If a line starts with "```" and we are in a language mode, switch back to markdown mode.
6. If we are in a language mode, write the line to the corresponding language file as is.
7. If we are in markdown mode, skip the line as it's markdown and doesn't belong in any of the language files.
8. After reading all lines, close all open language files.

Here's the Python code that implements this plan:

```python
def convert_md_to_files(md_file_path):
    language_files = {}
    language_mode = None
    language_extensions = {'python': '.py', 'shell': '.sh'}
    shebang_lines = {'python': '#!/usr/bin/env python3\n', 'shell': '#!/bin/bash\n'}

    with open(md_file_path, 'r') as md_file:
        for line in md_file:
            if line.startswith('```'):
                if language_mode:
                    # End of a language block, switch back to markdown mode
                    language_mode = None
                else:
                    # Start of a language block, open a new file for this language if not already open
                    language = line.strip('`\n')
                    if language in language_extensions:
                        language_mode = language
                        if language not in language_files:
                            language_file = open(md_file_path.replace('.md', language_extensions[language]), 'w')
                            if language in shebang_lines:
                                language_file.write(shebang_lines[language])
                            language_files[language] = language_file
                continue

            if language_mode:
                language_files[language_mode].write(line)

    # Close all open language files
    for language_file in language_files.values():
        language_file.close()

convert_md_to_files('zer0.md')
```

This version of the script should correctly handle code blocks that start with "```" and ignore any "```" that appear elsewhere on the line.