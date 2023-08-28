import discord
import responses
from time import sleep

def get_token():
    with open("data/bot/t.txt", "r") as f:
        return str(f.read())
    
TOKEN = get_token()

async def send_message(message, user_message, channel_id, server_id):
    try:
        response = responses.handle(user_message, channel_id, server_id)

        await message.channel.send(response)

    except Exception as e:
        print(e)


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

        if user_message.startswith(f"{prefix}"):
            print(f"{username} said: '{user_message}' in: '{server_id}:{channel_id}'")

            await send_message(message,user_message,channel_id)

    client.run(TOKEN)
