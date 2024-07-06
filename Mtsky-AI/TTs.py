import requests
from base64 import b64decode
def aduioStream(prompet,format) -> bytes:
    headers = {
        'accept': '*/*',
        'accept-base64': 'true',
        'accept-language': 'en,en-US;q=0.9,ar;q=0.8,en-GB;q=0.7,ar-IQ;q=0.6,zh-CN;q=0.5,zh-MO;q=0.4,zh;q=0.3,ar-AE;q=0.2',
        'content-type': 'application/json; charset=UTF-8',
        'origin': 'https://speechify.com',
        'priority': 'u=1, i',
        'referer': 'https://speechify.com/text-to-speech-online/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'x-speechify-client': 'EmbeddableSpeechify',
        'x-speechify-client-version': '0.1.301',
    }

    json_data = {
        'audioFormat': format,
        'paragraphChunks': [
            prompet,
        ],
        'voiceParams': {
            'name': 'hala',
            'engine': 'neural',
            'languageCode': 'ar-AE',
        },
    }

    return b64decode(requests.post('https://audio.api.speechify.com/generateAudioFiles', headers=headers, json=json_data).json()['audioStream'])