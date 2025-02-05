---
title: iTerm Tips and Tricks
description: Unlock your productivity with essential iTerm2 tips for customizing keybindings and navigating text efficiently in the terminal.
date: 2025-01-16T22:27:04.957Z
preview: /assets/images/iTerm-shortcuts-2.png
tags:
    - customization
    - iTerm2
    - macOS
    - productivity
    - terminal
categories:
    - guides
    - iTerm2
    - productivity tips
    - shortcuts
    - terminal customization
sub-title: null
excerpt: null
snippet: null
author: Amr
layout: null
keywords:
    - tips
    - iTerm
lastmod: 2025-01-17T02:11:14.485Z
permalink: null
attachments: ""
draft: draft
---


**How to Customize iTerm2 for Efficiency: Keybindings to Delete Words and Navigate Text**

**iTerm2**, a powerful terminal emulator for macOS, provides extensive customization options that can enhance your productivity when working in the terminal. In this guide, we'll walk through setting up keybindings to delete words and navigate text efficiently, and explore the benefits of mastering such customizations.

**Why Customize Your Terminal?**

Customizing keybindings in iTerm2 offers several benefits:

1. **Increased Productivity**: Quickly delete or navigate text without reaching for the mouse or typing redundant commands.

2. **Improved Workflow**: Align keybindings with your muscle memory or preferences, reducing friction during complex tasks.

3. **Skill Development**: Learn how terminals handle input/output, escape sequences, and shell behavior, which is invaluable for developers, sysadmins, and IT professionals.

4. **Cross-Environment Skills**: Customizing iTerm2 mirrors techniques used in Linux and Unix-like systems, enhancing your flexibility across platforms.

**Setting Up Keybindings in iTerm2**

**1\. Delete the Word Before the Cursor**

To delete the word before the cursor:

1. Open iTerm2 Preferences (Command + ,).

2. Navigate to the **Keys** tab.

3. Add a new keybinding by clicking the **+** button.

4. Set your desired shortcut (e.g., Option + Backspace).

5. Assign the **Action** as **Send Hex Code**.

6. Use the hex code:

0x1B 0x08

This sends the escape key (0x1B) followed by backspace (0x08), deleting the word before the cursor.

**2\. Delete the Word After the Cursor**

To delete the word after the cursor:

1. Open iTerm2 Preferences and go to the **Keys** tab.

2. Add a new keybinding.

3. Set the shortcut (e.g., Control + Delete).

4. Assign the **Action** as **Send Escape Sequence**.

5. In the **Esc+** field, enter:

d

This sends the ESC + d sequence, deleting the word after the cursor.

**3\. Scroll Back or Forward by Word**

Efficiently navigate text in your terminal:

1. Add a new keybinding for moving back by word.

- Shortcut: Option + Left Arrow

- Action: **Send Escape Sequence**

- Esc+: b

2. Add a keybinding for moving forward by word.

- Shortcut: Option + Right Arrow

- Action: **Send Escape Sequence**

- Esc+: f

These mimic common shortcuts in many shells (bash, zsh, fish) for word-by-word navigation.

**Advanced Benefits of Terminal Customization**

- **Faster Text Manipulation**: Editing long commands or configuration files becomes seamless with shortcuts for deleting or navigating by word.

- **Command Line Mastery**: These customizations align with common shell keybindings, improving your command-line proficiency across environments.

- **Ergonomic Workflow**: Custom shortcuts reduce repetitive hand movements, minimizing strain during extended terminal sessions.

- **Personalization**: Tailor iTerm2 to suit your preferences, creating an environment that feels intuitive and productive.

**Skills You'll Develop**

By customizing iTerm2, you'll:

- **Understand Escape Sequences**: Learn how input is translated into actions in the terminal.

- **Master Shell Behavior**: Familiarize yourself with default keybindings and how to enhance them.

- **Enhance Problem-Solving**: Troubleshoot and resolve conflicts between customizations and system defaults.

- **Optimize Tools**: Apply similar techniques in other terminal emulators or software environments.

![iterm](/assets/images/iTerm-shortcuts-2.png)

**Conclusion**

Customizing iTerm2 keybindings is more than a convenience---it's an investment in your efficiency and technical skills. By mastering shortcuts to delete words, navigate text, and tailor your terminal workflow, you'll gain tools that make your work faster, smoother, and more enjoyable. Dive into these customizations today and transform your terminal into a productivity powerhouse!