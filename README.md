# DeskScout Source Code
 An open source alert system for CGMs


# NOTICE
# DeskScout now features an updater, you must be on 0.7.0 or later to receive OTA updates.
# Updates are now staged, you may need to update multiple times to get to the latest version

# Requirements
Python 3.12.2 or later
Microsoft Windows App Runtime 1.7 (I have not tested 1.8)

# What works
- Urgent low glucose alerts
- Low glucose alerts
- High Glucose alerts
- Tray Icon
- Display in mmol/L
- Glucose history page
- Auto login
- Data export
- Falling Fast alert
- Rising Fast alert

# Whats being worked on
- Falling fast, Rising fast, Urgent Low Soon alerts
- Glucose overlay
- LibreLink glucose data providers
- DeskScout system alert customization
- Version string generation
- Updater
- Deleting glucose history
- Nightscout Settings
- Glucose graph

# Whats new
## Build 27
Critical update fix

As of now, there is no support for LibreLink, but it will be coming in the first official release, this is the definition of a developer release, there are many things that don't work but y'all deserve an update.

# Warning
Do not attempt to restore glucose data from version 0.6 or below, it will not work, the way the app handles timestamps has changed, and it will break your install. Please try your best to only update your installation via the over the air updates to mitigate corruption of settings if you decide to restore your data. TLDR: Only backup and restore from the version you are running, there are no guarantees that it will work if you do so
# Running the app
Run DeskScout.pyw to automatically start the server and open the app if the server is not running

Or start them separately, the server must be running to start the app

# Join the DeskScout Discord server!
https://discord.gg/Wf3XsDwsEk

