import os
import time
import requests
import urllib
import magic
import re
import json
import random
from urllib.parse import quote, urlparse
from posixpath import basename


def __init__():
    pass


def _create_directory(_directory):
    """
    Create directory to save images
    :param _directory:
    :return:
    """
    try:
        if not os.path.exists(_directory):
            os.makedirs(_directory)
            time.sleep(0.2)
    except OSError as e:
        if e.errno != 17:
            raise
        pass
    return


def _download_page(url):
    try:
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        }
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req)
        respData = str(resp.read())
        return respData
    except Exception as e:
        print(e)
        exit(0)


def download(keywords, limit, directory='images', extensions={'.jpg', '.png', '.jpeg'}):
    """
    Download images from Google Images
    :param keywords:
    :param limit:
    :param directory:
    :param extensions:
    :return:
    """
    keyword_to_search = [str(item).strip() for item in keywords.split(',')]
    main_directory = directory

    # Create main directory
    _create_directory(main_directory)

    all_images_dict = {}
    all_images_list = []
    for keyword in keyword_to_search:
        keyword_images_list = []

        i = 0
        while i < limit:
            url = 'https://www.google.com/search?q=' + quote(
                keyword.encode('utf-8')) + '&biw=1536&bih=674&tbm=isch&sxsrf=ACYBGNSXXpS6YmAKUiLKKBs6xWb4uUY5gA:1581168823770&source=lnms&sa=X&ved=0ahUKEwioj8jwiMLnAhW9AhAIHbXTBMMQ_AUI3QUoAQ'
            raw_html = _download_page(url)

            # Define the pattern for finding image URLs
            pattern = r'"https://[^"]+\.(?:jpg|png|ico|gif|jpeg)"'

            # Find all matches of the pattern in the raw HTML
            matches = re.findall(pattern, raw_html)

            # Randomly select a match (image URL)
            random_match = random.choice(matches) if matches else None

            # Check if the selected image is a duplicate or not related to the search
            if random_match and random_match not in keyword_images_list:
                object_raw = random_match.strip('"')

                # Extract file name from URL
                parsed_url = urlparse(object_raw)
                file_name = basename(parsed_url.path)
                
                try:
                    
                    r = requests.get(object_raw, allow_redirects=True, timeout=1)
                    byte = bytes(r.content)
                    if 'html' not in str(r.content):
                        mime = magic.Magic(mime=True)
                        file_type = mime.from_buffer(r.content)
                        file_extension = f'.{file_type.split("/")[1]}'
                        if file_extension not in extensions:
                            raise ValueError()
                        all_images_list.append({
                            'file_name': file_name,
                            'url': object_raw,
                            'bytes': byte,
                            'type': file_type,
                        })
                    else:
                        i -= 1
                except Exception as e:
                    i -= 1

                i += 1
    all_images_dict[keyword] = all_images_list
    return all_images_dict
    # with open('iamges.json','w+',encoding='utf-8') as JSONFile:
    #     json.dump(all_images_dict,JSONFile,ensure_ascii=False,indent=4)
    

