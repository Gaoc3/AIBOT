import requests.api as req
from typing import Optional , Union
def get_lyrics_by_request_param(param:str,title:str,artist:Optional[str]=None,duration:Optional[str]=None):
        if param == '/lyrics/GetLyrics':
            r = req.get(url=f'https://mtskyhazoki.pythonanywhere.com/{param}?q={title}&srt=true').json()
        elif param == '/lyrics/GetLyrPrecisily':
             r = req.get(url=f'https://mtskyhazoki.pythonanywhere.com/{param}?t={title}&a={artist}&duration={duration}&srt=false').json()
        return r
