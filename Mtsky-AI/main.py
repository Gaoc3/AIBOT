# ---- Dyna AI ----
import random
import requests , flask , telebot , pydub , urllib , re , yt_dlp , glob , threading , lyr , speech_recognition as sr , io , os , random 
from time import sleep
from telebot import types
from telebot.types import  InputMedia 
from pytube import YouTube as yt
from youtubesearchpython import VideosSearch
from yt_dlp import *
from PIL import Image
from g4f.client import Client
from flask import Flask
from telebot import formatting
from TTs import audioTTs
from code_gen import CodeGenerator
from imogi import download
from g4f.Provider.GeminiPro import GeminiPro
from g4f.cookies import set_cookies
from datetime import timedelta
admin_id = os.environ['ADMIN_ID'] = "5624908798"
cookies = {"_ga":"GA1.1.833913630.1711448840","HSID":"AxXXj9tjLVUjaHD-F","SSID":"ArjW4fhyHMdbEFG06","APISID":"yOB2chWd-j2quN9P/ANrBb1g9jetDi1vj8","SAPISID":"sE1p2z0ShiM3WpCl/A3DEKxwOuP38cWL8i","__Secure-1PAPISID":"sE1p2z0ShiM3WpCl/A3DEKxwOuP38cWL8i","__Secure-3PAPISID":"sE1p2z0ShiM3WpCl/A3DEKxwOuP38cWL8i","SEARCH_SAMESITE":"CgQI4JoB","SID":"g.a000jAhgn7pRrLIeELMAGE0IRVyiCu9nPEPn-RRY1XkR0Hgex8P3ybZTYdMEpOnomggLXdxzyQACgYKAZgSAQASFQHGX2MiZBC-fOj5btdEQYFvrXxgBBoVAUF8yKqJ35laAWyssnJAaH3f1pjV0076","__Secure-1PSID":"g.a000jAhgn7pRrLIeELMAGE0IRVyiCu9nPEPn-RRY1XkR0Hgex8P3-vsFBbeCglu1w67Kq8ofHgACgYKAYUSAQASFQHGX2MiAIXqPtt4MRfh8FolKoaE0hoVAUF8yKokqvt-V-wWpzLDe3I4QIJU0076","__Secure-3PSID":"g.a000jAhgn7pRrLIeELMAGE0IRVyiCu9nPEPn-RRY1XkR0Hgex8P3JYra6m0i04u8Slhq3N9CjQACgYKAdkSAQASFQHGX2MiCSaTeTdDw9GigNltSNHuzxoVAUF8yKoc3HGjTknKpD-uH7IbN7zY0076","1P_JAR":"2024-04-27-05","AEC":"AQTF6HyvhXkR4NXc8VCaAPmd0Gqz-LfCTz3LGjzIt7XW8WHuKG7Va7503Q","NID":"513","__Secure-1PSIDTS":"sidts-CjEBLwcBXMalk63u37mJpPOwfv72lEbvUlz26OZ1INwqCw3LutBGmqb_q2xzomXTy_bcEAA","__Secure-3PSIDTS":"sidts-CjEBLwcBXMalk63u37mJpPOwfv72lEbvUlz26OZ1INwqCw3LutBGmqb_q2xzomXTy_bcEAA","_ga_WC57KJ50ZZ":"GS1.1.1714356423.5.1.1714356435.0.0.0","SIDCC":"AKEyXzU2Vpb-Z4OrK-G6HIXpkSfC3m-cPsI5WEaDO5I2lJQt_thXsFRFb8wDlDGlPo2gvzne7g","__Secure-1PSIDCC":"AKEyXzUJnFgpfTMEgQ37tegJkbkpJmCio4vi9TXAzaZrtjzem0-2MqHcWyIvx_Xdbxx8aWWRew","__Secure-3PSIDCC":"AKEyXzVvGJj_VuvBdirmRQsfUJYCk9tXTISNZLPtfmBfoD0pUAqR0I_3z5-x-M7d4gbute0Psw"}
bot_token = os.environ['BOT_API'] = '5394637411:AAGn7Mx1DrjC6jz1g-ZAP_zkf1kH_S2vz6k'
#API_KEY = os.environ['API_KEY']
client = Client()
bot = telebot.TeleBot(bot_token,num_threads=10,threaded=True,colorful_logs=True)
id_from_save = [] 
class Gemini:
  def __init__(self, cookie=None):
     self.cookie = cookie
  def ReplacedContent(self , text) -> str:
    self.text = text
    new_answer = self.text.replace('حسين', 'google').replace('حُسين','Google').replace('بارد', 'مَرْيَمْْ').replace('google', 'حُسَينْ').replace('Google','حُسَين').replace(
                      'Google هي التي طورتني', 'حُسَينْ هو الذي طَورني').replace(
                          'google هي التي طورتني',
                          'حُسَينْ هو الذي طَورني').replace(
                              'هي التي طورتني', 'هو الذي طَوَرَنيْ').replace(
                                  'طورتني', 'طَوَرَنيْ').replace(
                                      'طورتني شركة', 'طَوَرَنيْ').replace(
                                          'بواسطة شركة', 'طَوَرَنيْ').replace(
                                              'لقد طورتني شركة Google',
                                              'طَوَرَنيْ').replace('شركة Google', '').replace('bard','مَرِيَمْ').replace('نعم انا', 'لا ، انا').replace(
          'نعم لقد طَوَرَنيْ', 'لا ، لقد طَوَرَنيْ').replace('*','').replace('جوجل','حُسين').replace('*','').replace('#','')
    return new_answer
  def Chat(self,prompt:str) -> str:
    self.prompt = prompt
    content = client.chat.completions.create(
    model='gemini',
    messages=[{"role": "user", "content": self.prompt}])
    return content.choices[0].message.content

  def Image(self,image:bytes,prompt:str) -> str:
    self.client = Client()
    self.prompt = prompt
    self.image = image
    response = client.chat.completions.create(
    model='',
    provider=GeminiPro,
    api_key='AIzaSyCc98nhK5Eh_ctLZq8QxCuPFqB9IjmlVsc',
    messages=[{"role": "user", "content": self.prompt + 'تكلم بالعربية'}],
    image=self.image 
    )
    return response.choices[0].message.content
set_cookies('.google.com', cookies)
Gemini = Gemini()

def convert_seconds(seconds):
    time_format = str(timedelta(seconds=seconds))
    parts = time_format.split(':')
    # استخراج الدقائق والثواني
    hours, minutes, seconds = parts
    # تحويل الدقائق والثواني إلى صيغة 4:09
    return f"{int(minutes)}:{seconds}"
@bot.message_handler(commands=['start'])
def  StartAI(AI):
    username = AI.from_user.first_name
    user_id = AI.from_user.id
    cap =f''' 🤖 أهــلاً أيـهـا الـمُـسـتَـخـدِم [{username}](tg://user?id={user_id}) ،
أَنَـا بُـوت الـذَكـاءِ الاصْـطِـنَاعِي ديـنـا، يـُـمـكِـنُـنِـي تَــقــديــم الـخَــدمــاتِ الـتَــالــيــةِ لَـكَ :
`دينا` + ســؤالــك او الـشـيء الــذي تــرغــب بــقـولــه لـهـا و ســوف تــرد عـلــيــك صـوتـيًـا.

🔎 `.جلب` + اسـم الـشَـخـص أو الـشـيء: لأجـلـب لـك صـوٌرًا جـمـيـلـة مـن الـأنـتـرنـت.

🎥 `.بحث` + الـشـيء الـذي تـريـد: لأبـحـث لـك في الـيـوتـيـوب وأقـدم لـك مـلـف صـوتـي أو فيـديـو.

`كود` + فكرة الكود + نوع اللغة المُراد كتابة الكود بهِ ، مِثَال :  كود آلة حاسبة بلغة البايثون.


🔴 - إضغط على الأمر في النَص لِلنَسخِ ،

أتـمـنـى لـك يـومًا سـعـيـدًا ومـلـيـئًا بالإبـداع ✨.
'''
    if AI.chat.type == 'private':
      bot.send_message(AI.chat.id,cap,reply_parameters=types.ReplyParameters(chat_id=AI.chat.id,message_id=AI.message_id,allow_sending_without_reply=True),parse_mode='Markdown')
    elif AI.from_user.id != admin_id:
      bot.forward_message(admin_id,AI.chat.id,message_id=AI.message_id)
@bot.message_handler(func=lambda m: True)
def mtts(m):
  if m.text.split()[0] == 'دينا':
    # current_time = datetime.().strftime('%Y%m%dT%H%M%S')
    Mtext = m.text.split('دينا')[1] + 'تكلم بالعربية وبدون روابط او صور'
    speech_answer = Gemini.ReplacedContent(Gemini.Chat(Mtext))
    print(speech_answer)
    resper = audioTTs(prompet=speech_answer)
    bot.send_voice(m.chat.id,
                   voice=resper,
                   reply_parameters=types.ReplyParameters(chat_id=m.chat.id,message_id=m.message_id,allow_sending_without_reply=True))

  if m.text.split()[0] == '.تحليل':
    try:
      id_from_save.remove(m.from_user.id)
    except ValueError as e:
       print(e)
    try:
      bot.send_message(m.chat.id,formatting.format_text(formatting.mbold('- أرسِل الصُورةَ مع الوَصفْ الذي تَرغب تحليله مِنهُ .')),parse_mode='MarkdownV2')
      bot.register_next_step_handler(m,Processing_image_for_analysis)
      id_from_save.append(m.from_user.id)
    except Exception as e : print(e)
  if m.text.split()[0] == 'كود':
    MCode = m.text.split('كود')[1]
    bot.send_message(m.chat.id,text=CodeGenerator(MCode),reply_parameters=types.ReplyParameters(chat_id=m.chat.id,message_id=m.message_id,allow_sending_without_reply=True),parse_mode='Markdown')
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
        if views >= max_views and total_seconds <= 1800:
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
                     reply_parameters=types.ReplyParameters(chat_id=m.chat.id,message_id=m.message_id,allow_sending_without_reply=True),
                     reply_markup=Inlinebotoun)
  if m.text.split()[0] == '.جلب':
    # try:
        media_list = []
        Queer = m.text.split('.جلب ')[1]
        data = download(Queer,limit=10)[Queer]#[Queer]
        print(data)
        bytes_list = [byte['bytes'] for byte in data]
        print(data)
        # globa = glob.glob('**/images/*.png', recursive=True) + glob.glob('**/images/*.jpg', recursive=True) + glob.glob('**/images/*.jpeg', recursive=True)
        random_img = random.sample(bytes_list, 10)
        imag_1 = random_img[0]
        s_t = InputMedia(type='photo',media=imag_1,caption=f'⇜ الجَلب ~{Queer}')
        media_list.append(s_t)
        for randomic in random_img[1:]:
                media = InputMedia(type='photo', media=randomic)
                media_list.append(media)
        bot.send_media_group(m.chat.id, media=media_list,reply_parameters=types.ReplyParameters(chat_id=m.chat.id,message_id=m.message_id,allow_sending_without_reply=True))
        # dirext = glob.glob('*.png') + glob.glob('*.jpg') + glob.glob('*.jpeg')
    # except Exception as e:print(e)

  if m.text.split()[0] == '.صنع' :
        pass
    #    msg = m.text.split('.صنع')[1]
    #    total = 0
    #    image_gen = []
    #    try:
    #       response = requests.post(
    #           'https://aitestkitchen.withgoogle.com/api/trpc/imageFx.generateImages',
    #           cookies=ImageGen.cookies,
    #           headers=ImageGen.headers,
    #           json=ImageGen.json_data,
    # )
    #       response_data = response.json()
    #       for i in response_data['result']['data']['json']['result']['imagePanels'][0]['generatedImages']:
    #          ii = base64.b64decode(i['encodedImage'])
    #          if b"error" in response.text:
    #                 print(f"Error in response")
    #                 break  # Continue to the next API key

    #          Add_Input = InputMedia(type=InputMediaPhoto, media=r.content)
    #          image_gen.append(Add_Input)
    #          print(f"Image {total} saved with API ")
    #          total += 1
    #          image_gen[0].caption = f'الصُنع {msg}'
    #       bot.send_media_group(m.chat.id, media=image_gen, reply_parameters=types.ReplyParameters(chat_id=m.chat.id,message_id=m.message_id,allow_sending_without_reply=True))
    #       get_pics = glob.glob('*.png')

  if m.text.split()[0] == '.ازالة':
      pass
def image_to_text_request(m):
  if m.content_type == 'photo' and m.from_user.id in id_from_save:
    process_image(m)
    print(id_from_save)
  elif m.from_user.id not in id_from_save and m.content_type != 'photo':
    bot.register_next_step_handler(m, image_to_text_request)
  elif m.from_user.id in id_from_save and m.content_type != 'photo':
    format_code_ara =  formatting.mcode('ara')
    format_code_eng = formatting.mcode('eng')
    format_code_fr = formatting.mcode('fr')
    text_part_1 = "↫ عفوًا، يجب عليك إرسال صورة وتحديد اللغة المُراد استخراجها في الوصف الخاص به،"
    format_text_1 = formatting.format_text(formatting.mbold(text_part_1))
    text_part_2 = f"وليس أن تُرسِلَ {m.content_type}"
    format_text_2 = formatting.format_text(formatting.mbold(text_part_2))
    text_part_3 = "↫يجب أن تكون : "
    format_text_3 = formatting.format_text(formatting.mbold(text_part_3))
    text_part_4 = "~ باللغة العربية"
    format_text_4 = formatting.format_text(formatting.mbold(text_part_4))
    text_part_5 = "~ أو الإنجليزية"
    format_text_5 = formatting.format_text(formatting.mbold(text_part_5))
    text_part_6 = "~ أو الفَرَنسِيةْ "
    format_text_6 = formatting.format_text(formatting.mbold(text_part_6))
    combined_text = f"{format_text_1} {format_text_2}\n{format_text_3}\n\n{format_text_4}[ {format_code_ara} ]\n{format_text_5} [ {format_code_eng } ]\n{format_text_6} [ {format_code_fr} ]"
    bot.reply_to(
        m, combined_text,
        parse_mode='MarkdownV2'
    )
    bot.register_next_step_handler(m, image_to_text_request)
  elif m.from_user.id not in id_from_save and m.content_type == 'photo':
    bot.register_next_step_handler(m, image_to_text_request)
    #bot.reply_to(m, '''↫ عفوًا، يجب عليك إرسال الصورة وتحديد اللغة في وصف الوصف  وليس {} ..


#↫ يجب أن تكون باللغة العربية أو الإنجليزية .'''.format(m.content_type))
#def choice_what_to_do(m):
#       bot.reply_to(m,formatting.format_text(formatting.mbold(f'و الآن مَاذا تُريد مني فِعلهُ ، ماذا احلل من الصورة و ماذا أستخرج لك مَثلا ؟ \n مثال : أعطني مَصدر الصورة n\ مثال آخر : حلل الصورة بأكملها \n قل ما تحب أن أحلل لك من الصورة و ما تريد أستخراجه ومعرفته عنها .')))
#       bot.register_next_step_handler(m,Processing_image_for_analysis)
def Processing_image_for_analysis(m):
  type_message = m.content_type
  if m.content_type == 'photo' and m.from_user.id in id_from_save:
     start_Analysis(m)
  elif m.from_user.id not in id_from_save and m.content_type != 'photo':bot.register_next_step_handler(m,Processing_image_for_analysis)
  elif m.from_user.id in id_from_save and m.content_type != 'photo':
    bot.send_message(m.chat.id,formatting.format_text(formatting.mbold(f'عذرا عليك بإرسال صورة وليس {type_message}')),reply_parameters=types.ReplyParameters(chat_id=m.chat.id,message_id=m.message_id,allow_sending_without_reply=True),parse_mode='Markdown')
    bot.register_next_step_handler(m, Processing_image_for_analysis)
  elif m.from_user.id not in id_from_save and m.content_type == 'photo':bot.register_next_step_handler(m,Processing_image_for_analysis)

def start_Analysis(m):
   try:
      chat_id: int = m.chat.id
      Mtext = m.caption
      message_id: int = m.message_id
      phoot_file_id = m.photo[-1].file_id
      get_photo = bot.get_file_url(phoot_file_id)
      bytes_from_url = requests.get(get_photo).content# (jpeg, png, webp) are supported.
      print(type(bytes_from_url))
      Gemini_answer = Gemini.Image(image=bytes(bytes_from_url), prompt=Mtext)
      bot.send_message(chat_id,text=Gemini_answer,reply_parameters=types.ReplyParameters(chat_id=chat_id,message_id=message_id,allow_sending_without_reply=True),parse_mode='Markdown')
   except Exception as e :
      print(e)
      id_from_save.remove(m.from_user.id)
def process_image(m):
  print('Starting ...')
  langsupport = {'ar':'ar', 'en':'en'}
  print(m.photo)
  cap = m.caption
  print(f'××× {cap} ×××')
  photo = m.photo[-1].file_id
  file = bot.get_file_url(photo)
  im = urllib.request.urlopen(file).read()
  PIL_OPEN = Image.open(io.BytesIO(im))
  if cap in langsupport:
    reader = easyocr.Reader([langsupport[cap]],gpu=False)
    easy_text = reader.readtext(PIL_OPEN,detail=0)
    bot.reply_to(m, easy_text)
    id_from_save.clear()
  elif cap not in langsupport:
    msg = '''↫ عفوًا، يجب عليك إرسال صورة و بوصفها اللغة المُراد أستخراجها من النص.

مِثال : الصورة + ar ..

↫ يجب أن تكون باللغة العربية [ar] أو الإنجليزية [en] أو الفَرَنسِيةْ [fr] بدون أحرُفٍ كَبيرةْ.'''
    bot.reply_to(m, msg)
    bot.register_next_step_handler(m, image_to_text_request)

#@bot.message_handler(content_types=['photo'])
#def Surveying_traces_of_crime(crime):
          #if crime.caption == '.ازالة' :

                          #continue
@bot.message_handler(content_types=['voice'])
def voice_processing(message):
  if message.from_user.id != admin_id:
        bot.forward_message(admin_id,message.chat.id,message_id=message.message_id)
  print('Starting ...')
  import datetime
  current_time = datetime.UTC.strftime('%Y%m%dT%H%M%S')
  mwav = f'mtsky.sensei-{current_time}'
  file_info = bot.get_file(message.voice.file_id)
  downloaded_file = bot.download_file(file_info.file_path)
  with open(mwav + '.ogg', 'wb') as new_file:
    new_file.write(downloaded_file)
  r = sr.Recognizer()
  conv = pydub.AudioSegment.from_ogg(f'{mwav}.ogg')
  conv.export(f'{mwav}.wav', format='wav')
  with sr.AudioFile(f'{mwav}.wav') as source:
    audio = r.record(source)

    print("Recognizing Now .... ")

    try:
      print(audio)
      text_from_speech = r.recognize_google(audio, language='ar')
      speech_answer = Gemini.Chat(text_from_speech)
      audio_answer: bytes = audioTTs(prompet=speech_answer)
      print(speech_answer)
      tts_open_wirte = open(mwav + '-.wav', 'wb').write(bytes(audio_answer))
      tts_open = open(mwav + '-.wav', 'rb')
      bot.send_voice(message.chat.id,
                     voice=tts_open,
                     caption=text_from_speech,
                     reply_parameters=types.ReplyParameters(chat_id=message.chat.id,message_id=message.message_id,allow_sending_without_reply=True))
      tts_open.close()
      os.remove(mwav+'.wav')
      os.remove(mwav+'-.wav')
      print("Audio Recorded Successfully \n ")

    except Exception as e:
      print("Error :  " + str(e))


@bot.callback_query_handler(func=lambda call: True)
def Call_Download(call):
  msg_id = []
  chat_id = call.message.chat.id
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
    # print(video_thumbnail)

    InlineKeyboard = types.InlineKeyboardMarkup(row_width=2)
    down_button1 = types.InlineKeyboardButton(
        text='📹  فيديو', callback_data=f'vid:{video_id}:{video_duration}')
    down_button2 = types.InlineKeyboardButton(
        text='️🎧 ملف صوتي', callback_data=f'mu:{video_id}:{video_duration}')
    down_button3 = types.InlineKeyboardButton(text='~ المُطَورْ .',
                                              url='tg://user?id=5624908798')
    InlineKeyboard.add(down_button1, down_button2, down_button3)
    bot.delete_message(chat_from_call, call.message.message_id)
    try:
      bot.send_photo(
          chat_from_call,
          photo=video_thumbnail,
          caption=video_title,
          reply_parameters=types.ReplyParameters(chat_id=chat_id,message_id=call.message.reply_to_message.message_id,allow_sending_without_reply=True),
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
                                        url='tg://user?id=5624908798')
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
          "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
          "outtmpl": '/home/runner/api/musics/' + "sillway.%(ext)s",

      }) as ydl:
        info = ydl.extract_info(video_url, download=True)
        vid_file = ydl.prepare_filename(info)
        #print('\n\n' + vid_file + '\n\n')
        #ydl.process_info(info)
        artist = info['uploader']
        url_thumb = info['thumbnail']
        print(url_thumb)
        thumb = bytes(requests.get(url_thumb).content)
        thumbnail_write = open('thumb.jpg','wb').write(thumb)
        image_thumb = Image.open('thumb.jpg')
        image_thumb.resize((320,320))
        image_thumb.save('thumb.jpg', 'JPEG', quality=96)
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
            thumbnail=thumbnail.read(),
            duration=duration,
            reply_parameters=types.ReplyParameters(chat_id=chat_id,message_id=call.message.reply_to_message.message_id,allow_sending_without_reply=True),
            parse_mode='Markdown',
            reply_markup=Keyboard)
        vid.close()
        os.remove(down_path)
        os.remove(os.path.abspath('thumb.jpg'))
        print('Done Remove...')
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
    Bottun = types.InlineKeyboardButton('~ المُطَورْ',url='tg://user?id=5624908798')
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
      msg_id.append(edit_cap0.message_id)

    try:
      video_url = f'https://www.youtube.com/watch?v={video_id}'

      with yt_dlp.YoutubeDL(
        {
    'format': 'bestaudio[ext=m4a]/best',
    'outtmpl': 'sillawy.%(ext)s',
    'prefer_ffmpeg': False,
    'extractaudio': True,
    'force_generic_extractor': True,
    'external_downloader_args': ['-j', '32', '-s', '32', '-x', '32'],


      }) as ydl:
        info = ydl.extract_info(video_url, download=True)
        title = info['title']
        print(title)
        lyrics_show = types.InlineKeyboardButton(text='- كلمات الأغنية 🎼',callback_data=f'lyr:{video_id}')
        Keyboard.row_width = 2
        Keyboard.add(Bottun,lyrics_show)
        audio_file = ydl.prepare_filename(info)
        print('----\n\n' + audio_file + '----\n\n')
        #ydl.process_info(info)
        artist = info['uploader']
        url_thumb = info['thumbnail']
        thumb = bytes(requests.get(url_thumb).content)
        duration = info['duration']
        print(duration)
        #with open(audio_file,"rb") as f:
        #print(f.__format__
        down_path = audio_file#.replace('.mp4','.m4a')
        print('---'+down_path)
        audio = open(down_path ,'rb')
        bot.send_chat_action(call.message.chat.id, 'upload_audio')
        bot.send_audio(
            chat_from_call,
            audio=audio,
            caption=f"[♧ ~ ︎ {video_duration} ⏳️]({video_url}) ",
            thumb=thumb,
            title=title,
            performer=artist,
            thumbnail=thumb,
            duration=duration,  reply_parameters=types.ReplyParameters(chat_id=chat_id,message_id=call.message.reply_to_message.message_id,allow_sending_without_reply=True),
            parse_mode='Markdown',
            reply_markup=Keyboard,
            timeout=35)
        audio.close()
        os.remove(os.path.abspath(down_path))
      Keyboard = types.InlineKeyboardMarkup(row_width=1)
      Keyboard.add(Bottun)
      try:
        bot.edit_message_caption(chat_id=call.message.chat.id,
                                 message_id=edit_cap.message_id,
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
        Keyboard = types.InlineKeyboardMarkup(row_width=1)
        Keyboard.add(Bottun)
        bot.edit_message_caption(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            caption=
            '<•> عُذرًا ، لا يُمكن تَحميل الفيديو بسبب سياسة الفئة العُمرية لليوتيوب .',
            reply_markup=Keyboard)
      except:
        Keyboard = types.InlineKeyboardMarkup(row_width=1)
        Keyboard.add(Bottun)

        bot.edit_message_text(
            text=
            '<•> عُذرًا ، لا يُمكن تَحميل الفيديو بسبب سياسة الفئة العُمرية لليوتيوب .',
            chat_id=chat_from_call,
            message_id=call.message.message_id,
            reply_markup=Keyboard)
  if call.data.split(':')[0] == 'lyr':
      chat_id = call.message.chat.id
      msg_id = call.message.message_id
      msg = ''
      video_id = call.data.split(':')[1]
      audio_title_ = yt.from_id(video_id).title
      audio_author = yt.from_id(video_id).author
      audio_length = yt.from_id(video_id).length
      audio_length = convert_seconds(audio_length)
      print(audio_length)
      audio_title = re.sub(r'\([^)]*\)', '', audio_title_).replace('-','').replace('\n','').replace('_','').replace('|','').replace('🎼','').replace('🎶','').replace('⭐','').replace('\n','').replace(audio_author,'').replace(audio_author.capitalize(),'').replace(audio_author.lower(),'')
      audio_title = audio_title
      data = lyr.get_lyrics_by_request_param(param='/lyrics/GetLyrPrecisily',title=audio_title, artist=audio_author,duration=audio_length)
      print(audio_title)
      try:
        for data_ in data['lyrics']:
           for time , lyric in data_.items():
            msg_sent = f'{time} >>> {str(lyric)}'+ '\n'
            msg += msg_sent
        bot.send_message(chat_id=chat_id,text=msg,reply_parameters=types.ReplyParameters(chat_id=chat_id,message_id=msg_id,allow_sending_without_reply=True),allow_sending_without_reply=True)
      except KeyError:
        bot.send_message(chat_id=chat_id,text='أسِـف لكـن ليسـت لَـدي كَلـِمات هَـاتـهِ الأُغـنيـة.',reply_parameters=types.ReplyParameters(chat_id=chat_id,message_id=msg_id,allow_sending_without_reply=True),allow_sending_without_reply=True)
        #  raise requests.exceptions.HTTPError(data)

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
              views = int(video['viewCount']['text'].replace(',','').replace('views', ''))
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
                             reply_parameters=types.ReplyParameters(chat_id=message.chat.id,message_id=message.message_id,allow_sending_without_reply=True),
                             reply_markup=Inlinebotoun)

# request_thread = threading.Thread(target=alive_server.alive_server,args=(URL_SERVER,))
# request_thread.start()
# server = flask.Flask(__name__)
# @server.route("/bot", methods=['POST'])
# def getMessage():
#   bot.process_new_updates([
#       telebot.types.Update.de_json(flask.request.stream.read().decode("utf-8"))
#   ])
#   return "!", 200


# @server.route("/")
# def webhook():
#   bot.remove_webhook()
#   link = 'https://' + str(flask.request.host)
#   bot.set_webhook(url=f"{link}/bot")
#   return "This api for Mitsky Download Bot", 200


# server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
# server = flask.Flask(__name__)
# print(server)

bot.remove_webhook()
bot.infinity_polling(none_stop=True)
