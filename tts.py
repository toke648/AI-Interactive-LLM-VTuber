import edge_tts

# Asynchronous function for speech generation
async def speech_generation_model(response):
    text = response
    # Change voice as needed
    voice = 'en-US-AvaNeural'
    # voice = 'ja-JP-NanamiNeural'

    output = "data/audio/audio.mp3"
    rate = '-5%'
    volume = '+50%'

    try:
        tts = edge_tts.Communicate(text=text,
                                   voice=voice,
                                   rate=rate,
                                   volume=volume,
                                   proxy='http://127.0.0.1:7897')
        await tts.save(output)
    except Exception as e:
        print(f'Error during speech generation: {e}')