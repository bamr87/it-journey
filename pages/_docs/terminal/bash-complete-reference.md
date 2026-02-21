---
title: "The Complete BASH Reference: Commands, Functions, Snippets & Techniques"
description: "Exhaustive reference guide covering every aspect of GNU Bash — built-in commands, parameter expansion, process control, scripting patterns, text processing, networking, and advanced techniques."
date: 2026-02-20T00:00:00.000Z
lastmod: 2026-02-20T00:00:00.000Z
author: "IT-Journey Team"
layout: journals
permalink: /docs/bash-complete-reference/
tags:
    - bash
    - shell
    - scripting
    - command-line
    - linux
    - macos
    - reference
    - sysadmin
    - automation
    - devops
categories:
    - Documentation
    - Terminal
    - Reference
keywords:
    primary:
        - bash commands
        - bash scripting
        - bash reference
    secondary:
        - shell scripting
        - linux commands
        - bash functions
        - bash built-ins
        - command line reference
        - it-journey
excerpt: "The definitive Bash reference — every built-in command, expansion, operator, scripting pattern, and real-world snippet you'll ever need."
preview: "Complete Bash reference covering commands, scripting, text processing, process control, networking, and advanced techniques."
difficulty: "🟡 Intermediate to Advanced"
estimated_time: "60+ minutes to read"
draft: false
---

# 🐚 The Complete BASH Reference

> **Everything you need** to master GNU Bash — from basic commands to advanced scripting, process management, text processing, networking, and system administration.

---

## Table of Contents

1. [Bash Fundamentals](#-bash-fundamentals)
2. [Built-in Commands](#-built-in-commands)
3. [Variables & Data Types](#-variables--data-types)
4. [Parameter Expansion](#-parameter-expansion)
5. [Arrays & Associative Arrays](#-arrays--associative-arrays)
6. [String Manipulation](#-string-manipulation)
7. [Arithmetic](#-arithmetic)
8. [Conditionals & Test Operators](#-conditionals--test-operators)
9. [Loops & Iteration](#-loops--iteration)
10. [Functions](#-functions)
11. [Input / Output & Redirection](#-input--output--redirection)
12. [Pipes & Process Substitution](#-pipes--process-substitution)
13. [Pattern Matching & Globbing](#-pattern-matching--globbing)
14. [Regular Expressions](#-regular-expressions)
15. [Command History & Expansion](#-command-history--expansion)
16. [Job Control & Process Management](#-job-control--process-management)
17. [Signal Handling & Traps](#-signal-handling--traps)
18. [File & Directory Operations](#-file--directory-operations)
19. [File Permissions & Ownership](#-file-permissions--ownership)
20. [Text Processing Commands](#-text-processing-commands)
21. [Search & Find](#-search--find)
22. [Archiving & Compression](#-archiving--compression)
23. [Networking Commands](#-networking-commands)
24. [System Information & Monitoring](#-system-information--monitoring)
25. [User & Group Management](#-user--group-management)
26. [Disk & Filesystem](#-disk--filesystem)
27. [Package Management](#-package-management)
28. [Environment & Shell Configuration](#-environment--shell-configuration)
29. [Debugging & Profiling](#-debugging--profiling)
30. [Security & Cryptography](#-security--cryptography)
31. [Date & Time](#-date--time)
32. [Scripting Best Practices](#-scripting-best-practices)
33. [Advanced Techniques](#-advanced-techniques)
34. [One-Liners & Recipes](#-one-liners--recipes)
35. [Heredocs & Herestrings](#-heredocs--herestrings)
36. [Subshells & Command Grouping](#-subshells--command-grouping)
37. [Coprocesses & Named Pipes](#-coprocesses--named-pipes)
38. [Bash Loadable Built-ins](#-bash-loadable-built-ins)

---

## 🏁 Bash Fundamentals

### What Is Bash?

Bash (**B**ourne **A**gain **Sh**ell) is a Unix shell and command language written by Brian Fox for the GNU Project. It is the default shell on most Linux distributions and macOS (prior to Catalina).

### Shebang Lines

```bash
#!/bin/bash           # Standard Bash
#!/usr/bin/env bash   # Portable (finds bash in PATH)
#!/bin/bash -e        # Exit on error
#!/bin/bash -eu       # Exit on error + unset variables
```

### Running a Script

```bash
# Make executable and run
chmod +x script.sh
./script.sh

# Run with bash explicitly
bash script.sh

# Run in current shell (source)
source script.sh
. script.sh

# Run with debug output
bash -x script.sh

# Syntax check without executing
bash -n script.sh
```

### Command Separators & Chaining

```bash
# Sequential execution
command1 ; command2

# AND — run command2 only if command1 succeeds
command1 && command2

# OR — run command2 only if command1 fails
command1 || command2

# Background execution
command1 &

# Pipe stdout of command1 to stdin of command2
command1 | command2

# Pipe both stdout and stderr
command1 |& command2

# Negate exit status
! command1
```

### Quoting Rules

```bash
# No quoting — word splitting & glob expansion
echo Hello World

# Single quotes — literal, no expansion
echo 'Hello $USER'       # => Hello $USER

# Double quotes — variable/command expansion, no glob
echo "Hello $USER"       # => Hello john

# $'...' — ANSI-C quoting (interprets escape sequences)
echo $'Line1\nLine2'     # => two lines

# $"..." — Locale translation (rarely used)
echo $"Hello"

# Escaping
echo "Price: \$5"        # => Price: $5
echo 'It'\''s here'      # => It's here
echo "She said \"hi\""   # => She said "hi"
```

### Exit Codes

```bash
# Success
exit 0

# General error
exit 1

# Misuse of shell built-in
exit 2

# Command not found (by convention)
exit 127

# Killed by signal N
exit $((128 + N))

# Check last exit code
echo $?

# Exit code of last background command
echo $!
```

---

## 🔧 Built-in Commands

### Shell Built-ins (Complete List)

| Command | Description |
|---------|-------------|
| `.` (dot) | Source/execute a file in current shell |
| `:` (colon) | Null command (always returns true) |
| `alias` | Define or display aliases |
| `bg` | Resume suspended job in background |
| `bind` | Display or modify readline key bindings |
| `break` | Exit from a loop |
| `builtin` | Run a shell built-in, bypassing functions |
| `caller` | Return call stack context (for debugging) |
| `cd` | Change working directory |
| `command` | Run command bypassing shell functions |
| `compgen` | Generate completion matches |
| `complete` | Specify command completion |
| `compopt` | Modify completion options |
| `continue` | Skip to next loop iteration |
| `declare` | Declare variables and attributes |
| `dirs` | Display directory stack |
| `disown` | Remove job from job table |
| `echo` | Display text |
| `enable` | Enable/disable built-in commands |
| `eval` | Execute arguments as shell command |
| `exec` | Replace shell with command |
| `exit` | Exit the shell |
| `export` | Set environment variables |
| `false` | Return unsuccessful exit status |
| `fc` | List/edit/re-execute commands from history |
| `fg` | Resume suspended job in foreground |
| `getopts` | Parse positional parameters/options |
| `hash` | Remember command locations |
| `help` | Display help for built-in commands |
| `history` | Display/manipulate command history |
| `jobs` | List active jobs |
| `kill` | Send signal to processes |
| `let` | Evaluate arithmetic expressions |
| `local` | Create local variables in functions |
| `logout` | Exit a login shell |
| `mapfile` | Read lines into an array (also `readarray`) |
| `popd` | Remove directory from stack |
| `printf` | Format and print data |
| `pushd` | Add directory to stack |
| `pwd` | Print working directory |
| `read` | Read a line of input |
| `readarray` | Read lines into an array (alias for `mapfile`) |
| `readonly` | Mark variables as read-only |
| `return` | Return from a function |
| `select` | Create a menu |
| `set` | Set/unset shell options and positional params |
| `shift` | Shift positional parameters |
| `shopt` | Set/unset shell options |
| `source` | Execute file in current shell (same as `.`) |
| `suspend` | Suspend shell execution |
| `test` | Evaluate conditional expression (same as `[`) |
| `time` | Report time consumed by pipeline |
| `times` | Print accumulated user and system times |
| `trap` | Set signal handlers |
| `true` | Return successful exit status |
| `type` | Display how a name would be interpreted |
| `typeset` | Declare variables (synonym for `declare`) |
| `ulimit` | Set/display resource limits |
| `umask` | Set file mode creation mask |
| `unalias` | Remove alias definitions |
| `unset` | Remove variable or function |
| `wait` | Wait for background processes |

### Essential External Commands

| Command | Description |
|---------|-------------|
| `ls` | List directory contents |
| `cp` | Copy files and directories |
| `mv` | Move/rename files and directories |
| `rm` | Remove files and directories |
| `mkdir` | Create directories |
| `rmdir` | Remove empty directories |
| `touch` | Create file / update timestamps |
| `cat` | Concatenate and display files |
| `less` / `more` | Paginate file output |
| `head` / `tail` | Display beginning/end of files |
| `ln` | Create links |
| `stat` | Display file status |
| `file` | Determine file type |
| `wc` | Word, line, character, byte count |
| `sort` | Sort lines |
| `uniq` | Report/omit repeated lines |
| `cut` | Remove sections from lines |
| `paste` | Merge lines of files |
| `tr` | Translate/delete characters |
| `tee` | Read stdin, write to stdout and files |
| `xargs` | Build and execute commands from stdin |
| `diff` | Compare files line by line |
| `patch` | Apply a diff file to an original |
| `comm` | Compare two sorted files line by line |
| `column` | Format output into columns |
| `rev` | Reverse lines character-wise |
| `tac` | Concatenate and print files in reverse |
| `nl` | Number lines of files |
| `fold` | Wrap lines to fit specified width |
| `expand` / `unexpand` | Convert tabs to/from spaces |

---

## 📦 Variables & Data Types

### Variable Assignment

```bash
# Simple assignment (no spaces around =)
name="John Doe"
age=30
readonly PI=3.14159

# From command output
current_date=$(date +%Y-%m-%d)
file_count=$(ls | wc -l)

# From arithmetic
result=$((5 + 3))

# Assign with default
: "${VAR:=default_value}"

# Multiple assignments
a=1 b=2 c=3
```

### Variable Types with `declare`

```bash
# Integer
declare -i num=42
num=num+8       # Arithmetic without $(())
echo $num       # => 50

# Read-only
declare -r CONST="immutable"

# Array
declare -a list=(one two three)

# Associative array (dictionary)
declare -A map=([key1]=val1 [key2]=val2)

# Export (environment variable)
declare -x GLOBAL_VAR="visible to child processes"

# Lowercase
declare -l lower="HELLO"
echo $lower     # => hello

# Uppercase
declare -u upper="hello"
echo $upper     # => HELLO

# Name reference (pointer to another variable)
declare -n ref=name
echo $ref       # => John Doe

# Print all attributes of a variable
declare -p name

# Function trace
declare -ft myfunc

# Print all functions
declare -F

# Print all function definitions
declare -f
```

### Special Variables

| Variable | Description |
|----------|-------------|
| `$0` | Script name / shell name |
| `$1` – `$9` | Positional parameters 1–9 |
| `${10}` | Positional parameter 10+ |
| `$#` | Number of positional parameters |
| `$*` | All parameters as single word |
| `$@` | All parameters as separate words |
| `$?` | Exit status of last command |
| `$$` | PID of current shell |
| `$!` | PID of last background command |
| `$-` | Current shell option flags |
| `$_` | Last argument of previous command |
| `$LINENO` | Current line number in script |
| `$FUNCNAME` | Current function name |
| `$BASH_SOURCE` | Source filename |
| `$BASH_LINENO` | Line number of caller |
| `$BASH_VERSION` | Bash version string |
| `$BASHPID` | PID of current bash process |
| `$BASH_SUBSHELL` | Subshell nesting level |
| `$RANDOM` | Random integer (0–32767) |
| `$SECONDS` | Seconds since shell started |
| `$REPLY` | Default variable for `read` |
| `$PIPESTATUS` | Array of exit statuses from last pipeline |
| `$HOSTNAME` | System hostname |
| `$HOSTTYPE` | Machine hardware type |
| `$OSTYPE` | Operating system type |
| `$MACHTYPE` | Complete system type |
| `$IFS` | Internal Field Separator |
| `$PATH` | Command search path |
| `$HOME` | Home directory |
| `$USER` | Current username |
| `$SHELL` | Default shell path |
| `$PWD` | Current working directory |
| `$OLDPWD` | Previous working directory |
| `$TERM` | Terminal type |
| `$EDITOR` | Default editor |
| `$LANG` | Locale setting |
| `$SHLVL` | Shell nesting level |
| `$TMOUT` | Auto-logout timeout (seconds) |
| `$HISTSIZE` | Number of commands to remember |
| `$HISTFILE` | History file location |
| `$HISTFILESIZE` | Max lines in history file |
| `$HISTCONTROL` | History recording control |
| `$HISTIGNORE` | Patterns to ignore in history |
| `$HISTTIMEFORMAT` | Timestamp format for history |
| `$PROMPT_COMMAND` | Command run before each prompt |
| `$PS1` | Primary prompt string |
| `$PS2` | Secondary prompt (continuation) |
| `$PS3` | Prompt for `select` |
| `$PS4` | Debug prompt (`set -x`) |
| `$COLUMNS` | Terminal width |
| `$LINES` | Terminal height |
| `$COMP_WORDS` | Array of words in current completion |
| `$COMP_CWORD` | Index of current word in completion |
| `$DIRSTACK` | Directory stack contents |
| `$EUID` | Effective user ID |
| `$UID` | Real user ID |
| `$GROUPS` | Array of group IDs |

### Environment Variables

```bash
# Set for current session
export MY_VAR="value"

# Set for a single command
MY_VAR="value" command

# Unset
unset MY_VAR

# List all environment variables
env
printenv

# List specific variable
printenv HOME

# Persist across sessions (add to ~/.bashrc or ~/.bash_profile)
echo 'export MY_VAR="value"' >> ~/.bashrc
source ~/.bashrc
```

---

## 🔤 Parameter Expansion

### Basic Expansion

```bash
name="world"
echo "Hello ${name}"          # => Hello world
echo "Hello $name"            # => Hello world (short form)
echo "Length: ${#name}"        # => Length: 5
```

### Default Values

```bash
# Use default if unset or null
echo "${var:-default}"         # $var or "default"

# Assign default if unset or null
echo "${var:=default}"         # Sets var=default if unset

# Use alternative if set and non-null
echo "${var:+alternative}"     # "alternative" if var is set

# Error if unset or null
echo "${var:?'var is required'}"

# Without colon — only checks if unset (null is OK)
echo "${var-default}"          # $var or "default" if unset
echo "${var=default}"
echo "${var+alternative}"
echo "${var?'error message'}"
```

### Substring Extraction

```bash
str="Hello World"
echo "${str:0:5}"              # => Hello (offset 0, length 5)
echo "${str:6}"                # => World (from offset 6)
echo "${str: -5}"              # => World (last 5 chars — note space)
echo "${str: -5:3}"            # => Wor (3 chars from -5)
echo "${str:(-5)}"             # => World (alternate negative syntax)
```

### String Removal (Trimming)

```bash
path="/usr/local/bin/script.sh"

# Remove shortest match from front
echo "${path#*/}"              # => usr/local/bin/script.sh

# Remove longest match from front
echo "${path##*/}"             # => script.sh (basename)

# Remove shortest match from end
echo "${path%/*}"              # => /usr/local/bin (dirname)

# Remove longest match from end
echo "${path%%/*}"             # => (empty — everything after first /)

# Practical examples
file="archive.tar.gz"
echo "${file%.*}"              # => archive.tar (remove ext)
echo "${file%%.*}"             # => archive (remove all ext)
echo "${file#*.}"              # => tar.gz (remove name)
echo "${file##*.}"             # => gz (get extension)
```

### String Replacement

```bash
str="Hello World World"

# Replace first occurrence
echo "${str/World/Earth}"      # => Hello Earth World

# Replace all occurrences
echo "${str//World/Earth}"     # => Hello Earth Earth

# Replace at beginning (prefix)
echo "${str/#Hello/Hi}"        # => Hi World World

# Replace at end (suffix)
echo "${str/%World/Earth}"     # => Hello World Earth

# Delete (replace with nothing)
echo "${str// /}"              # => HelloWorldWorld
```

### Case Modification (Bash 4+)

```bash
str="hello WORLD"

# Uppercase first char
echo "${str^}"                 # => Hello WORLD

# Uppercase all
echo "${str^^}"                # => HELLO WORLD

# Lowercase first char
echo "${str,}"                 # => hello WORLD

# Lowercase all
echo "${str,,}"                # => hello world

# Toggle case (Bash 4.4+?)
# echo "${str~~}"              # => HELLO world

# Apply to array elements
arr=(hello World)
echo "${arr[@]^}"              # => Hello World
echo "${arr[@],,}"             # => hello world
```

### Indirect Expansion

```bash
var_name="greeting"
greeting="Hello!"

# Indirect reference
echo "${!var_name}"            # => Hello! (value of $greeting)

# List matching variable names
echo "${!BASH*}"               # All vars starting with BASH
echo "${!HOME*}"               # All vars starting with HOME
```

### Transformation (Bash 5.1+)

```bash
var="hello world"

# Quoted for re-use
echo "${var@Q}"                # => 'hello world'

# Assignment form
echo "${var@A}"                # => var='hello world'

# Escape special characters
echo "${var@E}"

# Prompt expansion
echo "${var@P}"

# Lowercase
echo "${var@L}"                # => hello world

# Uppercase
echo "${var@U}"                # => HELLO WORLD

# Capitalize
echo "${var@u}"                # => Hello world

# Attributes/flags applied
echo "${var@a}"                # => (shows declare flags)
```

---

## 📚 Arrays & Associative Arrays

### Indexed Arrays

```bash
# Declaration methods
fruits=("Apple" "Banana" "Cherry")
declare -a colors

colors[0]="Red"
colors[1]="Green"
colors[2]="Blue"

# From command output
files=($(ls *.txt))

# From range
numbers=({1..10})

# From brace expansion
combos=(test{1..3}.{txt,log})  # test1.txt test1.log test2.txt ...
```

### Array Operations

```bash
arr=("one" "two" "three" "four" "five")

# Access elements
echo "${arr[0]}"               # => one (first)
echo "${arr[-1]}"              # => five (last)
echo "${arr[@]}"               # All elements
echo "${arr[*]}"               # All as single string

# Length
echo "${#arr[@]}"              # => 5 (number of elements)
echo "${#arr[0]}"              # => 3 (length of first element)

# Slice
echo "${arr[@]:1:3}"           # => two three four (offset:length)
echo "${arr[@]:2}"             # => three four five (from offset)

# Keys/indices
echo "${!arr[@]}"              # => 0 1 2 3 4

# Append
arr+=("six")
arr=("${arr[@]}" "seven")

# Prepend
arr=("zero" "${arr[@]}")

# Remove element
unset 'arr[2]'

# Re-index after removal
arr=("${arr[@]}")

# Copy
arr_copy=("${arr[@]}")

# Merge
merged=("${arr1[@]}" "${arr2[@]}")

# Filter by pattern
matches=("${arr[@]/t*/}")      # Remove matching elements

# Check if element exists
if [[ " ${arr[*]} " == *" two "* ]]; then
    echo "Found"
fi

# Sort array
IFS=$'\n' sorted=($(sort <<<"${arr[*]}")); unset IFS

# Unique values
IFS=$'\n' unique=($(sort -u <<<"${arr[*]}")); unset IFS

# Reverse array
for ((i=${#arr[@]}-1; i>=0; i--)); do
    reversed+=("${arr[i]}")
done

# Join with delimiter
function join_by {
    local d=${1-} f=${2-}
    if shift 2; then
        printf '%s' "$f" "${@/#/$d}"
    fi
}
join_by ',' "${arr[@]}"        # => one,two,three,four,five
```

### Array Iteration

```bash
# By value
for item in "${arr[@]}"; do
    echo "$item"
done

# By index
for i in "${!arr[@]}"; do
    echo "$i: ${arr[$i]}"
done

# While loop with index
i=0
while [ $i -lt ${#arr[@]} ]; do
    echo "${arr[$i]}"
    ((i++))
done
```

### Associative Arrays (Bash 4+)

```bash
# Declaration
declare -A user
user[name]="John"
user[age]=30
user[email]="john@example.com"

# Or inline
declare -A config=(
    [host]="localhost"
    [port]="8080"
    [debug]="true"
)

# Access
echo "${config[host]}"          # => localhost

# All values
echo "${config[@]}"

# All keys
echo "${!config[@]}"

# Number of elements
echo "${#config[@]}"

# Check key exists
if [[ -v config[host] ]]; then
    echo "Key exists"
fi

# Delete key
unset 'config[debug]'

# Iterate
for key in "${!config[@]}"; do
    echo "$key = ${config[$key]}"
done
```

### `mapfile` / `readarray`

```bash
# Read file into array (one line per element)
mapfile -t lines < file.txt

# Read with callback every N lines
mapfile -t -c 5 -C 'process_batch' lines < file.txt

# Read specific number of lines
mapfile -t -n 10 lines < file.txt

# Skip first N lines
mapfile -t -s 3 lines < file.txt

# From command output
mapfile -t results < <(find . -name "*.sh")

# Read into array starting at index
mapfile -t -O 5 lines < file.txt
```

---

## ✂️ String Manipulation

### String Operations

```bash
str="Hello, World!"

# Length
echo "${#str}"                  # => 13

# Concatenation
greeting="Hello"
name="World"
full="${greeting}, ${name}!"

# Substring check
if [[ "$str" == *"World"* ]]; then
    echo "Contains 'World'"
fi

# Starts with
if [[ "$str" == Hello* ]]; then
    echo "Starts with 'Hello'"
fi

# Ends with
if [[ "$str" == *'!' ]]; then
    echo "Ends with '!'"
fi

# Replace characters with tr
echo "$str" | tr '[:lower:]' '[:upper:]'    # => HELLO, WORLD!
echo "$str" | tr -d ','                      # => Hello World!
echo "$str" | tr ' ' '_'                     # => Hello,_World!

# Repeat string
printf '%0.s-' {1..40}         # Print 40 dashes
printf '%.0s=' {1..80}         # Print 80 equals

# Pad string
printf '%-20s|' "left aligned"
printf '%20s|' "right aligned"
printf '%020d' 42              # => 00000000000000000042

# Split string into array
IFS=',' read -ra parts <<< "a,b,c,d"
echo "${parts[1]}"             # => b

# Trim whitespace
trim() { 
    local var="$*"
    var="${var#"${var%%[![:space:]]*}"}"
    var="${var%"${var##*[![:space:]]}"}"
    echo "$var"
}
```

### `printf` Formatting

```bash
# Basic formatting
printf "Name: %s, Age: %d\n" "John" 30

# Float formatting
printf "Pi: %.4f\n" 3.14159    # => Pi: 3.1416

# Padding
printf "%-20s %5d\n" "Item" 42

# Hex/Octal
printf "Hex: %x, Oct: %o\n" 255 255   # => Hex: ff, Oct: 377

# Store in variable
printf -v result "Hello %s" "World"

# Print with width
printf "%*s\n" 20 "right"     # Right-aligned in 20-char field

# Repeat character
printf '%0.s*' {1..50}

# Print array as table
printf "%-15s %-10s %s\n" "Name" "Age" "City"
printf "%-15s %-10d %s\n" "Alice" 30 "NYC"
printf "%-15s %-10d %s\n" "Bob" 25 "LA"

# Print with color
printf "\e[31m%s\e[0m\n" "Red text"

# Print to stderr
printf "%s\n" "Error message" >&2

# Format specifiers
# %s   String
# %d   Decimal integer
# %i   Integer (same as %d)
# %f   Floating point
# %e   Scientific notation
# %g   Shorter of %f and %e
# %x   Hexadecimal (lowercase)
# %X   Hexadecimal (uppercase)
# %o   Octal
# %b   Interpret backslash escapes in argument
# %q   Shell-quoted string
# %%   Literal percent sign
# %n   Count of characters written (stored in argument)
```

---

## 🔢 Arithmetic

### Arithmetic Expansion

```bash
# $(( expression ))
echo $((5 + 3))            # => 8
echo $((10 - 4))           # => 6
echo $((6 * 7))            # => 42
echo $((20 / 3))           # => 6 (integer division)
echo $((20 % 3))           # => 2 (modulo)
echo $((2 ** 10))          # => 1024 (exponentiation)

# With variables
a=10 b=3
echo $((a + b))            # => 13
echo $((a / b))            # => 3
echo $((a % b))            # => 1

# Increment/decrement
((a++))                    # Post-increment
((a--))                    # Post-decrement
((++a))                    # Pre-increment
((--a))                    # Pre-decrement

# Compound assignment
((a += 5))
((a -= 2))
((a *= 3))
((a /= 4))
((a %= 7))

# Bitwise operations
echo $((5 & 3))            # => 1 (AND)
echo $((5 | 3))            # => 7 (OR)
echo $((5 ^ 3))            # => 6 (XOR)
echo $((~5))               # => -6 (NOT)
echo $((5 << 2))           # => 20 (left shift)
echo $((20 >> 2))          # => 5 (right shift)

# Ternary operator
echo $((a > b ? a : b))    # Max of a and b

# Comma operator
echo $((a=5, b=3, a+b))   # => 8

# Different bases
echo $((16#FF))            # => 255 (hex)
echo $((8#77))             # => 63 (octal)
echo $((2#1010))           # => 10 (binary)
```

### The `let` Command

```bash
let "a = 5 + 3"
let "b = a * 2"
let "a++"
let "c = a > b ? a : b"
```

### `bc` for Floating Point

```bash
# Basic arithmetic
echo "5.5 + 3.2" | bc        # => 8.7

# With scale (decimal places)
echo "scale=4; 10/3" | bc    # => 3.3333

# Square root
echo "scale=4; sqrt(2)" | bc # => 1.4142

# Power
echo "2^10" | bc             # => 1024

# Compare
echo "5.5 > 3.2" | bc        # => 1 (true)

# Using bc -l (math library)
echo "s(1)" | bc -l           # sine of 1 radian
echo "c(0)" | bc -l           # cosine of 0
echo "a(1)*4" | bc -l         # pi (arctan(1)*4)
echo "l(100)" | bc -l         # natural log of 100
echo "e(1)" | bc -l           # e (Euler's number)

# Multi-line bc
bc <<< "
scale=6
x=3.14159
s(x)
"
```

### `awk` for Floating Point

```bash
awk "BEGIN {printf \"%.2f\n\", 10/3}"    # => 3.33
awk "BEGIN {print sin(1)}"
awk "BEGIN {print exp(1)}"               # => e
awk "BEGIN {print log(100)}"
```

---

## 🧪 Conditionals & Test Operators

### `if` / `elif` / `else`

```bash
if [[ condition ]]; then
    # commands
elif [[ condition2 ]]; then
    # commands
else
    # commands
fi

# One-liner
[[ -f file.txt ]] && echo "exists" || echo "missing"
```

### `test`, `[`, and `[[`

```bash
# All equivalent for simple tests:
test -f file.txt
[ -f file.txt ]
[[ -f file.txt ]]

# [[ is preferred — supports:
#   - Pattern matching: [[ $str == pattern* ]]
#   - Regex:            [[ $str =~ regex ]]
#   - No word splitting or glob expansion
#   - Logical operators: && ||
```

### File Test Operators

| Operator | Description |
|----------|-------------|
| `-e FILE` | Exists (file or directory) |
| `-f FILE` | Regular file |
| `-d FILE` | Directory |
| `-L FILE` / `-h FILE` | Symbolic link |
| `-s FILE` | Size > 0 |
| `-r FILE` | Readable |
| `-w FILE` | Writable |
| `-x FILE` | Executable |
| `-b FILE` | Block special device |
| `-c FILE` | Character special device |
| `-p FILE` | Named pipe (FIFO) |
| `-S FILE` | Socket |
| `-t FD` | FD is open and refers to a terminal |
| `-u FILE` | Set-user-ID bit set |
| `-g FILE` | Set-group-ID bit set |
| `-k FILE` | Sticky bit set |
| `-O FILE` | Owned by effective user ID |
| `-G FILE` | Owned by effective group ID |
| `-N FILE` | Modified since last read |
| `FILE1 -nt FILE2` | FILE1 is newer |
| `FILE1 -ot FILE2` | FILE1 is older |
| `FILE1 -ef FILE2` | Same device and inode |

### String Test Operators

| Operator | Description |
|----------|-------------|
| `-z STRING` | String is empty (zero length) |
| `-n STRING` | String is non-empty |
| `STRING1 == STRING2` | Strings are equal |
| `STRING1 != STRING2` | Strings are not equal |
| `STRING1 < STRING2` | Lexicographically less than |
| `STRING1 > STRING2` | Lexicographically greater than |
| `STRING =~ REGEX` | Extended regex match (`[[` only) |
| `STRING == PATTERN` | Pattern/glob match (`[[` only) |

### Integer Test Operators

| Operator | Description |
|----------|-------------|
| `INT1 -eq INT2` | Equal |
| `INT1 -ne INT2` | Not equal |
| `INT1 -lt INT2` | Less than |
| `INT1 -le INT2` | Less than or equal |
| `INT1 -gt INT2` | Greater than |
| `INT1 -ge INT2` | Greater than or equal |

### Logical Operators

```bash
# Inside [[ ]]
[[ condition1 && condition2 ]]
[[ condition1 || condition2 ]]
[[ ! condition ]]

# Inside [ ] (POSIX)
[ condition1 ] && [ condition2 ]
[ condition1 -a condition2 ]      # AND (deprecated)
[ condition1 -o condition2 ]      # OR (deprecated)
[ ! condition ]
```

### `case` Statement

```bash
case "$variable" in
    pattern1)
        commands
        ;;
    pattern2|pattern3)
        commands
        ;;
    [0-9]*)
        echo "Starts with digit"
        ;;
    *.txt)
        echo "Text file"
        ;;
    *)
        echo "Default case"
        ;;
esac

# Fall-through (Bash 4+)
case "$var" in
    pattern1)
        commands
        ;;&              # Continue testing patterns
    pattern2)
        commands
        ;&               # Fall through to next case
    pattern3)
        commands
        ;;
esac
```

### `select` Menu

```bash
PS3="Choose an option: "
select opt in "Option 1" "Option 2" "Option 3" "Quit"; do
    case $opt in
        "Option 1") echo "You chose 1" ;;
        "Option 2") echo "You chose 2" ;;
        "Option 3") echo "You chose 3" ;;
        "Quit")     break ;;
        *)          echo "Invalid option" ;;
    esac
done
```

---

## 🔄 Loops & Iteration

### `for` Loop

```bash
# List iteration
for item in apple banana cherry; do
    echo "$item"
done

# Array iteration
for item in "${arr[@]}"; do
    echo "$item"
done

# File iteration
for file in *.txt; do
    echo "$file"
done

# Range
for i in {1..10}; do
    echo "$i"
done

# Range with step
for i in {0..100..5}; do
    echo "$i"
done

# Command output
for user in $(cut -d: -f1 /etc/passwd); do
    echo "$user"
done

# C-style
for ((i=0; i<10; i++)); do
    echo "$i"
done

# Infinite
for ((;;)); do
    echo "forever"
    break
done

# Multiple variables
for ((i=0, j=10; i<j; i++, j--)); do
    echo "i=$i, j=$j"
done
```

### `while` Loop

```bash
# Basic
count=0
while [[ $count -lt 5 ]]; do
    echo "$count"
    ((count++))
done

# Read file line by line
while IFS= read -r line; do
    echo "$line"
done < file.txt

# Read from command output
while IFS= read -r line; do
    echo "$line"
done < <(ls -la)

# Read with delimiter
while IFS=: read -r user _ uid gid _ home shell; do
    echo "$user uses $shell"
done < /etc/passwd

# Read CSV
while IFS=, read -r col1 col2 col3; do
    echo "$col1 | $col2 | $col3"
done < data.csv

# Infinite
while true; do
    # ...
    break
done

# Shorthand infinite
while :; do
    # ...
    break
done
```

### `until` Loop

```bash
count=0
until [[ $count -ge 5 ]]; do
    echo "$count"
    ((count++))
done
```

### Loop Control

```bash
# Break out of loop
for i in {1..10}; do
    [[ $i -eq 5 ]] && break
    echo "$i"
done

# Break out of nested loop (level N)
for i in {1..3}; do
    for j in {1..3}; do
        [[ $j -eq 2 ]] && break 2   # Break both loops
    done
done

# Skip iteration
for i in {1..10}; do
    [[ $((i % 2)) -eq 0 ]] && continue
    echo "$i"                          # Odd numbers only
done

# Continue in nested loop
for i in {1..3}; do
    for j in {1..3}; do
        [[ $j -eq 2 ]] && continue 2  # Skip to next i
    done
done
```

---

## ⚙️ Functions

### Defining Functions

```bash
# Standard syntax
function greet() {
    echo "Hello, $1!"
}

# POSIX syntax (preferred for portability)
greet() {
    echo "Hello, $1!"
}

# Call
greet "World"
```

### Parameters & Return Values

```bash
add() {
    local a=$1 b=$2
    echo $((a + b))
}

# Capture output
result=$(add 3 5)
echo "$result"          # => 8

# Return status code
is_even() {
    return $(( $1 % 2 ))
}

if is_even 4; then
    echo "Even"
fi

# Return via global variable
divide() {
    if [[ $2 -eq 0 ]]; then
        echo "Error: division by zero" >&2
        return 1
    fi
    RESULT=$(echo "scale=4; $1/$2" | bc)
}
```

### Local Variables & Scope

```bash
outer() {
    local x=10
    inner() {
        local y=20
        echo "inner: x=$x, y=$y"    # x is visible
    }
    inner
    echo "outer: x=$x"              # y is NOT visible
}

# Dynamic scoping
func_a() {
    local var="from A"
    func_b
}

func_b() {
    echo "$var"       # => "from A" (dynamic scoping)
}
```

### Name References (Bash 4.3+)

```bash
# Return values through reference
fill_array() {
    local -n arr_ref=$1
    arr_ref=(one two three)
}

declare -a my_array
fill_array my_array
echo "${my_array[@]}"   # => one two three
```

### Function Libraries

```bash
# library.sh
#!/bin/bash

log_info()  { echo "[INFO]  $(date '+%Y-%m-%d %H:%M:%S') $*"; }
log_warn()  { echo "[WARN]  $(date '+%Y-%m-%d %H:%M:%S') $*" >&2; }
log_error() { echo "[ERROR] $(date '+%Y-%m-%d %H:%M:%S') $*" >&2; }

die() {
    log_error "$@"
    exit 1
}

require_command() {
    command -v "$1" &>/dev/null || die "Required command not found: $1"
}

confirm() {
    local prompt="${1:-Are you sure?} [y/N] "
    read -rp "$prompt" response
    [[ "$response" =~ ^[Yy]$ ]]
}

# main.sh
source "$(dirname "$0")/library.sh"
require_command git
log_info "Starting process..."
```

### Recursion

```bash
# Factorial
factorial() {
    if [[ $1 -le 1 ]]; then
        echo 1
    else
        local prev=$(factorial $(($1 - 1)))
        echo $(($1 * prev))
    fi
}
echo $(factorial 5)     # => 120

# Directory tree walk
walk_tree() {
    local dir="$1" indent="${2:-}"
    for entry in "$dir"/*; do
        [[ -e "$entry" ]] || continue
        echo "${indent}$(basename "$entry")"
        [[ -d "$entry" ]] && walk_tree "$entry" "  $indent"
    done
}
walk_tree /some/path
```

### `getopts` for Option Parsing

```bash
usage() {
    echo "Usage: $0 [-v] [-n name] [-o output] file ..."
    exit 1
}

verbose=false
name=""
output=""

while getopts ":vn:o:h" opt; do
    case $opt in
        v) verbose=true ;;
        n) name="$OPTARG" ;;
        o) output="$OPTARG" ;;
        h) usage ;;
        \?) echo "Invalid option: -$OPTARG" >&2; usage ;;
        :)  echo "Option -$OPTARG requires an argument" >&2; usage ;;
    esac
done
shift $((OPTIND - 1))

# Remaining arguments in $@
echo "Files: $@"
```

### Long Option Parsing

```bash
while [[ $# -gt 0 ]]; do
    case "$1" in
        -v|--verbose)  verbose=true; shift ;;
        -n|--name)     name="$2"; shift 2 ;;
        -o|--output)   output="$2"; shift 2 ;;
        --name=*)      name="${1#*=}"; shift ;;
        --output=*)    output="${1#*=}"; shift ;;
        -h|--help)     usage ;;
        --)            shift; break ;;
        -*)            echo "Unknown option: $1" >&2; usage ;;
        *)             break ;;
    esac
done
```

---

## 📤 Input / Output & Redirection

### Standard Streams

| FD | Name | Description |
|----|------|-------------|
| 0 | stdin | Standard input |
| 1 | stdout | Standard output |
| 2 | stderr | Standard error |

### Output Redirection

```bash
# Redirect stdout to file (overwrite)
command > file.txt

# Redirect stdout to file (append)
command >> file.txt

# Redirect stderr to file
command 2> error.log

# Redirect stderr to file (append)
command 2>> error.log

# Redirect both stdout and stderr to file
command > file.txt 2>&1
command &> file.txt           # Shorthand
command &>> file.txt          # Append shorthand

# Redirect stdout and stderr separately
command > out.txt 2> err.txt

# Suppress all output
command &>/dev/null

# Suppress stderr only
command 2>/dev/null

# Redirect to /dev/null (discard)
command > /dev/null
```

### Input Redirection

```bash
# Read from file
command < file.txt

# Read from string (herestring)
command <<< "input string"

# Combine
command < input.txt > output.txt 2> error.log
```

### File Descriptors

```bash
# Open file for reading on FD 3
exec 3< file.txt
read -r line <&3
exec 3<&-               # Close FD 3

# Open file for writing on FD 4
exec 4> output.txt
echo "data" >&4
exec 4>&-               # Close FD 4

# Open file for read/write on FD 5
exec 5<> file.txt
read -r line <&5
echo "new data" >&5
exec 5>&-

# Duplicate FDs
exec 3>&1               # FD 3 = copy of stdout
exec 1>file.txt          # Redirect stdout to file
echo "goes to file"
exec 1>&3                # Restore stdout
exec 3>&-                # Close FD 3

# Swap stdout and stderr
command 3>&1 1>&2 2>&3 3>&-
```

### `read` Command

```bash
# Basic read
read -r answer
echo "You said: $answer"

# With prompt
read -rp "Enter name: " name

# Silent input (passwords)
read -rsp "Password: " pass; echo

# Read with timeout
read -rt 5 -p "Quick! " answer

# Read N characters
read -rn 1 -p "Press any key..."

# Read into array
read -ra arr <<< "one two three"

# Read with custom delimiter
read -rd '' content < file.txt    # Read entire file

# Read specific number of chars
read -rN 10 chunk < file.txt

# Default variable ($REPLY)
read -rp "Input: "
echo "$REPLY"
```

### `echo` vs `printf`

```bash
# echo — simple output
echo "Hello World"
echo -n "No newline"          # No trailing newline
echo -e "Tab\there"           # Interpret escapes
echo -E "No \t escapes"      # Disable escapes (default in bash)

# printf — formatted output (preferred)
printf "%s is %d years old\n" "Alice" 30
printf "%.2f\n" 3.14159
printf "%05d\n" 42            # => 00042
printf "%b\n" "Tab\there"    # Process backslash escapes in args
```

---

## 🔗 Pipes & Process Substitution

### Pipes

```bash
# Basic pipe
ls -la | grep ".txt"

# Multiple pipes
cat file.txt | sort | uniq -c | sort -rn

# Pipe with tee (write to file AND stdout)
command | tee output.txt
command | tee -a output.txt      # Append

# Pipe stderr
command 2>&1 | grep "error"
command |& grep "error"          # Shorthand (Bash 4+)

# Named pipe (FIFO)
mkfifo /tmp/mypipe
command1 > /tmp/mypipe &
command2 < /tmp/mypipe
rm /tmp/mypipe

# Check pipe status (all commands in pipe)
ls | grep foo | wc -l
echo "${PIPESTATUS[@]}"          # e.g., "0 1 0"
```

### Process Substitution

```bash
# Treat command output as a file
diff <(ls dir1) <(ls dir2)

# Treat input as a file
command > >(tee log.txt)

# Compare sorted files without temp files
diff <(sort file1.txt) <(sort file2.txt)

# Feed multiple commands' output
paste <(cut -f1 data.txt) <(cut -f3 data.txt)

# Write to multiple commands
echo "data" | tee >(cmd1) >(cmd2) > /dev/null

# While loop without subshell
while IFS= read -r line; do
    # Variables set here survive the loop
    count=$((count + 1))
done < <(some_command)
echo "$count"
```

### `xargs`

```bash
# Basic usage
find . -name "*.txt" | xargs rm

# With placeholder
find . -name "*.log" | xargs -I{} mv {} {}.bak

# Parallel execution
find . -name "*.jpg" | xargs -P4 -I{} convert {} {}.png

# Handle spaces in filenames
find . -name "*.txt" -print0 | xargs -0 rm

# Limit arguments per command
echo {1..100} | xargs -n 10

# Prompt before execution
find . -name "*.tmp" | xargs -p rm

# With custom delimiter
echo "a:b:c:d" | xargs -d: echo

# From file
xargs -a file_list.txt rm
```

---

## 🎭 Pattern Matching & Globbing

### Basic Globs

```bash
*           # Match any string (including empty)
?           # Match any single character
[abc]       # Match any character in set
[a-z]       # Match any character in range
[!abc]      # Match any character NOT in set
[^abc]      # Same as above (alternate syntax)
```

### Extended Globs (`shopt -s extglob`)

```bash
shopt -s extglob

?(pattern)   # Zero or one occurrence
*(pattern)   # Zero or more occurrences
+(pattern)   # One or more occurrences
@(pattern)   # Exactly one occurrence
!(pattern)   # Anything except the pattern

# Examples
ls *.@(jpg|png|gif)      # All image files
rm !(*.txt)              # Remove all except .txt files
ls ?(a)b                 # b or ab
ls *(.[0-9])             # Files like .1, .2, .12
ls +([0-9])              # One or more digits
```

### Globbing Options

```bash
shopt -s nullglob        # Unmatched globs expand to nothing
shopt -s failglob        # Unmatched globs cause error
shopt -s dotglob         # Include hidden files in globs
shopt -s nocaseglob      # Case-insensitive globs
shopt -s globstar        # ** matches directories recursively
shopt -s extglob         # Enable extended pattern matching

# Recursive glob (Bash 4+)
shopt -s globstar
ls **/*.txt              # All .txt files recursively

# Example with nullglob
shopt -s nullglob
files=(*.xyz)
echo "${#files[@]}"      # 0 if no match (instead of literal *.xyz)
```

### Brace Expansion

```bash
echo {A,B,C}             # => A B C
echo {1..5}              # => 1 2 3 4 5
echo {a..z}              # => a b c ... z
echo {01..12}            # => 01 02 03 ... 12 (zero-padded)
echo {1..20..2}          # => 1 3 5 7 ... 19 (step)
echo file{1..3}.txt      # => file1.txt file2.txt file3.txt
echo {A,B}{1,2}          # => A1 A2 B1 B2 (cartesian product)
mkdir -p project/{src,lib,test,docs}/{main,util}
```

### Tilde Expansion

```bash
~               # $HOME
~user           # Home directory of user
~+              # $PWD
~-              # $OLDPWD
```

---

## 🔍 Regular Expressions

### Bash Regex Matching

```bash
# Using [[ =~ ]]
if [[ "Hello123" =~ ^[A-Za-z]+[0-9]+$ ]]; then
    echo "Match!"
fi

# Capture groups
if [[ "2026-02-20" =~ ^([0-9]{4})-([0-9]{2})-([0-9]{2})$ ]]; then
    echo "Year:  ${BASH_REMATCH[0]}"   # Full match
    echo "Year:  ${BASH_REMATCH[1]}"   # 2026
    echo "Month: ${BASH_REMATCH[2]}"   # 02
    echo "Day:   ${BASH_REMATCH[3]}"   # 20
fi

# Store regex in variable (avoid quoting issues)
re='^[0-9]+$'
if [[ "$input" =~ $re ]]; then
    echo "Is a number"
fi
```

### Common Regex Patterns

```bash
# Email (basic)
'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

# IP Address
'^([0-9]{1,3}\.){3}[0-9]{1,3}$'

# URL
'^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$'

# Date (YYYY-MM-DD)
'^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$'

# Integer
'^-?[0-9]+$'

# Float
'^-?[0-9]*\.?[0-9]+$'

# Hex color
'^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$'

# MAC address
'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$'

# Alphanumeric only
'^[a-zA-Z0-9]+$'
```

---

## 📜 Command History & Expansion

### History Commands

```bash
history                  # Show all history
history 20               # Show last 20 commands
history -c               # Clear history
history -d 42            # Delete entry 42
history -a               # Append session history to file
history -r               # Read history file
history -w               # Write history to file
```

### History Expansion (Event Designators)

```bash
!!                       # Last command
!n                       # Command number n
!-n                      # n-th most recent command
!string                  # Most recent starting with string
!?string?                # Most recent containing string
^old^new                 # Repeat last, replacing old with new
^old^new^:G              # Replace all occurrences
```

### Word Designators

```bash
!!:0                     # Command name of last command
!!:1                     # First argument
!!:$                     # Last argument (same as !$)
!!:^                     # First argument (same as !^)
!!:n                     # n-th argument
!!:n-m                   # Arguments n through m
!!:n-$                   # Arguments n through last
!!:*                     # All arguments (same as !*)
```

### Modifiers

```bash
!!:h                     # Remove trailing filename (head/dirname)
!!:t                     # Remove leading path (tail/basename)
!!:r                     # Remove trailing suffix (.ext)
!!:e                     # Remove all but suffix
!!:p                     # Print without executing
!!:s/old/new/            # Substitute first
!!:gs/old/new/           # Substitute all (global)
!!:q                     # Quote the expansion
!!:x                     # Quote, breaking into words
```

### Practical History Examples

```bash
# Run previous command with sudo
sudo !!

# Use last argument of previous command
cd !$
mkdir !$ && cd !$

# Fix typo in last command
^typo^fixed

# Use all arguments from previous command
echo !*

# Show what would execute without running
!42:p
```

### History Configuration

```bash
# In ~/.bashrc
export HISTSIZE=10000            # Commands in memory
export HISTFILESIZE=20000        # Commands in file
export HISTCONTROL=ignoreboth    # Ignore dupes & leading spaces
export HISTIGNORE="ls:cd:exit"   # Don't record these
export HISTTIMEFORMAT="%F %T "   # Timestamp format
shopt -s histappend              # Append, don't overwrite
shopt -s histverify              # Show before executing
PROMPT_COMMAND='history -a'      # Save after each command
```

---

## 🏭 Job Control & Process Management

### Job Control

```bash
# Run in background
command &

# List jobs
jobs
jobs -l             # With PIDs
jobs -r             # Running only
jobs -s             # Stopped only

# Bring to foreground
fg                  # Most recent job
fg %1               # Job number 1
fg %string          # Job whose name starts with string

# Send to background
bg                  # Most recent job
bg %1               # Job number 1

# Suspend foreground process
# Ctrl+Z

# Wait for background jobs
wait                # Wait for all
wait %1             # Wait for job 1
wait $pid           # Wait for specific PID

# Disown (prevent SIGHUP on logout)
disown              # Most recent job
disown %1           # Job 1
disown -a           # All jobs
disown -h %1        # Don't kill on logout but keep in job table
```

### Process Commands

```bash
# View processes
ps                   # Current terminal
ps aux               # All processes (BSD style)
ps -ef               # All processes (System V style)
ps -ejH              # Process tree
ps axo pid,ppid,cmd  # Custom columns

# Real-time process viewer
top
htop                 # Interactive (if installed)

# Find process by name
pgrep process_name
pgrep -u root        # By user
pgrep -f "pattern"   # Match full command line
pidof process_name

# Kill processes
kill PID              # Send SIGTERM
kill -9 PID           # Send SIGKILL (force)
kill -STOP PID        # Pause process
kill -CONT PID        # Resume process
kill -HUP PID         # Hangup (reload config)
kill -USR1 PID        # User-defined signal 1
kill -0 PID           # Check if process exists

# Kill by name
killall process_name
pkill process_name
pkill -f "pattern"

# List all signals
kill -l

# Process niceness
nice -n 10 command    # Start with lower priority
renice 15 -p PID      # Change priority of running process

# Run immune to hangups
nohup command &
nohup command > output.log 2>&1 &

# Limit runtime
timeout 30 command    # Kill after 30 seconds
timeout -s KILL 60 command
```

### Background Process Patterns

```bash
# Start, capture PID, wait
cmd &
pid=$!
wait $pid
echo "Exit status: $?"

# Multiple background processes
for f in *.dat; do
    process "$f" &
done
wait                  # Wait for all to finish

# Parallel with limit
max_jobs=4
for f in *.dat; do
    while [[ $(jobs -r | wc -l) -ge $max_jobs ]]; do
        sleep 0.1
    done
    process "$f" &
done
wait
```

---

## 🪤 Signal Handling & Traps

### Common Signals

| Signal | Number | Description |
|--------|--------|-------------|
| `SIGHUP` | 1 | Hangup / terminal closed |
| `SIGINT` | 2 | Interrupt (Ctrl+C) |
| `SIGQUIT` | 3 | Quit (Ctrl+\) |
| `SIGKILL` | 9 | Kill (cannot be caught) |
| `SIGTERM` | 15 | Terminate (default kill) |
| `SIGSTOP` | 17/19/23 | Stop (cannot be caught) |
| `SIGTSTP` | 18/20/24 | Terminal stop (Ctrl+Z) |
| `SIGCONT` | 19/18/25 | Continue if stopped |
| `SIGUSR1` | 10/30/16 | User-defined 1 |
| `SIGUSR2` | 12/31/17 | User-defined 2 |
| `SIGCHLD` | 17/20/18 | Child process changed |
| `EXIT` | 0 | Shell exit (pseudo-signal) |
| `ERR` | — | Command returns non-zero (pseudo) |
| `DEBUG` | — | Before each command (pseudo) |
| `RETURN` | — | After function/source returns (pseudo) |

### Trap Syntax

```bash
# Set trap
trap 'commands' SIGNAL [SIGNAL...]

# Remove trap
trap - SIGNAL

# Ignore signal
trap '' SIGNAL

# Show all traps
trap -p

# Show trap for specific signal
trap -p SIGINT
```

### Trap Patterns

```bash
# Cleanup on exit
cleanup() {
    rm -f "$tmpfile"
    echo "Cleaned up"
}
trap cleanup EXIT

# Cleanup on multiple signals
trap cleanup EXIT INT TERM HUP

# Temporary file pattern
tmpfile=$(mktemp)
trap 'rm -f "$tmpfile"' EXIT

# Lock file pattern
lockfile="/tmp/myscript.lock"
trap 'rm -f "$lockfile"; exit' EXIT INT TERM
if ! mkdir "$lockfile" 2>/dev/null; then
    echo "Already running" >&2
    exit 1
fi

# Error handling
trap 'echo "Error on line $LINENO" >&2' ERR

# Debug tracing
trap 'echo "DEBUG: $BASH_COMMAND"' DEBUG

# On function return
trap 'echo "Returned from function"' RETURN

# Stack multiple handlers
on_exit() {
    for handler in "${exit_handlers[@]}"; do
        eval "$handler"
    done
}
trap on_exit EXIT

add_exit_handler() {
    exit_handlers+=("$1")
}

add_exit_handler 'echo "Handler 1"'
add_exit_handler 'rm -f /tmp/tempfile'
```

---

## 📁 File & Directory Operations

### File Operations

```bash
# Create
touch file.txt                    # Create empty / update timestamp
touch -t 202602201200 file.txt    # Set specific time
> file.txt                        # Create/truncate to empty

# Copy
cp source dest
cp -r dir1 dir2                   # Recursive
cp -a source dest                 # Archive (preserve all)
cp -i source dest                 # Interactive (prompt)
cp -u source dest                 # Only if newer
cp -v source dest                 # Verbose
cp --backup=numbered src dest     # Create numbered backups

# Move/Rename
mv old new
mv -i old new                     # Interactive
mv -n old new                     # Don't overwrite
mv -v old new                     # Verbose

# Delete
rm file.txt
rm -f file.txt                    # Force (no prompt)
rm -r directory/                  # Recursive
rm -ri directory/                 # Recursive + interactive
rm -rf directory/                 # Force recursive

# Link
ln source hardlink                # Hard link
ln -s source symlink              # Symbolic link
ln -sf source symlink             # Force overwrite existing

# Read
cat file.txt                      # Entire file
head -n 20 file.txt               # First 20 lines
head -c 100 file.txt              # First 100 bytes
tail -n 20 file.txt               # Last 20 lines
tail -f file.txt                  # Follow (live updates)
tail -F file.txt                  # Follow with retry
less file.txt                     # Paginated viewer
more file.txt                     # Simple pager

# Count
wc file.txt                       # lines, words, chars
wc -l file.txt                    # Lines only
wc -w file.txt                    # Words only
wc -c file.txt                    # Bytes
wc -m file.txt                    # Characters

# File info
file document.pdf                 # Determine type
stat file.txt                     # Detailed file info
stat -c %s file.txt               # Size in bytes (Linux)
stat -f %z file.txt               # Size in bytes (macOS)
basename /path/to/file.txt        # => file.txt
dirname /path/to/file.txt         # => /path/to
realpath file.txt                 # Absolute path
readlink -f symlink               # Resolve symlink
```

### Directory Operations

```bash
# Create
mkdir dirname
mkdir -p path/to/nested/dirs      # Create parents
mkdir -m 755 dirname              # With permissions

# Remove
rmdir dirname                     # Empty only
rm -rf dirname                    # Non-empty

# Navigate
cd /absolute/path
cd relative/path
cd ~                              # Home
cd -                              # Previous directory
cd ..                             # Parent
cd ../..                          # Grandparent

# Directory stack
pushd /some/path                  # Push and cd
popd                              # Pop and cd back
dirs                              # Show stack
dirs -v                           # Numbered stack

# List
ls                                # Basic listing
ls -la                            # Long format, hidden files
ls -lh                            # Human-readable sizes
ls -lS                            # Sort by size
ls -lt                            # Sort by time
ls -lR                            # Recursive
ls -1                             # One per line
ls -d */                          # Directories only
ls -i                             # Show inodes

# Tree view
tree                              # Full tree
tree -L 2                         # Depth limit
tree -d                           # Directories only
tree -a                           # Include hidden
tree -I 'node_modules|.git'      # Exclude patterns
```

### Temporary Files & Directories

```bash
# Create temp file
tmpfile=$(mktemp)
tmpfile=$(mktemp /tmp/myapp.XXXXXX)

# Create temp directory
tmpdir=$(mktemp -d)
tmpdir=$(mktemp -d /tmp/myapp.XXXXXX)

# Auto-cleanup
tmpfile=$(mktemp)
trap 'rm -f "$tmpfile"' EXIT
echo "data" > "$tmpfile"

# Temp dir with auto-cleanup
tmpdir=$(mktemp -d)
trap 'rm -rf "$tmpdir"' EXIT
```

---

## 🔐 File Permissions & Ownership

### `chmod` — Change Permissions

```bash
# Symbolic mode
chmod u+x file              # User: add execute
chmod g-w file              # Group: remove write
chmod o=r file              # Others: set to read only
chmod a+r file              # All: add read
chmod u+rwx,g+rx,o+r file   # Multiple

# Numeric mode (octal)
chmod 755 file              # rwxr-xr-x
chmod 644 file              # rw-r--r--
chmod 700 file              # rwx------
chmod 600 file              # rw-------
chmod 777 file              # rwxrwxrwx

# Recursive
chmod -R 755 directory/

# Special permissions
chmod u+s file              # Set-UID
chmod g+s directory         # Set-GID
chmod +t directory          # Sticky bit
chmod 4755 file             # Set-UID + 755
chmod 2755 dir              # Set-GID + 755
chmod 1755 dir              # Sticky + 755

# Reference another file
chmod --reference=ref_file target_file
```

### Permission Bits

| Octal | Binary | Permission |
|-------|--------|------------|
| 0 | 000 | `---` |
| 1 | 001 | `--x` |
| 2 | 010 | `-w-` |
| 3 | 011 | `-wx` |
| 4 | 100 | `r--` |
| 5 | 101 | `r-x` |
| 6 | 110 | `rw-` |
| 7 | 111 | `rwx` |

### `chown` — Change Ownership

```bash
chown user file
chown user:group file
chown :group file               # Group only
chown -R user:group directory/  # Recursive
chown --reference=ref target    # Copy ownership
```

### `chgrp` — Change Group

```bash
chgrp group file
chgrp -R group directory/
```

### `umask` — Default Permissions

```bash
umask                  # Show current mask
umask 022              # Default: files=644, dirs=755
umask 077              # Private: files=600, dirs=700
umask -S               # Show in symbolic form
```

### Access Control Lists (ACL)

```bash
# View ACLs
getfacl file

# Set ACL
setfacl -m u:user:rwx file
setfacl -m g:group:rx file
setfacl -m o::r file

# Default ACL (for new files in directory)
setfacl -d -m u:user:rwx directory/

# Remove ACL
setfacl -x u:user file
setfacl -b file              # Remove all ACLs

# Recursive
setfacl -R -m u:user:rx directory/
```

---

## 📝 Text Processing Commands

### `grep` — Search Text

```bash
# Basic search
grep "pattern" file

# Common options
grep -i "pattern" file           # Case insensitive
grep -v "pattern" file           # Invert match
grep -c "pattern" file           # Count matches
grep -n "pattern" file           # Show line numbers
grep -l "pattern" files*         # Show filenames only
grep -L "pattern" files*         # Files without match
grep -w "word" file              # Whole word match
grep -x "line" file              # Whole line match
grep -r "pattern" directory/     # Recursive
grep -rn "pattern" .             # Recursive with line numbers
grep -A3 "pattern" file          # 3 lines after
grep -B3 "pattern" file          # 3 lines before
grep -C3 "pattern" file          # 3 lines context (before+after)
grep -o "pattern" file           # Only matching part
grep -P "pattern" file           # Perl regex (GNU grep)
grep -E "pattern" file           # Extended regex (same as egrep)
grep -F "string" file            # Fixed string (same as fgrep)
grep -q "pattern" file           # Quiet (exit status only)
grep --include="*.py" -r "def"   # Filter files
grep --exclude="*.log" -r "err"  # Exclude files
grep --exclude-dir=".git" -r "x" # Exclude directories
grep -m5 "pattern" file          # Max 5 matches
grep -h "pattern" files*         # No filename prefix
grep -H "pattern" file           # Always show filename

# Multiple patterns
grep -e "pat1" -e "pat2" file
grep "pat1\|pat2" file
egrep "pat1|pat2" file
```

### `sed` — Stream Editor

```bash
# Substitute (first occurrence)
sed 's/old/new/' file

# Substitute all occurrences
sed 's/old/new/g' file

# Substitute in-place
sed -i 's/old/new/g' file
sed -i.bak 's/old/new/g' file    # With backup

# Case-insensitive substitute
sed 's/old/new/gi' file

# Delete lines
sed '5d' file                    # Delete line 5
sed '3,7d' file                  # Delete lines 3-7
sed '/pattern/d' file            # Delete matching lines
sed '/^$/d' file                 # Delete empty lines
sed '/^#/d' file                 # Delete comment lines

# Print specific lines
sed -n '5p' file                 # Print line 5
sed -n '3,7p' file              # Print lines 3-7
sed -n '/pattern/p' file        # Print matching lines

# Insert/append
sed '3i\new line' file           # Insert before line 3
sed '3a\new line' file           # Append after line 3
sed '1i\header' file             # Add header

# Replace line
sed '3c\replacement line' file

# Multiple commands
sed -e 's/a/b/' -e 's/c/d/' file
sed 's/a/b/; s/c/d/' file

# Address ranges
sed '10,20s/old/new/g' file     # Lines 10-20
sed '/start/,/end/s/old/new/g' file  # Between patterns

# Back-references
sed 's/\(foo\)bar/\1baz/' file  # foobar -> foobaz
sed -E 's/(foo)bar/\1baz/' file  # Extended regex

# Translate characters (like tr)
sed 'y/abc/ABC/' file

# Print line count
sed -n '$=' file

# Remove trailing whitespace
sed 's/[[:space:]]*$//' file

# Add prefix/suffix to lines
sed 's/^/PREFIX: /' file
sed 's/$/ :SUFFIX/' file
```

### `awk` — Pattern Scanning & Processing

```bash
# Basic syntax: awk 'pattern {action}' file

# Print specific columns
awk '{print $1, $3}' file       # Columns 1 and 3
awk '{print $NF}' file          # Last column
awk '{print $(NF-1)}' file      # Second to last

# With custom delimiter
awk -F: '{print $1}' /etc/passwd
awk -F, '{print $2}' data.csv

# Pattern matching
awk '/pattern/ {print}' file
awk '$3 > 100 {print $1, $3}' file
awk 'NR>=10 && NR<=20' file     # Lines 10-20

# Built-in variables
# NR    = Current record (line) number
# NF    = Number of fields in current record
# FS    = Field separator (default: whitespace)
# RS    = Record separator (default: newline)
# OFS   = Output field separator
# ORS   = Output record separator
# FILENAME = Current filename

# BEGIN and END blocks
awk 'BEGIN {print "Header"} {print $0} END {print "Footer"}' file

# Sum a column
awk '{sum += $3} END {print sum}' file

# Count lines matching pattern
awk '/error/ {count++} END {print count}' file

# Average
awk '{sum += $1; n++} END {print sum/n}' file

# Min / Max
awk 'BEGIN {max=0} $1>max {max=$1} END {print max}' file

# Conditional formatting
awk '{if ($3 > 100) print $1, "HIGH"; else print $1, "LOW"}' file

# String functions
awk '{print length($0)}' file            # Line length
awk '{print toupper($1)}' file           # Uppercase
awk '{print tolower($0)}' file           # Lowercase
awk '{gsub(/old/, "new"); print}' file   # Global replace
awk '{sub(/old/, "new"); print}' file    # First replace
awk '{print substr($0, 1, 10)}' file     # Substring

# Multiple rules
awk '
    /^#/ { next }
    NF == 0 { next }
    { sum += $1 }
    END { print "Total:", sum }
' file

# Set output separator
awk -F: 'BEGIN {OFS=","} {print $1, $3, $7}' /etc/passwd

# Associative arrays in awk
awk '{count[$1]++} END {for (k in count) print k, count[k]}' file

# Two-file processing
awk 'NR==FNR {a[$1]=$2; next} $1 in a {print $1, a[$1], $2}' file1 file2

# Print unique lines (like sort | uniq)
awk '!seen[$0]++' file

# CSV processing
awk -F'","' '{gsub(/"/, ""); print $2}' file.csv
```

### `sort`

```bash
sort file                    # Alphabetical sort
sort -n file                 # Numeric sort
sort -r file                 # Reverse sort
sort -u file                 # Unique lines
sort -k2 file                # Sort by column 2
sort -k2,2n file             # Numeric sort by column 2
sort -t: -k3 -n /etc/passwd  # Custom delimiter, sort by field 3
sort -h file                 # Human-readable sizes (1K, 2M)
sort -M file                 # Month sort (Jan, Feb, ...)
sort -V file                 # Version sort (1.0, 1.1, 1.10)
sort -f file                 # Case insensitive
sort -R file                 # Random order (shuffle)
sort -s file                 # Stable sort
sort -o output file          # Output to file (can be same as input)
sort -z file                 # Null-terminated lines
sort -c file                 # Check if sorted
```

### `cut`, `paste`, `join`

```bash
# cut — extract columns
cut -d: -f1 /etc/passwd          # Field 1, delimiter :
cut -d, -f2,4 data.csv           # Fields 2 and 4
cut -c1-10 file                  # Characters 1-10
cut -c5- file                    # From character 5 to end
cut --complement -d: -f2 file    # All except field 2

# paste — merge lines
paste file1 file2                # Side by side (tab-separated)
paste -d, file1 file2            # Comma-separated
paste -s file                    # Serial (all on one line)
paste -d'\n' file1 file2         # Interleave

# join — join files on common field
join file1 file2                 # Join on first field
join -1 2 -2 1 file1 file2      # Join field 2 of file1 with field 1 of file2
join -t: file1 file2             # Custom delimiter
join -a1 file1 file2             # Show unmatched from file1
join -v1 file1 file2             # Only unmatched from file1
```

### `uniq`, `tr`, `column`

```bash
# uniq — filter adjacent duplicates (sort first!)
sort file | uniq                 # Remove duplicates
sort file | uniq -c              # Count occurrences
sort file | uniq -d              # Show only duplicates
sort file | uniq -u              # Show only unique lines
sort file | uniq -i              # Case insensitive

# tr — translate/delete characters
tr 'a-z' 'A-Z' < file           # Lowercase to uppercase
tr '[:lower:]' '[:upper:]' < f   # Same, POSIX
tr -d '0-9' < file               # Delete all digits
tr -s ' ' < file                 # Squeeze repeated spaces
tr '\n' ' ' < file               # Join lines with spaces
tr -dc 'a-zA-Z0-9' < /dev/urandom | head -c 32  # Random string
tr ',' '\t' < file               # CSV to TSV

# column — format into columns
column -t file                   # Auto-align columns
column -t -s: file               # Custom separator
column -s, -t data.csv           # Format CSV as table
```

### `diff` & `patch`

```bash
# diff
diff file1 file2                 # Compare files
diff -u file1 file2              # Unified format
diff -y file1 file2              # Side by side
diff -w file1 file2              # Ignore whitespace
diff -r dir1 dir2                # Recursive directory diff
diff --color file1 file2         # Colored output
diff -q file1 file2              # Report only if different

# Create and apply patches
diff -u original modified > changes.patch
patch < changes.patch
patch original < changes.patch
patch -R < changes.patch         # Reverse patch
```

---

## 🔎 Search & Find

### `find`

```bash
# By name
find . -name "*.txt"             # Case sensitive
find . -iname "*.txt"            # Case insensitive
find . -not -name "*.log"        # Exclude pattern

# By type
find . -type f                   # Files only
find . -type d                   # Directories only
find . -type l                   # Symbolic links
find . -type f -name "*.sh"      # Combine

# By size
find . -size +10M                # Larger than 10MB
find . -size -1k                 # Smaller than 1KB
find . -size 0                   # Empty files
find . -empty                    # Empty files and dirs

# By time
find . -mtime -7                 # Modified in last 7 days
find . -mtime +30                # Modified more than 30 days ago
find . -mmin -60                 # Modified in last 60 minutes
find . -atime -1                 # Accessed in last day
find . -ctime -1                 # Changed in last day
find . -newer reference_file     # Newer than reference

# By permissions
find . -perm 755                 # Exact permissions
find . -perm -644                # At least these permissions
find . -perm /u+x                # Any with user execute
find . -executable               # Executable files

# By user/group
find . -user username
find . -group groupname
find . -uid 1000
find . -nouser                   # No matching user

# Depth control
find . -maxdepth 2 -name "*.txt"
find . -mindepth 1 -maxdepth 3

# Action: execute command
find . -name "*.log" -exec rm {} \;
find . -name "*.txt" -exec grep -l "word" {} \;
find . -name "*.sh" -exec chmod +x {} +     # Batch mode

# Action: print
find . -name "*.txt" -print
find . -name "*.txt" -print0     # Null-terminated

# Action: delete
find . -name "*.tmp" -delete

# Logical operators
find . \( -name "*.txt" -o -name "*.md" \)
find . -name "*.log" -a -size +1M
find . -not -name "*.txt"
find . ! -name "*.txt"           # Same as above

# Practical examples
find . -type f -name "*.py" -newer setup.py
find /var/log -type f -size +100M
find . -type f -mtime +90 -delete
find . -type d -empty -delete
find . -type f -exec file {} \; | grep "text"
```

### `locate` & `updatedb`

```bash
locate filename              # Fast file search (uses database)
locate -i filename           # Case insensitive
locate -c filename           # Count matches
locate -l 10 filename        # Limit results
sudo updatedb                # Update file database
```

### `which`, `whereis`, `type`

```bash
which command                # Path to command
which -a command             # All paths
whereis command              # Binary, source, man page
type command                 # How shell interprets name
type -a command              # All interpretations
command -v command           # POSIX way to check existence
hash -r                      # Clear command hash cache
```

---

## 📦 Archiving & Compression

### `tar`

```bash
# Create archive
tar cf archive.tar files/
tar czf archive.tar.gz files/     # gzip
tar cjf archive.tar.bz2 files/   # bzip2
tar cJf archive.tar.xz files/    # xz
tar cvf archive.tar files/       # Verbose

# Extract
tar xf archive.tar
tar xzf archive.tar.gz
tar xjf archive.tar.bz2
tar xJf archive.tar.xz
tar xf archive.tar -C /dest/     # Extract to directory
tar xf archive.tar file.txt      # Extract specific file

# List contents
tar tf archive.tar
tar tzf archive.tar.gz

# Append to archive
tar rf archive.tar newfile

# Exclude patterns
tar czf archive.tar.gz --exclude='*.log' --exclude='.git' dir/
tar czf archive.tar.gz --exclude-vcs dir/

# Incremental backup
tar czf backup-$(date +%F).tar.gz --newer-mtime="2026-01-01" dir/

# Preserve permissions
tar cpzf archive.tar.gz dir/
```

### Individual Compression Tools

```bash
# gzip
gzip file                    # Compress (replaces original)
gzip -k file                 # Keep original
gzip -d file.gz              # Decompress
gunzip file.gz               # Decompress
gzip -9 file                 # Max compression
gzip -1 file                 # Fast compression
zcat file.gz                 # View without decompressing

# bzip2
bzip2 file
bzip2 -d file.bz2
bunzip2 file.bz2
bzcat file.bz2

# xz
xz file
xz -d file.xz
unxz file.xz
xzcat file.xz

# zip/unzip
zip archive.zip files
zip -r archive.zip directory/
zip -e archive.zip files     # Encrypted
unzip archive.zip
unzip archive.zip -d dest/
unzip -l archive.zip         # List contents

# zstd (if available)
zstd file
zstd -d file.zst
zstdcat file.zst
```

---

## 🌐 Networking Commands

### Connectivity & DNS

```bash
# Ping
ping host
ping -c 4 host                # 4 packets
ping -i 0.5 host              # 0.5 second interval

# DNS lookup
host domain.com
dig domain.com
dig domain.com MX             # MX records
dig +short domain.com
nslookup domain.com

# Traceroute
traceroute host
tracepath host

# Network interfaces
ifconfig                       # (deprecated on Linux)
ip addr show                   # Linux
ip link show
ip route show

# Hostname
hostname
hostname -I                    # All IP addresses
```

### Data Transfer

```bash
# curl
curl https://example.com
curl -o file.html https://example.com
curl -O https://example.com/file.tar.gz
curl -L https://example.com             # Follow redirects
curl -s https://api.example.com         # Silent
curl -I https://example.com             # Headers only
curl -X POST -d "key=value" URL
curl -X POST -H "Content-Type: application/json" -d '{"key":"val"}' URL
curl -u user:pass URL                    # Basic auth
curl -k https://self-signed.example.com  # Skip SSL
curl -w "%{http_code}" URL              # Show HTTP code
curl --retry 3 URL                       # Retry
curl -F "file=@upload.txt" URL           # Upload file

# wget
wget https://example.com/file
wget -O output_name URL
wget -q URL                              # Quiet
wget -r URL                              # Recursive
wget -c URL                              # Continue/resume
wget --mirror URL                        # Mirror site
wget -i url_list.txt                     # From file
wget --limit-rate=200k URL              # Throttle

# scp (secure copy)
scp file user@host:/path
scp user@host:/path/file .
scp -r dir user@host:/path
scp -P 2222 file user@host:/path        # Custom port

# rsync
rsync -av src/ dest/
rsync -av src/ user@host:/dest/
rsync -avz src/ user@host:/dest/        # With compression
rsync -av --delete src/ dest/            # Mirror (delete extra)
rsync -av --exclude='*.log' src/ dest/
rsync -avn src/ dest/                    # Dry run
rsync -avP src/ dest/                    # Progress + partial

# sftp
sftp user@host
# Interactive commands: ls, cd, get, put, rm, mkdir, etc.
```

### SSH

```bash
# Connect
ssh user@host
ssh -p 2222 user@host                   # Custom port
ssh -i ~/.ssh/key.pem user@host         # Identity file

# Execute remote command
ssh user@host 'ls -la'
ssh user@host 'cat /etc/hostname; uptime'

# Port forwarding
ssh -L 8080:localhost:80 user@host      # Local port forward
ssh -R 9090:localhost:3000 user@host    # Remote port forward
ssh -D 1080 user@host                   # SOCKS proxy

# SSH tunnel in background
ssh -fN -L 8080:localhost:80 user@host

# Key management
ssh-keygen -t ed25519 -C "email"
ssh-copy-id user@host
ssh-agent bash
ssh-add ~/.ssh/id_ed25519

# Config file (~/.ssh/config)
# Host myserver
#   HostName 192.168.1.100
#   User admin
#   Port 2222
#   IdentityFile ~/.ssh/mykey
```

### Network Utilities

```bash
# Ports
ss -tlnp                    # TCP listening ports (Linux)
netstat -tlnp                # Older alternative
lsof -i :8080               # What's using port 8080
lsof -i TCP                 # All TCP connections

# Firewall (Linux)
sudo iptables -L             # List rules
sudo ufw status              # UFW status
sudo ufw allow 22            # Allow SSH
sudo ufw enable              # Enable firewall

# Network monitoring
netstat -an                  # All connections
ss -s                        # Socket statistics
nmap host                    # Port scan
nc -zv host 80               # Test port connectivity
nc -l 1234                   # Listen on port
```

---

## 💻 System Information & Monitoring

### System Info

```bash
uname -a                     # Full system info
uname -r                     # Kernel version
uname -m                     # Machine architecture
hostnamectl                  # System details (systemd)
lsb_release -a               # Distribution info (Linux)
cat /etc/os-release          # OS information
cat /proc/version            # Kernel version

# Hardware
lscpu                        # CPU info
cat /proc/cpuinfo            # Detailed CPU
free -h                      # Memory usage
cat /proc/meminfo            # Detailed memory
lsblk                        # Block devices
lspci                        # PCI devices
lsusb                        # USB devices
dmidecode                    # BIOS/hardware info

# macOS equivalents
sw_vers                      # macOS version
system_profiler              # Detailed hardware
sysctl -n machdep.cpu.brand_string  # CPU
```

### Process Monitoring

```bash
# top/htop
top                          # Real-time processes
top -o %MEM                  # Sort by memory
htop                         # Interactive top

# Process listing
ps aux                       # All processes
ps auxf                      # Process tree
ps -eo pid,ppid,%cpu,%mem,comm --sort=-%cpu | head
pstree                       # Process tree view

# System uptime
uptime
w                            # Who + uptime + load

# System load
cat /proc/loadavg

# Memory
free -h
vmstat 1 5                   # Virtual memory stats (5 seconds)

# I/O
iostat 1 5                   # I/O stats
iotop                        # I/O by process

# File access
strace -p PID                # Trace system calls
ltrace command               # Trace library calls
```

### Resource Monitoring

```bash
# Watch command (repeat periodically)
watch -n 2 'free -h'         # Every 2 seconds
watch -d 'ls -la'            # Highlight changes
watch -n1 "ps aux | grep nginx"

# Real-time log monitoring
tail -f /var/log/syslog
journalctl -f                # systemd journal
journalctl -u service_name -f

# System activity
sar -u 1 5                   # CPU (5 reports, 1 second)
sar -r 1 5                   # Memory
sar -d 1 5                   # Disk
dstat                        # Combined stats

# Resource limits
ulimit -a                    # Show all limits
ulimit -n                    # Open files limit
ulimit -n 65536              # Set open files limit
```

---

## 👤 User & Group Management

```bash
# User info
whoami                       # Current user
id                           # User ID, groups
id username                  # Specific user
who                          # Logged in users
w                            # Who + activity
last                         # Login history
lastlog                      # Last login per user
finger username              # User info (if installed)

# User management (requires root)
useradd username
useradd -m -s /bin/bash username   # With home dir, shell
userdel username
userdel -r username                # Remove with home dir
usermod -aG group username         # Add to group
usermod -s /bin/zsh username       # Change shell
passwd username                    # Set password
chage -l username                  # Password aging info

# Group management
groups                        # Current user's groups
groups username               # User's groups
groupadd groupname
groupdel groupname
groupmod -n newname oldname

# Switch user
su - username                # Login shell
sudo command                 # Run as root
sudo -u user command         # Run as another user
sudo -i                      # Root login shell
sudo -s                      # Root shell
visudo                       # Edit sudoers safely

# /etc/passwd format:
# username:x:UID:GID:comment:home:shell

# /etc/group format:
# groupname:x:GID:member1,member2
```

---

## 💾 Disk & Filesystem

```bash
# Disk usage
df -h                        # Filesystem usage (human)
df -i                        # Inode usage
du -sh directory/             # Directory size
du -h --max-depth=1 .        # Sizes one level deep
du -ah . | sort -rh | head   # Largest files/dirs

# ncdu (interactive, if installed)
ncdu /path

# Disk partitions
fdisk -l                     # List partitions
parted -l                    # List partitions
blkid                        # Block device attributes
lsblk -f                     # Filesystems

# Mount/Unmount
mount                        # Show mounts
mount /dev/sdb1 /mnt         # Mount
umount /mnt                  # Unmount
mount -o loop image.iso /mnt # Mount ISO

# Filesystem creation
mkfs.ext4 /dev/sdb1
mkfs.xfs /dev/sdb1

# Filesystem check
fsck /dev/sdb1               # Check (unmounted)

# Swap
swapon -s                    # Show swap
free -h                      # Memory + swap

# Quotas
quota -u username
repquota /home
```

---

## 📦 Package Management

### Debian/Ubuntu (apt)

```bash
apt update                   # Update package index
apt upgrade                  # Upgrade all packages
apt install package          # Install
apt remove package           # Remove
apt purge package            # Remove + config files
apt autoremove               # Remove unused dependencies
apt search keyword           # Search
apt show package             # Package info
apt list --installed         # List installed
dpkg -i package.deb          # Install .deb file
dpkg -l                      # List installed packages
```

### Red Hat/CentOS (yum/dnf)

```bash
yum update                   # Update all
yum install package          # Install
yum remove package           # Remove
yum search keyword           # Search
yum info package             # Info
rpm -qa                      # List installed
rpm -ivh package.rpm         # Install RPM
dnf install package          # Fedora/modern RHEL
```

### macOS (Homebrew)

```bash
brew update                  # Update Homebrew
brew upgrade                 # Upgrade all packages
brew install package         # Install
brew uninstall package       # Remove
brew search keyword          # Search
brew info package            # Info
brew list                    # List installed
brew doctor                  # Check for issues
brew cleanup                 # Remove old versions
brew services list           # List services
brew services start package  # Start service
```

---

## ⚙️ Environment & Shell Configuration

### Configuration Files (Load Order)

```
Login shell:
  1. /etc/profile
  2. ~/.bash_profile (or ~/.bash_login or ~/.profile)
  3. ~/.bash_logout (on logout)

Non-login interactive:
  1. /etc/bash.bashrc (or /etc/bashrc)
  2. ~/.bashrc

Non-interactive (scripts):
  1. $BASH_ENV (if set)
```

### Aliases

```bash
# Define aliases
alias ll='ls -la'
alias la='ls -A'
alias l='ls -CF'
alias ..='cd ..'
alias ...='cd ../..'
alias grep='grep --color=auto'
alias mkdir='mkdir -p'
alias df='df -h'
alias du='du -h'
alias free='free -h'
alias ports='ss -tlnp'

# Remove alias
unalias ll

# List all aliases
alias

# Bypass alias
\ls                          # Use original ls
command ls                   # Same
```

### Shell Options (`set`)

```bash
set -e              # Exit on error (errexit)
set -u              # Error on unset variables (nounset)
set -o pipefail     # Pipe fails if any command fails
set -x              # Print commands before execution (xtrace)
set -v              # Print input lines (verbose)
set -f              # Disable globbing (noglob)
set -n              # Syntax check only (noexec)
set -o noclobber    # Prevent overwriting with >
set -o vi           # Vi-style line editing
set -o emacs        # Emacs-style line editing (default)

# Common script header
set -euo pipefail

# Unset options
set +e              # Disable errexit
set +x              # Disable xtrace
```

### Shell Options (`shopt`)

```bash
# Enable
shopt -s option

# Disable
shopt -u option

# Query
shopt option

# List all
shopt

# Useful options
shopt -s autocd          # cd by typing directory name
shopt -s cdspell         # Correct minor cd typos
shopt -s dirspell        # Correct dir names during completion
shopt -s dotglob         # Include hidden files in glob
shopt -s extglob         # Extended pattern matching
shopt -s globstar        # ** recursive matching
shopt -s histappend      # Append to history file
shopt -s nocaseglob      # Case-insensitive globbing
shopt -s nullglob        # Unmatched globs expand to nothing
shopt -s checkwinsize    # Update LINES/COLUMNS after commands
shopt -s cmdhist         # Save multi-line commands as one entry
shopt -s lithist         # Save multi-line with newlines
shopt -s progcomp        # Programmable completion
shopt -s promptvars      # Variable expansion in prompts
shopt -s sourcepath      # Use PATH for source/dot builtin
```

### Prompt Customization (`PS1`)

```bash
# Escape sequences
# \u   Username
# \h   Hostname (short)
# \H   Full hostname
# \w   Working directory
# \W   Basename of working directory
# \d   Date (Weekday Month Date)
# \t   Time (24-hour HH:MM:SS)
# \T   Time (12-hour HH:MM:SS)
# \@   Time (12-hour AM/PM)
# \A   Time (24-hour HH:MM)
# \n   Newline
# \r   Carriage return
# \s   Shell name
# \v   Bash version
# \V   Bash version + patch level
# \#   Command number
# \!   History number
# \$   # if root, $ otherwise
# \j   Number of jobs
# \[   Begin non-printing characters
# \]   End non-printing characters
# \e   Escape character

# Examples
PS1='\u@\h:\w\$ '                    # user@host:~/dir$
PS1='[\t] \u@\h:\w\$ '              # [14:30:00] user@host:~/dir$
PS1='\[\e[32m\]\u@\h\[\e[0m\]:\[\e[34m\]\w\[\e[0m\]\$ '  # Colored

# Git branch in prompt
parse_git_branch() {
    git branch 2>/dev/null | sed -n 's/^\* //p'
}
PS1='\u@\h:\w ($(parse_git_branch))\$ '

# PROMPT_COMMAND (run before each prompt)
PROMPT_COMMAND='echo -ne "\033]0;${USER}@${HOSTNAME}: ${PWD}\007"'
```

### Readline Configuration (`~/.inputrc`)

```
# Case insensitive completion
set completion-ignore-case on

# Show completions on first Tab
set show-all-if-ambiguous on

# Append slash to directories
set mark-directories on

# Color completions by file type
set colored-stats on

# Show common prefix then cycle
set menu-complete-display-prefix on

# vi mode
set editing-mode vi

# Key bindings
"\e[A": history-search-backward
"\e[B": history-search-forward
```

---

## 🐛 Debugging & Profiling

### Debug Modes

```bash
# Trace execution (print each command)
bash -x script.sh
set -x                       # Enable in script
set +x                       # Disable

# Verbose (print input lines)
bash -v script.sh
set -v

# Custom debug prompt
export PS4='+(${BASH_SOURCE}:${LINENO}): ${FUNCNAME[0]:+${FUNCNAME[0]}(): }'

# Debug trap
trap 'echo "DEBUG: Line $LINENO: $BASH_COMMAND"' DEBUG

# Error trap with stack trace
err_report() {
    echo "Error on line $1"
    echo "Call stack:"
    for ((i=0; i<${#FUNCNAME[@]}; i++)); do
        echo "  ${FUNCNAME[$i]} at ${BASH_SOURCE[$i+1]}:${BASH_LINENO[$i]}"
    done
}
trap 'err_report $LINENO' ERR

# Strict mode
set -euo pipefail
IFS=$'\n\t'
```

### Syntax Check

```bash
bash -n script.sh               # Check syntax without running
shellcheck script.sh             # Static analysis (if installed)
shellcheck -x script.sh          # Follow source/. directives
```

### Profiling

```bash
# Time a command
time command
time { cmd1; cmd2; cmd3; }

# Timing with more detail
/usr/bin/time -v command         # Verbose (Linux)
/usr/bin/time -l command         # Verbose (macOS)

# Profile script with timestamps
PS4='+ $(date "+%s.%N") ' bash -x script.sh 2> profile.log

# Benchmark with hyperfine (if installed)
hyperfine 'command1' 'command2'

# Simple benchmark loop
start=$SECONDS
for i in {1..1000}; do
    command
done
elapsed=$((SECONDS - start))
echo "Elapsed: ${elapsed}s"
```

---

## 🔒 Security & Cryptography

### Checksums & Hashing

```bash
# MD5
md5sum file
echo -n "string" | md5sum

# SHA
sha1sum file
sha256sum file
sha512sum file

# Verify checksums
sha256sum -c checksums.txt

# macOS variants
md5 file
shasum -a 256 file

# OpenSSL hashing
openssl dgst -sha256 file
openssl dgst -md5 file
```

### Encryption & Certificates

```bash
# GPG
gpg -c file                   # Symmetric encryption
gpg file.gpg                  # Decrypt
gpg --gen-key                 # Generate key pair
gpg -e -r recipient file      # Encrypt with public key
gpg -d file.gpg                # Decrypt with private key
gpg --list-keys
gpg --export -a "Name" > public.key
gpg --import public.key

# OpenSSL
openssl enc -aes-256-cbc -in file -out file.enc
openssl enc -d -aes-256-cbc -in file.enc -out file
openssl rand -base64 32         # Random base64 string
openssl rand -hex 32            # Random hex string

# SSL Certificates
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365
openssl x509 -in cert.pem -text -noout
openssl s_client -connect host:443

# Base64
base64 file
base64 -d file.b64
echo "data" | base64
echo "ZGF0YQo=" | base64 -d
```

### Secure Practices

```bash
# Generate strong password
openssl rand -base64 24
tr -dc 'A-Za-z0-9!@#$%' < /dev/urandom | head -c 32

# Securely delete file (if shred available)
shred -vfz -n 5 file

# Check for open ports
ss -tlnp
nmap -sV localhost

# File integrity
# Create baseline
find /etc -type f -exec sha256sum {} \; > baseline.txt
# Check later
sha256sum -c baseline.txt

# Restricted bash
bash -r                        # Restricted shell
```

---

## 🕐 Date & Time

### `date` Command

```bash
# Current date/time
date                            # Default format
date -u                         # UTC

# Format strings
date +%Y-%m-%d                  # 2026-02-20
date +%H:%M:%S                  # 14:30:45
date "+%Y-%m-%d %H:%M:%S"      # 2026-02-20 14:30:45
date +%s                        # Unix timestamp
date +%F                        # Same as %Y-%m-%d
date +%T                        # Same as %H:%M:%S
date +%A                        # Full weekday name
date +%B                        # Full month name
date +%Z                        # Timezone name
date +%z                        # Timezone offset
date "+%b %d, %Y"               # Feb 20, 2026
date -R                         # RFC 2822 format
date -I                         # ISO 8601 format

# Date arithmetic
date -d "+1 day"                # Tomorrow (GNU)
date -d "-1 week"               # Last week
date -d "next friday"           # Next Friday
date -d "2 months ago"          # 2 months ago
date -d @1708387200             # From timestamp

# macOS date arithmetic
date -v+1d                      # Tomorrow
date -v-1w                      # Last week
date -v+2m                      # 2 months from now
date -r 1708387200              # From timestamp

# Convert between formats
date -d "2026-02-20" +%s        # Date to timestamp (GNU)
date -d @1708387200 +%Y-%m-%d   # Timestamp to date (GNU)

# Elapsed time
start=$(date +%s)
# ... work ...
end=$(date +%s)
echo "Duration: $((end - start)) seconds"
```

### Format Specifiers

| Specifier | Description | Example |
|-----------|-------------|---------|
| `%Y` | Year (4 digits) | 2026 |
| `%y` | Year (2 digits) | 26 |
| `%m` | Month (01-12) | 02 |
| `%d` | Day (01-31) | 20 |
| `%H` | Hour 24h (00-23) | 14 |
| `%I` | Hour 12h (01-12) | 02 |
| `%M` | Minute (00-59) | 30 |
| `%S` | Second (00-60) | 45 |
| `%N` | Nanoseconds | 123456789 |
| `%s` | Unix timestamp | 1771545045 |
| `%A` | Weekday name | Friday |
| `%a` | Weekday abbreviation | Fri |
| `%B` | Month name | February |
| `%b` | Month abbreviation | Feb |
| `%j` | Day of year (001-366) | 051 |
| `%u` | Day of week (1=Mon) | 5 |
| `%w` | Day of week (0=Sun) | 5 |
| `%U` | Week number (Sun start) | 07 |
| `%W` | Week number (Mon start) | 07 |
| `%Z` | Timezone name | EST |
| `%z` | Timezone offset | -0500 |
| `%F` | Full date (%Y-%m-%d) | 2026-02-20 |
| `%T` | Full time (%H:%M:%S) | 14:30:45 |
| `%p` | AM/PM | PM |
| `%P` | am/pm (lowercase) | pm |
| `%n` | Newline | |
| `%t` | Tab | |

### `cal` Calendar

```bash
cal                          # Current month
cal 2026                     # Full year
cal -3                       # Previous, current, next month
cal 2 2026                   # February 2026
ncal                         # Alternate layout
```

---

## 📐 Scripting Best Practices

### Script Template

```bash
#!/usr/bin/env bash
#
# Script: myscript.sh
# Description: Brief description of what this script does
# Author: Your Name
# Date: 2026-02-20
# Version: 1.0.0
#
# Usage: myscript.sh [-v] [-n name] [-o output] file ...
#

set -euo pipefail
IFS=$'\n\t'

# Constants
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"
readonly VERSION="1.0.0"

# Default values
verbose=false
dry_run=false
output_file=""

# Colors (if terminal supports it)
if [[ -t 1 ]]; then
    readonly RED='\033[0;31m'
    readonly GREEN='\033[0;32m'
    readonly YELLOW='\033[0;33m'
    readonly BLUE='\033[0;34m'
    readonly NC='\033[0m'  # No Color
else
    readonly RED=''
    readonly GREEN=''
    readonly YELLOW=''
    readonly BLUE=''
    readonly NC=''
fi

# Logging functions
log_info()  { printf "${GREEN}[INFO]${NC}  %s\n" "$*"; }
log_warn()  { printf "${YELLOW}[WARN]${NC}  %s\n" "$*" >&2; }
log_error() { printf "${RED}[ERROR]${NC} %s\n" "$*" >&2; }
log_debug() { $verbose && printf "${BLUE}[DEBUG]${NC} %s\n" "$*"; }

die() {
    log_error "$@"
    exit 1
}

usage() {
    cat <<EOF
Usage: $SCRIPT_NAME [OPTIONS] file...

Description of the script.

Options:
    -v, --verbose    Enable verbose output
    -n, --name NAME  Specify name
    -o, --output FILE  Output file
    -d, --dry-run    Dry run mode
    -h, --help       Show this help
    -V, --version    Show version

Examples:
    $SCRIPT_NAME -v file.txt
    $SCRIPT_NAME --name "test" -o output.txt file1 file2
EOF
    exit 0
}

version() {
    echo "$SCRIPT_NAME v$VERSION"
    exit 0
}

# Cleanup function
cleanup() {
    log_debug "Cleaning up..."
    # Remove temp files, restore state, etc.
}
trap cleanup EXIT INT TERM

# Parse arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -v|--verbose) verbose=true; shift ;;
            -n|--name)    name="$2"; shift 2 ;;
            -o|--output)  output_file="$2"; shift 2 ;;
            -d|--dry-run) dry_run=true; shift ;;
            -h|--help)    usage ;;
            -V|--version) version ;;
            --)           shift; break ;;
            -*)           die "Unknown option: $1" ;;
            *)            break ;;
        esac
    done
    
    # Remaining arguments
    files=("$@")
    
    # Validate
    [[ ${#files[@]} -eq 0 ]] && die "No files specified. Use -h for help."
}

# Main logic
main() {
    parse_args "$@"
    
    log_info "Starting $SCRIPT_NAME v$VERSION"
    
    for file in "${files[@]}"; do
        [[ -f "$file" ]] || die "File not found: $file"
        log_info "Processing: $file"
        # ... do work ...
    done
    
    log_info "Done!"
}

# Entry point
main "$@"
```

### Defensive Coding

```bash
# Always quote variables
echo "$variable"
cp "$source" "$dest"

# Use [[ ]] instead of [ ]
[[ -f "$file" ]] && echo "exists"

# Check commands exist before using
command -v git &>/dev/null || die "git is required"
hash curl 2>/dev/null || die "curl is required"

# Default values
name="${1:-default}"
config="${CONFIG_FILE:-/etc/myapp/config}"

# Validate arguments
[[ $# -lt 1 ]] && die "Usage: $0 <filename>"
[[ -z "$1" ]] && die "Argument cannot be empty"
[[ -f "$1" ]] || die "File not found: $1"
[[ -r "$1" ]] || die "File not readable: $1"

# Safe temporary files
tmpfile=$(mktemp) || die "Failed to create temp file"
trap 'rm -f "$tmpfile"' EXIT

# Prevent partial writes (write to temp then move)
tmpout=$(mktemp)
generate_output > "$tmpout"
mv "$tmpout" "$final_output"

# Use arrays for file lists (handle spaces)
files=("file with spaces.txt" "another file.txt")
for f in "${files[@]}"; do
    process "$f"
done

# Safe cd
cd "$dir" || die "Cannot cd to $dir"

# Avoid eval when possible
# BAD: eval "$user_input"
# GOOD: use arrays for commands
cmd=(ls -la "$directory")
"${cmd[@]}"
```

### Error Handling Patterns

```bash
# Try/catch pattern
try() {
    [[ $- = *e* ]]
    SAVED_OPT_E=$?
    set +e
}

catch() {
    export EXCEPTION=$?
    (( SAVED_OPT_E )) && set +e
    return $EXCEPTION
}

throw() {
    exit "$1"
}

# Usage
try
(
    command_that_might_fail
    another_command
)
catch || {
    case $EXCEPTION in
        1) echo "General error" ;;
        2) echo "Misuse of shell" ;;
        *) echo "Unknown error: $EXCEPTION" ;;
    esac
}

# Retry pattern
retry() {
    local max_attempts="${1:-3}"
    local delay="${2:-1}"
    local command="${@:3}"
    local attempt=1
    
    while [[ $attempt -le $max_attempts ]]; do
        if eval "$command"; then
            return 0
        fi
        log_warn "Attempt $attempt/$max_attempts failed. Retrying in ${delay}s..."
        sleep "$delay"
        ((attempt++))
    done
    
    log_error "All $max_attempts attempts failed"
    return 1
}

retry 5 2 curl -sf https://example.com/api
```

---

## 🚀 Advanced Techniques

### Coprocesses (Bash 4+)

```bash
# Start a coprocess
coproc myproc {
    while IFS= read -r line; do
        echo "Processed: $line"
    done
}

# Write to coprocess
echo "hello" >&"${myproc[1]}"

# Read from coprocess
read -r result <&"${myproc[0]}"
echo "$result"  # => Processed: hello

# Close write end
exec {myproc[1]}>&-

# Simple coproc (unnamed)
coproc bc -l
echo "scale=4; 22/7" >&"${COPROC[1]}"
read -r pi <&"${COPROC[0]}"
echo "$pi"  # => 3.1428
```

### Named Pipes (FIFOs)

```bash
# Create named pipe
mkfifo /tmp/mypipe

# Writer (in one terminal)
echo "Hello from writer" > /tmp/mypipe

# Reader (in another terminal)
cat < /tmp/mypipe

# Bidirectional communication
mkfifo /tmp/pipe1 /tmp/pipe2

# Process 1
while true; do
    read -r msg < /tmp/pipe1
    echo "Got: $msg"
    echo "Reply: ACK" > /tmp/pipe2
done

# Process 2
echo "Hello" > /tmp/pipe1
read -r reply < /tmp/pipe2
echo "$reply"

# Cleanup
rm /tmp/mypipe /tmp/pipe1 /tmp/pipe2
```

### Process Substitution Patterns

```bash
# Diff two command outputs
diff <(sort file1) <(sort file2)

# Feed multiple inputs
paste <(cut -f1 data.txt) <(cut -f3 data.txt)

# Log and display simultaneously
command > >(tee stdout.log) 2> >(tee stderr.log >&2)

# Multiple consumers
echo "data" | tee >(process1) >(process2) >(process3) > /dev/null
```

### Associative Array Patterns

```bash
# Config file parser
declare -A config
while IFS='=' read -r key value; do
    [[ "$key" =~ ^[[:space:]]*# ]] && continue   # Skip comments
    [[ -z "$key" ]] && continue                    # Skip empty
    key=$(echo "$key" | xargs)                     # Trim whitespace
    value=$(echo "$value" | xargs)
    config["$key"]="$value"
done < config.ini

# Word frequency counter
declare -A freq
while read -r word; do
    ((freq["$word"]++))
done < <(tr ' ' '\n' < text.txt | tr '[:upper:]' '[:lower:]' | sort)
for word in "${!freq[@]}"; do
    printf "%4d %s\n" "${freq[$word]}" "$word"
done | sort -rn

# Memoization
declare -A cache
fib() {
    local n=$1
    [[ -n "${cache[$n]+_}" ]] && { echo "${cache[$n]}"; return; }
    if (( n <= 1 )); then
        cache[$n]=$n
    else
        local a=$(fib $((n-1)))
        local b=$(fib $((n-2)))
        cache[$n]=$((a + b))
    fi
    echo "${cache[$n]}"
}
```

### `eval` and Indirect Assignment

```bash
# Dynamic variable names (prefer nameref instead)
varname="dynamic_var"
eval "$varname='hello'"
eval "echo \$$varname"

# Safer: nameref (Bash 4.3+)
declare -n ref="$varname"
ref="hello"
echo "$ref"

# Build and execute commands
cmd="ls"
args=("-la" "/tmp")
"$cmd" "${args[@]}"         # Preferred over eval
```

### Parallel Execution

```bash
# GNU Parallel (if available)
find . -name "*.jpg" | parallel convert {} {.}.png
cat urls.txt | parallel -j4 curl -sO {}
parallel -j8 gzip ::: *.log

# Native bash parallelism
max_procs=4
pids=()
for file in *.dat; do
    process "$file" &
    pids+=($!)
    
    # Limit concurrency
    while (( ${#pids[@]} >= max_procs )); do
        wait -n  # Wait for any to finish (Bash 4.3+)
        # Remove finished PIDs
        new_pids=()
        for pid in "${pids[@]}"; do
            kill -0 "$pid" 2>/dev/null && new_pids+=("$pid")
        done
        pids=("${new_pids[@]}")
    done
done
wait  # Wait for remaining
```

### Lock Files & Mutual Exclusion

```bash
# Using mkdir (atomic)
LOCKDIR="/tmp/myscript.lock"

cleanup_lock() {
    rm -rf "$LOCKDIR"
}

acquire_lock() {
    if mkdir "$LOCKDIR" 2>/dev/null; then
        trap cleanup_lock EXIT
        echo $$ > "$LOCKDIR/pid"
        return 0
    else
        local pid
        pid=$(cat "$LOCKDIR/pid" 2>/dev/null)
        if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
            echo "Already running (PID: $pid)" >&2
            return 1
        else
            # Stale lock — remove and retry
            rm -rf "$LOCKDIR"
            acquire_lock
        fi
    fi
}

acquire_lock || exit 1

# Using flock (Linux)
(
    flock -n 200 || { echo "Already running"; exit 1; }
    # Critical section
    echo "Running exclusively"
    sleep 10
) 200>/tmp/myscript.lock
```

---

## 📝 One-Liners & Recipes

### File Management

```bash
# Rename all .txt to .md
for f in *.txt; do mv "$f" "${f%.txt}.md"; done

# Rename with regex (rename command)
rename 's/\.txt$/.md/' *.txt

# Batch rename with prefix
for f in *.jpg; do mv "$f" "photo_$f"; done

# Find and replace in multiple files
find . -name "*.py" -exec sed -i 's/old/new/g' {} +

# Find large files
find / -type f -size +100M -exec ls -lh {} \; 2>/dev/null

# Find recently modified files
find . -type f -mmin -30

# Remove empty directories
find . -type d -empty -delete

# Count files by extension
find . -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn

# Recursive file count
find . -type f | wc -l

# Sync two directories
rsync -avh --delete source/ destination/

# Find duplicate files (by checksum)
find . -type f -exec md5sum {} + | sort | uniq -w32 -dD
```

### Text Processing

```bash
# Extract unique IPs from log
grep -oE '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b' access.log | sort -u

# Count unique IPs
grep -oE '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b' access.log | sort | uniq -c | sort -rn

# Extract email addresses
grep -oE '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' file

# Remove blank lines
sed '/^$/d' file
grep -v '^$' file

# Remove comments and blank lines
grep -Ev '^\s*(#|$)' file

# Number non-empty lines
grep -n '.' file

# Print specific columns from CSV
awk -F, '{print $1, $3}' data.csv

# Sum a column
awk '{sum += $1} END {print sum}' numbers.txt

# Top 10 most common words
tr -s ' ' '\n' < file | sort | uniq -c | sort -rn | head -10

# Convert CSV to JSON (basic)
awk -F, 'NR==1{split($0,h);next}{printf "{"; for(i=1;i<=NF;i++) printf "\"%s\":\"%s\"%s",h[i],$i,(i<NF?",":""); print "}"}' data.csv

# Replace ^M (carriage return) — DOS to Unix
sed -i 's/\r$//' file
tr -d '\r' < file > clean_file

# Generate sequence
seq 1 100
printf '%s\n' {001..100}

# Random line from file
shuf -n 1 file
sort -R file | head -1
```

### System Administration

```bash
# Who is using the most disk space
du -sh /home/* | sort -rh | head

# Find files modified in last 24 hours
find /var/log -mtime -1 -type f

# Monitor file changes
inotifywait -m -r /path/to/watch      # (requires inotify-tools)
fswatch /path/to/watch                  # macOS

# Kill all processes by name
pkill -9 process_name

# Check if port is in use
lsof -i :8080 | grep LISTEN

# HTTP health check
curl -sf http://localhost:8080/health > /dev/null && echo "UP" || echo "DOWN"

# Simple HTTP server (Python)
python3 -m http.server 8080

# Watch log file with highlighting
tail -f /var/log/syslog | grep --line-buffered --color "ERROR\|WARNING\|"

# Backup MySQL database
mysqldump -u root -p database > backup_$(date +%F).sql

# Monitor system resources
watch -n 1 'free -h; echo "---"; df -h; echo "---"; uptime'

# Find broken symlinks
find . -xtype l

# List all cron jobs for all users
for user in $(cut -f1 -d: /etc/passwd); do
    echo "--- $user ---"
    crontab -u "$user" -l 2>/dev/null
done

# System boot time
who -b
uptime -s
```

### Networking

```bash
# Check SSL certificate expiry
echo | openssl s_client -connect example.com:443 2>/dev/null | openssl x509 -noout -dates

# Download all links on a page
curl -s https://example.com | grep -oP 'href="\K[^"]+' | wget -i -

# Test port connectivity
timeout 3 bash -c '</dev/tcp/host/port' && echo "Open" || echo "Closed"

# Get public IP
curl -s ifconfig.me
curl -s icanhazip.com

# DNS lookup all records
dig any example.com +noall +answer

# Monitor HTTP response times
while true; do
    curl -so /dev/null -w "%{time_total}\n" https://example.com
    sleep 5
done

# Simple port scanner
for port in {1..1024}; do
    (echo >/dev/tcp/host/$port) 2>/dev/null && echo "Port $port open"
done
```

---

## 📜 Heredocs & Herestrings

### Heredocs

```bash
# Basic heredoc
cat <<EOF
Hello, $USER!
Today is $(date).
Current directory: $PWD
EOF

# No variable expansion (quoted delimiter)
cat <<'EOF'
This is literal: $USER
No expansion: $(date)
EOF

# Indented heredoc (strip leading tabs)
cat <<-EOF
	This is indented
	But tabs are stripped
	Variables: $USER
EOF

# To a file
cat > config.ini <<EOF
[database]
host=localhost
port=5432
EOF

# Pipe to command
mysql -u root <<EOF
CREATE DATABASE mydb;
USE mydb;
CREATE TABLE users (id INT, name VARCHAR(50));
EOF

# With sudo
sudo tee /etc/config.conf > /dev/null <<EOF
setting=value
another=setting
EOF

# Heredoc in function
generate_html() {
    cat <<EOF
<!DOCTYPE html>
<html>
<head><title>$1</title></head>
<body><h1>$1</h1></body>
</html>
EOF
}
generate_html "My Page" > page.html
```

### Herestrings

```bash
# Feed a string to command's stdin
bc <<< "2 + 3"              # => 5
grep "pattern" <<< "$string"
read -ra arr <<< "one two three"

# Variable-based
input="hello world"
wc -w <<< "$input"          # => 2

# Multi-word
cut -d',' -f2 <<< "a,b,c"  # => b
```

---

## 🔲 Subshells & Command Grouping

### Subshells `( )`

```bash
# Run in subshell (separate process)
(cd /tmp && ls)              # Current dir unchanged
echo "$PWD"                  # Still original directory

# Isolate variables
(
    x=100
    echo "Inside: $x"       # => 100
)
echo "Outside: $x"          # => (empty)

# Isolate options
(
    set -e
    failing_command           # Exits subshell, not parent
)
echo "Parent continues"

# Parallel subshells
(task1) &
(task2) &
(task3) &
wait
```

### Command Grouping `{ }`

```bash
# Run in CURRENT shell (no subshell)
{
    cd /tmp
    echo "Now in: $PWD"
}
echo "Still in: $PWD"        # /tmp! (changed in current shell)

# Redirect group output
{
    echo "Line 1"
    echo "Line 2"
    echo "Line 3"
} > output.txt

# Conditional execution group
[[ -f config.txt ]] && {
    source config.txt
    echo "Loaded config"
}

# Error handling group
{
    command1 &&
    command2 &&
    command3
} || {
    echo "Something failed"
    exit 1
}
```

---

## 🔌 Coprocesses & Named Pipes

### Coprocesses

```bash
# Simple unnamed coprocess
coproc bc -l
echo "22/7" >&"${COPROC[1]}"
read -r answer <&"${COPROC[0]}"
echo "$answer"    # => 3.14285714285714285714

# Named coprocess
coproc CALC { bc -l; }
echo "scale=10; sqrt(2)" >&"${CALC[1]}"
read -r result <&"${CALC[0]}"
echo "$result"    # => 1.4142135623

# Close coprocess input
exec {CALC[1]}>&-

# Interactive coprocess
coproc DIALOG {
    while read -r input; do
        case "$input" in
            hello) echo "Hi there!" ;;
            quit)  echo "Goodbye!"; break ;;
            *)     echo "Unknown: $input" ;;
        esac
    done
}

echo "hello" >&"${DIALOG[1]}"
read -r reply <&"${DIALOG[0]}"
echo "$reply"     # => Hi there!

echo "quit" >&"${DIALOG[1]}"
read -r reply <&"${DIALOG[0]}"
echo "$reply"     # => Goodbye!
```

---

## 🧩 Bash Loadable Built-ins

Bash can load additional built-ins from shared libraries.

```bash
# Enable a loadable built-in
enable -f /usr/lib/bash/sleep sleep

# List enabled built-ins
enable

# Disable a built-in
enable -n echo

# Common loadable built-ins (may vary by system)
# sleep   — built-in sleep (faster than /bin/sleep)
# mkdir   — built-in mkdir
# rmdir   — built-in rmdir
# ln      — built-in ln
# head    — built-in head
# tee     — built-in tee
# basename — built-in basename
# dirname  — built-in dirname
```

---

## 🎨 Colors & Formatting

### ANSI Color Codes

```bash
# Using tput
RED=$(tput setaf 1)
GREEN=$(tput setaf 2)
YELLOW=$(tput setaf 3)
BLUE=$(tput setaf 4)
MAGENTA=$(tput setaf 5)
CYAN=$(tput setaf 6)
WHITE=$(tput setaf 7)
BOLD=$(tput bold)
DIM=$(tput dim)
UNDERLINE=$(tput smul)
RESET=$(tput sgr0)

echo "${RED}Error${RESET}: something went wrong"
echo "${GREEN}${BOLD}Success!${RESET}"

# Using escape sequences
echo -e "\e[31mRed text\e[0m"
echo -e "\e[32mGreen text\e[0m"
echo -e "\e[1;34mBold blue\e[0m"
echo -e "\e[4;33mUnderlined yellow\e[0m"
echo -e "\e[41mRed background\e[0m"
echo -e "\e[1;37;41mBold white on red\e[0m"

# Color codes
# Foreground: 30-37 (standard), 90-97 (bright)
# Background: 40-47 (standard), 100-107 (bright)
# 0=Black 1=Red 2=Green 3=Yellow 4=Blue 5=Magenta 6=Cyan 7=White
# Attributes: 0=Reset 1=Bold 2=Dim 3=Italic 4=Underline 5=Blink 7=Reverse

# 256 colors
echo -e "\e[38;5;208mOrange text\e[0m"

# True color (24-bit)
echo -e "\e[38;2;255;100;50mCustom RGB\e[0m"

# Progress bar
progress_bar() {
    local current=$1 total=$2 width=50
    local percent=$((current * 100 / total))
    local filled=$((current * width / total))
    local empty=$((width - filled))
    
    printf "\r["
    printf "%${filled}s" | tr ' ' '#'
    printf "%${empty}s" | tr ' ' '-'
    printf "] %3d%%" "$percent"
}

for i in {1..100}; do
    progress_bar "$i" 100
    sleep 0.02
done
echo
```

### Cursor Control

```bash
# Move cursor
tput cup 10 20          # Move to row 10, col 20
tput cuu 5              # Move up 5 lines
tput cud 5              # Move down 5 lines
tput cuf 10             # Move forward 10 columns
tput cub 10             # Move backward 10 columns
tput sc                 # Save cursor position
tput rc                 # Restore cursor position

# Clear
tput clear              # Clear screen
tput el                 # Clear to end of line
tput ed                 # Clear to end of screen

# Terminal info
tput cols               # Terminal width
tput lines              # Terminal height
tput colors             # Number of colors supported

# Hide/show cursor
tput civis              # Hide cursor
tput cnorm              # Show cursor
```

---

## 🗂️ Cron & Scheduling

```bash
# Edit crontab
crontab -e

# List crontab
crontab -l

# Remove all cron jobs
crontab -r

# Crontab format:
# MIN HOUR DOM MON DOW  command
# *   *    *   *   *
# │   │    │   │   │
# │   │    │   │   └── Day of Week (0-7, 0 & 7 = Sunday)
# │   │    │   └────── Month (1-12)
# │   │    └─────────── Day of Month (1-31)
# │   └──────────────── Hour (0-23)
# └───────────────────── Minute (0-59)

# Examples
* * * * *     command            # Every minute
*/5 * * * *   command            # Every 5 minutes
0 * * * *     command            # Every hour
0 9 * * *     command            # Daily at 9 AM
0 9 * * 1-5   command            # Weekdays at 9 AM
0 0 1 * *     command            # First of every month
0 0 * * 0     command            # Every Sunday midnight
@reboot       command            # At startup
@hourly       command            # Every hour
@daily        command            # Daily at midnight
@weekly       command            # Weekly
@monthly      command            # Monthly
@yearly       command            # Yearly

# at command (one-time scheduling)
echo "command" | at 2pm tomorrow
at now + 5 minutes <<< "command"
at 14:00 2026-03-01 <<< "command"
atq                              # List pending jobs
atrm job_number                  # Remove job
```

---

## 📖 Bash Version Features

| Feature | Version |
|---------|---------|
| Associative arrays | 4.0 |
| `coproc` | 4.0 |
| `&>>` redirect | 4.0 |
| `|&` pipe stderr | 4.0 |
| Case fall-through `;&` and `;;&` | 4.0 |
| `mapfile` / `readarray` | 4.0 |
| `${var,,}` case modification | 4.0 |
| `**` globstar | 4.0 |
| `declare -g` global from function | 4.2 |
| Negative array indexing | 4.2 |
| `declare -n` nameref | 4.3 |
| `wait -n` (any job) | 4.3 |
| `${parameter@operator}` | 5.0 |
| `EPOCHSECONDS` / `EPOCHREALTIME` | 5.0 |
| `local -` (save/restore options) | 5.0 |
| `wait -p VAR` | 5.1 |
| `${var@U}` / `${var@L}` | 5.1 |

---

## 📚 Additional Resources

### Official Documentation
- [GNU Bash Manual](https://www.gnu.org/software/bash/manual/)
- [Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html)
- [POSIX Shell Specification](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html)

### Learning Resources
- [The Bash Hackers Wiki](https://wiki.bash-hackers.org)
- [Advanced Bash-Scripting Guide](https://tldp.org/LDP/abs/html/)
- [ShellCheck Wiki (common mistakes)](https://www.shellcheck.net/wiki/)
- [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html)

### Related IT-Journey Quests
- [Terminal Shortcuts Cheat Sheet](/docs/terminal-shortcuts-cheat-sheet/)
- [Terminal Fundamentals Quest](/quests/level-0000-terminal-fundamentals/)
- [Git Basics Quest](/quests/level-0000-git-basics/)

### `man` and `help`
```bash
man bash                     # Full bash manual
help                         # List all built-in commands
help cd                      # Help for specific built-in
info bash                    # GNU info pages
```

---

*Pro tip: Bookmark this page and combine it with the [Terminal Shortcuts Cheat Sheet](/docs/terminal-shortcuts-cheat-sheet/) for maximum command line productivity!*

---

**Last Updated**: February 2026 | **Author**: IT-Journey Team | **Bash Version Coverage**: 3.2 – 5.2+
