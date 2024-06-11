import os

def convert_md_to_files(md_file_path):
    language_files = {}
    language_mode = None
    language_extensions = {'python': '.py', 'shell': '.sh'}
    shebang_lines = {'python': '#!/usr/bin/env python3\n', 'shell': '#!/bin/bash\n'}

    output_folder = "script"
    os.makedirs(output_folder, exist_ok=True)

    with open(md_file_path, 'r') as md_file:
        for line in md_file:
            if line.startswith('```'):
                if language_mode:
                    language_mode = None
                else:
                    language = line.strip('`\n')
                    if language in language_extensions:
                        language_mode = language
                        if language not in language_files:
                            output_file_path = os.path.join(output_folder, os.path.basename(md_file_path).replace('.md', language_extensions[language]))
                            language_file = open(output_file_path, 'w')
                            if language in shebang_lines:
                                language_file.write(shebang_lines[language])
                            language_files[language] = language_file
                continue

            if language_mode:
                language_files[language_mode].write(line)

    for language_file in language_files.values():
        language_file.close()

convert_md_to_files('zer0.md')