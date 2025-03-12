A simple client for a Discord bot designed to interact with the Home Assistant assist pipeline.

How to setup:

```
python3 -m venv bot-env
bot-env\Scripts\activate.bat
pip install -U discord.py
pip install websockets
```
then create a file called **mysecrets.py**
with the following content:
```
home_assistant_url = "YOUR_HA_IP:8123"
home_assistant_token = "YOUR_HA_TOKEN"
discord_bot_token = "YOUR_DISCORD_BOT_TOKEN"
```
to Start simple type:
```
python init.py
```
