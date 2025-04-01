import edge_tts
import asyncio

async def generate_options():
    voices = await edge_tts.list_voices()
    for voice in voices:
        print(f'<option value="{voice["ShortName"]}">{voice["ShortName"]}</option>')

asyncio.run(generate_options())
