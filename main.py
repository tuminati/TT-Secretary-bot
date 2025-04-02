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

# --- Track a specific user's VC activity ---
@bot.event
async def on_voice_state_update(member, before, after):
    TARGET_USER_ID = 308259834657243139  # Replace with actual user's Discord ID

    if member.id != TARGET_USER_ID:
        return  # Ignore all other users

    # User joins a voice channel
    if before.channel is None and after.channel is not None:
        voice_channel = after.channel
        await voice_channel.connect()
        print(f"🎯 Target user joined. Bot joined {voice_channel.name}")

    # User leaves a voice channel
    elif before.channel is not None and after.channel is None:
        vc = discord.utils.get(bot.voice_clients, guild=member.guild)
        if vc and vc.is_connected():
            await vc.disconnect()
            print("👋 Target user left. Bot disconnected.")


# === Run the bot ===
bot.run(TOKEN)



