# Overflow Discord Bot

This is a Discord bot built using [discord.py](https://discordpy.readthedocs.io/en/stable/) library. The bot provides basic event handling, command handling, and slash command handling functionality.

## Installation

Clone the repository:

   ```bash
   git clone https://github.com/np-overflow/discord_bot.git

## Event Handling
The bot includes basic event handling for common Discord events such as on_ready, on_message, on_member_join, etc. You can modify the event handlers in the bot.py file according to your requirements.

## Command Handling
The bot supports basic command handling using the commands extension provided by discord.py. You can define new commands by creating separate modules in the commands directory. Check out the commands/example.py module for an example command implementation.

## Slash Command Handling
The bot also includes support for slash command handling, which allows for a more structured way of creating commands. Slash commands are defined in the slash_commands directory as separate JSON files. Refer to the slash_commands/example.json file for an example slash command definition.
