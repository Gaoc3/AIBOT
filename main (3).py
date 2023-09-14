#import os ; os.system('pip install gtts bardapi edgegpt')
import requests
from time import sleep
import telebot , random
from telebot import types
from telebot.types import  InputMedia
from icrawler.builtin import GoogleImageCrawler
import gtts, os, re, io, pytube
import  glob
#os.system('ls /home/runner/api/')
#os.chdir('/home/runner/api/musics/')
from ordered_set import OrderedSet
from youtubesearchpython import VideosSearch
from youtubesearchpython import VideosSearch
import re, yt_dlp
from yt_dlp import *
from PIL import Image
from pytesseract import image_to_string
import urllib
from datetime import datetime
from bardapi import Bard
import asyncio, json
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle, Path
from EdgeGPT.EdgeUtils import Query, Cookie
import speech_recognition as sr
import pydub
import flask
from flask import Flask
admin_id = 5001475594
api_keys = ['3c24352408ccf290acd2a9adbaa0e78439beb1d61dbf3b9aba6baf62f622625d16465bad8ad71c2a2a630ec5eacbf333']
token = os.environ['BARD_API_KEY']
bot_token = os.environ['TELE_API_KEY']
#API_URL = os.environ['API_URL']
#API_KEY = os.environ['API_KEY']
bard = Bard(token=token)
askforadmin = [
    '.سؤال من هو مطورك؟', '.سؤال من هو صانعك؟', '.سؤال المطور',
    '.سؤال المبرمج', '.سؤال هو مبرمجك؟', '.سؤال من هو مبرمجك',
    '.سؤال من هو مطورك', '.سؤال من هو صانعك', '.سؤال من هو مطورك؟'
]
# توليد الوقت الحالي بتنسيق UTC
bot = telebot.TeleBot(bot_token,num_threads=900,threaded=True)
id_from_save = []
#async def get_bard_answer(text):
#    return await bard.get_answer(text)

# تحويل استدعاء bard.speech إلى كائن
#async def get_bard_speech(text):
#    return await bard.speech(input_text=text)

@bot.message_handler(commands=['start'])
def  StartAI(AI):
    username = AI.from_user.first_name
    user_id = AI.from_user.id
    cap =f''' 🤖 أهــلاً أيـهـا الـمُـسـتَـخـدِم [{username}](tg://user?id={user_id}) ،
أَنـا بُـوت الـذَكـاءِ الاصْطِـنَاعِي، يـُمـكِـنُـنِـي تَـقـديم الـخَـدمـاتِ الـتَـالـيـةِ لَـكَ:

🔎 `.جلب` + اسـم الـشـخـص أو الـشـيء: لأجـلـب لـك صـوٌرًا جـمـيـلـة مـن الـأنـتـرنـت.

🎥 `.بحث` + الـشـيء الـذي تـريـد: لأبـحـث لـك في الـيـوتـيـوب وأقـدم لـك مـلـف صـوتـي أو فيـديـو.

🖼️ `.صنع` + وصـف الـصـوٌرة بالـإنـجـلـيـزية: لأصـنـع لـك صـوٌرة تـلـيق بذوقـك ووصـفِـك.

🚫 `.ازالة` (يُرجـى وضـع هـذا الـأمـر في وصـف الـصـوٌرة قـبـل إرسـالهـا لـي وسـأقـوم بإزالـة أي حقـوق أو نـص فيـهـا).

🔴 - إضغط على الأمر في النَص لِلنَسخِ ،

أتـمـنـى لـك يـومًا سـعـيـدًا ومـلـيـئًا بالإبـداع ✨.
'''
    if AI.chat.type == 'private':
      bot.send_message(AI.chat.id,cap,reply_to_message_id=AI.message_id,parse_mode='Markdown')
    elif AI.from_user.id != admin_id:
        bot.forward_message(admin_id,AI.chat.id,message_id=AI.message_id)
@bot.message_handler(func=lambda m: True)
def mtts(m):
  if m.text.split()[0] == '.سؤال' and m.text not in askforadmin:
    current_time = datetime.utcnow().strftime('%Y%m%dT%H%M%S')
    mttsgen = m.text.split('.سؤال')[1]
    speech_answer = bard.get_answer(
        mttsgen.replace('حسين', 'google').replace(
            'حُسين',
            'Google'))['content'].replace('بارد', 'مُساعِدُ مِتسكي').replace(
                'google', 'حُسَينْ').replace('Google', 'حُسَينْ').replace(
                    'Google هي التي طورتني', 'حُسَينْ هو الذي طَورني').replace(
                        'google هي التي طورتني',
                        'حُسَينْ هو الذي طَورني').replace(
                            'هي التي طورتني', 'هو الذي طَوَرَنيْ').replace(
                                'طورتني', 'طَوَرَنيْ').replace(
                                    'طورتني شركة', 'طَوَرَنيْ').replace(
                                        'بواسطة شركة', 'طَوَرَنيْ').replace(
                                            'لقد طورتني شركة Google',
                                            'طَوَرَنيْ').replace(
                                                'شركة Google', '')
    speech_answer_ = speech_answer.replace('نعم انا', 'لا ، انا').replace(
        'نعم لقد طَوَرَنيْ', 'لا ، لقد طَوَرَنيْ')
    resper = bard.speech(input_text=speech_answer_)
    print(resper)
    ms = f'mtsky.sensei-{current_time}.mp3'
    #tts_open_wirte = open(ms,'wb').write(bytes(resper['audio']))
    #tts_open = open(ms,'rb')
    bot.send_voice(m.chat.id,
                   voice=io.BytesIO(resper['audio']),
                   reply_to_message_id=m.message_id)
    #tts_open.close()
    #os.remove(f'{ms}')
  if m.text in askforadmin:
    current_time = datetime.utcnow().strftime('%Y%m%dT%H%M%S')
    mttsgen = re.match(".سؤال (.*?)$", m.text).group(1).strip()
    speech_answer = 'My Developer named Mitsky Sensei is the one who programmed me, developed me, and trained me on a huge number of databases, and trained me to analyze and understand them.'
    resper = bard.speech(input_text=speech_answer)
    print(resper)
    ms = f'mtsky.sensei-{current_time}.mp3'
    tts_open_wirte = open(ms, 'wb').write(bytes(resper['audio']))
    tts_open = open(ms, 'rb')
    bot.send_voice(m.chat.id,
                   voice=tts_open,
                   caption=mttsgen,
                   reply_to_message_id=m.message_id)
    tts_open.close()
    os.remove(f'{ms}')
  if m.text == 'آمنت بالحسين' or m.text == 'امنت بالحسين' or m.text == 'امنت':
    with open(
        '/sdcard/Siilawy - Yama (Official Music Video)  ياما.mp4',
        'rb',
    ) as OpenFile:
      bot.send_video(m.chat.id, video=OpenFile)

    #audio = open('C:/Users/mtsky/Downloads/قصيدة-امنت-بالحسين-بصوت-الفنان-صاحب-شاكر.mp3','rb')
    #bot.send_voice(m.chat.id,voice=audio)

  if m.text.split()[0] == '.كود':
    mttcode = re.match(r'\.سؤال\s+(.*(?:\n.*)*)', m.text).group(1)
    print(mttcode)
    q = Query(
        prompt=mttcode,
        style="creative",  # or: 'balanced', 'precise'
        cookie_files="bing_cookies_.json")
    print(q.code)
    bot.send_message(
        m.chat.id,
        f'Code:\n{q.code.replace("مرحبًا ، هذا بينج","مرحبًا ، انا MitskyBot").replace("مرحبًا ، هذا بينغ","مرحبًا ، انا MitskyBot").replace("مرحبا ، هذا بينغ","مرحبًا ، انا MitskyBot").replace("مرحبا ، هذا بينج","مرحبًا ، انا MitskyBot").replace("بينغ","MitskyBot").replace("بينج","MitskyBot").replace("Hello, this is Bing","Hello, Im MitskyBot").replace(": https://www.bing.com/search?q=python+programming+language","").replace("Bing","MitskyBot")}',
        reply_to_message_id=m.message_id)
  msg = m.text
  start_command(m)


def start_command(m):
  if m.text == '.تحويل':
    try:
      id_from_save.remove(m.from_user.id)
    except ValueError as e:
      print(e)
    msg_send = '''↫ أرسل الصورة الّتي تريد أن أحولها إلى نص ..
↫ يجب أن تكون باللغة العربية أو الإنجليزية .'''
    bot.reply_to(m, msg_send)
    bot.register_next_step_handler(m, image_to_text_request)
    id_from_save.append(m.from_user.id)

  if m.text.split()[0] == '.بحث':
    max_views = 1500
    lis = []
    Inlinebotoun = types.InlineKeyboardMarkup(row_width=1)
    querytext = m.text.split('.بحث')[1]  #.replace('*','')
    print(querytext)
    videos_search = VideosSearch(querytext, limit=10)
    for video in videos_search.result()['result']:
      views = int(video['viewCount']['text'].replace(',',
                                                     '').replace('views', ''))
      video_title = video['title']
      video_duration = video['duration']
      time_parts = video_duration.split(':')
      total_seconds = 0

      if len(time_parts) == 3:  # إذا كان هناك ساعات
        hours, minutes, seconds = map(int, time_parts)
        total_seconds = (hours * 3600) + (minutes * 60) + seconds
        pass

      elif len(time_parts) == 2:  # إذا كانت دقائق وثوانٍ فقط
        minutes, seconds = map(int, time_parts)
        total_seconds = (minutes * 60) + seconds
        if views >= max_views and total_seconds <= 950:
          if len(lis) == 4: break
          #max_views = views
          best_video_id = video['id']
          best_video_title = video['title']
          print(video['title'], '\n', total_seconds)
          lis.append(best_video_id)
          #print(f"Video Title: {video_title}")
          #print(f"Duration in Seconds: {total_seconds}")
          tubebot = types.InlineKeyboardButton(
              f'{best_video_title}',
              callback_data=f'url:{best_video_id}:{video_duration}')
          Inlinebotoun.add(tubebot)
    bot.send_message(m.chat.id,
                     text=f'⇜ البحث ~ {querytext}',
                     reply_to_message_id=m.message_id,
                     reply_markup=Inlinebotoun)                     
  if m.text.split()[0] == '.جلب':
    try:
        Queer = m.text.split('.جلب')[1]
        google_crawler = GoogleImageCrawler(
        feeder_threads=25,
        parser_threads=25,
        downloader_threads=30,
        storage={'root_dir': ''})
        google_crawler.crawl(keyword=Queer+'FullHD',overwrite=True, offset=0, max_num=20,
        min_size=None , max_size=None, file_idx_offset=1)    
        media_list = []
        folder_path = 'musics/'
        globa = glob.glob('*.png') + glob.glob('*jpeg') + glob.glob('*.jpg')
        random_pic = random.sample(globa, 10)
        opner = open(random_pic[0],'rb')
        s_t = InputMedia(type='photo',media=opner,caption=f'⇜ الجَلب ~{Queer}')
        media_list.append(s_t)       
        for file in random_pic[1:10]:
            with open(file, 'rb') as image_file:
                image_data = image_file.read()
                media = InputMedia(type='photo', media=image_data)
                media_list.append(media)
        
        bot.send_media_group(m.chat.id, media=media_list,reply_to_message_id=m.message_id)
        dirext = glob.glob('*.png') + glob.glob('*.jpg') + glob.glob('*.jpeg')
        print(dirext)
        for dir in dirext:
            paths = os.path.abspath(dir)
            os.remove(paths)
    except Exception as e: print(e)  
    
  if m.text.split()[0] == '.صنع' :
       msg = m.text.split('.صنع')[1]
       image_gen = []
       for api_key in api_keys:
        try:
            for i in range(3):
                r = requests.post('https://clipdrop-api.co/text-to-image/v1',
                    files={
                        'prompt': (None,msg, 'cinematic , realistic , 8K')
                    },
                    headers={'x-api-key': api_key}
                )
                
                if b"error" in r.content:
                    print(f"Error in response with API key: {api_key}")
                    continue  # Continue to the next API key
                
                Add_Input = InputMedia(type='photo', media=r.content)
                image_gen.append(Add_Input)
                print(f"Image {i + 1} saved with API key: {api_key}")
    
            image_gen[0].caption = f'الصُنع {msg}' 
            bot.send_media_group(m.chat.id, media=image_gen, reply_to_message_id=m.message_id)
            get_pics = glob.glob('*.png')
            
            for dir in get_pics:
                get_dir = os.path.abspath(dir)
                os.remove(get_dir)           
    
            break  # If everything was successful, exit the loop
        except Exception as e:
            print(f'Filled API KEY REQUEST : {e}')
            continue
    

#if (r.ok):                                                         
def image_to_text_request(m):
  if m.content_type == 'photo' and m.from_user.id in id_from_save:
    process_image(m)
    print(id_from_save)
  elif m.from_user.id not in id_from_save and m.content_type != 'photo':
    bot.register_next_step_handler(m, image_to_text_request)
  elif m.from_user.id in id_from_save and m.content_type != 'photo':
    bot.reply_to(
        m,
        '''↫ عفوًا ، يجب عليك إرسال صورة و تحديد اللغة المُراد أستخراجها في الوصف الخاص به ، 
وليس أن تُرسِلَ {} \.\.
↫ يجب أن تكون :
\~ باللغة العربية \[ `ara` \]
\~ أو الإنجليزية \[ `eng` \]
\~ أو الفَرَنسِيةْ \[ `fr` \] \.
'''.format(m.content_type),
        parse_mode='MarkdownV2')
    bot.register_next_step_handler(m, image_to_text_request)
  elif m.from_user.id not in id_from_save and m.content_type == 'photo':
    bot.register_next_step_handler(m, image_to_text_request)
    #bot.reply_to(m, '''↫ عفوًا، يجب عليك إرسال الصورة وتحديد اللغة في وصف الوصف  وليس {} ..


#↫ يجب أن تكون باللغة العربية أو الإنجليزية .'''.format(m.content_type))


def process_image(m):
  print('Starting ...')
  langsupport = ['ara', 'eng', 'fr']
  print(m.photo)
  cap = m.caption
  print(f'××× {cap} ×××')
  photo = m.photo[-1].file_id
  file = bot.get_file_url(photo)
  im = urllib.request.urlopen(file).read()
  PIL_OPEN = Image.open(io.BytesIO(im))
  if cap in langsupport:
    pytesseract_text = image_to_string(PIL_OPEN, lang=cap)
    bot.reply_to(m, pytesseract_text)
    id_from_save.clear()
  elif cap not in langsupport:
    msg = '''↫ عفوًا، يجب عليك إرسال صورة و بوصفها اللغة المُراد أستخراجها من النص.
        
مِثال : الصورة + ara ..

↫ يجب أن تكون باللغة العربية [ara] أو الإنجليزية [eng] أو الفَرَنسِيةْ [fr] بدون أحرُفٍ كَبيرةْ.'''
    bot.reply_to(m, msg)
    bot.register_next_step_handler(m, image_to_text_request)

@bot.message_handler(content_types=['photo'])
def Surveying_traces_of_crime(crime):
          if crime.caption == '.ازالة' :
              phoot_file_id = crime.photo[-1].file_id
              get_photo = bot.get_file_url(phoot_file_id)
              #current_time = datetime.utcnow().strftime('%Y%m%dT%H%M%S')
              bytes_from_url = urllib.request.urlopen(get_photo)
              #image_name = f'image_{current_time}.jpg'
              #down_photo = bot.download_file(get_photo.file_path)
              for api_key in api_keys:
                  try:
                      r = requests.post('https://clipdrop-api.co/remove-text/v1',
      files = {
        'image_file': ('image.jpg',bytes_from_url , 'image/jpeg')
        },
      headers = { 'x-api-key': api_key}
    )
                      bot.send_photo(crime.chat.id,photo=r.content,reply_to_message_id=crime.message_id)    
                      break
                  except requests.exceptions.RequestException as e:
                          print(e)
                          continue
@bot.message_handler(content_types=['voice'])
def voice_processing(message):
  print('Starting ...')
  current_time = datetime.utcnow().strftime('%Y%m%dT%H%M%S')
  mwav = f'mtsky.sensei-{current_time}'
  file_info = bot.get_file(message.voice.file_id)
  downloaded_file = bot.download_file(file_info.file_path)
  with open(mwav + '.ogg', 'wb') as new_file:
    new_file.write(downloaded_file)
  r = sr.Recognizer()
  conv = pydub.AudioSegment.from_ogg(f'{mwav}.ogg')
  conv.export(f'{mwav}.wav', format='wav')
  with sr.AudioFile(f'{mwav}.wav') as source:
    #r.adjust_for_ambient_noise(source)

    print("Please say something")

    audio = r.record(source)

    print("Recognizing Now .... ")

    # recognize speech using google

    try:
      print(audio)
      text_from_speech = r.recognize_google(audio, language='ar')
      speech_answer = bard.get_answer(text_from_speech)
      print(speech_answer['content'])
      resper = bard.speech(input_text=speech_answer)
      tts_open_wirte = open(mwav + '-.wav', 'wb').write(bytes(resper['audio']))
      tts_open = open(mwav + '-.wav', 'rb')
      bot.send_voice(message.chat.id,
                     voice=tts_open,
                     caption=text_from_speech,
                     reply_to_message_id=message.message_id)
      tts_open.close()
      #os.remove(mwav+'.wav')
      #os.remove(mwav+'-.wav')
      print("Audio Recorded Successfully \n ")

    except Exception as e:
      print("Error :  " + str(e))


@bot.callback_query_handler(func=lambda call: True)
def Call_Download(call):
  msg_id = []
  if call.data.split(':')[0] == 'url':
    video_id = call.data.split(':')[1]
    video_duration = ':'.join(call.data.split(':')[2:])
    print(video_duration)
    print(video_id)
    chat_from_call = call.message.chat.id
    reply_msg_id = call.message.message_id
    video_url = f'https://www.youtube.com/watch?v={video_id}'
    ydl = yt_dlp.YoutubeDL()
    info_dict = ydl.extract_info(video_url, download=False)
    video_title = info_dict.get('title')
    video_thumbnail = bytes(requests.get(info_dict['thumbnail']).content)
    print(video_thumbnail)
    InlineKeyboard = types.InlineKeyboardMarkup(row_width=2)
    down_button1 = types.InlineKeyboardButton(
        text='📹  فيديو', callback_data=f'vid:{video_id}:{video_duration}')
    down_button2 = types.InlineKeyboardButton(
        text='️🎧 ملف صوتي', callback_data=f'mu:{video_id}:{video_duration}')
    down_button3 = types.InlineKeyboardButton(text='~ المُطَورْ .',
                                              url='tg://user?id=5001475594')
    InlineKeyboard.add(down_button1, down_button2, down_button3)
    bot.delete_message(chat_from_call, call.message.message_id)
    try:
      bot.send_photo(
          chat_from_call,
          photo=video_thumbnail,
          caption=video_title,
          reply_to_message_id=call.message.reply_to_message.message_id,
          reply_markup=InlineKeyboard)
    except telebot.apihelper.ApiTelegramException:
      bot.send_message(chat_from_call,
                       text=video_title,
                       reply_markup=InlineKeyboard)
  elif call.data.split(':')[0] == 'vid':
    chat_from_call = call.message.chat.id
    reply_msg_id = call.message.message_id
    video_id = call.data.split(':')[1]
    video_duration = ':'.join(call.data.split(':')[2:])
    Keyboard = types.InlineKeyboardMarkup(row_width=1)
    Bottun = types.InlineKeyboardButton('~ المُطَورْ',
                                        url='tg://user?id=5001475594')
    Keyboard.add(Bottun)
    try:
      edit_cap = bot.edit_message_caption(chat_id=call.message.chat.id,
                                          message_id=call.message.message_id,
                                          caption='<•> جَاري التَحميل ...',
                                          reply_markup=Keyboard)
    except:
      edit_cap0 = bot.edit_message_text(text='<•> جَاري التَحميل ...',
                                        chat_id=chat_from_call,
                                        message_id=call.message.message_id,
                                        reply_markup=Keyboard)

    try:
      video_url = f'https://www.youtube.com/watch?v={video_id}'

      with yt_dlp.YoutubeDL({
          "format":
          "bestvideo[ext=mp4]+bestaudio[ex=m4a]/mp4",
"outtmpl": '/home/runner/api/musics/' + "sillway.%(ext)s"
      }) as ydl:
        info = ydl.extract_info(video_url, download=True)
        vid_file = ydl.prepare_filename(info)
        #print('\n\n' + vid_file + '\n\n')
        #ydl.process_info(info)
        artist = info['uploader']
        url_thumb = info['thumbnail']
        print(url_thumb)
        thumb = bytes(requests.get(url_thumb).content)
        thumbnail_write = open('thumb.jpg',
                               'wb').write(thumb)
        image_thumb = Image.open('thumb.jpg')
        image_thumb.resize((320,320))
        image_thumb.save('thumb.jpg', 'jpg', quality=100)
        print(f"{os.path.getsize('thumb.jpg') / 1024} KB")
        title = info['title']
        duration = info['duration']
        thumbnail = open('thumb.jpg', 'rb')
        #with open(audio_file,"rb") as f:
        #print(f.__format__)
        down_path = vid_file
        vid = open(down_path, 'rb')
        bot.send_chat_action(call.message.chat.id, 'upload_video')
        bot.send_video(
            chat_from_call,
            video=vid,
            caption=f"[♧ ~ ︎ {video_duration} ⏳️]({video_url}) ",
            thumbnail=thumbnail,
            duration=duration,
            reply_to_message_id=call.message.reply_to_message.message_id,
            parse_mode='Markdown',
            reply_markup=Keyboard)
        os.remove(down_path)
        os.remove('/home/runner/api/musics/thumb.jpg')
        print('Done remove...')
      try:
        bot.edit_message_caption(caption='● ~ تَم إكتِمَال التَحميل 🎧 .',
                                 chat_id=chat_from_call,
                                 message_id=edit_cap.message_id,
                                 reply_markup=Keyboard)
      except Exception as e:
        print(e)
        bot.edit_message_text(text='● ~ تَم إكتِمَال التَحميل 🎧 .',
                              chat_id=chat_from_call,
                              message_id=edit_cap0.message_id,
                              reply_markup=Keyboard)
    except Exception as e:
      print(e)
      try:
        bot.edit_message_caption(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            caption=
            '<•> عُذرًا ، لا يُمكن تَحميل الفيديو بسبب سياسة الفئة العُمرية لليوتيوب .',
            reply_markup=Keyboard)
      except:
        bot.edit_message_text(
            text=
            '<•> عُذرًا ، لا يُمكن تَحميل الفيديو بسبب سياسة الفئة العُمرية لليوتيوب .',
            chat_id=chat_from_call,
            message_id=call.message.message_id,
            reply_markup=Keyboard)
  elif call.data.split(':')[0] == 'mu':
    chat_from_call = call.message.chat.id
    reply_msg_id = call.message.message_id
    video_id = call.data.split(':')[1]
    video_duration = ':'.join(call.data.split(':')[2:])

    Keyboard = types.InlineKeyboardMarkup(row_width=1)
    Bottun = types.InlineKeyboardButton('~ المُطَورْ',
                                        url='tg://user?id=5001475594')
    Keyboard.add(Bottun)
    try:
      edit_cap = bot.edit_message_caption(chat_id=call.message.chat.id,
                                          message_id=call.message.message_id,
                                          caption='<•> جَاري التَحميل ...',
                                          reply_markup=Keyboard)
      msg_id.append(edit_cap.message_id)
    except:
      edit_cap0 = bot.edit_message_text(text='<•> جَاري التَحميل ...',
                                        chat_id=chat_from_call,
                                        message_id=call.message.message_id,
                                        reply_markup=Keyboard)
      msg_id.append(edit_cap0)

    try:
      video_url = f'https://www.youtube.com/watch?v={video_id}'

      with yt_dlp.YoutubeDL({
          "format": "bestaudio[ext=m4a]",
          "audio-format": "m4a",
          "audio-quality": "320K+",
          "audio-sample-rate": "48000+",
          "outtmpl":
          '/home/runner/api/musics/' + "sillway.%(ext)s"
      }) as ydl:
        info = ydl.extract_info(video_url, download=True)
        audio_file = ydl.prepare_filename(info)
        print('\n\n' + audio_file + '\n\n')
        #ydl.process_info(info)
        artist = info['uploader']
        url_thumb = info['thumbnail']
        thumb = bytes(requests.get(url_thumb).content)
        title = info['title']
        duration = info['duration']
        print(duration)
        #with open(audio_file,"rb") as f:
        #print(f.__format__
        down_path = audio_file
        audio = open(down_path, 'rb')
        bot.send_chat_action(call.message.chat.id, 'upload_audio')
        bot.send_audio(
            chat_from_call,
            audio=audio,
            caption=f"[♧ ~ ︎ {video_duration} ⏳️]({video_url}) ",
            thumb=thumb,
            title=title,
            performer=artist,
            thumbnail=thumb,
            duration=duration,
            reply_to_message_id=call.message.reply_to_message.message_id,
            parse_mode='Markdown',
            reply_markup=Keyboard)
        os.remove(down_path)
      try:
        bot.edit_message_caption(chat_id=call.message.chat.id,
                                 message_id=msg_id[0],
                                 caption='● ~ تَم إكتِمَال التَحميل 🎧 .',
                                 reply_markup=Keyboard)
      except Exception as e:
        print(e)
        bot.edit_message_text(text='● ~ تَم إكتِمَال التَحميل 🎧 .',
                              chat_id=chat_from_call,
                              message_id=edit_cap0.message_id,
                              reply_markup=Keyboard)
    except Exception as e:
      print(e)
      try:
        bot.edit_message_caption(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            caption=
            '<•> عُذرًا ، لا يُمكن تَحميل الفيديو بسبب سياسة الفئة العُمرية لليوتيوب .',
            reply_markup=Keyboard)
      except:
        bot.edit_message_text(
            text=
            '<•> عُذرًا ، لا يُمكن تَحميل الفيديو بسبب سياسة الفئة العُمرية لليوتيوب .',
            chat_id=chat_from_call,
            message_id=call.message.message_id,
            reply_markup=Keyboard)

@bot.edited_message_handler(func=lambda message : True)
def edited(message):
    if message.text.split()[0] == '.بحث':
            max_views = 1500
            lis = []
            Inlinebotoun = types.InlineKeyboardMarkup(row_width=1)
            querytext = message.text.split('.بحث')[1]  #.replace('*','')
            print(querytext)
            videos_search = VideosSearch(querytext, limit=10)
            for video in videos_search.result()['result']:
              views = int(video['viewCount']['text'].replace(',',
                                                             '').replace('views', ''))
              video_title = video['title']
              video_duration = video['duration']
              time_parts = video_duration.split(':')
              total_seconds = 0
        
              if len(time_parts) == 3:  # إذا كان هناك ساعات
                hours, minutes, seconds = map(int, time_parts)
                total_seconds = (hours * 3600) + (minutes * 60) + seconds
                pass
        
              elif len(time_parts) == 2:  # إذا كانت دقائق وثوانٍ فقط
                minutes, seconds = map(int, time_parts)
                total_seconds = (minutes * 60) + seconds
                if views >= max_views and total_seconds <= 950:
                  if len(lis) == 4: break
                  #max_views = views
                  best_video_id = video['id']
                  best_video_title = video['title']
                  print(video['title'], '\n', total_seconds)
                  lis.append(best_video_id)
                  #print(f"Video Title: {video_title}")
                  #print(f"Duration in Seconds: {total_seconds}")
                  tubebot = types.InlineKeyboardButton(
                      f'{best_video_title}',
                      callback_data=f'url:{best_video_id}:{video_duration}')
                  Inlinebotoun.add(tubebot)
            bot.send_message(message.chat.id,
                             text=f'⇜ البحث ~ {querytext}',
                             reply_to_message_id=message.message_id,
                             reply_markup=Inlinebotoun)
bot.remove_webhook()                
server = flask.Flask(__name__)
@server.route("/bot", methods=['POST'])
def getMessage():
  bot.process_new_updates([
      telebot.types.Update.de_json(flask.request.stream.read().decode("utf-8"))
  ])
  return "!", 200


@server.route("/")
def webhook():
  bot.remove_webhook()
  link = 'https://' + str(flask.request.host)
  bot.set_webhook(url=f"{link}/bot")
  return "This api for Mitsky Download Bot", 200


server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
server = flask.Flask(__name__)
print(server)
