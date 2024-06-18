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
