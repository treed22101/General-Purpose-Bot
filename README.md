# General_Purpose_Bot
A general purpose discord bot made with discord.py.
Moderation, setup, level system, and more.

## How To Use
1. Set your token in the ```.env``` and install anything needed in ```requirements.txt```

2. If the token for any reason is not being imported properly, move the .env file to your DESKTOP and not your IDE dir.

3. Launch from ```bot.py```

4. All of the commands are listed via !help once you setup the bot

# Setup Note
1. Some of the commands are not customized such as banned words, so set them to your liking.

2. The role in ```Autorole.py``` and the welcome channel id in ```Greeting.py``` needs to be set by you, and make sure you have a "logging" channel by that name (you can change the names if you want in ```Logging.py file```).

3. Use !setmuterole {the name of the role} to set the mute role.
