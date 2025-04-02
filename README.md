1. On bot startup:
    - Do nothing in VC yet (wait passively).

2. When TARGET_USER_ID joins VC:
    - Bot automatically joins the same VC.
    - Start quietly listening in background.

3. During live voice:
    - Continuously transcribe short audio chunks (e.g., every 5s).

4. Keyword detection:
    - Start transcribing only when "call" (or similar) is detected.
    - Keep transcribing until "end" (or similar) is detected.
    - Extract only what’s spoken between "call" and "end".

5. Post that specific snippet into the text channel.

6. When TARGET_USER_ID leaves VC:
    - Bot also disconnects from VC.
    - Stops listening/transcribing.

