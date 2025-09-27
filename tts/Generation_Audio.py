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
            if not text or not text.strip():
                raise ValueError("TTS 输入文本为空")
            audio_path = self.settings.get_audio_path()
            print(audio_path)
            os.makedirs(self.settings.audio_directory, exist_ok=True)

            communicate = edge_tts.Communicate(
                text=text,
                voice=self.settings.tts_voice,
                rate=self.settings.tts_rate,
                volume=self.settings.tts_volume,
            )

            print(f"Saving audio to {audio_path} with voice={self.settings.tts_voice}, rate={self.settings.tts_rate}, volume={self.settings.tts_volume}")
            await communicate.save(audio_path)
            # 校验生成文件大小，防止静音/空文件
            try:
                file_size = os.path.getsize(audio_path)
            except FileNotFoundError:
                raise RuntimeError("音频文件未生成")
            print(f"Audio saved successfully: {audio_path}, size={file_size} bytes")
            if file_size < 2048:
                raise RuntimeError(f"音频文件过小({file_size} bytes)，疑似静音或生成失败")
        except Exception as e:
            print(f"Error during audio generation: {e}")
            raise

