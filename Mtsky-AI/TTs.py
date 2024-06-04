import os
import edge_tts

def audioTTs(prompet: str, rate: str = '+0%', volume: str = '+100%', value: str = 'ar-OM-AyshaNeural') -> bytes:
    audio_file = f'{value}.mp3'
    communicate = edge_tts.Communicate(text=prompet, voice=value,volume=volume,rate=rate)
    communicate.save_sync(audio_file)
    
    with open(audio_file, 'rb') as file:
        audio_bytes = file.read()
        file.close()
        
    os.remove(audio_file)
    return audio_bytes


# from base64 import b64decode
# response = requests.post('https://api.edenai.run/v2/audio/text_to_speech', headers=headers, json=json_data)
# print(response.json())
# with open('simple.mp3','wb') as file:
#     file.write(b64decode(response.json()['openai']['audio']))
import requests

headers = {
    'Authorization': 'Bearer <ACCESS TOKEN>',
    'Content-Type': 'application/json',
}

json_data = {
    'platform': 'edge_tts',
    'message': '欢迎回家',
    'language': 'zh-CN-XiaoyiNeural',
    'cache': True,
    'options': {
        'volume': '+10%',
    },
}

response = requests.post('http://home-assistant.local:8123/api/tts_get_url', headers=headers, json=json_data)
print(response.json())

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"platform": "edge_tts", "message": "欢迎回家", "language": "zh-CN-XiaoyiNeural", "cache": true, "options": {"volume": "+10%"}}'.encode()
#response = requests.post('http://home-assistant.local:8123/api/tts_get_url', headers=headers, data=data)