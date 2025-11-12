import os
import discord
from discord.ext import commands
from openai import OpenAI
import asyncio

class Image(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    @commands.command()
    async def image(self, ctx, *, prompt: str):
        """Generates an image from a text prompt using DALL-E."""
        await ctx.send(f"Generating image for: '{prompt}'...")

        try:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    n=1,
                    size="1024x1024",
                )
            )
            image_url = response.data[0].url
            await ctx.send(image_url)
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

async def setup(bot):
    await bot.add_cog(Image(bot))
