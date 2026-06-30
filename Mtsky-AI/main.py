# ---- Mtsky Standalone Download & Lyrics Bot ----
import sys
import io
import os
import re
import random
import tempfile
import threading
from time import sleep
from datetime import timedelta

# Ensure UTF-8 output on Windows console to prevent UnicodeEncodeError with Arabic text
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import requests
import flask
import telebot
from telebot import types
import yt_dlp

import lyr

admin_id = os.environ.get('ADMIN_ID', "5247891243")
# Updated with the new token provided by the user
bot_token = os.environ.get('BOT_API', '5400583582:AAGzJn3F2TGQBS0b96AE1ItvoXR-T-J8WtU')

bot = telebot.TeleBot(bot_token, num_threads=30, threaded=True)

# Get current script directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

import json

CACHE_FILE = os.path.join(BASE_DIR, "audio_cache.json")

def get_cached_audio(video_id):
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get(video_id)
        except Exception:
            pass
    return None

def save_cached_audio(video_id, file_id):
    data = {}
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception:
            pass
    data[video_id] = file_id
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving cache: {e}")

import urllib.request
import urllib.parse
import re

TITLE_CACHE = {}

def fast_youtube_search(query):
    results = []
    try:
        url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
        html = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')

        # 1. Try parsing ytInitialData JSON
        match = re.search(r'ytInitialData\s*=\s*({.+?});\s*</script>', html)
        if not match:
            match = re.search(r'window\["ytInitialData"\]\s*=\s*({.+?});\s*</script>', html)
        
        if match:
            data = json.loads(match.group(1))
            contents = data.get('contents', {}).get('twoColumnSearchResultsRenderer', {}).get('primaryContents', {}).get('sectionListRenderer', {}).get('contents', [])
            for section in contents:
                items = section.get('itemSectionRenderer', {}).get('contents', [])
                for item in items:
                    video = item.get('videoRenderer')
                    if video:
                        vid_id = video.get('videoId')
                        title = video.get('title', {}).get('runs', [{}])[0].get('text')
                        length_text = video.get('lengthText', {}).get('simpleText')
                        if not length_text:
                            runs = video.get('lengthText', {}).get('runs', [])
                            length_text = "".join([r.get('text', '') for r in runs])
                        
                        if vid_id and title and length_text:
                            if vid_id not in [r['id'] for r in results]:
                                results.append({'id': vid_id, 'title': title, 'duration_str': length_text})
                                TITLE_CACHE[vid_id] = title
                                if len(results) >= 10:
                                    break
    except Exception as e:
        print(f"ytInitialData parse error: {e}")

    # 2. Fallback to regex scraping if JSON navigation missed anything
    if not results:
        try:
            matches = re.findall(r'"videoRenderer":\{"videoId":"([^"]+)".*?"title":\{"runs":\[\{"text":"([^"]+)"\}\].*?"lengthText":\{.*?"simpleText":"([^"]+)"\}', html)
            for vid_id, title, duration in matches:
                if vid_id not in [r['id'] for r in results]:
                    results.append({'id': vid_id, 'title': title, 'duration_str': duration})
                    TITLE_CACHE[vid_id] = title
                    if len(results) >= 10:
                        break
        except Exception as e:
            print(f"Regex parse error: {e}")

    # 3. Ultimate Fallback to yt-dlp if YouTube completely redesigned their page
    if not results:
        try:
            ydl_opts = {'extract_flat': True, 'quiet': True, 'nocheckcertificate': True, 'socket_timeout': 10, 'extractor_args': {'youtube': {'player_client': ['ios', 'android', 'web'], 'player_skip': ['js', 'configs']}}}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                res = ydl.extract_info(f"ytsearch10:{query}", download=False).get('entries', [])
                for v in res:
                    vid_id = v.get('id')
                    title = v.get('title', 'Unknown Title')
                    raw_dur = v.get('duration', 0)
                    dur_str = convert_seconds(raw_dur) if raw_dur else '0:00'
                    if vid_id:
                        results.append({'id': vid_id, 'title': title, 'duration_str': dur_str})
                        TITLE_CACHE[vid_id] = title
        except Exception as e:
            print(f"Fallback yt-dlp error: {e}")

    return results


def convert_seconds(seconds):
    time_format = str(timedelta(seconds=int(seconds)))
    parts = time_format.split(':')
    hours, minutes, secs = parts
    if int(hours) > 0:
        return f"{int(hours)}:{int(minutes):02}:{secs}"
    return f"{int(minutes)}:{secs}"


def safe_react(chat_id, message_id, emoji):
    """Safely set a message reaction if supported by the chat."""
    try:
        bot.set_message_reaction(chat_id, message_id, [types.ReactionTypeEmoji(emoji)])
    except Exception:
        pass


@bot.message_handler(commands=['start', 'help'])
def StartAI(message):
    safe_react(message.chat.id, message.message_id, '⚡')
    username = message.from_user.first_name
    user_id = message.from_user.id
    
    if message.text.startswith('/help'):
        cap = f'''💡 *مـسـاعـدة وطـريـقـة الاسـتـخـدام* 💡

> يمكنك استخدام هذا البوت بطريقتين ذكيتين:

1️⃣ *الطريقة الأولى (داخل محادثة البوت):*
أرسل الأمر `.بحث` متبوعاً باسم الأغنية أو المقطع، مثال:
`.بحث Hello Adele`

2️⃣ *الطريقة الثانية (البحث المضمن - Inline):*
في أي محادثة أو مجموعة، اكتب معرف البوت متبوعاً بكلمة البحث، مثال:
`@mtsky_bot Hello`
ثم اختر النتيجة لإرسالها فوراً إلى أصدقائك!

🎧 *الميزات الإضافية:*
- تحميل فوري بصيغ فيديو وصوت عالية الجودة.
- جلب كلمات الأغاني بدقة تامة وبنقرة واحدة.
'''
    else:
        cap = f'''🤖 أهــلاً أيـهـا الـمُـسـتَـخـدِم [{username}](tg://user?id={user_id}) ،
> أَنَـا بُـوت الـتَـحـمـيـل والـبَـحـث الـذَكـي ديـنـا، يـُـمـكِـنُـنِـي تَــقــديــم الـخَــدمــاتِ الـتَــالــيــةِ لَـكَ :

🎥 `.بحث` + اسـم الأغنية أو الـفـيـديـو: لأبـحـث لـك في الـيـوتـيـوب وأقـدم لـك مـلـف صـوتـي أو فيـديـو مع كـلـمـات الأغـنـيـة بـدقـة فـائـقـة.

💡 لمعرفة المزيد من الطرق والميزات، اضغط على /help.

🔴 - إضغط على الأمر في النَص لِلنَسخِ ،

أتـمـنـى لـك يـومًا سـعـيـدًا ومـلـيـئًا بالإبـداع ✨.
'''

    if message.chat.type == 'private':
        bot.send_message(
            message.chat.id, 
            cap, 
            reply_parameters=types.ReplyParameters(chat_id=message.chat.id, message_id=message.message_id, allow_sending_without_reply=True), 
            parse_mode='Markdown'
        )
    elif str(message.from_user.id) != admin_id:
        try:
            bot.forward_message(admin_id, message.chat.id, message_id=message.message_id)
        except Exception:
            pass


@bot.message_handler(commands=['search'])
def search_command(message):
    safe_react(message.chat.id, message.message_id, '⚡')
    parts = message.text.split(' ', 1)
    if len(parts) > 1 and parts[1].strip():
        perform_search(message, f".بحث {parts[1].strip()}")
    else:
        bot.send_message(message.chat.id, "⚠️ الرجاء كتابة كلمة البحث بعد الأمر، مثال:\n`/search Hello Adele`", parse_mode='Markdown')


@bot.message_handler(func=lambda m: True)
def main_handler(m):
    text = m.text or ""
    if text.startswith('.بحث'):
        perform_search(m, text)


@bot.edited_message_handler(func=lambda message: True)
def edited_handler(message):
    text = message.text or ""
    if text.startswith('.بحث'):
        perform_search(message, text)


def perform_search(message, text):
    safe_react(message.chat.id, message.message_id, '⚡')
    try:
        querytext = text.split('.بحث', 1)[1].strip()
        if not querytext:
            bot.send_message(message.chat.id, "⚠️ الرجاء كتابة كلمة البحث بعد الأمر، مثال: `.بحث Hello Adele`", parse_mode='Markdown')
            return

        print(f"Searching via fast_youtube_search: {querytext}")
        lis = []
        Inlinebotoun = types.InlineKeyboardMarkup(row_width=1)
        
        results = fast_youtube_search(querytext)

        for video in results:
            try:
                best_video_id = video.get('id')
                best_video_title = video.get('title', 'Unknown Title')
                video_duration = video.get('duration_str', '0:00')

                if not best_video_id:
                    continue

                if len(lis) >= 4:
                    break
                print(f"Candidate match: {best_video_title} | Duration: {video_duration}")
                lis.append(best_video_id)
                tubebot = types.InlineKeyboardButton(
                    f'{best_video_title} ({video_duration})',
                    callback_data=f'url:{best_video_id}:{video_duration}'
                )
                Inlinebotoun.add(tubebot)
            except Exception as e:
                print(f"Error parsing search result item: {e}")
                continue

        if not lis:
            bot.send_message(message.chat.id, f"⚠️ لم يتم العثور على نتائج مناسبة للبحث: {querytext}")
            return

        bot.send_message(
            message.chat.id,
            text=f'⇜ نتائج البحث ~ {querytext}',
            reply_parameters=types.ReplyParameters(chat_id=message.chat.id, message_id=message.message_id, allow_sending_without_reply=True),
            reply_markup=Inlinebotoun
        )
    except Exception as e:
        print(f"Search failure: {e}")
        bot.send_message(message.chat.id, "⚠️ عذراً، حدث خطأ أثناء البحث. الرجاء المحاولة مرة أخرى.")


@bot.inline_handler(func=lambda query: len(query.query) > 0)
def query_text(inline_query):
    """Next-Gen Inline Query Engine with Instant Audio Caching & ChosenInlineResult Architecture"""
    try:
        query = inline_query.query.strip()
        results = fast_youtube_search(query)

        inline_results = []

        for video in results:
            video_id = video.get('id')
            title = video.get('title', 'Unknown Title')
            duration = video.get('duration_str', '0:00')
            thumb = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"

            cached_file_id = get_cached_audio(video_id)

            Keyboard = types.InlineKeyboardMarkup(row_width=2)
            Bottun = types.InlineKeyboardButton('~ المُطَورْ', url='tg://user?id=5247891243')
            lyrics_show = types.InlineKeyboardButton(text='- كلمات الأغنية 🎼', callback_data=f'lyr:{video_id}')
            Keyboard.add(Bottun, lyrics_show)

            caption = f"🎶 [{title}](https://www.youtube.com/watch?v={video_id})\n> ⏳ المدة: {duration}"

            if cached_file_id:
                # INSTANT AUDIO DELIVERY!!!
                r = types.InlineQueryResultCachedAudio(
                    id=video_id,
                    audio_file_id=cached_file_id,
                    caption=caption,
                    parse_mode='Markdown',
                    reply_markup=Keyboard
                )
            else:
                # High-speed download placeholder with ChosenInlineResult triggering
                load_kb = types.InlineKeyboardMarkup(row_width=1)
                load_btn = types.InlineKeyboardButton(text='⚡ جاري معالجة الملف الصوتي... (اضغط للتحميل) 🎧', callback_data=f'mu:{video_id}:{duration}')
                load_kb.add(load_btn, Bottun)
                
                desc = f"المدة: {duration} | ⚡ سيتم إرسال الملف الصوتي فوراً"
                r = types.InlineQueryResultPhoto(
                    id=f"dl:{video_id}:{duration}",
                    photo_url=thumb,
                    thumb_url=thumb,
                    title=title,
                    description=desc,
                    caption=f"⏳ جاري تجهيز وتحميل الملف الصوتي بسرعة البرق...\n> 🎶 **{title}**",
                    parse_mode='Markdown',
                    reply_markup=load_kb
                )
            inline_results.append(r)

        bot.answer_inline_query(inline_query.id, inline_results, cache_time=300)
    except Exception as e:
        print(f"Inline query error: {e}")


def process_and_send_audio(video_id, video_duration, chat_id=None, msg_id=None, inline_msg_id=None, from_user_id=None):
    video_url = f'https://www.youtube.com/watch?v={video_id}'
    Keyboard = types.InlineKeyboardMarkup(row_width=2)
    Bottun = types.InlineKeyboardButton('~ المُطَورْ', url='tg://user?id=5247891243')
    lyrics_show = types.InlineKeyboardButton(text='- كلمات الأغنية 🎼', callback_data=f'lyr:{video_id}')
    Keyboard.add(Bottun, lyrics_show)

    caption = f"[♧ ~ {video_duration} ⏳️]({video_url})"

    # Check if already cached
    cached_file_id = get_cached_audio(video_id)
    if cached_file_id:
        try:
            if inline_msg_id:
                bot.edit_message_media(media=types.InputMediaAudio(media=cached_file_id, caption=caption, parse_mode='Markdown'), inline_message_id=inline_msg_id, reply_markup=Keyboard)
            elif chat_id and msg_id:
                try:
                    bot.edit_message_media(media=types.InputMediaAudio(media=cached_file_id, caption=caption, parse_mode='Markdown'), chat_id=chat_id, message_id=msg_id, reply_markup=Keyboard)
                except Exception:
                    bot.send_audio(chat_id, audio=cached_file_id, caption=caption, parse_mode='Markdown', reply_markup=Keyboard)
            return
        except Exception as e:
            print(f"Cached audio send/edit failed, downloading fresh: {e}")

    # Status update
    status_kb = types.InlineKeyboardMarkup(row_width=1)
    status_kb.add(Bottun)
    try:
        if inline_msg_id:
            bot.edit_message_caption(inline_message_id=inline_msg_id, caption='<•> جَاري التَحميل الخارق ...', reply_markup=status_kb)
        elif chat_id and msg_id:
            bot.edit_message_caption(chat_id=chat_id, message_id=msg_id, caption='<•> جَاري التَحميل الخارق ...', reply_markup=status_kb)
    except Exception:
        pass

    try:
        temp_dir = tempfile.gettempdir()
        out_tmpl = os.path.join(temp_dir, f"audio_{video_id}.%(ext)s")
        thumb_path = os.path.join(temp_dir, f"thumb_{video_id}.jpg")

        ydl_opts = {
            'format': 'm4a/bestaudio/best',
            'outtmpl': out_tmpl,
            'quiet': True,
            'nocheckcertificate': True,
            'http_chunk_size': 2097152,
            'concurrent_fragment_downloads': 30,
            'buffersize': 1024 * 1024 * 4,
            'socket_timeout': 15,
            'retries': 10,
            'fragment_retries': 10,
            'extractor_args': {
                'youtube': {
                    'player_client': ['web_embedded', 'mweb', 'default'],
                    'player_skip': ['js', 'configs']
                }
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            title = info.get('title', 'Unknown Title')
            artist = info.get('uploader', 'Unknown Artist')
            duration = info.get('duration', 0)
            url_thumb = info.get('thumbnail')
            audio_file = ydl.prepare_filename(info)

        if url_thumb:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
            thumb_bytes = requests.get(url_thumb, headers=headers, timeout=10).content
            with open(thumb_path, 'wb') as f:
                f.write(thumb_bytes)

        dump_chat = from_user_id or chat_id or admin_id
        
        with open(audio_file, 'rb') as audio:
            thumb_file = open(thumb_path, 'rb') if os.path.exists(thumb_path) else None
            
            # 1. Upload to dump_chat to grab file_id
            try:
                sent_dump = bot.send_audio(
                    dump_chat,
                    audio=audio,
                    caption=caption,
                    thumb=thumb_file,
                    title=title,
                    performer=artist,
                    duration=duration,
                    parse_mode='Markdown',
                    reply_markup=Keyboard,
                    timeout=90
                )
                new_file_id = sent_dump.audio.file_id
                save_cached_audio(video_id, new_file_id)
                
                # If dump_chat was the actual target chat and not inline, we are done! Just delete the loading message
                if chat_id and msg_id and not inline_msg_id and dump_chat == chat_id:
                    try:
                        bot.delete_message(chat_id, msg_id)
                    except Exception:
                        pass
                elif inline_msg_id:
                    bot.edit_message_media(media=types.InputMediaAudio(media=new_file_id, caption=caption, parse_mode='Markdown'), inline_message_id=inline_msg_id, reply_markup=Keyboard)
            except Exception as upload_err:
                print(f"Dump upload or edit media failed: {upload_err}")
                # Fallback direct edit/send if possible
                if chat_id and msg_id and not inline_msg_id:
                    audio.seek(0)
                    if thumb_file: thumb_file.seek(0)
                    bot.send_audio(chat_id, audio=audio, caption=caption, thumb=thumb_file, title=title, performer=artist, duration=duration, parse_mode='Markdown', reply_markup=Keyboard, timeout=90)
                    try: bot.delete_message(chat_id, msg_id)
                    except Exception: pass

            if thumb_file:
                thumb_file.close()

        if os.path.exists(audio_file):
            os.remove(audio_file)
        if os.path.exists(thumb_path):
            os.remove(thumb_path)

    except Exception as e:
        import traceback
        err_str = traceback.format_exc()
        print(err_str)
        try:
            err_chat = chat_id or from_user_id or admin_id
            bot.send_message(err_chat, f"⚠️ EXCEPTION IN AUDIO PROCESSOR:\n\n```python\n{err_str[:3800]}\n```", parse_mode='Markdown')
        except Exception:
            pass


@bot.chosen_inline_handler(func=lambda chosen_inline_result: True)
def chosen_inline(chosen_inline_result):
    try:
        res_id = chosen_inline_result.result_id
        if res_id.startswith('dl:'):
            parts = res_id.split(':')
            video_id = parts[1]
            duration = ':'.join(parts[2:])
            threading.Thread(target=process_and_send_audio, args=(video_id, duration, None, None, chosen_inline_result.inline_message_id, chosen_inline_result.from_user.id)).start()
    except Exception as e:
        print(f"Chosen inline error: {e}")


@bot.callback_query_handler(func=lambda call: True)
def Call_Download(call):
    try:
        bot.answer_callback_query(call.id, text="⚡ جاري معالجة طلبك...", cache_time=5)
    except Exception:
        pass

    is_inline = call.message is None
    if is_inline:
        chat_id = call.from_user.id
        msg_id = None
        inline_msg_id = call.inline_message_id
        reply_id = None
        reply_params = None
    else:
        chat_id = call.message.chat.id
        msg_id = call.message.message_id
        inline_msg_id = None
        reply_id = call.message.reply_to_message.message_id if call.message.reply_to_message else None
        reply_params = types.ReplyParameters(chat_id=chat_id, message_id=reply_id, allow_sending_without_reply=True) if reply_id else None

    data_parts = call.data.split(':')
    action = data_parts[0]

    if action == 'url':
        if not is_inline:
            safe_react(chat_id, msg_id, '⚡')
        video_id = data_parts[1]
        video_duration = ':'.join(data_parts[2:])
        print(f"Selected video: {video_id} | {video_duration}")
        video_url = f'https://www.youtube.com/watch?v={video_id}'

        try:
            video_title = TITLE_CACHE.get(video_id, f"🎶 Track ({video_duration})")
            thumb_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"

            InlineKeyboard = types.InlineKeyboardMarkup(row_width=2)
            down_button1 = types.InlineKeyboardButton(text='📹 فيديو', callback_data=f'vid:{video_id}:{video_duration}')
            down_button2 = types.InlineKeyboardButton(text='️🎧 ملف صوتي', callback_data=f'mu:{video_id}:{video_duration}')
            down_button3 = types.InlineKeyboardButton(text='~ المُطَورْ .', url='tg://user?id=5247891243')
            InlineKeyboard.add(down_button1, down_button2, down_button3)

            if not is_inline:
                try:
                    bot.delete_message(chat_id, msg_id)
                except Exception:
                    pass
            
            photo_sent = False
            if thumb_url:
                try:
                    temp_dir = tempfile.gettempdir()
                    thumb_path = os.path.join(temp_dir, f"thumb_get_{video_id}.jpg")
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
                    thumb_bytes = requests.get(thumb_url, headers=headers, timeout=10).content
                    with open(thumb_path, 'wb') as f:
                        f.write(thumb_bytes)
                    with open(thumb_path, 'rb') as photo_file:
                        bot.send_photo(chat_id, photo=photo_file, caption=video_title, reply_parameters=reply_params, reply_markup=InlineKeyboard)
                    photo_sent = True
                    if os.path.exists(thumb_path):
                        os.remove(thumb_path)
                except Exception as thumb_err:
                    print(f"Failed to send photo thumbnail: {thumb_err}")
            
            if not photo_sent:
                bot.send_message(chat_id, text=video_title, reply_parameters=reply_params, reply_markup=InlineKeyboard)
        except Exception as e:
            import traceback
            err_str = traceback.format_exc()
            print(err_str)
            try:
                bot.send_message(chat_id, f"⚠️ EXCEPTION IN URL HANDLER:\n\n```python\n{err_str[:3800]}\n```", parse_mode='Markdown')
            except Exception:
                pass

    elif action == 'vid':
        if not is_inline:
            safe_react(chat_id, msg_id, '⏳')
        video_id = data_parts[1]
        video_duration = ':'.join(data_parts[2:])
        video_url = f'https://www.youtube.com/watch?v={video_id}'

        Keyboard = types.InlineKeyboardMarkup(row_width=1)
        Bottun = types.InlineKeyboardButton('~ المُطَورْ', url='tg://user?id=5247891243')
        Keyboard.add(Bottun)

        try:
            if is_inline:
                bot.edit_message_caption(inline_message_id=inline_msg_id, caption='<•> جَاري التَحميل ...', reply_markup=Keyboard)
            else:
                bot.edit_message_caption(chat_id=chat_id, message_id=msg_id, caption='<•> جَاري التَحميل ...', reply_markup=Keyboard)
        except Exception:
            try:
                if is_inline:
                    bot.edit_message_text(inline_message_id=inline_msg_id, text='<•> جَاري التَحميل ...', reply_markup=Keyboard)
                else:
                    bot.edit_message_text(text='<•> جَاري التَحميل ...', chat_id=chat_id, message_id=msg_id, reply_markup=Keyboard)
            except Exception:
                pass

        try:
            temp_dir = tempfile.gettempdir()
            out_tmpl = os.path.join(temp_dir, f"vid_{video_id}.%(ext)s")
            thumb_path = os.path.join(temp_dir, f"thumb_{video_id}.jpg")

            ydl_opts = {
                "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                "outtmpl": out_tmpl,
                "quiet": True,
                "nocheckcertificate": True,
                "http_chunk_size": 2097152,
                "concurrent_fragment_downloads": 30,
                "buffersize": 1024 * 1024 * 4,
                'socket_timeout': 15,
                'retries': 10,
                'fragment_retries': 10,
                'extractor_args': {
                    'youtube': {
                        'player_client': ['web_embedded', 'mweb', 'default'],
                        'player_skip': ['js', 'configs']
                    }
                }
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                vid_file = ydl.prepare_filename(info)
                title = info.get('title', 'Unknown Title')
                duration = info.get('duration', 0)
                url_thumb = info.get('thumbnail')

            if url_thumb:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
                thumb_bytes = requests.get(url_thumb, headers=headers, timeout=10).content
                with open(thumb_path, 'wb') as f:
                    f.write(thumb_bytes)

            with open(vid_file, 'rb') as vid:
                thumb_file = open(thumb_path, 'rb') if os.path.exists(thumb_path) else None
                try:
                    bot.send_chat_action(chat_id, 'upload_video')
                except Exception:
                    pass
                sent_msg = bot.send_video(
                    chat_id,
                    video=vid,
                    caption=f"[♧ ~ {video_duration} ⏳️]({video_url})",
                    thumbnail=thumb_file,
                    duration=duration,
                    reply_parameters=reply_params,
                    parse_mode='Markdown',
                    reply_markup=Keyboard,
                    timeout=90
                )
                if thumb_file:
                    thumb_file.close()
                safe_react(chat_id, sent_msg.message_id, '🔥')

            if os.path.exists(vid_file):
                os.remove(vid_file)
            if os.path.exists(thumb_path):
                os.remove(thumb_path)

            try:
                if is_inline:
                    bot.edit_message_caption(inline_message_id=inline_msg_id, caption='● ~ تَم إكتِمَال التَحميل 🎧 .', reply_markup=Keyboard)
                else:
                    bot.edit_message_caption(caption='● ~ تَم إكتِمَال التَحميل 🎧 .', chat_id=chat_id, message_id=msg_id, reply_markup=Keyboard)
            except Exception:
                try:
                    if is_inline:
                        bot.edit_message_text(inline_message_id=inline_msg_id, text='● ~ تَم إكتِمَال التَحميل 🎧 .', reply_markup=Keyboard)
                    else:
                        bot.edit_message_text(text='● ~ تَم إكتِمَال التَحميل 🎧 .', chat_id=chat_id, message_id=msg_id, reply_markup=Keyboard)
                except Exception:
                    pass

        except Exception as e:
            import traceback
            err_str = traceback.format_exc()
            print(err_str)
            try:
                bot.send_message(chat_id, f"⚠️ EXCEPTION IN VID HANDLER:\n\n```python\n{err_str[:3800]}\n```", parse_mode='Markdown')
            except Exception:
                pass

    elif action == 'mu':
        if not is_inline:
            safe_react(chat_id, msg_id, '⏳')
        video_id = data_parts[1]
        video_duration = ':'.join(data_parts[2:])
        threading.Thread(target=process_and_send_audio, args=(video_id, video_duration, chat_id, msg_id, inline_msg_id, call.from_user.id)).start()

    elif action == 'lyr':
        if not is_inline:
            safe_react(chat_id, msg_id, '⚡')
        video_id = data_parts[1]
        video_url = f'https://www.youtube.com/watch?v={video_id}'

        try:
            ydl_opts = {'extract_flat': True, 'skip_download': True, 'quiet': True, 'nocheckcertificate': True}

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                audio_title_ = info.get('title', '')
                audio_author = info.get('uploader', '')
                raw_duration = info.get('duration', 0)

            audio_length = convert_seconds(raw_duration)
            print(f"Fetching lyrics for: {audio_title_} | {audio_author} | {audio_length}")

            # Clean up title for precise lyrics matching
            audio_title = re.sub(r'\([^)]*\)', '', audio_title_)
            audio_title = re.sub(r'\[[^\]]*\]', '', audio_title)
            for char in ['-', '\n', '_', '|', '🎼', '🎶', '⭐']:
                audio_title = audio_title.replace(char, '')
            
            if audio_author:
                audio_title = audio_title.replace(audio_author, '').replace(audio_author.capitalize(), '').replace(audio_author.lower(), '')
            audio_title = audio_title.strip()

            data = lyr.get_lyrics_by_request_param(param='/lyrics/GetLyrPrecisily', title=audio_title, artist=audio_author, duration=audio_length)
            
            lyr_reply_params = types.ReplyParameters(chat_id=chat_id, message_id=msg_id, allow_sending_without_reply=True) if msg_id else None
            
            msg = ''
            if 'lyrics' in data and data['lyrics']:
                for data_ in data['lyrics']:
                    for time_str, lyric in data_.items():
                        msg += f'{time_str} >>> {str(lyric)}\n'
                sent_msg = bot.send_message(chat_id=chat_id, text=msg, reply_parameters=lyr_reply_params)
                safe_react(chat_id, sent_msg.message_id, '🔥')
            else:
                bot.send_message(chat_id=chat_id, text='أسِـف لكـن ليسـت لَـدي كَلـِمات هَـاتـهِ الأُغـنيـة.', reply_parameters=lyr_reply_params)
        except Exception as e:
            print(f"Error fetching lyrics: {e}")
            try:
                lyr_reply_params = types.ReplyParameters(chat_id=chat_id, message_id=msg_id, allow_sending_without_reply=True) if msg_id else None
                bot.send_message(chat_id=chat_id, text='⚠️ عذراً، حدث خطأ أثناء جلب كلمات الأغنية.', reply_parameters=lyr_reply_params)
            except Exception:
                pass


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
    # Set up menu commands automatically when webhook is registered
    try:
        bot.set_my_commands([
            telebot.types.BotCommand("/start", "🚀 بدء تشغيل البوت"),
            telebot.types.BotCommand("/help", "💡 مساعدة وطريقة الاستخدام"),
            telebot.types.BotCommand("/search", "🔍 بحث عن فيديو أو أغنية")
        ])
    except Exception as e:
        print(f"Failed to set menu commands: {e}")
    return "This API is for Mitsky Download & Lyrics Bot", 200


if __name__ == '__main__':
    if os.environ.get('WEBHOOK', 'false').lower() == 'true':
        server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5001)))
    else:
        print("Starting bot in infinity_polling mode...")
        bot.remove_webhook()
        try:
            bot.set_my_commands([
                telebot.types.BotCommand("/start", "🚀 بدء تشغيل البوت"),
                telebot.types.BotCommand("/help", "💡 مساعدة وطريقة الاستخدام"),
                telebot.types.BotCommand("/search", "🔍 بحث عن فيديو أو أغنية")
            ])
        except Exception as e:
            print(f"Failed to set menu commands: {e}")
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
