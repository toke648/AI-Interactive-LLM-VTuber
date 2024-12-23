import edge_tts

# Asynchronous function for speech generation
async def speech_generation_model(response, output):
    text = response
    # Change voice as needed
    voice = 'en-US-AvaNeural'
    # voice = 'ja-JP-NanamiNeural'
    # voice = 'zh-CN-XiaoxiaoNeural'
    rate = '-5%'
    volume = '+50%'

    try:
        communicate = edge_tts.Communicate(text=text,
                                   voice=voice,
                                   rate=rate,
                                   volume=volume,)
        await communicate.save(output)
    except Exception as e:
        print(f'Error during speech generation: {e}')

    # print(edge_tts.voices)
