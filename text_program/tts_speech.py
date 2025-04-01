import edge_tts
# Asynchronous function for speech generation
async def speech_edge_tts(text: str, path: str, speech_language: str) -> None:
    # Change voice as needed
    # voice = 'en-US-AvaNeural'
    # voice = 'ja-JP-NanamiNeural'
    # voice = 'zh-CN-XiaoxiaoNeural'
    rate = '-5%'
    volume = '+50%'

    try:
        communicate = edge_tts.Communicate(text=text,
                                   voice=speech_language,
                                   rate=rate,
                                   volume=volume,)
        await communicate.save(path)
    except Exception as e:
        print(f'Error during speech generation: {e}')





