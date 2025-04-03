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
 
# --- Track a specific user's VC activity ---
@bot.event
async def on_voice_state_update(member, before, after):
    TARGET_USER_ID = 308259834657243139  # Replace with actual user's Discord ID

    if member.id != TARGET_USER_ID:
        return  # Ignore all other users

    # User joins a voice channel
    if before.channel is None and after.channel is not None:
        voice_channel = after.channel
        voice_client = await voice_channel.connect()  # ✅ store the VoiceClient
        await asyncio.create_task(record_audio(voice_client))  # ✅ pass the correct object
        print(f"🎯 Target user joined. Bot joined {voice_channel.name}")

    # User leaves a voice channel
    elif before.channel is not None and after.channel is None:
        vc = discord.utils.get(bot.voice_clients, guild=member.guild)
        if vc and vc.is_connected():
            await vc.disconnect()
            print("👋 Target user left. Bot disconnected.")

import asyncio
import tempfile
import wave
import pydub
import whisper

AUDIO_CHUNK_DURATION = 5  # seconds
TRIGGER_START = "call"
TRIGGER_END = "end"
TARGET_USER_ID = 302859384567421319  # Already in your logic

recording = False
collected_chunks = []

model = whisper.load_model("base")

async def record_audio(vc):
    global recording, collected_chunks
    print("🎙️ Bot is now listening for trigger...")

    while vc.is_connected():
        audio_data = await vc.recv_audio(AUDIO_CHUNK_DURATION)

        # TEMP: Save audio chunk to memory/tempfile
        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        with wave.open(temp.name, "wb") as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(16000)
            f.writeframes(audio_data)

        # Transcribe small chunk to check for trigger
        result = model.transcribe(temp.name)
        transcript = result["text"].lower().strip()

        print(f"[🟡 Listening] Heard: {transcript}")

        if TRIGGER_START in transcript:
            print("🟢 Trigger START detected. Begin recording...")
            recording = True
            collected_chunks = []

        elif TRIGGER_END in transcript and recording:
            print("🔴 Trigger END detected. Transcribing full message...")
            recording = False

            # Merge chunks and transcribe
            merged = pydub.AudioSegment.empty()
            for chunk in collected_chunks:
                merged += pydub.AudioSegment.from_wav(chunk)

            merged_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            merged.export(merged_file.name, format="wav")

            result = model.transcribe(merged_file.name)
            final_text = result["text"]

            channel = discord.utils.get(vc.guild.text_channels, id=TEXT_ID)
            await channel.send(f"📢 Final Callout: {final_text}")

        # If we're inside trigger, collect audio
        if recording:
            collected_chunks.append(temp.name)

        await asyncio.sleep(1)




# === Run the bot ===
bot.run(TOKEN)



