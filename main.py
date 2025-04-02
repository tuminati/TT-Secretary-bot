import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

#environment variables
load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID = int(os.getenv("DISCORD_GUILD_ID"))
VC_ID = int(os.getenv("VOICE_CHANNEL_ID"))
TEXT_ID = int(os.getenv("TEXT_CHANNEL_ID"))


#bot permissions
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)



# === Bot startup confirmation ===
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# === Command: Join voice channel ===
@bot.command()
async def startCalloutBot(ctx):
    """Bot joins the voice channel."""
    voice_channel = ctx.guild.get_channel(VC_ID)
    if voice_channel:
        await voice_channel.connect()
        await ctx.send("📡 Bot connected to voice channel!")

# === Command: Leave voice channel ===
@bot.command()
async def stopCalloutBot(ctx):
    """Bot leaves the voice channel."""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Bot disconnected from voice.")

# 🧠 Whisper transcription test command
@bot.command()
async def testcallout(ctx):
    """
    Transcribes a local audio file (test_callout.wav) using Whisper and sends the text to Discord.
    """
    import whisper  # Import the Whisper model

    model = whisper.load_model("base")  # Load the base Whisper model (can use "tiny", "small", etc.)
    result = model.transcribe("test_callout.wav")  # Transcribe the audio file

    transcription = result["text"]  # Get just the transcribed text portion

    await ctx.send(f"🧠 Transcribed: {transcription}")  # Send result to the Discord text channel

print("Looking for:", os.path.abspath("test_callout.wav"))

# === Run the bot ===
bot.run(TOKEN)



