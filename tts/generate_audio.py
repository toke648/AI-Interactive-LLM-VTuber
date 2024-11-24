from main_setting import MainSetting
import edge_tts
import os

# 没想到可以不在class中引用父类对象，直接调用父类对象
class SpeechGenerator:
    def __init__(self):
        # super().__init__()
        # 本地引用 外部传参
        self.settings = MainSetting()
        # self.settings = settings

    async def generate_audio(self, text: str):
        try:
            audio_path = self.settings.get_audio_path()
            os.makedirs(self.settings.audio_directory, exist_ok=True)

            communicate = edge_tts.Communicate(
                text=text,
                voice=self.settings.default_voice,
                rate=self.settings.default_rate,
                volume=self.settings.default_volume,
            )

            print(f"Saving audio to {audio_path}")
            await communicate.save(audio_path)
            print(f"Audio saved successfully: {audio_path}")
        except Exception as e:
            print(f"Error during audio generation: {e}")



    # Asynchronous function for speech generation
    # async def speech_generation_model(response, audio_address, voice):
    #
    #     text = response
    #     # Change voice as needed
    #     # voice = 'en-US-AvaNeural'
    #     # voice = 'ja-JP-NanamiNeural'
    #     # voice = 'zh-CN-XiaoxiaoNeural'
    #     rate = '-5%'
    #     volume = '+50%'
    #
    #     try:
    #         communicate = edge_tts.Communicate(text=text,
    #                                            voice=voice,
    #                                            rate=rate,
    #                                            volume=volume, )
    #         print(f"Saving audio to {audio_address}")
    #         await communicate.save(audio_address)
    #         print(f"Audio saved successfully: {audio_address}")
    #     except Exception as e:
    #         print(f'Error during speech generation: {e}')

