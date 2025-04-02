On bot startup:
    
Load audio transcription model (e.g., Whisper)
Define regex patterns or NLP model for parsing option callouts
Set command(s) to join/leave voice channel

When user sends command "/startCalloutBot":
    
Bot joins the voice channel
Start capturing raw audio from all speakers
Continuously process audio in chunks (e.g., 5–10 seconds)

Loop:
    For each audio chunk:
        
Transcribe audio to text using Whisper or other STT model
Check if transcription contains a trigger phrase (e.g., "Hey Callout")

        If trigger phrase is detected:
            
Run parsing logic on the transcription
Extract:
Strike price (e.g., "489C" → 489, Call)
Ticker symbol (e.g., QQQ)
Expiry (e.g., "0DTE")
Entry price (e.g., "limit 1.2")

            If all required fields are found:
                
Format into a rich Discord message
Post in a specific text channel (e.g., #live-callouts)

        Else:
            
Optionally log or ignore unrecognized speech

On "/stopCalloutBot" command:
    
Stop listening
Leave voice channel