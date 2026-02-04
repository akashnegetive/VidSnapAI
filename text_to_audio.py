import os
from openai import OpenAI


def text_to_speech_file(text: str, folder: str) -> str:

    base_dir = os.path.dirname(os.path.abspath(__file__))
    save_dir = os.path.join(base_dir, "user_uploads", folder)
    save_file_path = os.path.join(save_dir, "audio.mp3")

    os.makedirs(save_dir, exist_ok=True)

    print("[TTS] start request")

    try:
        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            timeout=30   # ⭐ prevents Render hangs
        )

        with client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=text
        ) as response:

            response.stream_to_file(save_file_path)

        print("[TTS] ✅ Audio saved")

        return save_file_path

    except Exception as e:
        print("[TTS ERROR]", e)
        return ""
