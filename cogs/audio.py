import os
import shutil
import discord
from discord.ext import commands
import speech_recognition as sr
import subprocess

class Audio(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def audio_to_text(self, audio_file):
        recognizer = sr.Recognizer()
        try:
            with sr.AudioFile(audio_file) as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.record(source)
            return recognizer.recognize_google(audio, language="fr-FR")
        except sr.UnknownValueError:
            return "Speech Recognition could not understand the audio"
        except sr.RequestError:
            return "Could not request results, check your internet connection"

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or not isinstance(message.channel, discord.DMChannel):
            return

        if message.attachments:
            for attachment in message.attachments:
                if attachment.filename.endswith(('.mp3', '.wav', '.ogg')):
                    await self.process_audio_attachment(attachment, message.channel)

    async def process_audio_attachment(self, attachment, channel):
        file_path = f"./downloads/{attachment.filename}"
        await attachment.save(file_path)

        if attachment.filename.endswith('.ogg'):
            wav_file_path = file_path.replace('.ogg', '.wav')
            subprocess.run(['ffmpeg', '-i', file_path, wav_file_path])
            file_path = wav_file_path

        text = self.audio_to_text(file_path)
        await channel.send(text)

        self.cleanup_downloads()

    def cleanup_downloads(self):
        folder = './downloads'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

async def setup(bot):
    await bot.add_cog(Audio(bot))