# This example requires the 'message_content' intent.
import mysecrets
import discord
from HomeAssistantpy import HomeAssistant
import time

new_coversation_every_x_seconds_of_inactivty = 5

        


class DHAclient(discord.Client):
    Home = None
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        self.Home = HomeAssistant(new_coversation_every_x_seconds_of_inactivty, on_response_callback=self.on_response_callback)  # Pass the callback to HomeAssistant
        await self.Home.connect()
        

    async def on_message(self, message):
        if message.author != self.user:
            if client.user in message.mentions:
                await self.Home.initAssistPipeline(f"You are inside a discord channel Please respond to users requests and its nice to use peoples names the user {message.author} just said {message.content} to you",message)


    async def on_response_callback(self, discord_message, message):
        await discord_message.reply(message)

intents = discord.Intents.default()
intents.message_content = True

client = DHAclient(intents=intents)
client.run(mysecrets.discord_bot_token)

