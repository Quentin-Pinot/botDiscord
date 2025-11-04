import discord
from discord.ext import commands
import os
import logging
import traceback
from dotenv import load_dotenv
import subprocess
import shutil

from audio2text import Audio2Text

# Load environment variables from .env file
load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

logging.basicConfig(filename='discodBot.log', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S', encoding='utf-8')
logging.getLogger("discord").setLevel(logging.WARNING)

intents = discord.Intents.default()
intents.members = True
intents.messages = True  # Ensure the bot can receive message events

client = commands.Bot(command_prefix = '!', intents=intents, description='Bot de BigC')

@client.event
async def on_ready():
    logging.info('The bot is now ready for use !')

@client.command()
async def whoami(ctx):
    await ctx.send('Hello, I am the bot of Albion channel')

@client.event
async def on_member_join(member):
    channel = client.get_channel(338066803781664770)
    await channel.send('Welcome')

@client.event
async def on_member_remove(member):
    channel = client.get_channel(338066803781664770)
    await channel.send('Goodbye')

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if isinstance(message.channel, discord.DMChannel):
        if message.attachments:
            for attachment in message.attachments:
                if attachment.filename.endswith(('.mp3', '.wav', '.ogg')):
                    await message.channel.send("It's an audio")
                    file_path = f"./downloads/{attachment.filename}"
                    await attachment.save(file_path)
                    
                    if attachment.filename.endswith('.ogg'):
                        wav_file_path = file_path.replace('.ogg', '.wav')
                        print(file_path, wav_file_path)
                        subprocess.run(['./ffmpeg/bin/ffmpeg.exe', '-i', file_path, wav_file_path])
                        file_path = wav_file_path
                    
                    audio_2_txt = Audio2Text(file_path)
                    await message.channel.send(audio_2_txt)
                    
                    # Delete everything inside the downloads folder
                    for filename in os.listdir('./downloads'):
                        file_path = os.path.join('./downloads', filename)
                        try:
                            if os.path.isfile(file_path) or os.path.islink(file_path):
                                os.unlink(file_path)
                            elif os.path.isdir(file_path):
                                shutil.rmtree(file_path)
                        except Exception as e:
                            logging.error(f'Failed to delete {file_path}. Reason: {e}')
                else:
                    await message.channel.send("It's a text")
        else:
            await message.channel.send("It's a text")

    await client.process_commands(message)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

try:
    client.run(DISCORD_TOKEN)
except Exception:
    logging.error('The error is -> ' + str(traceback.format_exc()))