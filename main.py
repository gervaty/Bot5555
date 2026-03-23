import time
import telebot
import requests
import re
import json
import random
import ast
import os
import base64
import pytz
from http.cookies import SimpleCookie
from datetime import datetime, timedelta, UTC

with open('tokens.json', 'r', encoding='utf-8') as f:
    TOKENS = json.load(f)

trusted = [5184185845, 7417081858, 7894813633, 5452789572, 6678922340, 1327137572, 5464616347, 5253491877, 1413199933,
           6685504562, 1208376516, 5769586223, 5598453128]
#supertrusted = [1327137572, 5184185845, 7894813633, 5452789572, 7417081858]
supertrusted = [5663217441]
blocklist = [7857488037]  # , 1087968824, 136817688, 777000]
testacc = TOKENS['testacc']
token = TOKENS['telegram_bot_token']
print('Запуск')
remixes_cloud_id = 1269146365
remixes_cloud_token = TOKENS['remixes_cloud_token']
remix_db = None
account_remixer = TOKENS['account_remixer']
remixer_token = TOKENS['remixer_token']
bot = telebot.TeleBot(token)
cors = ''
click_db = {}
rps_db = {}
ttt_db = {}
cards_db = {}
sldb = ["аαᥲᴀaᚤᗩãɑⲁᗣ", "бδƃᎶⳝ6ᘜ", "вʙVᛒᗷBⲂᙖ", "гᴦrⲅցgᒋ", "дꙣgⲇᗪ", "еȇᥱᴇ℮eⲉᛊẾεᙓ", "ёëᕧ", "жⵣᙧ", "зɜzᤋ3ᙐ", "иuᥙᥢυᛋÛᑌ",
        "йӣᥔŭύᕫ", "кkκᴋқᛕҡⲕᏦ", "лᴧⲗl᧘ᙁ", "мʍMᴍḿⲙᗰ", "нӊʜHዙⲏᕼ", "оȯ᧐οoᴏⲟᛜőøόⳝò0ᗝ", "пᴨπnᚢກᥰᑎⲠ", "рρᴩpⲣᴘᚹᖘ", "сcᴄＣℂᥴⲥϹᙅ",
        "тᴛƮᛠŤtτ੮Ⲧᙢ", "уyγʏⲩᎽ", "фɸⲫφᛄᙨ", "хx᙭𝚡ⵋ", "цųᘈ", "ч౺੫ᔦ", "шɯᛞⲱᗯ", "щպɰᘺ", "ъѣᕹ", "ыӹᕠ", "ьᏏbᖚ", "э϶ꎆᑓ", "юꙗᕡ",
        "яᴙᖆ", " ", " ㅤ ̲", ' ' "\n"]


class Troll:
    def __init__(self):
        self.token = 'Тут могла быть ваша реклама'


def protect(content):
    return content.replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;")


def getlt(lt):
    for i in range(len(sldb)):
        if lt.upper() in sldb[i].upper():
            return i
    return -1


def interact_with_remix_db(type='get', data={}):
    if type == 'get':
        r = requests.get(f'https://api.scratch.mit.edu/projects/{str(remixes_cloud_id)}',
                         headers={'X-Token': remixes_cloud_token})
        return ast.literal_eval(r.json()['instructions'])
    elif type == 'put':
        r = requests.put(f'https://api.scratch.mit.edu/projects/{str(remixes_cloud_id)}',
                         headers={'X-Token': remixes_cloud_token}, json={'instructions': str(data)})


def remixproject(id, cookie):
    resp = requests.get("https://api.scratch.mit.edu/projects/510186917/")
    data = resp.json()
    resp = requests.get("https://projects.scratch.mit.edu/510186917?token=" + data.get("project_token"))
    data = resp.json()
    head = cookie
    resp = requests.post("https://projects.scratch.mit.edu/?is_remix=1&original_id=" + str(id), headers=head, json=data)
    if resp.status_code == 200:
        data = resp.json()
        return {'success': True, 'value': data.get("content-name")}
    else:
        return {'success': False}


def getid(url):
    # Регулярное выражение для разных форматов
    # Улавливает ID из watch?v=, youtu.be/, /embed/, /v/
    regex = (r'(?:https?://)?'  # Необязательный http(s)://
             r'(?:www\.)?'  # Необязательный www.
             r'(?:youtube\.com/(?:watch\?v=|embed/|v/)|youtu\.be/)'  # Домены и пути
             r'([\w-]{11})')  # 11 символов ID видео
    match = re.search(regex, url)
    return match.group(1) if match else None


def cookie_to_string(cookie):
    c = SimpleCookie()
    c[cookie.name] = cookie.value
    morsel = c[cookie.name]
    if getattr(cookie, 'domain', None):
        morsel['domain'] = cookie.domain
    if getattr(cookie, 'path', None):
        morsel['path'] = cookie.path
    if getattr(cookie, 'secure', None):
        morsel['secure'] = True
    if getattr(cookie, 'httponly', None):
        morsel['httponly'] = True
    if hasattr(cookie, 'expires'):
        expires_date = datetime.now(UTC) + timedelta(weeks=2)
        morsel['expires'] = expires_date.strftime('%a, %d-%b-%Y %H:%M:%S GMT')
    if isinstance(getattr(cookie, 'expires', None), int):
        morsel['Max-Age'] = cookie.expires
    return morsel.OutputString()


def login(username, password):
    session = requests.Session()
    session.get("https://scratch.mit.edu/csrf_token/")
    csrf_token = session.cookies.get('scratchcsrftoken')
    headers = {
        "referer": "https://scratch.mit.edu",
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": csrf_token,
        "Content-Type": "application/json",
        "Accept-Language": "ru-RU,ru;q=0.9"
    }
    body = {
        "username": username,
        "password": password,
        "useMessages": "true"
    }
    try:
        respo = session.post(
            "https://scratch.mit.edu/accounts/login/",
            headers=headers,
            json=body
        )
    except Exception as e:
        return {"success": False, "msg": f"Ошибка входа: {e}"}
    if respo.status_code == 200:
        cookies = respo.cookies
        for cook in cookies:
            if cook.name == 'scratchsessionsid':
                cookie_string = cookie_to_string(cook)
        match = re.search(r'([^=]+)="\\"([^"]+)\\""', cookie_string)
        if match:
            cookie_name = match.group(1)
            cookie_value = match.group(2)
            clean_cookie = f'{cookie_name}="{cookie_value}"'
            clean_cookie = clean_cookie + ";scratchcsrftoken=" + csrf_token
        head = {
            "Cookie": clean_cookie,
            "referer": "https://scratch.mit.edu/",
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": csrf_token,
            "Content-Type": "application/json",
            "Accept-Language": "ru-RU,ru;q=0.9",
            "Origin": "https://scratch.mit.edu",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept": "*/*",
        }
        resp = requests.get("https://scratch.mit.edu/session/", headers=head)
        lol = resp.json()
        return {"success": True, "cookie": head, "token": lol["user"]["token"], "username": lol["user"]["username"],
                "isbanned": lol["user"]["banned"], "email": lol["user"]["email"]}
    else:
        data = respo.json()
        return {"success": False, "msg": data[0].get("msg")}


def cmd(c, msg):
    return msg in [f'/{c}', f'/{c}@rsokolov3Bot', f'/{c}@rsokolov3Bot']


def msg(chat, text, reply, is_topic_message, thr, parse=False):
    text = text.replace('42', '43')
    if parse:
        if is_topic_message:
            return bot.send_message(chat, text, reply_to_message_id=reply, message_thread_id=thr, parse_mode='HTML',
                                    link_preview_options=telebot.types.LinkPreviewOptions(is_disabled=True))
        else:
            return bot.send_message(chat, text, reply_to_message_id=reply, parse_mode='HTML',
                                    link_preview_options=telebot.types.LinkPreviewOptions(is_disabled=True))
    else:
        if is_topic_message:
            return bot.send_message(chat, text, reply_to_message_id=reply, message_thread_id=thr,
                                    link_preview_options=telebot.types.LinkPreviewOptions(is_disabled=True))
        else:
            return bot.send_message(chat, text, reply_to_message_id=reply,
                                    link_preview_options=telebot.types.LinkPreviewOptions(is_disabled=True))


def media(chat, photo, text, reply, is_topic_message, thr, parse=False):
    if parse:
        if is_topic_message:
            bot.send_photo(chat_id=chat, photo=photo, caption=text, message_thread_id=thr, parse_mode='HTML',
                           reply_to_message_id=reply)
        else:
            bot.send_photo(chat_id=chat, photo=photo, caption=text, parse_mode='HTML', reply_to_message_id=reply)
    else:
        if is_topic_message:
            bot.send_photo(chat_id=chat, photo=photo, caption=text, message_thread_id=thr, reply_to_message_id=reply)
        else:
            bot.send_photo(chat_id=chat, photo=photo, caption=text, reply_to_message_id=reply)


def doc(chat, dc, text, reply, is_topic_message, thr, parse=False):
    if parse:
        if is_topic_message:
            bot.send_document(chat_id=chat, document=dc, caption=text, message_thread_id=thr, parse_mode='HTML',
                              reply_to_message_id=reply)
        else:
            bot.send_document(chat_id=chat, document=dc, caption=text, parse_mode='HTML', reply_to_message_id=reply)
    else:
        if is_topic_message:
            bot.send_document(chat_id=chat, document=dc, caption=text, message_thread_id=thr, reply_to_message_id=reply)
        else:
            bot.send_document(chat_id=chat, document=dc, caption=text, reply_to_message_id=reply)


def aud(chat, dc, text, reply, is_topic_message, thr, parse=False):
    if parse:
        if is_topic_message:
            bot.send_audio(chat_id=chat, audio=dc, caption=text, message_thread_id=thr, parse_mode='HTML',
                           reply_to_message_id=reply)
        else:
            bot.send_audio(chat_id=chat, audio=dc, caption=text, parse_mode='HTML', reply_to_message_id=reply)
    else:
        if is_topic_message:
            bot.send_audio(chat_id=chat, audio=dc, caption=text, message_thread_id=thr, reply_to_message_id=reply)
        else:
            bot.send_audio(chat_id=chat, audio=dc, caption=text, reply_to_message_id=reply)


def docs(chat, dc, text, reply, is_topic_message, thr, parse=False):
    if parse:
        if is_topic_message:
            bot.send_media_group(chat_id=chat, media=dc, message_thread_id=thr, parse_mode='HTML',
                                 reply_to_message_id=reply)
        else:
            bot.send_media_group(chat_id=chat, media=dc, parse_mode='HTML', reply_to_message_id=reply)
    else:
        if is_topic_message:
            bot.send_media_group(chat_id=chat, media=dc, message_thread_id=thr, reply_to_message_id=reply)
        else:
            bot.send_media_group(chat_id=chat, media=dc, reply_to_message_id=reply)


def voice(chat, dc, text, reply, is_topic_message, thr, parse=False):
    if parse:
        if is_topic_message:
            bot.send_voice(chat_id=chat, voice=dc, caption=text, message_thread_id=thr, parse_mode='HTML',
                           reply_to_message_id=reply)
        else:
            bot.send_voice(chat_id=chat, voice=dc, caption=text, parse_mode='HTML', reply_to_message_id=reply)
    else:
        if is_topic_message:
            bot.send_voice(chat_id=chat, voice=dc, caption=text, message_thread_id=thr, reply_to_message_id=reply)
        else:
            bot.send_voice(chat_id=chat, voice=dc, caption=text, reply_to_message_id=reply)


# 👊✌️✋
def getform(num):  # 0 - корова 1 - коровы 2 - коров
    if num % 100 // 10 == 1:
        return 2
    elif num % 10 == 1:
        return 0
    elif num % 10 <= 4 and num % 10 != 0:
        return 1
    else:
        return 2


def getagent(user):
    r1 = requests.get(f"{cors}https://api.scratch.mit.edu/users/{user}/projects")
    if r1.status_code == 200:
        if r1.text == "[]":
            return f"У {user} нет проектов!"
        else:
            j1 = r1.json()
            r2 = requests.get(f"{cors}https://api.scratch.mit.edu/projects/{j1[0]['id']}")
            if r2.status_code == 200:
                j2 = r2.json()
                r3 = requests.get(f"{cors}https://projects.scratch.mit.edu/{j1[0]['id']}?token={j2['project_token']}")
                if r3.status_code == 200:
                    m = json.loads(r3.text)
                    try:
                        return m.get("meta").get("agent")
                    except Exception as e:
                        return f'Ошибка: {user} - слишком старый скретчер! '
                else:
                    return "Ошибка :("
            else:
                return "Ошибка :("
    else:
        return "Ошибка :("


def getjson(p):
    r2 = requests.get(f"{cors}https://api.scratch.mit.edu/projects/{p}")
    if r2.status_code == 200:
        j2 = r2.json()
        r3 = requests.get(f"{cors}https://projects.scratch.mit.edu/{p}?token={j2['project_token']}")
        if r3.status_code == 200:
            return r3.text
        else:
            return "Ошибка :("
    else:
        return "Ошибка :("


def todec(num):
    num = str(num)
    r = 0
    for i in range(len(str(num))):
        if str(num)[i] == '1':
            r += 2 ** (len(str(num)) - (i + 1))
    return int(r)


def tobin(number, r=''):
    number = int(number)
    if number <= 1:
        return number
    return int(f'{str(tobin(number // 2, r))}{number % 2}')


def addzeros(number, length):
    return f"{'0' * (length - len(str(number)))}{str(number)}"


def rps_create():
    keyboard = telebot.types.InlineKeyboardMarkup()
    a = []
    a.append(telebot.types.InlineKeyboardButton(text="👊", callback_data="r"))
    a.append(telebot.types.InlineKeyboardButton(text="✌️", callback_data="s"))
    a.append(telebot.types.InlineKeyboardButton(text="✋", callback_data="p"))
    keyboard.add(a[0], a[1], a[2])
    return keyboard


def secretjson(id):
    r = requests.get(f'https://scratch-projects.scratch.org/{id}')
    return {'success': r.status_code == 200, 'text': r.text}


def tttgen(board, gamehere=True):
    keyboard = telebot.types.InlineKeyboardMarkup()
    d = []
    for i in range(9):
        item = board[i]
        if item == None:
            if gamehere:
                d.append(telebot.types.InlineKeyboardButton(text="ㅤ", callback_data=f"ttt{str(i)}"))
            else:
                d.append(telebot.types.InlineKeyboardButton(text="ㅤ", callback_data=f"err_end"))
        elif item == 'x':
            d.append(telebot.types.InlineKeyboardButton(text="❌", callback_data=f'err_full'))
        elif item == 'o':
            d.append(telebot.types.InlineKeyboardButton(text="⭕", callback_data=f'err_full'))
        else:
            d.append(telebot.types.InlineKeyboardButton(text="⚠️", callback_data=f'err_full'))
    keyboard.add(d[0], d[1], d[2])
    keyboard.add(d[3], d[4], d[5])
    keyboard.add(d[6], d[7], d[8])
    return keyboard


def cardsgen(cards, chosen=[], opened=[]):
    keyboard = telebot.types.InlineKeyboardMarkup()
    dd = []
    for i in range(20):
        # print(dd)
        if i in chosen:
            dd.append(telebot.types.InlineKeyboardButton(text=cards[i], callback_data=f"err_chosen"))
            # print('Added in chosen', i, dd)
        elif i in opened:
            dd.append(telebot.types.InlineKeyboardButton(text=cards[i], callback_data=f"err_chosen"))
            # print('Added in opened', i, dd)
        else:
            dd.append(telebot.types.InlineKeyboardButton(text="ㅤ", callback_data=f"card{str(i)}"))
            # print('Added in closed', i, dd)
        if (i + 1) % 5 == 0:
            # print(cards, dd, i)
            keyboard.add(dd[0], dd[1], dd[2], dd[3], dd[4], row_width=5)
            dd = []
    if len(opened) < len(cards):
        keyboard.add(telebot.types.InlineKeyboardButton(text='🔧 Починить', callback_data=f"fixcards"))
    return keyboard


def getwinner(b):
    combs = [b[0] == b[1] == b[2], b[3] == b[4] == b[5], b[6] == b[7] == b[8], b[0] == b[3] == b[6],
             b[1] == b[4] == b[7], b[2] == b[5] == b[8], b[0] == b[4] == b[8], b[2] == b[4] == b[6]]
    ress = [b[1], b[4], b[7], b[3], b[4], b[5], b[4], b[4]]
    for i in range(8):
        if combs[i] and ress[i] != None:
            return {'x': 0, 'o': 1}[ress[i]]
    return None


succ = True

try:
    remix_db = interact_with_remix_db()
    print(remix_db)
except Exception:
    succ = False
@bot.message_handler(content_types=["text"])
@bot.message_handler(content_types=["text"])
def everything(message):  # Название функции не играет никакой роли
    print(f'{message.from_user.first_name}: {message.text}')

    # if message.from_user.id == 777000 and message.chat.id == -1002108064042:
    #    bot.forward_message(from_chat_id=message.chat.id, chat_id=-1003844000741, message_id=message.message_id)
    # if message.from_user.id == 777000 and message.chat.id == -1003717893572:
    #    bot.forward_message(from_chat_id=message.chat.id, chat_id=-1003336995454, message_id=message.message_id, protect_content=True)
    # elif message.from_user.id == 777000 and message.chat.id == -1002004771264:
    #    bot.forward_message(from_chat_id=message.chat.id, chat_id=-1002501164190, message_id=message.message_id, protect_content=True)
    # elif message.from_user.id == 777000 and message.chat.id == -1003807292893:
    #        bot.forward_message(from_chat_id=message.chat.id, chat_id=-1002035207889, message_id=message.message_id, protect_content=True)
    if message.chat.id > 0 and message.from_user.id != 5184185845:
        bot.forward_message(from_chat_id=message.chat.id, chat_id=-1003767712566, message_id=message.message_id,
                            message_thread_id=28)
    if message.chat.id == -1003623810305:
        if message.message_thread_id == 5:
            bot.forward_message(from_chat_id=message.chat.id, chat_id=-1003531260500, message_id=message.message_id,
                                message_thread_id=3)
        elif message.message_thread_id == 127:
            bot.forward_message(from_chat_id=message.chat.id, chat_id=-1003531260500, message_id=message.message_id,
                                message_thread_id=5)
        elif message.message_thread_id == 40:
            bot.forward_message(from_chat_id=message.chat.id, chat_id=-1003531260500, message_id=message.message_id,
                                message_thread_id=7)
        else:
            bot.forward_message(from_chat_id=message.chat.id, chat_id=-1003531260500, message_id=message.message_id)
    if message.from_user.id == 5464616347 and message.text == 'Здравствуйте':
        msg(message.chat.id, "Здравствуйте", message.message_id, message.is_topic_message, message.message_thread_id)
    if message.from_user.id == 6954179869:
        time.sleep(random.randint(1, 10))
        bot.set_message_reaction(chat_id=message.chat.id, message_id=message.message_id,
                                 reaction=[telebot.types.ReactionTypeEmoji(random.choice(['❤️', '🥰', '❤️‍🔥']))])
    cou = False
    r = ''
    for i in message.text.split():
        if cou:
            r += f' {i}'
        if i.upper() in ['НАПИШИТЕ', 'НАПИШИ', 'ВВЕДИТЕ', 'ВВЕДИ', "ОТПРАВЬ", "ОТПРАВЬТЕ", "СКАЖИ", "СКАЖИТЕ"]:
            cou = True
    if cou and r != '':
        msg(message.chat.id, r, message.message_id, message.is_topic_message, message.message_thread_id)
    if message.from_user.id != 777000 and message.chat.id == -1002108064042:
        bot.forward_message(from_chat_id=message.chat.id, chat_id=-1003774229761, message_id=message.message_id)
        bot.forward_message(from_chat_id=message.chat.id, chat_id=-1003889896766, message_id=message.message_id)
    elif message.from_user.id != 777000 and message.chat.id == -1003774229761:
        bot.forward_message(from_chat_id=message.chat.id, chat_id=-1003889896766, message_id=message.message_id)
    if message.chat.id == -1003272408860 and message.message_thread_id in [1290, 1814, 1822]:
        bot.delete_message(chat_id=-1003272408860, message_id=message.message_id)
    elif (not message.from_user.id in blocklist) or cmd('start', message.text):
        if message.text.startswith('/studio'):
            # msg = bot.send_message(message.chat.id, "Обработка...")
            if (re.findall(r'\d+', message.text) == [] and not message.text.startswith('/studio@')) or (
                    len(re.findall(r'\d+', message.text)) == 1 and message.text.startswith('/studio@')):
                if message.text == '/studio ссылку или ID':
                    msg(message.chat.id, "Гениально...", message.message_id, message.is_topic_message,
                        message.message_thread_id)
                else:
                    msg(message.chat.id, "А какую студию? Дай ссылку или ID", message.message_id,
                        message.is_topic_message, message.message_thread_id)
            else:
                if message.text.startswith('/studio@'):
                    id = re.findall(r'\d+', message.text)[1]
                else:
                    id = re.findall(r'\d+', message.text)[0]
                m = requests.get(f"{cors}https://api.scratch.mit.edu/studios/{id}/")
                if m.status_code == 200:
                    s = m.json()
                    media(message.chat.id, f"https://uploads.scratch.mit.edu/get_image/gallery/{id}_480x360.png",
                          f'<a href="https://scratch.mit.edu/studios/{s["id"]}/"><b>{s["title"]}</b></a>\n<blockquote expandable>{s["description"][0:900]}</blockquote>\n{str(s['stats']['followers'])} {['подписчик', 'подписчика', 'подписчиков'][getform(s['stats']['followers'])]}',
                          message.message_id, message.is_topic_message, message.message_thread_id, True)
                else:
                    gr = requests.get(f"{cors}https://api.scratch.mit.edu/users/griffpatch/projects?limit=40")
                    gg = random.choice(gr.json())
                    addproj = requests.post(f"https://api.scratch.mit.edu/studios/{id}/project/{gg['id']}/",
                                            headers={"X-Token": testacc})
                    if addproj.status_code == 403:
                        media(message.chat.id, f"https://uploads.scratch.mit.edu/get_image/gallery/{id}_480x360.png",
                              '🔒 Добавлять проекты могут только кураторы', message.message_id, message.is_topic_message,
                              message.message_thread_id)
                    elif addproj.status_code == 200:
                        activity = requests.get(
                            f"{cors}https://scratch.mit.edu/messages/ajax/user-activity?user=FFFFFFFayno&max=1",
                            headers=TOKENS['scratch_activity_headers'])
                        var = activity.text
                        steps = ['<!-- templates/notifications/includes/user-feed.html -->',
                                 '<ul class="activity-stream">', '</ul>', '<li>', '</li>',
                                 '<span class="icon-xs black project"></span>', '<div>',
                                 '<span class="actor"><a href="/users/FFFFFFFayno/">FFFFFFFayno</a></span>', '<div>',
                                 f' <a href="/projects/{gg["id"]}/">{gg["title"]}</a> в студию', '<div>', '\n',
                                 f'добавлен             <a href="/studios/{id}', '/" data-tag="target">',
                                 '<span data-tag="time" class="time">0 минут назад</span>', '</a>', '</div>']
                        for step in steps:
                            var = var.replace(step, '')
                        var = var.strip()
                        media(message.chat.id, f"https://uploads.scratch.mit.edu/get_image/gallery/{id}_480x360.png",
                              var, message.message_id, message.is_topic_message, message.message_thread_id)
                    # bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text="Успешно")
                    elif addproj.status_code == 404:
                        msg(message.chat.id, "Такой студии не существует", message.message_id, message.is_topic_message,
                            message.message_thread_id)
                    else:
                        msg(message.chat.id, f"Произошла ошибка: {addproj.status_code}", message.message_id,
                            message.is_topic_message, message.message_thread_id)
        elif cmd('start', message.text):
            if message.from_user.id in blocklist:
                if message.from_user.id in [1087968824, 136817688, 777000]:
                    msg(message.chat.id,
                        "Привет!\nПисать от имени каналов и групп нельзя, чтобы нельзя было обходить игнор-лист в этом боте",
                        message.message_id, message.is_topic_message, message.message_thread_id)
                else:
                    msg(message.chat.id,
                        "Привет!\nТы находишься в чёрном списке этого бота, из-за чего все команды отключены",
                        message.message_id, message.is_topic_message, message.message_thread_id)
            else:
                msg(message.chat.id, "Привет!\n"
                                     "Я бот, форк бота, созданного @polzovatel_5555, поддерживаюсь @gervatyy!\n"
                                     "Репозиторий - https://github.com/gervaty/Bot5555\n"
                                     "Команды бота - /help",
                    message.message_id, message.is_topic_message, message.message_thread_id)
        elif message.text.startswith('/start ') and message.chat.id > 0:
            if message.text.startswith('/start r'):
                try:
                    t = base64.b64decode(
                        message.text.replace('/start r', '').replace('-', '+').replace('_', '/')).decode('utf-8')
                except Exception:
                    try:
                        t = base64.b64decode(
                            message.text.replace('/start r', '').replace('-', '+').replace('_', '/') + '=').decode(
                            'utf-8')
                    except Exception:
                        try:
                            t = base64.b64decode(
                                message.text.replace('/start r', '').replace('-', '+').replace('_', '/') + '==').decode(
                                'utf-8')
                        except Exception:
                            try:
                                t = base64.b64decode(message.text.replace('/start r', '').replace('-', '+').replace('_',
                                                                                                                    '/') + '===').decode(
                                    'utf-8')
                            except Exception:
                                t = 'Что-то пошло не так, сообщи об этом создателю: @Fedor_K10'
                msg(message.chat.id, t, message.message_id, message.is_topic_message, message.message_thread_id)
            else:
                msg(message.chat.id, f"Нажми: /start", message.message_id, message.is_topic_message,
                    message.message_thread_id)
        elif cmd('info', message.text) and message.reply_to_message == None:
            msg(message.chat.id, f"@polzovatel_5555 - канал\n@superchat_5555 - форум\n@polzovatel_chat - чат канала",
                message.message_id, message.is_topic_message, message.message_thread_id)
        elif cmd('test', message.text):
            if random.randint(1, 100) == 1:
                msg(message.chat.id, f"Это сообщение появилось с шансом 1%", message.message_id,
                    message.is_topic_message, message.message_thread_id)
        elif message.text.startswith('/project'):
            # msg = bot.send_message(message.chat.id, "Обработка...")
            if (re.findall(r'\d+', message.text) == [] and not message.text.startswith('/project@')) or (
                    len(re.findall(r'\d+', message.text)) == 1 and message.text.startswith('/project@')):
                if message.text == '/project ссылку или ID':
                    msg(message.chat.id, "Гениально...", message.message_id, message.is_topic_message,
                        message.message_thread_id)
                else:
                    msg(message.chat.id, "А какой проект? Дай ссылку или ID", message.message_id,
                        message.is_topic_message, message.message_thread_id)
            else:
                if message.text.startswith('/project@'):
                    id = re.findall(r'\d+', message.text)[1]
                else:
                    id = re.findall(r'\d+', message.text)[0]
                if len(str(id)) > 10 or int(id) % 1 > 0 or int(id) < 1:
                    msg(message.chat.id, "Без приколов пж, иначе уберу trusted", message.message_id,
                        message.is_topic_message, message.message_thread_id)
                else:
                    m = requests.get(f"{cors}https://api.scratch.mit.edu/projects/{id}/")
                    if m.status_code == 200:
                        s = m.json()
                        if s["instructions"] == '':
                            if s["description"] == '':
                                media(message.chat.id,
                                      f"https://uploads.scratch.mit.edu/get_image/project/{id}_480x360.png",
                                      f'<a href="https://scratch.mit.edu/projects/{s["id"]}/"><b>{s["title"]}</b></a>\n❤️ {str(s['stats']['loves'])} ⭐ {str(s['stats']['favorites'])} 📝 {str(s['stats']['remixes'])} 👁️ {str(s['stats']['views'])}',
                                      message.message_id, message.is_topic_message, message.message_thread_id, True)
                            else:
                                media(message.chat.id,
                                      f"https://uploads.scratch.mit.edu/get_image/project/{id}_480x360.png",
                                      f'<a href="https://scratch.mit.edu/projects/{s["id"]}/"><b>{s["title"]}</b></a>\nПримечания и благодарности:\n<blockquote expandable>{s["description"][0:850]}</blockquote>\n❤️ {str(s['stats']['loves'])} ⭐ {str(s['stats']['favorites'])} 📝 {str(s['stats']['remixes'])} 👁️ {str(s['stats']['views'])}',
                                      message.message_id, message.is_topic_message, message.message_thread_id, True)
                        else:
                            if s["description"] == '':
                                media(message.chat.id,
                                      f"https://uploads.scratch.mit.edu/get_image/project/{id}_480x360.png",
                                      f'<a href="https://scratch.mit.edu/projects/{s["id"]}/"><b>{s["title"]}</b></a>\nИнструкции:\n<blockquote expandable>{s["instructions"][0:850]}</blockquote>\n❤️ {str(s['stats']['loves'])} ⭐ {str(s['stats']['favorites'])} 📝 {str(s['stats']['remixes'])} 👁️ {str(s['stats']['views'])}',
                                      message.message_id, message.is_topic_message, message.message_thread_id, True)
                            else:
                                media(message.chat.id,
                                      f"https://uploads.scratch.mit.edu/get_image/project/{id}_480x360.png",
                                      f'<a href="https://scratch.mit.edu/projects/{s["id"]}/"><b>{s["title"]}</b></a>\nИнструкции:\n<blockquote expandable>{s["instructions"][0:425]}</blockquote>\nПримечания и благодарности:\n<blockquote expandable>{s["description"][0:425]}</blockquote>\n❤️ {str(s['stats']['loves'])} ⭐ {str(s['stats']['favorites'])} 📝 {str(s['stats']['remixes'])} 👁️ {str(s['stats']['views'])}',
                                      message.message_id, message.is_topic_message, message.message_thread_id, True)
                    else:
                        if remix_db == None:
                            remix_db = interact_with_remix_db()
                        if str(id) in remix_db:
                            if remix_db[str(id)] != None:
                                m = requests.get(f"{cors}https://api.scratch.mit.edu/projects/{remix_db[str(id)]}/",
                                                 headers={'X-Token': remixer_token})
                                print(m.text)
                                j = m.json()
                                if j['title'] == 'Untitled Project':
                                    media(message.chat.id,
                                          f"https://uploads.scratch.mit.edu/get_image/project/{id}_480x360.png",
                                          f'<a href="https://scratch.mit.edu/projects/{j["id"]}/"><i>Название подверглось цензуре</i></a>\nИнструкции:\n<blockquote expandable>{j["instructions"][0:850]}</blockquote>',
                                          message.message_id, message.is_topic_message, message.message_thread_id, True)
                                else:
                                    media(message.chat.id,
                                          f"https://uploads.scratch.mit.edu/get_image/project/{id}_480x360.png",
                                          f'<a href="https://scratch.mit.edu/projects/{j["id"]}/"><b>{j["title"][0:-6]}</b></a>\nИнструкции:\n<blockquote expandable>{j["instructions"][0:850]}</blockquote>',
                                          message.message_id, message.is_topic_message, message.message_thread_id, True)
                            else:
                                msg(message.chat.id, "Сорри, но ремикс уже делается. Ожидай ответа от бота 😎",
                                    message.message_id, message.is_topic_message, message.message_thread_id)
                        else:
                            if message.from_user.id in trusted and succ:
                                remix_db[str(id)] = None
                                try:
                                    if message.is_topic_message:
                                        bot.send_chat_action(message.chat.id, 'typing',
                                                             message_thread_id=message.message_thread_id)
                                    else:
                                        bot.send_chat_action(message.chat.id, 'typing')
                                except Exception as e:
                                    print(e)
                                remix = remixproject(id, account_remixer)
                                if remix['success']:
                                    remix_db[str(id)] = remix['value']
                                    interact_with_remix_db('put', remix_db)
                                    m = requests.get(f"{cors}https://api.scratch.mit.edu/projects/{remix_db[str(id)]}/",
                                                     headers={'X-Token': remixer_token})
                                    print(m.text)
                                    j = m.json()
                                    if j['title'] == 'Untitled Project':
                                        media(message.chat.id,
                                              f"https://uploads.scratch.mit.edu/get_image/project/{id}_480x360.png",
                                              f'<a href="https://scratch.mit.edu/projects/{j["id"]}/"><i>Название подверглось цензуре</i></a>\nИнструкции:\n<blockquote expandable>{j["instructions"][0:850]}</blockquote>',
                                              message.message_id, message.is_topic_message, message.message_thread_id,
                                              True)
                                    else:
                                        media(message.chat.id,
                                              f"https://uploads.scratch.mit.edu/get_image/project/{id}_480x360.png",
                                              f'<a href="https://scratch.mit.edu/projects/{j["id"]}/"><b>{j["title"][0:-6]}</b></a>\nИнструкции:\n<blockquote expandable>{j["instructions"][0:850]}</blockquote>',
                                              message.message_id, message.is_topic_message, message.message_thread_id,
                                              True)
                                else:
                                    remix_db.pop(str(id))
                                    media(message.chat.id,
                                          f"https://uploads.scratch.mit.edu/get_image/project/{id}_480x360.png",
                                          '⚠️ Не удалось сделать ремикс', message.message_id, message.is_topic_message,
                                          message.message_thread_id)
                            else:
                                media(message.chat.id,
                                      f"https://uploads.scratch.mit.edu/get_image/project/{id}_480x360.png",
                                      'Проект без общего доступа', message.message_id, message.is_topic_message,
                                      message.message_thread_id)
                # bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text="Успешно")
        elif message.text.startswith('/case'):
            if message.text.startswith('/case ') or message.text.startswith('/case@rsokolov3Bot '):
                try:
                    case = int(message.text.split()[1])
                except ValueError:
                    msg(message.chat.id, "Неверно передан аргумент", message.message_id, message.is_topic_message,
                        message.message_thread_id)
                finally:
                    if case % 1 == 0 and case >= 0 and case < 256 ** 4:
                        bin = f"{'0' * (32 - len(str(tobin(case, ''))))}{tobin(case, '')}"
                        # print(bin)
                        ip = f'{todec(f"{bin[0:8]}")}.{todec(f"{bin[8:16]}")}.{todec(f"{bin[16:24]}")}.{todec(f"{bin[24:32]}")}'
                        msg(message.chat.id, f'Результат: {ip}', message.message_id, message.is_topic_message,
                            message.message_thread_id)
                    else:
                        msg(message.chat.id, "И как я должен это сделать?", message.message_id,
                            message.is_topic_message, message.message_thread_id)
            else:
                msg(message.chat.id, "Не хватает аргумента", message.message_id, message.is_topic_message,
                    message.message_thread_id)
        elif message.text.startswith('/ip'):
            if message.text.startswith('/ip ') or message.text.startswith('/ip@rsokolov3Bot '):
                try:
                    ip = message.text.split()[1].split('.')
                    isval = True
                    for v in ip:
                        if int(v) < 0 or int(v) > 255:
                            isval = False
                    ok = True
                except ValueError:
                    ok = False
                    if message.text.split()[1] != 'ip':
                        if ':' in message.text.split()[1]:
                            msg(message.chat.id, "Это ipv6, гений!", message.message_id, message.is_topic_message,
                                message.message_thread_id)
                        else:
                            msg(message.chat.id, "Разве это ip?", message.message_id, message.is_topic_message,
                                message.message_thread_id)
                    else:
                        msg(message.chat.id, "Результат: результат", message.message_id, message.is_topic_message,
                            message.message_thread_id)
                if ok:
                    if len(ip) == 4 and isval:
                        case = todec(
                            f'{addzeros(tobin(ip[0]), 8)}{addzeros(tobin(ip[1]), 8)}{addzeros(tobin(ip[2]), 8)}{addzeros(tobin(ip[3]), 8)}')
                        msg(message.chat.id, f'Результат: {str(case)}', message.message_id, message.is_topic_message,
                            message.message_thread_id)
                    elif isval:
                        if len(ip) > 4:
                            msg(message.chat.id,
                                f"Съешь ещё {str(len(ip) - 4)} {['точку', 'точки', 'точек'][getform(len(ip) - 4)]}",
                                message.message_id, message.is_topic_message, message.message_thread_id)
                        else:
                            msg(message.chat.id,
                                f"Кто съел {str(4 - len(ip))} {['точку', 'точки', 'точек'][getform(4 - len(ip))]}?!",
                                message.message_id, message.is_topic_message, message.message_thread_id)
                    else:
                        if ':' in ip:
                            msg(message.chat.id, "Это ipv6, гений!", message.message_id, message.is_topic_message,
                                message.message_thread_id)
                        else:
                            msg(message.chat.id, "Разве это ip?", message.message_id, message.is_topic_message,
                                message.message_thread_id)
            else:
                msg(message.chat.id, "Эээ... А где ip?", message.message_id, message.is_topic_message,
                    message.message_thread_id)
        elif message.text.startswith('/agent'):
            if message.text.startswith('/agent ') or message.text.startswith('/agent@rsokolov3Bot '):
                if message.is_topic_message:
                    bot.send_chat_action(message.chat.id, 'typing', message_thread_id=message.message_thread_id)
                else:
                    bot.send_chat_action(message.chat.id, 'typing')
                msg(message.chat.id, getagent(message.text.split()[1]), message.message_id, message.is_topic_message,
                    message.message_thread_id)
            else:
                msg(message.chat.id, "Эта команда не должна быть пустой", message.message_id, message.is_topic_message,
                    message.message_thread_id)
        elif message.text.startswith('/messages'):
            if message.text.startswith('/messages ') or message.text.startswith('/messages@rsokolov3Bot '):
                try:
                    req = requests.get(
                        f'{cors}https://api.scratch.mit.edu/users/{message.text.split()[1]}/messages/count')
                    err = False
                except Exception as e:
                    err = True
                if err:
                    msg(message.chat.id, "Connection Error. Не удалось получить данные. Попробуй ещё раз!",
                        message.message_id, message.is_topic_message, message.message_thread_id)
                if req.status_code == 200:
                    rsp = req.json()
                    msg(message.chat.id,
                        f'У {message.text.split()[1]} {str(rsp["count"])} {["сообщение", "сообщения", "сообщений"][getform(rsp["count"])]}',
                        message.message_id, message.is_topic_message, message.message_thread_id)
                else:
                    msg(message.chat.id, "Этого пользователя не существует", message.message_id,
                        message.is_topic_message, message.message_thread_id)
            else:
                msg(message.chat.id, "Эта команда не должна быть пустой", message.message_id, message.is_topic_message,
                    message.message_thread_id)
        elif message.text == 'когда':
            if random.randint(1, 100) == 1:
                msg(message.chat.id, "Никогда", message.message_id, message.is_topic_message, message.message_thread_id)
            else:
                msg(message.chat.id, "Скоро", message.message_id, message.is_topic_message, message.message_thread_id)
        elif cmd("id", message.text):
            if message.from_user.id in trusted:
                msg(message.chat.id, "Команда /id не была удалена", message.message_id, message.is_topic_message,
                    message.message_thread_id)
            else:
                msg(message.chat.id, f'Команда /id была удалена', message.message_id, message.is_topic_message,
                    message.message_thread_id)
        elif message.text.startswith('/member'):
            if message.text.startswith('/member ') or message.text.startswith('/member@rsokolov3Bot '):
                req = requests.get(f'{cors}https://api.scratch.mit.edu/users/{message.text.split()[1]}/')
                if req.status_code == 200:
                    rsp = req.json()
                    if 'membership_avatar_badge' in rsp['profile'].keys():
                        msg(message.chat.id,
                            f'{rsp["username"]} является участником membership!\n{["❌", "✅"][int(rsp["profile"]["membership_avatar_badge"] == 1)]} Украшение аватарки\n{["❌", "✅"][int(rsp["profile"]["membership_label"] == 1)]} Метка',
                            message.message_id, message.is_topic_message, message.message_thread_id)
                    else:
                        msg(message.chat.id, f'{rsp["username"]} не является участником membership', message.message_id,
                            message.is_topic_message, message.message_thread_id)
                else:
                    msg(message.chat.id, "Этого пользователя не существует", message.message_id,
                        message.is_topic_message, message.message_thread_id)
            else:
                msg(message.chat.id, "Эта команда не должна быть пустой", message.message_id, message.is_topic_message,
                    message.message_thread_id)
        elif message.text.startswith('/sound'):
            if message.text.startswith('/sound ') or message.text.startswith('/sound@rsokolov3Bot '):
                if re.findall(r'\d+', message.text.split()[1]) == []:
                    msg(message.chat.id, "Хватит меня ломать", message.message_id, message.is_topic_message,
                        message.message_thread_id)
                else:
                    if message.is_topic_message:
                        bot.send_chat_action(message.chat.id, 'upload_voice',
                                             message_thread_id=message.message_thread_id)
                    else:
                        bot.send_chat_action(message.chat.id, 'upload_voice')
                    req = requests.get(
                        f"{cors}https://api.scratch.mit.edu/projects/{re.findall(r'\d+', message.text.split()[1])[0]}/")
                    # print(re.findall(r'\d+', message.text.split()[1]))
                    if req.status_code == 200:
                        rsp = req.json()
                        cntnt = requests.get(
                            f"{cors}https://projects.scratch.mit.edu/{re.findall(r'\d+', message.text.split()[1])[0]}?token={rsp['project_token']}")
                        # print(cntnt.text)
                        j = json.loads(cntnt.text)
                        targets = j['targets']
                        max_len = 0
                        r_sound = None
                        for target in targets:
                            for sound in target['sounds']:
                                if (sound['sampleCount'] / sound['rate']) > max_len and sound[
                                    'md5ext'] != '83c36d806dc92327b9e7049a565c6bff.wav' and sound[
                                    'md5ext'] != '83a9787d4cb6f3b7632b4ddfebf74367.wav':
                                    r_sound = sound
                        if r_sound == None:
                            msg(message.chat.id, 'Звуков не найдено', message.message_id, message.is_topic_message,
                                message.message_thread_id)
                        else:
                            # aud(message.chat.id, f"https://assets.scratch.mit.edu/{r_sound['md5ext']}", r_sound['name'], message.message_id, message.is_topic_message, message.message_thread_id)

                            if r_sound['dataFormat'] == 'mp3':
                                aud(message.chat.id, f"https://assets.scratch.mit.edu/{r_sound['md5ext']}",
                                    r_sound['name'], message.message_id, message.is_topic_message,
                                    message.message_thread_id)
                            else:
                                try:
                                    bot.send_audio(chat_id=message.chat.id, reply_to_message_id=message.message_id,
                                                   message_thread_id=message.message_thread_id, audio=requests.get(
                                            f"https://assets.scratch.mit.edu/{r_sound['md5ext']}").content,
                                                   caption=r_sound['name'])
                                except Exception:
                                    msg(message.chat.id,
                                        f"Мне не удалось отправить файл: https://assets.scratch.mit.edu/{r_sound['md5ext']}",
                                        message.message_id, message.is_topic_message, message.message_thread_id)
                    else:
                        a = secretjson(re.findall(r'\d+', message.text.split()[1])[0])
                        if a['success']:
                            j = json.loads(a['text'])
                            targets = j['targets']
                            max_len = 0
                            r_sound = None
                            for target in targets:
                                for sound in target['sounds']:
                                    if (sound['sampleCount'] / sound['rate']) > max_len and sound[
                                        'md5ext'] != '83c36d806dc92327b9e7049a565c6bff.wav' and sound[
                                        'md5ext'] != '83a9787d4cb6f3b7632b4ddfebf74367.wav':
                                        r_sound = sound
                            if r_sound == None:
                                msg(message.chat.id, 'Звуков не найдено', message.message_id, message.is_topic_message,
                                    message.message_thread_id)
                            else:
                                # aud(message.chat.id, f"https://assets.scratch.mit.edu/{r_sound['md5ext']}", r_sound['name'], message.message_id, message.is_topic_message, message.message_thread_id)

                                if r_sound['dataFormat'] == 'mp3':
                                    aud(message.chat.id, f"https://assets.scratch.mit.edu/{r_sound['md5ext']}",
                                        r_sound['name'], message.message_id, message.is_topic_message,
                                        message.message_thread_id)
                                else:
                                    try:
                                        bot.send_audio(chat_id=message.chat.id, reply_to_message_id=message.message_id,
                                                       message_thread_id=message.message_thread_id, audio=requests.get(
                                                f"https://assets.scratch.mit.edu/{r_sound['md5ext']}").content,
                                                       caption=r_sound['name'])
                                    except Exception:
                                        msg(message.chat.id,
                                            f"Мне не удалось отправить файл: https://assets.scratch.mit.edu/{r_sound['md5ext']}",
                                            message.message_id, message.is_topic_message, message.message_thread_id)

                        else:
                            msg(message.chat.id, "Этого проекта не существует", message.message_id,
                                message.is_topic_message, message.message_thread_id)
            else:
                msg(message.chat.id, "Скачать музыку из проекта бесплатно, без смс и регистрации", message.message_id,
                    message.is_topic_message, message.message_thread_id)
        elif (('youtu.be' in message.text) or ('youtube.com' in message.text)) and (len(message.text) > 18):
            vid = getid(message.text)
            print(vid)
            if vid != None:
                bypass_h = {
                    "Referer": "https://pggamer2.github.io/"
                }
                req = requests.get(
                    f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={vid}&key=AIzaSyBL2YFcQ_L9TAGh0H_EYnqLNvMPmaQU8Co",
                    headers=bypass_h)
                print(req.status_code)
                if req.status_code == 200:
                    d = req.json()
                    media(message.chat.id, d['items'][0]['snippet']['thumbnails']['high']['url'],
                          f'{d['items'][0]['snippet']['title']}\n<blockquote expandable>{d['items'][0]['snippet']['description'][0:(1000 - len(d['items'][0]['snippet']['title']))]}</blockquote>',
                          message.message_id, message.is_topic_message, message.message_thread_id, True)
        elif cmd('roulette', message.text):
            options = []
            l = random.randint(2, 12)
            for i in range(l):
                options.append(str(i + 1))
            if message.is_topic_message:
                bot.send_poll(message.chat.id, question='Русская рулетка', type='quiz',
                              correct_option_id=random.randint(0, l - 1), is_anonymous=False, options=options,
                              message_thread_id=message.message_thread_id)
            else:
                bot.send_poll(message.chat.id, question='Русская рулетка', type='quiz',
                              correct_option_id=random.randint(0, l - 1), is_anonymous=False, options=options)
        elif cmd('link', message.text):
            if message.is_topic_message:
                bot.send_message(message.chat.id, 'https://scratch.mit.edu/users/67-',
                                 message_thread_id=message.message_thread_id,
                                 link_preview_options={"is_disabled": True})
            else:
                bot.send_message(message.chat.id, 'https://scratch.mit.edu/users/67-',
                                 link_preview_options=telebot.types.LinkPreviewOptions(is_disabled=True))
        elif message.text.startswith('/echo') and message.from_user.id in trusted:
            if message.text.startswith('/echo '):
                msg(message.chat.id, message.text[6:], None, message.is_topic_message, message.message_thread_id)
            else:
                msg(message.chat.id, "Эта команда не должна быть пустой", message.message_id, message.is_topic_message,
                    message.message_thread_id)
        elif cmd('help', message.text):
            msg(message.chat.id,
                "СПИСОК КОМАНД\n<blockquote expandable>📺 Проекты:\n/project [ID/ссылка] - получает информацию о проекте\n/sound [ID/ссылка] - скачивает музыку из проекта\n🎞️ Студии:\n/studio [ID/ссылка] - получает данные студии\n👤 Люди:\n/agent [имя] - получает user agent по нику\n/member [имя] - детектор membership\n/messages [имя] - счётчик сообщений\n/randomuser - случайный профиль\n/user - показывает подробную информацию профиля scratch, включая удалённого\n🎮 Игровые:\n/roulette - создаёт викторину со случайным ответом в качестве правильного\n/rps (ответом на сообщение соперника) - камень-ножницы-бумага\n/ttt (ответом на сообщение соперника) - крестики-нолики\n/randmsg показывает случайное сообщение в чате. Если сообщение является удалённым, то бот ставит реакцию\n/clicker - простой кликер\nℹ️ Информация:\n/start - запуск бота\n/guidelines - правила пользования ботом\n/info - ресурсы бота\n/help - помощь по боту\n🤖 Другое:\n/case - получает ip адрес по case code\n/ip - получает case code по ip\n/time - показывает время некоторых скретчеров\n🔗 Отправьте ссылку на видео youtube, чтобы получить описание видео</blockquote>\n🤖 Хотите узнавать о новых командах? Они тут: @superchat_5555",
                message.message_id, message.is_topic_message, message.message_thread_id, parse=True)
        elif cmd('guidelines', message.text):
            msg(message.chat.id,
                "ПРАВИЛА ПОЛЬЗОВАНИЯ БОТОМ:\n1. Не спамить API-командами\n2. Если бот не отвечает, то подождать некоторое время, чтобы бот был включен. У создателя нет сервера, чтобы хостить 24/7\n3. Не нарушать правила в группах из /info\nСписок может пополняться новыми правилами.\nВсе полученные сообщения логируются, чтобы в случае ошибок находить и исправлять их.\nЗа нарушения правил Вы будете добавлены в игнор-лист",
                message.message_id, message.is_topic_message, message.message_thread_id)
        elif message.text.startswith('/proxy'):
            if message.text.startswith('/proxy ') or message.text.startswith('/proxy@rsokolov3Bot '):
                doc(message.chat.id, message.text.split()[1], None, message.message_id, message.is_topic_message,
                    message.message_thread_id)
            else:
                msg(message.chat.id, "Эта команда не должна быть пустой", message.message_id, message.is_topic_message,
                    message.message_thread_id)
        elif cmd('rps', message.text):
            if message.reply_to_message != None:
                if message.from_user.id != message.reply_to_message.json['from']['id']:
                    if message.reply_to_message.json['from']['is_bot']:
                        msg(message.chat.id, "🤖 Ты не можешь играть с ботами. Они не умеют нажимать на кнопки!",
                            message.message_id, message.is_topic_message, message.message_thread_id)
                    else:
                        players = [{"name": message.from_user.first_name, "id": message.from_user.id},
                                   {"name": message.reply_to_message.json['from']['first_name'],
                                    "id": message.reply_to_message.json['from']['id']}]
                        randpl = random.randint(0, 1)
                        botmsg = bot.send_message(chat_id=message.chat.id,
                                                  text=f"Камень-ножницы-бумага!\n🎲 Ходит: {players[randpl]['name']}",
                                                  reply_markup=rps_create(),
                                                  message_thread_id=message.message_thread_id)  # msg(message.chat.id, "Укажите соперника, ответив на его сообщение", message.message_id, message.is_topic_message, message.message_thread_id)
                        if message.is_topic_message:
                            uniqueid = f'{str(message.chat.id)}{str(message.message_thread_id)}{str(botmsg.message_id)}'
                        else:
                            uniqueid = f'{str(message.chat.id)}None{str(botmsg.message_id)}'
                        rps_db[uniqueid] = {'players': players, 'player': randpl, 'step': 1,
                                            'secret': None}  # 1 - не выбрано, 2 - 50%, 3 - конец игры
                        # print(uniqueid)
                else:
                    msg(message.chat.id, "👥 Ты не можешь играть с собой!", message.message_id, message.is_topic_message,
                        message.message_thread_id)
            else:
                msg(message.chat.id, "Ответь командой на сообщение соперника, чтобы начать", message.message_id,
                    message.is_topic_message, message.message_thread_id)
        elif cmd('debug', message.text):
            print(message)
            msg(message.chat.id, f"Айди: {message.reply_to_message.json['message_id']}\nВсё остальное в консоли",
                message.message_id, message.is_topic_message,
                message.message_thread_id)  # message.reply_to_message.json['from']['first_name']
        elif message.text.startswith('/tts'):
            if cmd('tts', message.text):
                if message.reply_to_message != None:
                    try:
                        voice(message.chat.id,
                              f"https://synthesis-service.scratch.mit.edu/synth?locale=ru-RU&gender=male&text={message.reply_to_message.json['text']}",
                              None, message.message_id, message.is_topic_message, message.message_thread_id)
                    except Exception as e:
                        print(e)
                        doc(message.chat.id,
                            f"https://synthesis-service.scratch.mit.edu/synth?locale=ru-RU&gender=male&text={message.reply_to_message.json['text']}",
                            None, message.message_id, message.is_topic_message, message.message_thread_id)
                else:
                    msg(message.chat.id,
                        "Использовать эту команду можно двумя способами:\n/tts Синтезируемый текст\n/tts (Ответом на нужное сообщение)",
                        message.message_id, message.is_topic_message, message.message_thread_id)
            elif message.text.startswith('/tts '):
                try:
                    voice(message.chat.id,
                          f"https://synthesis-service.scratch.mit.edu/synth?locale=ru-RU&gender=male&text={message.text[5:]}",
                          None, message.message_id, message.is_topic_message, message.message_thread_id)
                except Exception as e:
                    print(e)
                    doc(message.chat.id,
                        f"https://synthesis-service.scratch.mit.edu/synth?locale=ru-RU&gender=male&text={message.text[5:]}",
                        None, message.message_id, message.is_topic_message, message.message_thread_id)
        elif cmd('ttt', message.text):
            if message.reply_to_message != None:
                if message.from_user.id != message.reply_to_message.json['from'][
                    'id'] or message.from_user.id in trusted:
                    if message.reply_to_message.json['from']['is_bot']:
                        msg(message.chat.id, "🤖 Ты не можешь играть с ботами. Они не умеют нажимать на кнопки!",
                            message.message_id, message.is_topic_message, message.message_thread_id)
                    else:
                        xo = ['x', 'o']
                        randpl = 0
                        players = [{"name": message.from_user.first_name, "id": message.from_user.id},
                                   {"name": message.reply_to_message.json['from']['first_name'],
                                    "id": message.reply_to_message.json['from']['id']}]
                        random.shuffle(players)
                        players[0]["sign"] = xo[0]
                        players[1]["sign"] = xo[1]

                        botmsg = bot.send_message(chat_id=message.chat.id,
                                                  text=f"Крестики-нолики!\n❌ Ходит: {players[randpl]['name']}",
                                                  reply_markup=tttgen([None] * 9),
                                                  message_thread_id=message.message_thread_id)  # msg(message.chat.id, "Укажите соперника, ответив на его сообщение", message.message_id, message.is_topic_message, message.message_thread_id)
                        if message.is_topic_message:
                            uniqueid = f'{str(message.chat.id)}{str(message.message_thread_id)}{str(botmsg.message_id)}'
                        else:
                            uniqueid = f'{str(message.chat.id)}None{str(botmsg.message_id)}'
                        ttt_db[uniqueid] = {'players': players, 'player': randpl,
                                            'board': [None] * 9}  # 1 - не выбрано, 2 - 50%, 3 - конец игры
                        # print(uniqueid)
                else:
                    msg(message.chat.id,
                        "👥 Ты не можешь играть с собой!\n<tg-spoiler>🤫 <i>Некоторые могут обойти это ограничение</i></tg-spoiler>",
                        message.message_id, message.is_topic_message, message.message_thread_id, parse=True)
            else:
                msg(message.chat.id, "Ответь командой на сообщение соперника, чтобы начать", message.message_id,
                    message.is_topic_message, message.message_thread_id)
        elif cmd('p', message.text) and message.from_user.id in trusted:
            if message.reply_to_message != None:
                try:
                    bot.pin_chat_message(chat_id=message.chat.id,
                                         message_id=message.reply_to_message.json['message_id'],
                                         disable_notification=True)
                except Exception:
                    bot.set_message_reaction(chat_id=message.chat.id, message_id=message.message_id,
                                             reaction=[telebot.types.ReactionTypeEmoji('😢')])
            else:
                msg(message.chat.id, "Эта штука для закрепления сообщений пользователям призрака", message.message_id,
                    message.is_topic_message, message.message_thread_id)
        elif cmd('unp', message.text) and message.from_user.id in trusted:
            if message.reply_to_message != None:
                try:
                    bot.unpin_chat_message(chat_id=message.chat.id,
                                           message_id=message.reply_to_message.json['message_id'])
                except Exception:
                    bot.set_message_reaction(chat_id=message.chat.id, message_id=message.message_id,
                                             reaction=[telebot.types.ReactionTypeEmoji('😢')])
            else:
                msg(message.chat.id, "Эта штука для открепления сообщений пользователям призрака", message.message_id,
                    message.is_topic_message, message.message_thread_id)
        elif cmd('button', message.text):
            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.add(telebot.types.InlineKeyboardButton(text="Кнопка", callback_data="button"))
            keyboard.add(telebot.types.InlineKeyboardButton(text="Кнопка",
                                                            copy_text=telebot.types.CopyTextButton('Секретный текст')))
            keyboard.add(telebot.types.InlineKeyboardButton(text="Кнопка", url='tg://settings'))
            bot.send_message(message.chat.id, "Тест", reply_markup=keyboard)
        elif cmd('opt', message.text) and message.from_user.id in trusted:
            if message.is_topic_message:
                try:
                    bot.reopen_forum_topic(chat_id=message.chat.id, message_thread_id=message.message_thread_id)
                except Exception:
                    bot.set_message_reaction(chat_id=message.chat.id, message_id=message.message_id,
                                             reaction=[telebot.types.ReactionTypeEmoji('😢')])
            else:
                msg(message.chat.id, "Эта штука для открытия тем пользователям призрака", message.message_id,
                    message.is_topic_message, message.message_thread_id)
        elif cmd('clt', message.text) and message.from_user.id in trusted:
            if message.is_topic_message:
                try:
                    bot.close_forum_topic(chat_id=message.chat.id, message_thread_id=message.message_thread_id)
                except Exception:
                    bot.set_message_reaction(chat_id=message.chat.id, message_id=message.message_id,
                                             reaction=[telebot.types.ReactionTypeEmoji('😢')])
            else:
                msg(message.chat.id, "Эта штука для закрытия тем пользователям призрака", message.message_id,
                    message.is_topic_message, message.message_thread_id)
        elif cmd('cards', message.text):
            if message.from_user.id in trusted:
                if message.reply_to_message == None:
                    cards = random.choice([['🍬', '🍫', '🍪', '🍕', '🍩', '🍦', '🍭', '🥐', '🍰', '🥨'],
                                           ['🗿', '💀', '🤯', '🫠', '🤓', '🚨', '🌚', '🤠', '🧐', '🫡'],
                                           ['🐱', '🐶', '🐭', '🦊', '🐻', '🐼', '🐥', '🐸', '🐵', '🐙']])
                    cards *= 2
                    random.shuffle(cards)
                    # print(cards)
                    # players[0]["sign"] = xo[0]
                    # players[1]["sign"] = xo[1]

                    botmsg = bot.send_message(chat_id=message.chat.id,
                                              text=f"Игра с карточками!\n🎲 Играет: {message.from_user.first_name}\nИспользуется режим на одного игрока. Для использования режима на двоих нужно ответить командой /cards на сообщение соперника",
                                              reply_markup=cardsgen(cards),
                                              message_thread_id=message.message_thread_id)  # msg(message.chat.id, "Укажите соперника, ответив на его сообщение", message.message_id, message.is_topic_message, message.message_thread_id)
                    if message.is_topic_message:
                        uniqueid = f'{str(message.chat.id)}{str(message.message_thread_id)}{str(botmsg.message_id)}'
                    else:
                        uniqueid = f'{str(message.chat.id)}None{str(botmsg.message_id)}'
                    cards_db[uniqueid] = {'mode': 1,
                                          'player': {'id': message.from_user.id, 'name': message.from_user.first_name},
                                          'cards': cards, 'chosen': [], 'opened': [],
                                          'tries': 0}  # 1 - не выбрано, 2 - 50%, 3 - конец игры
                    # print(uniqueid)
                else:
                    msg(message.chat.id, "Скоро на двоих...\n- когда\n- Скоро", message.message_id,
                        message.is_topic_message, message.message_thread_id)
            else:
                msg(message.chat.id,
                    "Это только для людей из trusted, потому что эта игра требует частого изменения сообщения, что быстро приводит к попаданию в рейт-лимиты",
                    message.message_id, message.is_topic_message, message.message_thread_id)
        elif cmd('randomuser', message.text):
            if message.is_topic_message:
                bot.send_chat_action(message.chat.id, 'typing', message_thread_id=message.message_thread_id)
            else:
                bot.send_chat_action(message.chat.id, 'typing')
            ru = requests.get('https://scratchinfo.quuq.dev/api/v1/users/random')
            if ru.status_code == 200:
                msg(message.chat.id, f'<a href="https://scratch.mit.edu/users/{ru.text}/">{ru.text}</a>',
                    message.message_id, message.is_topic_message, message.message_thread_id, parse=True)
            else:
                msg(message.chat.id, f'Ошибка, API недоступен', message.message_id, message.is_topic_message,
                    message.message_thread_id)
        elif message.text.startswith('/login'):
            if message.from_user.id in supertrusted:
                data = message.text.split(' ', 2)
                account = login(data[1], data[2])
                text = f"{data[1]}\n"
                if account["success"]:
                    if account["isbanned"]:
                        text += "#Забаненные\n"
                    text += f"{account['email']}\n"
                    text += f'<span class="tg-spoiler">{account["token"]}</span>\n'
                    text += f'<blockquote expandable>ТУТ\nКУКИ\n(НЕ ПОКАЗЫВАТЬ)\n{account["cookie"]}</blockquote>'
                else:
                    text += f"#Неуспешные\n{account['msg']}"
                msg(message.chat.id, text, message.message_id, message.is_topic_message, message.message_thread_id,
                    parse=True)
            else:
                msg(message.chat.id, 'Обратись к 5555', message.message_id, message.is_topic_message,
                    message.message_thread_id, parse=True)
        elif 'СОСИРС' in message.text.upper() or 'СКРЕТЧЕН' in message.text.upper() or 'SCRATCHEN' in message.text.upper() or 'SOSIRS' in message.text.upper():
            if message.chat.id == -1002547061249 or message.chat.id == 5184185845:
                msg(message.chat.id, "Хватит", message.message_id, message.is_topic_message, message.message_thread_id)
        elif message.text.startswith('/getjson'):
            if message.text.startswith('/getjson ') or message.text.startswith('/getjson@rsokolov3Bot '):
                if message.is_topic_message:
                    bot.send_chat_action(message.chat.id, 'typing', message_thread_id=message.message_thread_id)
                else:
                    bot.send_chat_action(message.chat.id, 'typing')
                msg(message.chat.id, f'<blockquote expandable>{getjson(message.text.split()[1])}</blockquote>',
                    message.message_id, message.is_topic_message, message.message_thread_id, parse=True)
            else:
                msg(message.chat.id, "Эта команда не должна быть пустой", message.is_topic_message,
                    message.message_thread_id)
        elif cmd('стырить', message.text) and message.from_user.id in trusted:
            if message.reply_to_message != None:
                try:
                    bot.forward_message(chat_id=message.from_user.id, from_chat_id=message.chat.id,
                                        message_id=message.reply_to_message.json['message_id'])
                    msg(message.chat.id, "Готово!", message.message_id, message.is_topic_message,
                        message.message_thread_id)
                except Exception:
                    msg(message.chat.id, "Запусти меня пж 🥺", message.message_id, message.is_topic_message,
                        message.message_thread_id)
            else:
                msg(message.chat.id, "А что стырить?", message.message_id, message.is_topic_message,
                    message.message_thread_id)
        elif message.text == 'а почему система не хочет чтоб основной профиль видел рабочий':
            msg(message.chat.id, "Чтобы приложения из одного профиля не видели содержимое другого", message.message_id,
                message.is_topic_message, message.message_thread_id)
        # elif message.text.startswith('/ban') or message.text.startswith('/mute') or message.text.startswith('/kick') or message.text.startswith('/warn') or message.text.startswith('/del'):
        #    if message.chat.id == -1001953022316:
        #        if message.from_user.id == 1413199933:
        #            msg(message.chat.id, random.choice(["Хватит злить Фёдора!", "Сколько можно злить Фёдора?", "Перестаньте злить Фёдора!", "Фёдор хороший, его злить нельзя", "Нарушать правила - ошибка\nЗлить Фёдора - фатальная ошибка"]), message.message_id, message.is_topic_message, message.message_thread_id)
        #        elif message.from_user.id != 5184185845:
        #            msg(message.chat.id, "Хватит нарушать правила!", message.message_id, message.is_topic_message, message.message_thread_id)
        # elif message.text.startswith('/unban') or message.text.startswith('/unmute'):
        #    if message.chat.id == -1001953022316:
        ##        if message.from_user.id == 1413199933:
        #            msg(message.chat.id, random.choice(["Фёдор сегодня добри 🤗\nЦените это!"]), message.message_id, message.is_topic_message, message.message_thread_id)
        elif cmd('орбузеры', message.text):
            time.sleep(2)
            msg(message.chat.id, "Живите с этим", None, message.is_topic_message, message.message_thread_id)
        elif message.text == 'и' and message.from_user.id == 7417081858:
            msg(message.chat.id, "й", None, message.is_topic_message, message.message_thread_id)
        elif cmd('getvidname', message.text):
            if message.reply_to_message != None:
                if 'video' in message.reply_to_message.json.keys():
                    msg(message.chat.id, message.reply_to_message.json['video']['file_name'], message.message_id,
                        message.is_topic_message, message.message_thread_id)
            else:
                msg(message.chat.id, "Ответь на сообщение с видео", message.message_id, message.is_topic_message,
                    message.message_thread_id)
        elif message.text.startswith('/get') and message.from_user.id in supertrusted:
            if message.text.startswith('/get ') or message.text.startswith('/get@rsokolov3Bot '):
                req = requests.get(f'{message.text.split()[1]}', headers={"User-Agent": 'curl/8.18.0'})
                try:
                    msg(message.chat.id, f"<blockquote expandable>{req.text}</blockquote>", message.message_id,
                        message.is_topic_message, message.message_thread_id, parse=True)
                except Exception:
                    msg(message.chat.id, "Не удалось отправить сообщение", message.message_id, message.is_topic_message,
                        message.message_thread_id)
            else:
                msg(message.chat.id, "Эта команда не должна быть пустой", message.message_id, message.is_topic_message,
                    message.message_thread_id)
        elif message.text.startswith('/get') and message.from_user.id in trusted:
            if message.text.startswith('/get ') or message.text.startswith('/get@rsokolov3Bot '):
                msg(message.chat.id,
                    "Эта команда особенная. Доступ к ней имеют всего 4 человека, потому что она позволяет отправлять GET-запросы на любые URL-адреса от моего имени!",
                    message.message_id, message.is_topic_message, message.message_thread_id)
        elif message.text.startswith('/ayu'):
            if message.text.startswith('/ayu ') or message.text.startswith('/ayu@rsokolov3Bot '):
                if message.reply_to_message != None:
                    if len(message.reply_to_message.json['text']) > 99:
                        txt = message.reply_to_message.json['text'][0:100] + '…'
                    else:
                        txt = message.reply_to_message.json['text']
                    if 'username' in message.reply_to_message.json['from'].keys():
                        msg(message.chat.id,
                            f'<blockquote><b><a href="https://t.me/{message.reply_to_message.json['from']['username']}">{message.reply_to_message.json['from']['first_name']}</a></b>\n{txt}</blockquote>{message.text.split(' ', 1)[1]}',
                            None, message.is_topic_message, message.message_thread_id, parse=True)
                    else:
                        msg(message.chat.id,
                            f'<blockquote><b><a href="tg://user?id={message.reply_to_message.json['from']['id']}">{message.reply_to_message.json['from']['first_name']}</a></b>\n{txt}</blockquote>{message.text.split(' ', 1)[1]}',
                            None, message.is_topic_message, message.message_thread_id, parse=True)

                else:
                    msg(message.chat.id, "Ответь на нужное сообщение", message.message_id, message.is_topic_message,
                        message.message_thread_id)
            else:
                msg(message.chat.id, "Напиши текст после команды", message.message_id, message.is_topic_message,
                    message.message_thread_id)
        # elif len(message.text) == 1:
        #    if message.reply_to_message != None:
        #        msg(message.chat.id, chr(ord(message.text[0])+1), message.message_id, message.is_topic_message, message.message_thread_id)
        #    else:
        #       msg(message.chat.id, chr(ord(message.text[0])+1), None, message.is_topic_message, message.message_thread_id)
        elif message.text == 'poop' or 'poopy' in message.text:
            bot.set_message_reaction(chat_id=message.chat.id, message_id=message.message_id,
                                     reaction=[telebot.types.ReactionTypeEmoji('💩')])
        elif message.text.startswith('/linkbtn'):
            dataa = message.text.split(' ', 2)
            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.add(telebot.types.InlineKeyboardButton(text=dataa[2], url=dataa[1]))
            bot.send_message(message.chat.id, "ㅤ", reply_markup=keyboard, message_thread_id=message.message_thread_id)

        # elif message.text == 'квквкверерербан':
        #    keyboard = telebot.types.InlineKeyboardMarkup()
        #    keyboard.add(telebot.types.InlineKeyboardButton(text="Разбанить", callback_data='unbanqwerty'))
        #    bot.send_message(chat_id=-1002491394762, message_thread_id=20, reply_to_message_id=12729, reply_markup=keyboard, text='Нажми на кнопку ниже, чтобы получить разбан. Но стикеры не проси, иначе опять будет бан')
        elif message.text.startswith('/copybtn'):
            dataa = message.text.split(' ', 3)
            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.add(
                telebot.types.InlineKeyboardButton(text=dataa[3], copy_text=telebot.types.CopyTextButton(dataa[2])))
            bot.send_message(message.chat.id, dataa[1], reply_markup=keyboard,
                             message_thread_id=message.message_thread_id)
        elif (cmd('normalise', message.text) or cmd('antislut', message.text) or cmd('normalizate',
                                                                                     message.text) or cmd('normalize',
                                                                                                          message.text)) and message.from_user.id in trusted:
            if message.reply_to_message != None:
                r = ''
                for l in message.reply_to_message.json['text']:
                    n = getlt(l)
                    if int(n) == -1:
                        if (l in '–—/$,.-+1245789_=!"№;%:?*()`~<>{}[]\'@;\\') == False:
                            r += ''
                    if getlt(message.reply_to_message.json['text']) != 33:
                        if l in '–—/$,.-+1245789_=!"№;%:?*()`~<>{}[]\'@;\\':
                            r += l
                        else:
                            r += sldb[n][0]
                msg(message.chat.id, f"Результат расшифровки:\n<blockquote expandable>{r}</blockquote>",
                    message.message_id, message.is_topic_message, message.message_thread_id, parse=True)
            else:
                msg(message.chat.id, f"Ответом на сообщение", message.message_id, message.is_topic_message,
                    message.message_thread_id)
        elif re.search(r"\d{10}:[a-zA-Z0-9-_]{35}", message.text):
            if re.search(r"\d{10}:[a-zA-Z0-9-_]{35}", message.text)[0] == bot.token:
                if message.chat.id < 0:
                    blocklist.append(message.from_user.id)
                    msg(message.chat.id, f"Поздравляю! Ты попал в блоклист, потому что спалил всем токен",
                        message.message_id, message.is_topic_message, message.message_thread_id)
                else:
                    msg(message.chat.id, random.choice(
                        ["Хацкер", "Меня взломали 😭", "Кажется, кто-то знает про команду /eval",
                         "КАК ТЫ УЗНАЛ МОЙ ТОКЕН?!?!? 😨", "Шпасиба, теперь все в этой группе знают мой токен",
                         "Нееееееееееееет не взламывай меня! 😧", "Меня взломали 🫠",
                         f"Теперь мы знаем, что {message.from_user.first_name} - хакер", "Ах ты взломщик!"]),
                        message.message_id, message.is_topic_message, message.message_thread_id)
            else:
                a = requests.get(
                    f'https://api.telegram.org/bot{re.search(r"\d{10}:[a-zA-Z0-9-_]{35}", message.text)[0]}/getMe')
                if a.status_code == 200:
                    msg(message.chat.id, f"Хахахах, спасибо за токен от @{a.json()['result']['username']}!",
                        message.message_id, message.is_topic_message, message.message_thread_id)
                else:
                    msg(message.chat.id, f"Не работает :(", message.message_id, message.is_topic_message,
                        message.message_thread_id)
        elif cmd('hidegen', message.text) and message.from_user.id in trusted:
            bot.hide_general_forum_topic(chat_id=message.chat.id)
            bot.promote_chat_member()
        elif message.text.startswith('/eval'):
            if message.text.startswith('/eval ') or message.text.startswith('/eval@rsokolov3Bot '):
                if message.from_user.id in trusted:
                    # msg(message.chat.id, f"https://t.me/pojvera_chat/137163", message.message_id, message.is_topic_message, message.message_thread_id)
                    comm = message.text.split(' ', 1)[1]
                    forbidden = ['exec', 'eval', 'token', 'requests', 'import', 'os.', 'shutdown', 'delete', '__file__',
                                 '.pop', 'blocklist.append', 'bot.', 'everything', 'compile', 'locals', 'dir()',
                                 'builtins', '__', 'globals', 'message', 'exit', 'quit', 'clear', 'getattr', 'copy',
                                 'trusted.', 'blocklist.', 'open', '**', ').', 'set_my', 'listdir', 'system', 'dir',
                                 'vars','append', 'insert', 'remove', 'blocklist', 'supertrusted', 'trusted', 'copy']
                    replacements = 'Ах ты хакер!'
                    if message.from_user.id in supertrusted:
                        forbidden = ['__import__']
                    is_safe = True
                    for rule in forbidden:
                        if rule in comm:
                            is_safe = False
                            break
                    if is_safe:
                        forbidden = 'Всё, теперь это стирается после обработки'
                        try:
                            r = str(eval(comm))
                            replacements = [[bot.token, TOKENS['eval_mask_token']],
                                            [forbidden, 'None']]
                            for rep in replacements:
                                r = r.replace(rep[0], rep[1])
                            msg(message.chat.id, r.replace('42', '43'), message.message_id, message.is_topic_message,
                                message.message_thread_id)
                        except Exception as e:
                            msg(message.chat.id, f"Ошибка:\n{e}", message.message_id, message.is_topic_message,
                                message.message_thread_id)
                    else:
                        msg(message.chat.id, f"НИЗЯ ИСПОЛЬЗОВАТЬ {rule}!!!", message.message_id,
                            message.is_topic_message, message.message_thread_id)
                elif message.from_user.id in trusted == False:
                    msg(message.chat.id, "Использовать её могу только я", message.message_id, message.is_topic_message,
                        message.message_thread_id)
            else:
                msg(message.chat.id, f"А какой код мне выполнять?", message.message_id, message.is_topic_message,
                    message.message_thread_id)
        elif cmd('time', message.text):
            msg(message.chat.id,
                f"МСК: {datetime.now().hour}:{addzeros(datetime.now().minute, 2)}\nУ Тиги: {(datetime.now().hour - 1) % 24}:{addzeros(datetime.now().minute, 2)}\nУ Мираза: {(datetime.now().hour + 2) % 24}:{addzeros(datetime.now().minute, 2)}\nУ Дамира: {(datetime.now().hour + 4) % 24}:{addzeros(datetime.now().minute, 2)}\nУ Лобо: {(datetime.now().hour + 5) % 24}:{addzeros(datetime.now().minute, 2)}\nКого ещё добавить?",
                message.message_id, message.is_topic_message, message.message_thread_id)
        elif cmd('here', message.text):
            if message.chat.username == None:
                os.system(f"start tg://privatepost?channel={str(message.chat.id).replace('-100', '')}")
            else:
                os.system(f"start tg://resolve?domain={message.chat.username}")
            bot.set_message_reaction(chat_id=message.chat.id, message_id=message.message_id,
                                     reaction=[telebot.types.ReactionTypeEmoji('👌')])
        elif cmd('randmsg', message.text):
            try:
                bot.forward_message(chat_id=message.chat.id, from_chat_id=message.chat.id,
                                    message_id=random.randint(1, message.id),
                                    message_thread_id=message.message_thread_id)
            except Exception as e:
                bot.set_message_reaction(chat_id=message.chat.id, message_id=message.message_id,
                                         reaction=[telebot.types.ReactionTypeEmoji('🤔')])
        elif cmd('restart', message.text) and message.from_user.id in supertrusted:
            os.system(f'start {__file__}')
            bot.stop_polling()
        elif message.text.startswith('/dm ') and message.from_user.id in trusted:
            data = message.text.split(' ', 2)
            try:
                mmmmm = bot.send_message(data[1], data[2])
                msg(message.chat.id, f"Отправлено! ID: {mmmmm.message_id}", message.message_id,
                    message.is_topic_message, message.message_thread_id)
            except Exception:
                msg(message.chat.id, f"У меня нет права на отпраку сообщений в его лс", message.message_id,
                    message.is_topic_message, message.message_thread_id)
        elif message.text.startswith('/user'):
            if message.text.startswith('/user ') or message.text.startswith('/user@rsokolov3Bot '):
                username = message.text.split()[1]
                main_data = requests.get(f'https://api.scratch.mit.edu/users/{username}/')
                if main_data.status_code == 404:
                    msg(message.chat.id, f"Скретчер {username} не найден", message.message_id, message.is_topic_message,
                        message.message_thread_id)
                elif main_data.status_code == 200:
                    deleted = requests.get(f'https://scratch.mit.edu/users/{username}/').status_code == 404
                    username = main_data.json()['username']
                    is_student = requests.get(
                        f'https://scratch.mit.edu/site-api/classrooms/moderate/profile/{username}/thumbnail').status_code == 403
                    messages = requests.get(f'https://api.scratch.mit.edu/users/{username}/messages/count').json()[
                        'count']
                    feat = requests.get(f'https://scratch.mit.edu/site-api/users/all/{username}/',
                                        headers=account_remixer)
                    date_string = main_data.json()["history"]["joined"]
                    dt = datetime.fromisoformat(date_string.replace("Z", "+00:00"))
                    utc_tz = pytz.UTC
                    msk_tz = pytz.timezone("Europe/Moscow")
                    dt_msk = dt.astimezone(msk_tz)
                    months = {'January': 'января', 'February': 'февраля', 'March': 'марта', 'April': 'апреля',
                              'May': 'мая', 'June': 'июня', 'July': 'июля', 'August': 'августа',
                              'September': 'сентября', 'October': 'октября', 'November': 'ноября',
                              'December': 'декабря'}
                    if deleted:
                        keyboard = telebot.types.InlineKeyboardMarkup()
                        keyboard.add(telebot.types.InlineKeyboardButton(text="Проекты",
                                                                        url=f'https://scratch.mit.edu/projects/all/{username}/public/'),
                                     telebot.types.InlineKeyboardButton(text="Избранные",
                                                                        url=f'https://scratch.mit.edu/projects/all/{username}/favorites/'),
                                     telebot.types.InlineKeyboardButton(text="Понравившиеся",
                                                                        url=f'https://scratch.mit.edu/projects/all/{username}/loves/'))
                        keyboard.add(telebot.types.InlineKeyboardButton(text="Студии с подпиской",
                                                                        url=f'https://scratch.mit.edu/users/{username}/studios_following/'),
                                     telebot.types.InlineKeyboardButton(text="Курируемые",
                                                                        url=f'https://scratch.mit.edu/users/{username}/studios/'))
                        keyboard.add(telebot.types.InlineKeyboardButton(text="Подписки",
                                                                        url=f'https://scratch.mit.edu/users/{username}/following/'),
                                     telebot.types.InlineKeyboardButton(text="Подписчики",
                                                                        url=f'https://scratch.mit.edu/users/{username}/followers/'))
                        keyboard.add(telebot.types.InlineKeyboardButton(text="Активность",
                                                                        url=f'https://scratch.mit.edu/messages/ajax/user-activity?user={username}'),
                                     telebot.types.InlineKeyboardButton(text="Аватарка",
                                                                        url=f'https://uploads.scratch.mit.edu/get_image/user/{main_data.json()["id"]}_500x500.png'))
                        a_a = "" if feat.json()["featured_project_data"] == None else (
                            f'{feat.json()["featured_project_label_name"]}:\n<a href="https://scratch.mit.edu/projects/{feat.json()["featured_project_data"]["id"]}/">{feat.json()["featured_project_data"]["title"]}</a>\n\n')
                        about = "" if main_data.json()["profile"][
                                          "bio"] == "" else f'Обо мне:<blockquote expandable>{protect(main_data.json()["profile"]["bio"])}</blockquote>\n'
                        status = "" if main_data.json()["profile"][
                                           "status"] == "" else f'Над чем я работаю:<blockquote expandable>{protect(main_data.json()["profile"]["status"])}</blockquote>\n'
                        bot.send_message(message.chat.id,
                                         f'<b><a hef="https://scratch.mit.edu/users/{username}/">{username}</a></b> 🗑️ {"🎓" if is_student else ""}\n{main_data.json()["profile"]["country"]} | Присоединился(ась) {dt_msk.strftime("%d ") + months[dt_msk.strftime("%B")] + dt_msk.strftime(" %Y года, %H:%M:%S МСК")} | {messages} {["сообщение", "сообщения", "сообщений"][getform(messages)]}\n\n{a_a}{about}{status}',
                                         reply_to_message_id=message.message_id,
                                         message_thread_id=message.message_thread_id, parse_mode='HTML',
                                         reply_markup=keyboard)
                    else:
                        keyboard = telebot.types.InlineKeyboardMarkup()
                        keyboard.add(telebot.types.InlineKeyboardButton(text="Проекты",
                                                                        url=f'https://scratch.mit.edu/users/{username}/projects/'),
                                     telebot.types.InlineKeyboardButton(text="Избранные",
                                                                        url=f'https://scratch.mit.edu/users/{username}/favorites/'),
                                     telebot.types.InlineKeyboardButton(text="Понравившиеся",
                                                                        url=f'https://scratch.mit.edu/projects/all/{username}/loves/'))
                        keyboard.add(telebot.types.InlineKeyboardButton(text="Студии с подпиской",
                                                                        url=f'https://scratch.mit.edu/users/{username}/studios_following/'),
                                     telebot.types.InlineKeyboardButton(text="Курируемые",
                                                                        url=f'https://scratch.mit.edu/users/{username}/studios/'))
                        keyboard.add(telebot.types.InlineKeyboardButton(text="Подписки",
                                                                        url=f'https://scratch.mit.edu/users/{username}/following/'),
                                     telebot.types.InlineKeyboardButton(text="Подписчики",
                                                                        url=f'https://scratch.mit.edu/users/{username}/followers/'))
                        keyboard.add(telebot.types.InlineKeyboardButton(text="Активность",
                                                                        url=f'https://scratch.mit.edu/messages/ajax/user-activity?user={username}'),
                                     telebot.types.InlineKeyboardButton(text="Аватарка",
                                                                        url=f'https://uploads.scratch.mit.edu/get_image/user/{main_data.json()["id"]}_500x500.png'))
                        a_a = "" if feat.json()["featured_project_data"] == None else (
                            f'{feat.json()["featured_project_label_name"]}:\n<a href="https://scratch.mit.edu/projects/{feat.json()["featured_project_data"]["id"]}/">{feat.json()["featured_project_data"]["title"]}</a>\n\n')
                        about = "" if main_data.json()["profile"][
                                          "bio"] == "" else f'Обо мне:<blockquote expandable>{protect(main_data.json()["profile"]["bio"])}</blockquote>\n'
                        status = "" if main_data.json()["profile"][
                                           "status"] == "" else f'Над чем я работаю:<blockquote expandable>{protect(main_data.json()["profile"]["status"])}</blockquote>\n'
                        bot.send_message(message.chat.id,
                                         f'<b><a hef="https://scratch.mit.edu/users/{username}/">{username}</a></b> {"🎓" if is_student else ""}\n{main_data.json()["profile"]["country"]} | Присоединился(ась) {dt_msk.strftime("%d ") + months[dt_msk.strftime("%B")] + dt_msk.strftime(" %Y года, %H:%M:%S МСК")} | {messages} {["сообщение", "сообщения", "сообщений"][getform(messages)]}\n\n{a_a}{about}{status}',
                                         reply_to_message_id=message.message_id,
                                         message_thread_id=message.message_thread_id, parse_mode='HTML',
                                         reply_markup=keyboard)
                else:
                    msg(message.chat.id, f"Ошибка {main_data.status_code}", message.message_id,
                        message.is_topic_message, message.message_thread_id)
            else:
                msg(message.chat.id, "Эта команда не должна быть пустой", message.message_id, message.is_topic_message,
                    message.message_thread_id)
        elif cmd('clicker', message.text):
            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.add(telebot.types.InlineKeyboardButton(text='Нажми!', callback_data='click'))
            botmsg = bot.send_message(message.chat.id, 'Кликер', message_thread_id=message.message_thread_id,
                                      reply_to_message_id=message.message_id, reply_markup=keyboard)
            if message.is_topic_message:
                uniqueid = f'{str(message.chat.id)}{str(message.message_thread_id)}{str(botmsg.message_id)}'
            else:
                uniqueid = f'{str(message.chat.id)}None{str(botmsg.message_id)}'
            click_db[uniqueid] = 0
        # elif message.text.startswith('/exec'):
        #    if message.text.startswith('/exec ') or message.text.startswith('/exec@rsokolov3Bot '):
        #        if message.from_user.id in trusted:
        ##            if message.from_user.id in [1327137572, 5184185845, 7417081858, 5452789572]:
        #                try:
        #                    comm = message.text.split(' ', 1)[1]
        #                    if 'bot.token' in comm:
        #                        comm = comm.replace('bot.token', 'token')
        #                    if '= bot' in comm:
        #                        comm = comm.replace('= bot', '= Troll()')
        #                    r = str(exec(comm))
        #                    msg(message.chat.id, 'Успешно выполнено', message.message_id, message.is_topic_message, message.message_thread_id)
        #                except Exception as e:
        ##                    msg(message.chat.id, f"Ошибка:\n{e}", message.message_id, message.is_topic_message, message.message_thread_id)
        #            else:
        #                msg(message.chat.id, f"403!!!", message.message_id, message.is_topic_message, message.message_thread_id)
        #        elif message.from_user.id in trusted == False:
        #            msg(message.chat.id, "Использовать её могу только я", message.message_id, message.is_topic_message, message.message_thread_id)
        #    else:
        #        msg(message.chat.id, f"А какой код мне выполнять?", message.message_id, message.is_topic_message, message.message_thread_id)
        # elif cmd('/mypanel', message.text):
        #    if message.from_user.id in verytrusted:
        #        botmsg = bot.send_message(chat_id=message.chat.id, text=f"Панелька", reply_markup=mypanel(cards), message_thread_id=message.message_thread_id)#msg(message.chat.id, "Укажите соперника, ответив на его сообщение", message.message_id, message.is_topic_message, message.message_thread_id)
        #        if message.is_topic_message:
        #            uniqueid = f'{str(message.chat.id)}{str(message.message_thread_id)}{str(botmsg.message_id)}'
        #        else:
        #            uniqueid = f'{str(message.chat.id)}None{str(botmsg.message_id)}'
        #        cards_db[uniqueid]
        #    elif message.from_user.id in trusted:
        #        msg(message.chat.id, f"Упс! Кажется, у тебя недостаточно прав", message.message_id, message.is_topic_message, message.message_thread_id)


@bot.channel_post_handler(func=lambda m: True,
                          content_types=['text', 'photo', 'audio', 'video', 'document', 'sticker', 'animation', 'voice',
                                         'location', 'contact', 'poll'])
@bot.channel_post_handler(func=lambda m: True,
                          content_types=['text', 'photo', 'audio', 'video', 'document', 'sticker', 'animation', 'voice',
                                         'location', 'contact', 'poll'])
def handle_posts(message: telebot.types.Message):
    if message.has_protected_content == None:
        # if message.chat.id == -1002035207889:
        # bot.forward_message(from_chat_id=message.chat.id, chat_id=-1003844000741, message_id=message.message_id)
        # bot.forward_message(from_chat_id=message.chat.id, chat_id=-1003336995454, message_id=message.message_id)
        if message.chat.id == -1001527586013:
            bot.forward_message(from_chat_id=message.chat.id, chat_id=-1002501164190, message_id=message.message_id,
                                protect_content=True)
        elif message.chat.id == -1003844000741:
            bot.forward_message(from_chat_id=message.chat.id, chat_id=-1003336995454, message_id=message.message_id,
                                protect_content=True)


@bot.message_handler(
    content_types=['text', 'photo', 'audio', 'video', 'document', 'sticker', 'animation', 'voice', 'location',
                   'contact', 'poll'])
@bot.message_handler(
    content_types=['text', 'photo', 'audio', 'video', 'document', 'sticker', 'animation', 'voice', 'location',
                   'contact', 'poll'])
def allmsgs(message):
    if message.chat.id > 0:
        bot.forward_message(from_chat_id=message.chat.id, chat_id=-1003767712566, message_id=message.message_id,
                            message_thread_id=28)
    if message.from_user.id == 6954179869:
        time.sleep(random.randint(1, 10))
        bot.set_message_reaction(chat_id=message.chat.id, message_id=message.message_id,
                                 reaction=[telebot.types.ReactionTypeEmoji(random.choice(['❤️', '🥰', '❤️‍🔥']))])
    if message.chat.id == -1003623810305:
        if message.message_thread_id == 5:
            bot.forward_message(from_chat_id=message.chat.id, chat_id=-1003531260500, message_id=message.message_id,
                                message_thread_id=3)
        elif message.message_thread_id == 127:
            bot.forward_message(from_chat_id=message.chat.id, chat_id=-1003531260500, message_id=message.message_id,
                                message_thread_id=5)
        elif message.message_thread_id == 40:
            bot.forward_message(from_chat_id=message.chat.id, chat_id=-1003531260500, message_id=message.message_id,
                                message_thread_id=7)
        else:
            bot.forward_message(from_chat_id=message.chat.id, chat_id=-1003531260500, message_id=message.message_id)
    if message.from_user.id != 777000 and message.chat.id == -1002108064042:
        bot.forward_message(from_chat_id=message.chat.id, chat_id=-1003774229761, message_id=message.message_id)
        bot.forward_message(from_chat_id=message.chat.id, chat_id=-1003889896766, message_id=message.message_id)
    elif message.from_user.id != 777000 and message.chat.id == -1003774229761:
        bot.forward_message(from_chat_id=message.chat.id, chat_id=-1003889896766, message_id=message.message_id)
    elif message.from_user.id != 777000 and message.chat.id == -1003807292893:
        bot.forward_message(from_chat_id=message.chat.id, chat_id=-1002035207889, message_id=message.message_id,
                            protect_content=True)
    elif message.chat.id == -1003272408860 and message.message_thread_id in [1290, 1814, 1822]:
        bot.delete_message(chat_id=-1003272408860, message_id=message.message_id)
        # elif message.from_user.id == 777000 and message.chat.id == -1003807292893:
        #    bot.forward_message(from_chat_id=message.chat.id, chat_id=-1002035207889, message_id=message.message_id, protect_content=True)


@bot.message_handler(content_types=['new_chat_members'])
@bot.message_handler(content_types=['new_chat_members'])
def new_member_handler(message):
    for new_member in message.new_chat_members:
        if new_member.id == 5213140289:
            bot.ban_chat_member(message.chat.id, 5213140289)


@bot.callback_query_handler(func=lambda call: True)
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        print(f"*{call.from_user.first_name} нажимает на кнопку {call.data}*")
        if call.data in ['r', 'p', 's']:
            # print(call)
            # print('===')
            if call.message.is_topic_message:
                uniqueid = f'{str(call.message.chat.id)}{str(call.message.message_thread_id)}{str(call.message.message_id)}'
            else:
                uniqueid = f'{str(call.message.chat.id)}None{str(call.message.message_id)}'
            # print(uniqueid)
            if uniqueid in rps_db:
                # print(call.from_user.id)
                # print(rps_db[uniqueid]['players'][rps_db[uniqueid]['player']]['id'])
                if call.from_user.id == rps_db[uniqueid]['players'][rps_db[uniqueid]['player']]['id']:
                    if rps_db[uniqueid]['step'] == 1:
                        rps_db[uniqueid]['secret'] = call.data
                        rps_db[uniqueid]['player'] = 1 - rps_db[uniqueid]['player']
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              text=f"Камень-ножницы-бумага!\n🎲 Ходит: {rps_db[uniqueid]['players'][rps_db[uniqueid]['player']]['name']}",
                                              reply_markup=rps_create())  # , message_thread_id=call.message.message_thread_id)
                    elif rps_db[uniqueid]['step'] == 2:
                        if rps_db[uniqueid]['player'] == 1:
                            r = f"{rps_db[uniqueid]['secret']}{call.data}"
                        else:
                            r = f"{call.data}{rps_db[uniqueid]['secret']}"
                        chars = {'r': '👊', 'p': '✋', 's': '✌️'}
                        if r in ['pr', 'rs', 'sp']:
                            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                  text=f"Камень-ножницы-бумага!\n🏆 Победитель: {rps_db[uniqueid]['players'][0]['name']}\n{rps_db[uniqueid]['players'][0]['name']}: {chars[r[0]]}\n{rps_db[uniqueid]['players'][1]['name']}: {chars[r[1]]}")
                        elif r in ['rp', 'sr', 'ps']:
                            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                  text=f"Камень-ножницы-бумага!\n🏆 Победитель: {rps_db[uniqueid]['players'][1]['name']}\n{rps_db[uniqueid]['players'][0]['name']}: {chars[r[0]]}\n{rps_db[uniqueid]['players'][1]['name']}: {chars[r[1]]}")
                        elif rps_db[uniqueid]['secret'] == call.data:
                            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                  text=f"Камень-ножницы-бумага!\n🎲 Ничья!\n{rps_db[uniqueid]['players'][0]['name']}: {chars[rps_db[uniqueid]['secret']]}\n{rps_db[uniqueid]['players'][1]['name']}: {chars[call.data]}")
                        else:
                            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                  text=f"Камень-ножницы-бумага!\n❌ Что-то пошло не так\n{rps_db[uniqueid]['players'][0]['name']}: {chars[r[0]]}\n{rps_db[uniqueid]['players'][1]['name']}: {chars[r[1]]}")
                    rps_db[uniqueid]['step'] += 1
                else:
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Сейчас не твой ход!")
            else:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=True,
                                          text="Бот перезапущен, вызовите команду снова")
        elif call.data.startswith('ttt'):
            if call.message.is_topic_message:
                uniqueid = f'{str(call.message.chat.id)}{str(call.message.message_thread_id)}{str(call.message.message_id)}'
            else:
                uniqueid = f'{str(call.message.chat.id)}None{str(call.message.message_id)}'
            # print(uniqueid)
            if uniqueid in ttt_db:
                # print(call.from_user.id)
                # print(rps_db[uniqueid]['players'][rps_db[uniqueid]['player']]['id'])
                if call.from_user.id == ttt_db[uniqueid]['players'][ttt_db[uniqueid]['player']]['id']:
                    # print(ttt_db[uniqueid])
                    ttt_db[uniqueid]['board'][int(call.data[3])] = \
                    ttt_db[uniqueid]['players'][ttt_db[uniqueid]['player']]['sign']

                    res = getwinner(ttt_db[uniqueid]['board'])
                    if res != None:
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              text=f"Крестики-нолики!\n{['❌', '⭕'][res]} Победитель: {ttt_db[uniqueid]['players'][res]['name']}",
                                              reply_markup=tttgen(ttt_db[uniqueid]['board'], False))
                    elif None in ttt_db[uniqueid]['board']:
                        ttt_db[uniqueid]['player'] = 1 - ttt_db[uniqueid]['player']
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              text=f"Крестики-нолики!\n{['❌', '⭕'][ttt_db[uniqueid]['player']]} Ходит: {ttt_db[uniqueid]['players'][ttt_db[uniqueid]['player']]['name']}",
                                              reply_markup=tttgen(ttt_db[uniqueid]['board']))
                    else:
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              text=f"Крестики-нолики!\n👥 Ничья!",
                                              reply_markup=tttgen(ttt_db[uniqueid]['board'], False))
                else:
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Сейчас не твой ход!")
            else:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=True,
                                          text="Бот перезапущен, вызовите команду снова")
        elif call.data == 'err_full':
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Тут занято")
        elif call.data == 'err_end':
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Игра была окончена")
        elif call.data == 'button':
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Привет!")
        elif call.data.startswith('card'):
            if call.message.is_topic_message:
                uniqueid = f'{str(call.message.chat.id)}{str(call.message.message_thread_id)}{str(call.message.message_id)}'
            else:
                uniqueid = f'{str(call.message.chat.id)}None{str(call.message.message_id)}'
            # print(uniqueid)
            if uniqueid in cards_db:
                # print(call.from_user.id)
                # print(rps_db[uniqueid]['players'][rps_db[uniqueid]['player']]['id'])
                if cards_db[uniqueid]['mode'] == 1:
                    if call.from_user.id == cards_db[uniqueid]['player']['id']:
                        # print(ttt_db[uniqueid])
                        if len(cards_db[uniqueid]['chosen']) < 2:
                            cards_db[uniqueid]['chosen'].append(int(call.data[4:6]))
                            try:
                                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                      text=f"Игра с карточками!\n🎲 Играет: {cards_db[uniqueid]['player']['name']}",
                                                      reply_markup=cardsgen(cards_db[uniqueid]['cards'],
                                                                            cards_db[uniqueid]['chosen'],
                                                                            cards_db[uniqueid]['opened']))
                            except Exception:
                                time.sleep(10)
                                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                      text=f"Игра с карточками!\n🎲 Играет: {cards_db[uniqueid]['player']['name']}",
                                                      reply_markup=cardsgen(cards_db[uniqueid]['cards'],
                                                                            cards_db[uniqueid]['chosen'],
                                                                            cards_db[uniqueid]['opened']))
                            if len(cards_db[uniqueid]['chosen']) == 2:
                                cards_db[uniqueid]['tries'] += 1
                                if cards_db[uniqueid]['cards'][int(cards_db[uniqueid]['chosen'][0])] == \
                                        cards_db[uniqueid]['cards'][int(cards_db[uniqueid]['chosen'][1])]:
                                    cards_db[uniqueid]['opened'] += cards_db[uniqueid]['chosen']
                                    cards_db[uniqueid]['chosen'] = []
                                    if len(cards_db[uniqueid]['opened']) == len(cards_db[uniqueid]['cards']):
                                        try:
                                            bot.edit_message_text(chat_id=call.message.chat.id,
                                                                  message_id=call.message.message_id,
                                                                  text=f"Игра с карточками!\n🎲 Играл: {cards_db[uniqueid]['player']['name']}\n{['Была', 'Было', 'Было'][getform(cards_db[uniqueid]['tries'])]} {['потрачена', 'потрачено', 'потрачено'][getform(cards_db[uniqueid]['tries'])]} {str(cards_db[uniqueid]['tries'])} {['попытка', 'попытки', 'попыток'][getform(cards_db[uniqueid]['tries'])]}",
                                                                  reply_markup=cardsgen(cards_db[uniqueid]['cards'],
                                                                                        cards_db[uniqueid]['chosen'],
                                                                                        cards_db[uniqueid]['opened']))
                                        except Exception:
                                            time.sleep(10)
                                            bot.edit_message_text(chat_id=call.message.chat.id,
                                                                  message_id=call.message.message_id,
                                                                  text=f"Игра с карточками!\n🎲 Играл: {cards_db[uniqueid]['player']['name']}\n{['Была', 'Было', 'Было'][getform(cards_db[uniqueid]['tries'])]} {['потрачена', 'потрачено', 'потрачено'][getform(cards_db[uniqueid]['tries'])]} {str(cards_db[uniqueid]['tries'])} {['попытка', 'попытки', 'попыток'][getform(cards_db[uniqueid]['tries'])]}",
                                                                  reply_markup=cardsgen(cards_db[uniqueid]['cards'],
                                                                                        cards_db[uniqueid]['chosen'],
                                                                                        cards_db[uniqueid]['opened']))
                                else:
                                    time.sleep(2.5)
                                    cards_db[uniqueid]['chosen'] = []
                                    try:
                                        bot.edit_message_text(chat_id=call.message.chat.id,
                                                              message_id=call.message.message_id,
                                                              text=f"Игра с карточками!\n🎲 Играет: {cards_db[uniqueid]['player']['name']}",
                                                              reply_markup=cardsgen(cards_db[uniqueid]['cards'],
                                                                                    cards_db[uniqueid]['chosen'],
                                                                                    cards_db[uniqueid]['opened']))
                                    except Exception:
                                        time.sleep(10)
                                        bot.edit_message_text(chat_id=call.message.chat.id,
                                                              message_id=call.message.message_id,
                                                              text=f"Игра с карточками!\n🎲 Играет: {cards_db[uniqueid]['player']['name']}",
                                                              reply_markup=cardsgen(cards_db[uniqueid]['cards'],
                                                                                    cards_db[uniqueid]['chosen'],
                                                                                    cards_db[uniqueid]['opened']))
                        else:
                            if int(call.data[4:6]) in cards_db[uniqueid]['chosen']:
                                bot.answer_callback_query(callback_query_id=call.id, show_alert=True,
                                                          text="Ты слишком быстро нажимаешь на кнопки!")
                            else:
                                bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                                          text="Ты не можешь выбрать больше двух карт")
                        '''
                        ttt_db[uniqueid]['board'][int(call.data[3])] = ttt_db[uniqueid]['players'][ttt_db[uniqueid]['player']]['sign']

                        res = getwinner(ttt_db[uniqueid]['board'])
                        if res != None:
                            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Крестики-нолики!\n{['❌', '⭕'][res]} Победитель: {ttt_db[uniqueid]['players'][res]['name']}", reply_markup=tttgen(ttt_db[uniqueid]['board'], False))
                        elif None in ttt_db[uniqueid]['board']:
                            ttt_db[uniqueid]['player'] = 1 - ttt_db[uniqueid]['player']
                            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Крестики-нолики!\n{['❌', '⭕'][ttt_db[uniqueid]['player']]} Ходит: {ttt_db[uniqueid]['players'][ttt_db[uniqueid]['player']]['name']}", reply_markup=tttgen(ttt_db[uniqueid]['board']))
                        else:
                            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Крестики-нолики!\n👥 Ничья!", reply_markup=tttgen(ttt_db[uniqueid]['board'], False))
                        '''
                    else:
                        bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                                  text="Сейчас не твой ход!")
                else:
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                              text="Как ты играешь в несуществующий режим?")
            else:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=True,
                                          text="Бот перезапущен, вызовите команду снова")
        elif call.data == 'fixcards':
            if call.message.is_topic_message:
                uniqueid = f'{str(call.message.chat.id)}{str(call.message.message_thread_id)}{str(call.message.message_id)}'
            else:
                uniqueid = f'{str(call.message.chat.id)}None{str(call.message.message_id)}'
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f"Игра с карточками!\n🎲 Играет: {cards_db[uniqueid]['player']['name']}",
                                  reply_markup=cardsgen(cards_db[uniqueid]['cards'], cards_db[uniqueid]['chosen'],
                                                        cards_db[uniqueid]['opened']))
        elif call.data == 'unbanqwerty':
            if call.from_user.id == 6954179869:
                bot.unban_chat_member(chat_id=-1002004771264, user_id=6954179869)
                bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Готово!")
            else:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Ты не кверти")
        elif call.data == 'doxx':
            bot.answer_callback_query(callback_query_id=call.id, show_alert=True,
                                      text=f"Поздравляю, {call.from_user.first_name}! Вас докснули")
        elif call.data.startswith('p '):
            bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text=call.data.split(' ', 1)[1])
        elif call.data.startswith('a '):
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=call.data.split(' ', 1)[1])
        elif call.data == 'nothing lol':
            bot.answer_callback_query(callback_query_id=call.id)
        elif call.data == 'click':
            if call.message.is_topic_message:
                uniqueid = f'{str(call.message.chat.id)}{str(call.message.message_thread_id)}{str(call.message.message_id)}'
            else:
                uniqueid = f'{str(call.message.chat.id)}None{str(call.message.message_id)}'
            try:
                click_db[uniqueid] += 1
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=str(click_db[uniqueid]))
            except Exception:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text='Ошибочка')


token = TOKENS['telegram_bot_token']
if __name__ == '__main__':
    bot.infinity_polling()

'''
if call.data == "button1":
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Кнопки удалились")
elif call.data == "button2":
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Кнопки должны остаться", reply_markup=rps_create(), message_thread_id=call.message.message_thread_id)
elif call.data == "button3":
    bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Привет!")
elif call.data == "button4":
    bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Привет!")
'''
