from main_setting import MainSetting
import edge_tts
import os

class SpeechGenerator:
    def __init__(self):
        # Initialize settings from MainSetting
        self.settings = MainSetting()
        # Alternative: receive settings as parameter
        # self.settings = settings

    async def generate_audio(self, text: str):
        try:
            audio_path = self.settings.get_audio_path()
            print(audio_path)
            os.makedirs(self.settings.audio_directory, exist_ok=True)

            communicate = edge_tts.Communicate(
                text=text,
                voice=self.settings.tts_voice,
                rate=self.settings.tts_rate,
                volume=self.settings.tts_volume,
            )

            print(f"Saving audio to {audio_path}")
            await communicate.save(audio_path)
            print(f"Audio saved successfully: {audio_path}")
        except Exception as e:
            print(f"Error during audio generation: {e}")

