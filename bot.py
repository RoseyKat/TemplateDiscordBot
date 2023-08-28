import discord
import responses
from time import sleep
import os
import json

def get_token():
    with open("data/bot/t.txt", "r") as f:
        return str(f.read())
    
TOKEN = get_token()

async def send_message(message, user_message, channel_id, server_id, prefix):
    try:
        response = responses.handle(user_message, channel_id, server_id, prefix)

        await message.channel.send(response)

    except Exception as e:
        if str(e) == "400 Bad Request (error code: 50006): Cannot send an empty message":
            print("No response found")
        else:
            print(e)

async def get_prefix(server) -> str():
    # Check if server has assigned prefix
    if os.path.exists(f"data/server/{server}/prefix.txt") == False:
        # If not then make server path, and create prefix from server_defaults.json
        os.makedirs(name=f"data/server/{server}", exist_ok=True)

        with open("data/client/server_defaults.json", "r") as f:
            prefix = json.loads(f.read())["prefix"]
        
        with open(f"data/server/{server}/prefix.txt", "w") as f:
            f.write(prefix)

        return prefix
        
        
    else:
        # If it does exist then read prefix and return it.
        with open(f"data/server/{server}/prefix.txt", "r") as f:
            return f.read()




def run():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.presences = True
    intents.members = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"{client.user} Running....")

        sleep(2)
        await change_presence("Template")

    async def change_presence(title:str):
        await client.change_presence(activity=discord.Game(name=title))

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return 
        
        user_id = str(message.author.id)
        username = str(message.author)
        user_message = str(message.content)
        channel_id = str(message.channel.id)
        server_id = str(message.guild.id)

        prefix = await get_prefix(server_id)

        print(f"{username} said: '{user_message}' in: '{server_id}:{channel_id}'")

        await send_message(message,user_message,channel_id,server_id,prefix)

    client.run(TOKEN)
