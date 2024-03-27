---
title: Bootable mac os
description: null
author: null
excerpt: null
date: 2024-03-27T22:53:26.161Z
lastmod: 2024-03-27T22:53:47.995Z
draft: true
tags: []
categories: []
meta: null
snippet: null
slug: bootable-mac-os
---


Create a bootable installer for macOS
=====================================

You can use an external drive or secondary volume as a startup disk from which to install the Mac operating system.

These advanced steps are primarily for system administrators and other experienced users who are familiar with entering commands in Terminal.

You don't need a bootable installer to [upgrade macOS](https://support.apple.com/kb/HT201541) or [reinstall macOS](https://support.apple.com/kb/HT204904), but it can be useful if you want to install macOS on multiple computers without downloading the installer each time, or you're unable to install a compatible macOS from the Finder or macOS Recovery.

What you need to create a bootable installer
--------------------------------------------

-   A USB flash drive or other secondary volume with at least 14GB of available storage, formatted as Mac OS Extended

-   A full macOS installer

To download a full installer, your Mac must be using macOS High Sierra or later, the latest version of macOS Sierra, or the latest version of OS X El Capitan. Your Mac must also be compatible with the macOS that you're downloading. Enterprise administrators: download from Apple, not a locally hosted update server.

[Download a macOS installer using the App Store or your browser](https://support.apple.com/kb/HT211683)

Use Terminal to create the bootable installer
---------------------------------------------

![Terminal window showing the completed process](https://cdsassets.apple.com/live/7WUAS350/images/macos/ventura/macos-ventura-terminal-command-createinstallmedia.png)

1.  Plug the USB flash drive into your Mac.

2.  Open Terminal, which is in the Utilities folder of your Applications folder.

3.  Type or paste one of the [commands below](https://support.apple.com/en-us/101578#commands) into Terminal, then press Return to enter the command. Each command assumes that the installer is in your Applications folder, and MyVolume is the name of the USB flash drive or other volume you're using. If the volume has a different name, replace `MyVolume` in the command with the name of your volume.

4.  When prompted, type your administrator password. Terminal doesn't show any characters as you type. Then press Return.

5.  When prompted, type Y to confirm that you want to erase the volume, then press Return. Terminal shows the progress as the volume is erased.

6.  After the volume is erased, you may see an alert that Terminal would like to access files on a removable volume. Click OK to allow the copy to proceed.

7.  When Terminal says that it's done, the volume will have the same name as the installer you downloaded, such as Install macOS Sonoma. You can now quit Terminal and eject the volume.

Commands
--------

Depending on which macOS you downloaded, enter one of the following commands in Terminal as instructed above.

-   Remember to replace `MyVolume` in the command with the name of your volume.

-   If your Mac is using macOS Sierra or earlier, append `--applicationpath` to your command, followed by the appropriate installer path, similar to what is shown in the command below for El Capitan.

### Sonoma

`sudo /Applications/Install\ macOS\ Sonoma.app/Contents/Resources/createinstallmedia --volume /Volumes/MyVolume`

### Ventura

`sudo /Applications/Install\ macOS\ Ventura.app/Contents/Resources/createinstallmedia --volume /Volumes/MyVolume`

### Monterey

`sudo /Applications/Install\ macOS\ Monterey.app/Contents/Resources/createinstallmedia --volume /Volumes/MyVolume`

### Big Sur

`sudo /Applications/Install\ macOS\ Big\ Sur.app/Contents/Resources/createinstallmedia --volume /Volumes/MyVolume`

### Catalina

`sudo /Applications/Install\ macOS\ Catalina.app/Contents/Resources/createinstallmedia --volume /Volumes/MyVolume`

### Mojave

`sudo /Applications/Install\ macOS\ Mojave.app/Contents/Resources/createinstallmedia --volume /Volumes/MyVolume`

### High Sierra

`sudo /Applications/Install\ macOS\ High\ Sierra.app/Contents/Resources/createinstallmedia --volume /Volumes/MyVolume`

### El Capitan

`sudo /Applications/Install\ OS\ X\ El\ Capitan.app/Contents/Resources/createinstallmedia --volume /Volumes/MyVolume --applicationpath /Applications/Install\ OS\ X\ El\ Capitan.app`

Use the bootable installer
--------------------------

[Determine whether you're using a Mac with Apple silicon](https://support.apple.com/kb/HT211814), then follow the appropriate steps. Remember that the Mac you're starting up with the bootable installer must be compatible with the macOS on the bootable installer. If not, the Mac might [start up to a circle with a line through it](https://support.apple.com/101666).

### Mac with Apple silicon

1.  Plug the bootable installer into a Mac that is connected to the internet and compatible with the version of macOS you're installing. A bootable installer doesn't download macOS from the internet, but it does require an internet connection to get firmware and other information specific to the Mac model.

2.  Turn on the Mac and continue to hold the power button until you see the [startup options window](https://support.apple.com/kb/HT211873), which shows your bootable volumes.

3.  Select the volume containing the bootable installer, then click Continue.

4.  When the macOS installer opens, follow the onscreen installation instructions.

### Any other Mac

1.  Plug the bootable installer into a Mac that is connected to the internet and compatible with the version of macOS you're installing. A bootable installer doesn't download macOS from the internet, but it does require an internet connection to get firmware and other information specific to the Mac model.

2.  Turn on your Mac, then immediately press and hold the Option (Alt) key.

3.  Release the Option key when you see a dark screen showing your bootable volumes.

4.  Select the volume containing the bootable installer. Then click the onscreen arrow or press Return.

5.  If you're using a [Mac with the Apple T2 Security Chip](https://support.apple.com/HT208862) and you can't start up from the bootable installer, make sure that [Startup Security Utility](https://support.apple.com/kb/HT208198) is set to allow booting from external or removable media.

6.  Choose your language, if prompted.

7.  Select Install macOS (or Install OS X) from the Utilities window, then click Continue and follow the onscreen instructions.

Learn more
----------

For information about the `createinstallmedia` command and the arguments you can use with it, make sure that the macOS installer is in your Applications folder, then enter the appropriate path in Terminal:

`/Applications/Install\ macOS\ Sonoma.app/Contents/Resources/createinstallmedia`

`/Applications/Install\ macOS\ Ventura.app/Contents/Resources/createinstallmedia`

`/Applications/Install\ macOS\ Monterey.app/Contents/Resources/createinstallmedia`

`/Applications/Install\ macOS\ Big\ Sur.app/Contents/Resources/createinstallmedia`

`/Applications/Install\ macOS\ Catalina.app/Contents/Resources/createinstallmedia`

`/Applications/Install\ macOS\ Mojave.app/Contents/Resources/createinstallmedia`

`/Applications/Install\ macOS\ High\ Sierra.app/Contents/Resources/createinstallmedia`

`/Applications/Install\ OS\ X\ El\ Capitan.app/Contents/Resources/createinstallmedia`

Published Date: November 30, 2023