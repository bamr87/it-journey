#!/usr/bin/env python3
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
