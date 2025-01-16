---
title: Mastering iTerm Shortcuts for Efficiency
description: Enhance your productivity with iTerm shortcuts for deleting and navigating words efficiently on macOS.
date: 2025-01-16T18:00:08.715Z
preview: ""
tags:
    - iTerm
    - macOS
    - productivity
    - shortcuts
    - terminal
categories:
    - guides
    - it-journey
    - notes
    - programming
    - shortcuts
sub-title: null
excerpt: null
snippet: null
author: ""
layout: null
keywords: {}
lastmod: 2025-01-16T18:04:19.994Z
permalink: null
attachments: ""
draft: draft
slug: mastering-iterm-shortcuts-efficiency
---

In iTerm on macOS, you can set up keyboard shortcuts to delete the selected word by configuring key bindings. Here's how you can set it up:

**1\. Open iTerm Preferences**

- Press Command + , or navigate to **iTerm2 > Preferences** from the menu bar.

**2\. Go to the "Keys" Tab**

- In the Preferences window, select the **Keys** tab.

**3\. Add a New Key Binding**

- Click the **+** button in the lower-right corner to add a new shortcut.

**4\. Configure the Key Binding**

- In the **Keyboard Shortcut** field, press the key combination you want to use for deleting the selected word (e.g., Option + Backspace or Control + W).

- In the **Action** dropdown menu, select **Send Hex Code**.

- For deleting the word before the cursor, use this hex code:

0x1B 0x08

This corresponds to sending the ESC (0x1B) key followed by the Backspace (0x08) key.

**5\. Save and Test**

- Click **OK** to save the key binding.

- Test your new shortcut in the terminal by typing a few words and then using the shortcut to delete the word.

**Additional Notes**

- If you're using zsh or another shell, ensure the keybinding aligns with your shell's configuration.

- You can use similar key bindings to configure other shortcuts (e.g., deleting the word after the cursor).

Let me know if you'd like further customization details!


To set up a shortcut in iTerm2 for scrolling back by a word, you need to define a custom key binding in iTerm's preferences. Here's how you can do it:

**Steps to Configure a Shortcut for Scrolling Back by Word**

1. **Open iTerm2 Preferences**

Press Command + , or go to **iTerm2 > Preferences** from the menu bar.

2. **Navigate to the "Keys" Tab**

In the Preferences window, select the **Keys** tab.

3. **Add a New Key Binding**

Click the **+** button in the lower-right corner to create a new shortcut.

4. **Set the Shortcut Key**

- In the **Keyboard Shortcut** field, press the key combination you want to use for scrolling back by a word (e.g., Option + Left Arrow or Control + Left Arrow).

5. **Assign the Action**

- In the **Action** dropdown, select **Send Escape Sequence**.

- In the **Esc+** field, enter:

b

This sends the ESC + b sequence, which moves back by a word in most shells like bash, zsh, and fish.

6. **Repeat for Forward Movement (Optional)**

If you also want a shortcut to scroll forward by a word:

- Click the **+** button again to add another shortcut.

- Set the **Keyboard Shortcut** to something like Option + Right Arrow or Control + Right Arrow.

- Assign the action **Send Escape Sequence** and enter:

f

This sends the ESC + f sequence to move forward by a word.

7. **Save and Test**

Close the Preferences window and test your shortcuts in the terminal. Use the configured keys to move backward and forward by word.

**Additional Notes**

- The ESC + b and ESC + f shortcuts rely on shell support. Most common shells like zsh, bash, and fish support this by default.

- If you encounter conflicts with macOS system shortcuts (like Option+Arrow), you might need to disable conflicting shortcuts in **System Preferences > Keyboard > Shortcuts**.

To set up a shortcut in iTerm2 to delete the word after the cursor, you need to configure a custom key binding that sends the correct escape sequence. Here's how to do it:

**Steps to Set Up a Shortcut to Delete the Word After the Cursor**

1. **Open iTerm2 Preferences**

Press Command + , or go to **iTerm2 > Preferences** from the menu bar.

2. **Go to the "Keys" Tab**

In the Preferences window, select the **Keys** tab.

3. **Add a New Key Binding**

Click the **+** button in the lower-right corner to create a new shortcut.

4. **Configure the Shortcut**

- In the **Keyboard Shortcut** field, press the key combination you want to use for deleting the word after the cursor (e.g., Option + Delete or Control + Delete).

- In the **Action** dropdown, select **Send Escape Sequence**.

- In the **Esc+** field, enter:

d

This sends the ESC + d sequence, which deletes the word after the cursor in most shells like bash, zsh, and fish.

5. **Save and Test**

Close the Preferences window and test your shortcut in the terminal. Move your cursor to the beginning or middle of a word, and press your configured shortcut. The word after the cursor should be deleted.

**Notes**

- The ESC + d escape sequence works by default in many shells (bash, zsh, fish). If it doesn't work as expected, verify your shell configuration.

- If you want a similar shortcut to delete the word before the cursor, follow the same steps but use the escape sequence Ctrl + w or ESC + Backspace (depending on your preference).

Let me know if you need further assistance!