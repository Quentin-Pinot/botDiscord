import asyncio
import discord
from discord.ext import commands
import os
import logging
import traceback
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
WELCOME_CHANNEL_ID = int(os.getenv('WELCOME_CHANNEL_ID'))

logging.basicConfig(filename='discodBot.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S', encoding='utf-8')
logging.getLogger("discord").setLevel(logging.WARNING)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents, description='Bot de BigC')

@bot.event
async def on_ready():
    logging.info('The bot is now ready for use!')
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

@bot.command()
async def whoami(ctx):
    await ctx.send('Hello, I am the bot of Albion channel')

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        await channel.send(f'Welcome {member.mention}!')

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        await channel.send(f'Goodbye {member.name}!')

@bot.command()
async def load(ctx, extension):
    try:
        await bot.load_extension(f'cogs.{extension}')
        await ctx.send(f'Loaded extension: {extension}')
    except Exception as e:
        await ctx.send(f'Error loading extension: {e}')

@bot.command()
async def unload(ctx, extension):
    try:
        await bot.unload_extension(f'cogs.{extension}')
        await ctx.send(f'Unloaded extension: {extension}')
    except Exception as e:
        await ctx.send(f'Error unloading extension: {e}')

@bot.command()
async def reload(ctx, extension):
    try:
        await bot.reload_extension(f'cogs.{extension}')
        await ctx.send(f'Reloaded extension: {extension}')
    except Exception as e:
        await ctx.send(f'Error reloading extension: {e}')

async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
            except Exception as e:
                logging.error(f'Failed to load extension {filename}: {e}')

async def main():
    async with bot:
        await load_cogs()
        await bot.start(DISCORD_TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception:
        logging.error('The error is -> ' + str(traceback.format_exc()))