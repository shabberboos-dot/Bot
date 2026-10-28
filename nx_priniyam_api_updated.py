#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
============================================================
   NX XHAWON BOT — COMPLETE SYSTEM v25 (AUTO REACTION ALL POSTS)
============================================================
"""

import telebot
import requests
import time
import threading
import sqlite3
import random
from datetime import datetime, timedelta
import pytz
import logging
import sys
import os
import traceback
import io
import concurrent.futures

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def error_handler(exctype, value, tb):
    print(f"❌ Error: {exctype} - {value}")
    traceback.print_tb(tb)

sys.excepthook = error_handler

TOKEN = "8542213652:AAGEWnraqxaqHSThjy2cwW1jnkGj-q22Bps"
BOT_USERNAME = "nx_TDR_xhawon_bot"
OWNER_LINK = "https://t.me/BDT_NX_Owner?text=ভাই%2C%20আমি%20আপনার%20বট%20সিগন্যাল%20নিতে%20চাই।"
PREMIUM_LINK = "https://t.me/BDT_NX_Owner?text=ভাই%20আমি%20আপনার%20প্রিনিয়ামে%20তে%20এড%20হতে%20চাই"
OWNER_ID = 7853834431

GROUP_LINK = "https://t.me/+n4Q7PRRvxZAyMjhl"
PUBLIC_CHANNEL_ID = "-1002367017451"
PREMIUM_PROMO_CHANNEL = "-1002367017451"
JOIN_REQUEST_CHANNEL_ID = -1002367017451

MORNING_PHOTO_URL = "https://i.ibb.co/sp31tLz9/IMG-20260918-082401-105.jpg" 
NIGHT_PHOTO_URL = "https://i.ibb.co/RTvGDxmD/IMG-20260918-082419-744.jpg"
START_PHOTO_URL = "https://i.ibb.co.com/r2wzZ7W8/file-000000008abc8208bb111987a1f20ba6.png"

REFER_REWARD = 4
VERIFY_BONUS = 10
MIN_WITHDRAW = 1000
MIN_RECHARGE = 20
PAID_SIGNAL_PER_WIN = 3
NUMBER_SHOT_PER_WIN = 5
NAGAD_NUMBER = "01956355328"
BIKASH_NUMBER = "01703476087"
PRINIYAM_JOIN_LINK = "https://t.me/BDT_NX_Owner?text=ভাই%20আমি%20প্রিনিয়ামে%20জয়েন%20হতে%20চাই"
PRINIYAM_CHANNEL_LINK = "https://t.me/NX_ALL_FACALITY/120"

# History API is used ONLY to verify actual outcomes.
API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_30S/GetHistoryIssuePage.json"

# Prediction API discovered in the supplied Remix AI Hack project source.
PREDICTION_API_URL = "https://remix-ai-hack-2-8-9298.ai.studio/pro1-main.json"
PREDICTION_API_KEY = os.getenv("MILI_PREDICTION_API_KEY", "mili_bot_live_token_77a902df3b4c18e")

def get_prediction_from_api(market="30s"):
    """Return only API-generated predictions; never use local fallback logic."""
    try:
        response = requests.get(
            PREDICTION_API_URL,
            params={"api_key": PREDICTION_API_KEY, "market": market, "fresh": "true"},
            headers={"Accept": "application/json"},
            timeout=20,
        )
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, dict) or payload.get("status") != "success":
            logging.warning("Prediction API unsuccessful: %s", payload.get("message", payload) if isinstance(payload, dict) else "invalid JSON")
            return None

        value = payload.get("main_prediction") or payload.get("outcome") or payload.get("winner")
        signal = str(value or "").strip().upper()
        if signal not in ("BIG", "SMALL"):
            logging.warning("Prediction API response missing a valid BIG/SMALL signal.")
            return None

        digits = []
        for item in payload.get("digits", []) if isinstance(payload.get("digits"), list) else []:
            try:
                digit = int(item)
                if 0 <= digit <= 9 and digit not in digits:
                    digits.append(digit)
            except (TypeError, ValueError):
                continue

        target_period = str(payload.get("target_period") or "").strip()
        if not target_period:
            logging.warning("Prediction API response has no target_period.")
            return None

        return {
            "signal": signal,
            "digits": digits[:2],
            "target_period": target_period,
            "final_prediction": str(payload.get("final_prediction") or ""),
            "confidence": str(payload.get("win_probability") or ""),
        }
    except requests.RequestException as exc:
        logging.warning("Prediction API network/HTTP error: %s", exc)
    except ValueError as exc:
        logging.warning("Prediction API returned invalid JSON: %s", exc)
    except Exception:
        logging.exception("Unexpected Prediction API error")
    return None

BD_TZ = pytz.timezone('Asia/Dhaka')
def get_bd_time():
    return datetime.now(BD_TZ)

BOTS_CONFIG = [
    {"token": "8937192597:AAELlosLpqb3I5ZTN6s2K6Zhap3PJO4uzB8", "reaction": "❤️"},
    {"token": "8876788174:AAHujDB1TVnk9_ThpIAn8pHsYLDehUqsNKQ", "reaction": "❤️"},
    {"token": "8920310994:AAEqQuCQdLmbo6SeyOP6Iu4dlTLxbiUZSkQ", "reaction": "❤️"},
    {"token": "8622774554:AAFfv08W1CbXYeP0rC_WJ8VHZ658nJWXM-0", "reaction": "❤️"},
    {"token": "8842921487:AAGrlWes02_oksMEygaHniAcMAxo3JTerp0", "reaction": "❤️"},
    {"token": "8627561004:AAHHWelSln1AcssTgzky72E-y8pVh0Vwyhg", "reaction": "❤️"},
    {"token": "8904864130:AAHI_yzU_0hgofuR5jNxE0YAC1_EUlws8Kc", "reaction": "❤️"},
    {"token": "7901207649:AAE04lTTO5IY7ffflMcl5sVm2lJ4UC4ABTY", "reaction": "❤️"},
    {"token": "8892291822:AAGsfKecZQxxWd9rg608Xzp1RoqiD_iwVRI", "reaction": "❤️"},
    {"token": "8752386254:AAHDeTAMbcxv-WNKspggUmDvRprkWCzniYk", "reaction": "❤️"},
    {"token": "8336933019:AAH1wH8b70-gGxXVW7xnsBry9j3O4JBCNWA", "reaction": "❤️"},
    {"token": "8701420121:AAEI4iJ3jv6luqXA-gDiseohOGz8-f28EVI", "reaction": "🔥"},
    {"token": "8754157010:AAHWYmAAWPx52TprIngrgzet5eVKHdvnkIY", "reaction": "🔥"},
    {"token": "8708746014:AAFWpEwwM2nyQHud1QSBgb24b8Em5NGKkxE", "reaction": "🔥"},
    {"token": "8712000048:AAHOoHBLL-rdVmlwjE1maDrA6QjpCIx1YR0", "reaction": "🔥"},
    {"token": "8890365411:AAH4SjzWxAxPX_7IhF-V-9V2RXxPM0yH7OQ", "reaction": "🔥"},
    {"token": "8910857583:AAFlYtG0GVoQFnFl1BS4bvTJILcrG8tu_HA", "reaction": "💯"},
    {"token": "8963054575:AAH2odIb1SPBVpV_JzeFWff74-YuQJDtSfM", "reaction": "💯"},
    {"token": "8331787567:AAEttDUqjJxdfQC-blq5OA3HDNtNKw9ansE", "reaction": "⚡"},
    {"token": "8259799484:AAGpwD2c284TnSPis9icOtC50Cbt_REOatw", "reaction": "⚡"},
]

reaction_bots = []

daily_flags = {
    "morning_sent": False,
    "promo_reminder_1230": False,
    "promo_reminder_17": False,
    "promo_reminder_20": False,
    "report_2130_sent": False,
    "night_sent": False,
    "user_list_sent": False,
}

CHANNELS = [
    {
        "name": "MORNING VIP SIGNAL",
        "id": "-1002691716665",
        "link": "https://t.me/+73AHPqLvlII0MWE9",
        "start_hour": 12, "start_min": 6,
        "end_hour": 13, "end_min": 10,
        "target_wins": 15,
        "logic": "normal_recovery",
        "unlimited": False,
        "wins": 0, "losses": 0,
        "completed": False,
        "last_period": "0",
        "pending_sig": None, "pending_period": None,
        "is_recovery": False,
        "loss_count": 0, "current_step": 0,
        "max_loss_streak": 0,
        "notified": False,
        "history": [],
        "wins_70_reported": False,
    },
    {
        "name": "DUPUR PUBLIC SIGNAL",
        "id": "-1002367017451",
        "link": "https://t.me/+XFpXmlGPjMI5N2U1",
        "start_hour": 15, "start_min": 6,
        "end_hour": 16, "end_min": 0,
        "target_wins": 10,
        "logic": "normal_recovery",
        "unlimited": False,
        "wins": 0, "losses": 0,
        "completed": False,
        "last_period": "0",
        "pending_sig": None, "pending_period": None,
        "is_recovery": False,
        "loss_count": 0, "current_step": 0,
        "max_loss_streak": 0,
        "notified": False,
        "history": [],
        "wins_70_reported": False,
    },
    {
        "name": "BIKAL BOT SIGNAL",
        "id": "-1004494117146",
        "link": "https://t.me/+n4Q7PRRvxZAyMjhl",
        "start_hour": 18, "start_min": 6,
        "end_hour": 19, "end_min": 30,
        "target_wins": 25,
        "logic": "normal_recovery",
        "unlimited": False,
        "wins": 0, "losses": 0,
        "completed": False,
        "last_period": "0",
        "pending_sig": None, "pending_period": None,
        "is_recovery": False,
        "loss_count": 0, "current_step": 0,
        "max_loss_streak": 0,
        "notified": False,
        "history": [],
        "wins_70_reported": False,
    },
    {
        "name": "NX RECOVERY SIGNAL",
        "id": "-1003695274493",
        "link": "https://t.me/+OIBI2EVdXNtkNDE1",
        "start_hour": 0, "start_min": 0,
        "end_hour": 23, "end_min": 59,
        "target_wins": 0,
        "logic": "recovery_only",
        "unlimited": True,
        "wins": 0, "losses": 0,
        "completed": False,
        "last_period": "0",
        "pending_sig": None, "pending_period": None,
        "is_recovery": True,
        "loss_count": 0, "current_step": 0,
        "max_loss_streak": 0,
        "notified": False,
        "history": [],
        "wins_70_reported": False,
        "report_counter": 0,
        "report_start_time": None,
        "report_start_wins": 0,
        "report_losses": 0,
    },
    {
        "name": "NX DUAL MODE SIGNAL",
        "id": "-1003826327611",
        "link": "https://t.me/+-cm5JcgwuPUxMzhl",
        "start_hour": 0, "start_min": 0,
        "end_hour": 23, "end_min": 59,
        "target_wins": 0,
        "logic": "normal_recovery",
        "unlimited": True,
        "wins": 0, "losses": 0,
        "completed": False,
        "last_period": "0",
        "pending_sig": None, "pending_period": None,
        "is_recovery": False,
        "loss_count": 0, "current_step": 0,
        "max_loss_streak": 0,
        "notified": False,
        "history": [],
        "wins_70_reported": False,
        "report_counter": 0,
        "report_start_time": None,
        "report_start_wins": 0,
        "report_losses": 0,
    },
]

CHANNEL_LINKS = [
    "https://t.me/+XFpXmlGPjMI5N2U1",
    "https://t.me/NX_TEAM_07",
    "https://t.me/NX_FREE_EARNING",
    "https://t.me/NX_ALL_FACALITY"
]
CHANNEL_IDS = [
    "-1002367017451",
    "@NX_TEAM_07",
    "@NX_FREE_EARNING",
    "@NX_ALL_FACALITY"
]

conn = sqlite3.connect("bot_data.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    is_verified INTEGER DEFAULT 0,
    refer_count INTEGER DEFAULT 0,
    referred_by INTEGER DEFAULT NULL,
    total_referrals INTEGER DEFAULT 0,
    join_date TEXT DEFAULT NULL,
    first_name TEXT DEFAULT NULL,
    balance REAL DEFAULT 0,
    refer_reward_given INTEGER DEFAULT 0
)
""")
conn.commit()

try:
    cursor.execute("ALTER TABLE users ADD COLUMN balance REAL DEFAULT 0")
    conn.commit()
except: pass

try:
    cursor.execute("ALTER TABLE users ADD COLUMN refer_reward_given INTEGER DEFAULT 0")
    conn.commit()
except: pass

print("✅ Database connected")

bot = telebot.TeleBot(TOKEN)
print("✅ Bot initialized")

def load_child_bot(bot_config):
    try:
        b = telebot.TeleBot(bot_config["token"])
        me = b.get_me()
        return {"bot": b, "token": bot_config["token"], "reaction": bot_config["reaction"],
                "username": me.username, "id": me.id, "active": True}
    except Exception as e:
        return {"bot": None, "token": bot_config["token"], "reaction": bot_config["reaction"],
                "username": "Failed", "id": "N/A", "active": False, "error": str(e)[:50]}

print("=" * 60)
print("⚡ Loading Reaction Bots (20)...")
for i, cfg in enumerate(BOTS_CONFIG):
    cb = load_child_bot(cfg)
    if cb["active"]:
        reaction_bots.append(cb)
        print(f"  ✅ Bot {len(reaction_bots)}: @{cb['username']} [{cb['reaction']}]")
    else:
        print(f"  ❌ Bot {i+1}: {cb.get('error', 'Failed')}")

print("=" * 60)
print(f"⚡ Active Reaction Bots: {len(reaction_bots)}")
print("=" * 60)

def add_reactions_to_channel(message_id, retry=False):
    """২০টি Bot একসাথে Reaction — Stagger + Retry সহ"""
    react_success = 0
    failed = 0
    failed_list = []
    failed_bots = []
    total = len(reaction_bots)
    
    print(f"\n🚀 AUTO REACTION STARTED — Message ID: {message_id}" + (" [RETRY]" if retry else ""))
    print("=" * 60)
    
    def send_one_reaction(cb, index):
        time.sleep(index * 0.2)
        try:
            react_url = f"https://api.telegram.org/bot{cb['token']}/setMessageReaction"
            payload = {
                "chat_id": PUBLIC_CHANNEL_ID,
                "message_id": message_id,
                "reaction": [{"type": "emoji", "emoji": cb["reaction"]}]
            }
            resp = requests.post(react_url, json=payload, timeout=10)
            rdata = resp.json()
            if rdata.get("ok"):
                return ("success", cb, None)
            else:
                return ("failed", cb, rdata.get("description", "Unknown")[:60])
        except Exception as e:
            return ("failed", cb, str(e)[:60])
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(send_one_reaction, cb, i) for i, cb in enumerate(reaction_bots)]
        results = [f.result() for f in futures]
    
    for status, cb, err in results:
        if status == "success":
            react_success += 1
            print(f"  {cb['reaction']} React {react_success}/{total} @{cb['username']}")
        else:
            failed += 1
            failed_bots.append(cb)
            failed_list.append(f"@{cb['username']}: {err}")
            print(f"  ❌ @{cb['username']}: {err}")
    
    print("=" * 60)
    print(f"✅ Reactions: {react_success}/{total} | Failed: {failed}")
    print("=" * 60)
    
    if failed > 0 and not retry:
        print(f"🔄 Retrying {failed} failed bots in 15 seconds...")
        time.sleep(15)
        
        def retry_one(cb, index):
            time.sleep(index * 0.3)
            try:
                react_url = f"https://api.telegram.org/bot{cb['token']}/setMessageReaction"
                payload = {
                    "chat_id": PUBLIC_CHANNEL_ID,
                    "message_id": message_id,
                    "reaction": [{"type": "emoji", "emoji": cb["reaction"]}]
                }
                resp = requests.post(react_url, json=payload, timeout=10)
                return resp.json().get("ok", False)
            except:
                return False
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(failed_bots)) as executor:
            futures = [executor.submit(retry_one, cb, i) for i, cb in enumerate(failed_bots)]
            retry_results = [f.result() for f in futures]
        
        retry_success = sum(1 for r in retry_results if r)
        react_success += retry_success
        print(f"✅ Retry Success: {retry_success}/{len(failed_bots)}")
    
    return react_success, failed, failed_list


def auto_boost_worker(message_id):
    """Reaction Worker (Background) — Lock ছাড়া"""
    try:
        r_s, f, f_list = add_reactions_to_channel(message_id)
        
        try:
            report = f"""
🤖 <b>AUTO REACTION REPORT</b>
━━━━━━━━━━━━━━━━━━━━━
📢 <b>Channel:</b> NX TDR
📝 <b>Message ID:</b> <code>{message_id}</code>
━━━━━━━━━━━━━━━━━━━━━
🎯 <b>Reactions:</b> {r_s}/{len(reaction_bots)}
❌ <b>Failed:</b> {f}
━━━━━━━━━━━━━━━━━━━━━
⏰ {get_bd_time().strftime('%H:%M:%S')}
"""
            if f_list:
                report += "\n❌ <b>Failed Bots:</b>\n"
                for x in f_list[:5]:
                    report += f"• {x}\n"
            
            bot.send_message(OWNER_ID, report, parse_mode='HTML')
        except: pass
    except Exception as e:
        print(f"❌ Worker error: {e}")


# ============================================
# 📨 CHANNEL POST HANDLER — সব ধরনের Post
# ============================================
@bot.channel_post_handler(func=lambda msg: True)
def handle_channel_post(message):
    """Channel এ যেকোনো Post এ Auto Reaction (Text/Photo/Video/Sticker/Forward/Poll সব)"""
    try:
        chat_id = message.chat.id
        msg_id = message.message_id
        
        content_type = "Unknown"
        if message.text: content_type = "Text"
        elif message.photo: content_type = "Photo"
        elif message.video: content_type = "Video"
        elif message.document: content_type = "Document"
        elif message.audio: content_type = "Audio"
        elif message.voice: content_type = "Voice"
        elif message.sticker: content_type = "Sticker"
        elif message.animation: content_type = "GIF/Animation"
        elif message.video_note: content_type = "Video Note"
        elif message.poll: content_type = "Poll"
        elif message.contact: content_type = "Contact"
        elif message.location: content_type = "Location"
        elif message.venue: content_type = "Venue"
        elif message.dice: content_type = "Dice"
        elif message.game: content_type = "Game"
        elif message.forward_from or message.forward_from_chat: content_type = "Forwarded"
        elif message.caption: content_type = "Caption Media"
        
        print(f"\n{'='*60}")
        print(f"📨 CHANNEL POST DETECTED!")
        print(f"   Chat ID:  {chat_id}")
        print(f"   Msg ID:   {msg_id}")
        print(f"   Type:     {content_type}")
        print(f"{'='*60}")
        
        if int(chat_id) != int(PUBLIC_CHANNEL_ID):
            print(f"   ⏭️ SKIPPED — Not target channel!")
            return
        
        print(f"   ✅ Adding Reactions...")
        threading.Thread(target=auto_boost_worker, args=(msg_id,), daemon=True).start()
        
    except Exception as e:
        print(f"❌ Channel post handler error: {e}")
        traceback.print_exc()


# ============================================
# ✏️ EDITED CHANNEL POST HANDLER
# ============================================
@bot.edited_channel_post_handler(func=lambda msg: True)
def handle_edited_channel_post(message):
    """Channel Post Edit হলেও Reaction দিবে"""
    try:
        chat_id = message.chat.id
        msg_id = message.message_id
        
        print(f"\n✏️ CHANNEL POST EDITED!")
        print(f"   Chat ID: {chat_id}")
        print(f"   Msg ID:  {msg_id}")
        
        if int(chat_id) != int(PUBLIC_CHANNEL_ID):
            return
        
        print(f"   ✅ Adding Reactions (Edit)...")
        threading.Thread(target=auto_boost_worker, args=(msg_id,), daemon=True).start()
        
    except Exception as e:
        print(f"❌ Edited channel post error: {e}")


def is_member(user_id, channel):
    try:
        member = bot.get_chat_member(channel, user_id)
        return member.status in ["member", "administrator", "creator"]
    except: return False

def check_all_channels(user_id):
    not_joined = []
    for ch in CHANNEL_IDS:
        if not is_member(user_id, ch):
            not_joined.append(ch)
    return len(not_joined) == 0, not_joined

def get_verify_keyboard():
    k = telebot.types.InlineKeyboardMarkup(row_width=2)
    k.add(
        telebot.types.InlineKeyboardButton("🔴 চ্যানেল ১", url=CHANNEL_LINKS[0]),
        telebot.types.InlineKeyboardButton("🔴 চ্যানেল ২", url=CHANNEL_LINKS[1])
    )
    k.add(
        telebot.types.InlineKeyboardButton("🔴 চ্যানেল ৩", url=CHANNEL_LINKS[2]),
        telebot.types.InlineKeyboardButton("🔴 চ্যানেল ৪", url=CHANNEL_LINKS[3])
    )
    k.add(telebot.types.InlineKeyboardButton("✅ ভেরিফাই করুন", callback_data="verify"))
    return k

def get_owner_id_button():
    k = telebot.types.InlineKeyboardMarkup(row_width=1)
    k.add(telebot.types.InlineKeyboardButton("📞 𝗢𝗪𝗡𝗘𝗥 𝗜𝗗", url=PREMIUM_LINK))
    return k

def get_premium_owner_button():
    k = telebot.types.InlineKeyboardMarkup(row_width=1)
    k.add(telebot.types.InlineKeyboardButton("📞 𝗢𝗪𝗡𝗘𝗥 𝗜𝗗 — 𝗣𝗥𝗜𝗡𝗜𝗬𝗔𝗠 𝗝𝗢𝗜𝗡", url=PREMIUM_LINK))
    return k

def get_bottom_menu():
    k = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    k.add(telebot.types.KeyboardButton("👤 MY ACCOUNT"), telebot.types.KeyboardButton("💰 DEPOSIT"))
    k.add(telebot.types.KeyboardButton("😎JOIN NX PRINIYAM"), telebot.types.KeyboardButton("💎 PAID SIGNAL"))
    k.add(telebot.types.KeyboardButton("💵 NUMBER SHOT"), telebot.types.KeyboardButton("🟢 JOIN NX COMMUNITY"))
    k.add(telebot.types.KeyboardButton("📞 HELP AND SUPPORT"), telebot.types.KeyboardButton("𝗥𝗘𝗙𝗙𝗘𝗥 𝗔𝗡𝗗 𝗘𝗔𝗥𝗡"))
    return k

def get_welcome_dm(first_name):
    return f"""
💚✨ <b>𝗛𝗘𝗬 {first_name} মামা!</b> 🩷✨
💠 আমি <b>𝗡𝗫 𝗕𝗢𝗧</b> — আসসালামু আলাইকুম! 💠

🥰 <b>NX Family</b>-তে স্বাগতম জানাচ্ছি! 🎉

✅ আপনার <b>Join Request Accepted</b> হয়েছে!

━━━━━━━━━━━━━━━━━━━━━
📢 <b>আপনি এখন NX TDR COMMUNITY-এর সদস্য</b>
━━━━━━━━━━━━━━━━━━━━━

🟢 <b>09:00 AM</b> — Morning NX Bot Signal
🔵 <b>03:00 PM</b> — NX PUBLIC BOT SIGNAL
🔴 <b>06:00 PM</b> — Evening NX Bot Signal
🟣 <b>09:00 PM</b> — NX PREMIUM TRAILER + 🎁 Giveaway

📚 Learn • Practice • Grow 🚀
🔥 <b>NO HACK</b> ❌ | <b>ONLY REAL KNOWLEDGE</b> ✅

👇 <b>নিচের বাটনে ক্লিক করুন</b> 👇

👑 <b>WELCOME TO NX FAMILY</b> 💛
✨ <b>STAY WITH NX XHAWON</b> 📊💎
"""

def get_welcome_keyboard():
    k = telebot.types.InlineKeyboardMarkup(row_width=1)
    k.add(telebot.types.InlineKeyboardButton("🟢 𝗝𝗢𝗜𝗡 𝗡𝗫 𝗧𝗗𝗥 𝗖𝗢𝗠𝗠𝗨𝗡𝗜𝗧𝗬", url="https://t.me/+XFpXmlGPjMI5N2U1"))
    k.add(telebot.types.InlineKeyboardButton("🚀 𝗝𝗢𝗜𝗡 𝗢𝗪𝗡𝗘𝗥 (Premium)", url=PREMIUM_LINK))
    return k

def send_followup_message(user_id, first_name):
    try:
        try:
            member = bot.get_chat_member(PUBLIC_CHANNEL_ID, user_id)
            if member.status in ["member", "administrator", "creator"]: return
        except: pass
        promo_msg = """
📊🟢 <b>𝗕𝗔𝗡𝗚𝗟𝗔𝗗𝗘𝗦𝗛 𝗧𝗢𝗣 𝗣𝗥𝗢𝗝𝗘𝗖𝗧</b> 🟢📊

🔮 <b>𝗔𝗨𝗧𝗢 𝗧𝗥𝗔𝗗𝗘𝗫</b> 🤖 এটা আপনার <b>DKWIN/HGNICE ACCOUNT</b> এ নিজে নিজে ট্রেড করবে ✅

💎⭐ <b>𝗔𝗨𝗧𝗢 𝗧𝗥𝗔𝗗𝗘𝗫</b> নিতে জয়েন করুন ⭐💎
"""
        k = telebot.types.InlineKeyboardMarkup(row_width=1)
        k.add(telebot.types.InlineKeyboardButton("🟢 𝗝𝗢𝗜𝗡 𝗡𝗫 𝗧𝗗𝗥 𝗖𝗢𝗠𝗠𝗨𝗡𝗜𝗧𝗬", url="https://t.me/+XFpXmlGPjMI5N2U1"))
        k.add(telebot.types.InlineKeyboardButton("🚀 𝗔𝗨𝗧𝗢 𝗧𝗥𝗔𝗗𝗘𝗫 (Premium)", url=PREMIUM_LINK))
        bot.send_message(user_id, promo_msg, parse_mode='HTML', reply_markup=k)
    except Exception as e:
        print(f"❌ Follow-up error to {user_id}: {e}")

@bot.message_handler(commands=['start'])
def start_command(message):
    try:
        user_id = message.from_user.id
        first_name = message.from_user.first_name or "N/A"
        last_name = message.from_user.last_name or ""
        username = message.from_user.username

        cursor.execute("INSERT OR IGNORE INTO users (user_id, first_name, join_date) VALUES (?, ?, ?)",
                       (user_id, first_name, get_bd_time().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()

        try:
            full_name = f"{first_name} {last_name}".strip()
            username_display = f"@{username}" if username else "No Username"
            notify_msg = f"""
🆕 <b>NEW USER STARTED BOT</b>

👤 <b>Name:</b> {full_name}
🔗 <b>Username:</b> {username_display}
🆔 <b>User ID:</b> <code>{user_id}</code>
📅 <b>Time:</b> {get_bd_time().strftime('%d-%m-%Y %H:%M:%S')}
"""
            bot.send_message(OWNER_ID, notify_msg, parse_mode='HTML')
        except: pass

        if message.text and "ref_" in message.text:
            try:
                referrer_id = int(message.text.split("ref_")[1])
                if referrer_id != user_id:
                    cursor.execute("SELECT referred_by FROM users WHERE user_id = ?", (user_id,))
                    ex = cursor.fetchone()
                    if not ex or ex[0] is None:
                        cursor.execute("UPDATE users SET referred_by = ? WHERE user_id = ?", (referrer_id, user_id))
                        conn.commit()
            except Exception as e:
                print(f"❌ Ref save error: {e}")

        welcome_caption = f"""🔥 <b>𝗡𝗫 𝗧𝗗𝗥 𝗖𝗢𝗠𝗠𝗨𝗡𝗜𝗧𝗬</b>-তে আপনাকে স্বাগতম! 💙

🔮আমি <b>𝗡𝗫 •𝗡𝗘𝗫𝗢𝗥𝗔 𝗚𝗣𝗧• 𝗕𝗢𝗧</b> 🔵
একটি COLOUR TRADING SIGNAL প্রফেশনাল কমিউনিটি <b>𝗡𝗫 𝗧𝗗𝗥 𝗖𝗢𝗠𝗠𝗜𝗡𝗜𝗧𝗬</b> ❤️

এই <b>𝗡𝗫</b> কমিউনিটিতে যোগ দিন এবং স্মার্টভাবে ট্রেড করতে যা দরকার সব পাবেন 👇

✅ 🎯 <b>𝗔𝗨𝗧𝗢 𝗧𝗥𝗔𝗗𝗘𝗫</b> 🔥😎
✅ 💡 <b>𝗔𝗨𝗧𝗢 𝗦𝗜𝗚𝗡𝗔𝗟 𝗕𝗢𝗧</b> 🤖
✅ 📊 <b>𝗣𝗔𝗜𝗗 𝗦𝗜𝗚𝗡𝗔𝗟</b> 💰💣
✅ 🧠 <b>𝗙𝗥𝗘𝗘 𝗣𝗨𝗕𝗟𝗜𝗖𝗞 𝗟𝗜𝗩𝗘 𝗦𝗜𝗚𝗡𝗔𝗟</b> 📈
✅ 🔔 <b>𝗣𝗨𝗥𝗘 𝗡𝗨𝗠𝗕𝗘𝗥 𝗣𝗔𝗡𝗘𝗟</b>😎
✅ 📚 <b>𝗡𝗫 𝗙𝗨𝗟𝗟 𝗥𝗘𝗔𝗟 𝗞𝗡𝗢𝗪𝗟𝗘𝗗𝗚𝗘</b>🏅
✅ 🤖 <b>𝗡𝗫 𝗡𝗘𝗫𝗢𝗥𝗔 𝗚𝗢𝗧 𝗕𝗢𝗧</b> 😭

🟢 এখন এই বট থেকে <b>𝟭𝟬𝟬% 𝗣𝗥𝗢𝗙𝗜𝗧</b> সিগন্যাল নিতে এখনই ভেরিফিকেশন করুন এবং <b>২ টি রেফার</b> করুন তাহলে পেয়ে যাবেন সিগন্যাল 📊✅
👇<b>𝗩𝗘𝗥𝗬𝗙𝗜𝗖𝗔𝗧𝗜𝗢𝗡 𝗙𝗜𝗥𝗦𝗧</b>👇"""

        bot.send_photo(message.chat.id, photo=START_PHOTO_URL, caption=welcome_caption, 
                       parse_mode='HTML', reply_markup=get_verify_keyboard())

    except Exception as e:
        print(f"❌ Start error: {e}")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    try:
        user_id = call.from_user.id

        if call.data == "verify":
            all_joined, not_joined = check_all_channels(user_id)
            if all_joined:
                cursor.execute("SELECT is_verified, refer_reward_given FROM users WHERE user_id = ?", (user_id,))
                user_data = cursor.fetchone()
                was_verified = (user_data[0] == 1) if user_data else False
                reward_given = (user_data[1] == 1) if user_data else False
                
                if not was_verified:
                    cursor.execute("UPDATE users SET is_verified = 1, balance = balance + ? WHERE user_id = ?", (VERIFY_BONUS, user_id))
                    conn.commit()
                
                if not reward_given:
                    cursor.execute("SELECT referred_by FROM users WHERE user_id = ?", (user_id,))
                    ref_data = cursor.fetchone()
                    if ref_data and ref_data[0] is not None:
                        rid = ref_data[0]
                        cursor.execute("""
                            UPDATE users 
                            SET total_referrals = total_referrals + 1, 
                                balance = balance + ? 
                            WHERE user_id = ?
                        """, (REFER_REWARD, rid))
                        conn.commit()
                        cursor.execute("UPDATE users SET refer_reward_given = 1 WHERE user_id = ?", (user_id,))
                        conn.commit()
                        
                        cursor.execute("SELECT total_referrals, balance FROM users WHERE user_id = ?", (rid,))
                        ref_info = cursor.fetchone()
                        
                        bot.send_message(rid, f"""
🎉 <b>নতুন রেফার সফল!</b>

👥 <b>মোট সফল রেফার:</b> {ref_info[0]}
💰 <b>যোগ হয়েছে:</b> {REFER_REWARD} টাকা
📊 <b>বর্তমান ব্যালেন্স:</b> {ref_info[1]:.2f} টাকা
""", parse_mode='HTML')

                        if ref_info[0] == 2:
                            k2 = telebot.types.InlineKeyboardMarkup(row_width=2)
                            k2.add(
                                telebot.types.InlineKeyboardButton("𝗬𝗘𝗦 ✅", callback_data="start_signal_yes"),
                                telebot.types.InlineKeyboardButton("𝗡𝗢 🚫", callback_data="start_signal_no")
                            )
                            bot.send_message(rid, """🌼অভিনন্দন✨ 🥳

💠আপনার ২ টা রেফার সফলভাবে হয়ছে💠
🔵আপনি যদি চান তাহলে এখন সিগন্যাল নিতে পারেন📈

🩷সিগন্যাল কি দেওয়া শুরু করবো🩷""", parse_mode='HTML', reply_markup=k2)

                bot_username = bot.get_me().username
                user_ref_link = f"https://t.me/{bot_username}?start=ref_{user_id}"
                
                verify_success_msg = f"""🟢<b>𝗩𝗘𝗥𝗬𝗙𝗜𝗖𝗔𝗧𝗜𝗢𝗡 𝗦𝗨𝗖𝗖𝗘𝗦𝗙𝗨𝗟𝗟</b> ✅

📊এখন আপনি <b>২ টি রেফার</b> করুন তাহলে আপনি <b>𝗡𝗫 𝗡𝗘𝗫𝗢𝗥𝗔 𝗚𝗣𝗧 𝗕𝗢𝗧</b> এর ফ্রি <b>১০০% প্রফিট সিগন্যাল</b> পাবেন ✅

🤖আপনার বট রেফার লিংক 👇
<code>{user_ref_link}</code>

🔵 <b>𝟮 টি রেফারকে অবশ্যই ভেরিফিকেশন করাবেন</b> তাহলে সফল হয়বে রেফার 🔵"""
                
                k = telebot.types.InlineKeyboardMarkup(row_width=1)
                k.add(telebot.types.InlineKeyboardButton(
                    "🟢 𝗥𝗘𝗙𝗙𝗘𝗥 𝗡𝗔𝗪 📊", 
                    url=f"https://t.me/share/url?url={user_ref_link}&text=Join%20NX%20XHAWON"
                ))
                
                bot.edit_message_caption(verify_success_msg, call.message.chat.id, call.message.message_id, 
                                        parse_mode='HTML', reply_markup=k)
                
                bot.send_message(call.message.chat.id, "👇 নিচের মেনু থেকে সেবা নিন:", reply_markup=get_bottom_menu())
            else:
                msg = "❌ <b>আপনি সব চ্যানেলে জয়েন করেননি মামা!</b>\n\n"
                for i, ch in enumerate(not_joined):
                    if i < len(CHANNEL_LINKS):
                        msg += f"• <a href='{CHANNEL_LINKS[i]}'>চ্যানেল {i+1}</a>\n"
                msg += "\nজয়েন করে আবার <b>ভেরিফাই</b> করুন।"
                bot.edit_message_caption(msg, call.message.chat.id, call.message.message_id,
                                      parse_mode='HTML', reply_markup=get_verify_keyboard())
            bot.answer_callback_query(call.id)

        elif call.data == "start_signal_yes":
            bot.answer_callback_query(call.id, "✅ Signal চালু হচ্ছে...")
            bot.send_message(call.message.chat.id, """
✅ <b>চমৎকার মামা!</b>

🎯 আপনার <b>5 WIN Signal</b> চালু করা হচ্ছে...
📌 অপেক্ষা করুন কিছুক্ষণ ⏳
""", parse_mode='HTML')
            threading.Thread(target=paid_signal_engine, args=(user_id, 5), daemon=True).start()

        elif call.data == "start_signal_no":
            bot.answer_callback_query(call.id, "🚫 Cancel")
            bot.send_message(call.message.chat.id, """
❌ <b>ঠিক আছে মামা!</b>

🩷 আপনি যখন সিগন্যাল নিতে চাইবেন, তখন আবার বলবেন ✅
""", parse_mode='HTML')

        elif call.data == "send_payment_proof":
            bot.answer_callback_query(call.id)
            msg = f"""
📤 <b>Send Payment Proof</b>

📌 নিচের তথ্যগুলো পাঠান:
১. <b>Send Money এর স্ক্রিনশট</b>
২. <b>Last 2 Digit</b> (যেমন: 28)

⚠️ <b>শুধু Send Money করুন।</b>

👇 এখন স্ক্রিনশট + Last 2 Digit একসাথে পাঠান।
"""
            bot.send_message(call.message.chat.id, msg, parse_mode='HTML')
            bot.register_next_step_handler(call.message, process_recharge_screenshot)

        elif call.data.startswith("pkg_paid_"):
            wins_str = call.data.split("_")[2]
            if wins_str == "custom":
                msg = "🎯 <b>Paid Signal Custom Order</b>\n\n💰 প্রতি WIN = 3 টাকা\n\n👉 আপনি কত WIN কিনতে চান? সংখ্যা লিখে পাঠান।"
                bot.edit_message_text(msg, call.message.chat.id, call.message.message_id, parse_mode='HTML')
                bot.register_next_step_handler(call.message, process_paid_custom)
                return
            
            wins = int(wins_str)
            cost = wins * PAID_SIGNAL_PER_WIN
            
            cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
            data = cursor.fetchone()
            balance = data[0] if data else 0
            
            if balance < cost:
                bot.answer_callback_query(call.id, f"❌ ব্যালেন্সে {cost} টাকা নেই!", show_alert=True)
                return
            
            cursor.execute("UPDATE users SET balance = balance - ? WHERE user_id = ?", (cost, user_id))
            conn.commit()
            remaining = balance - cost
            
            msg = f"""
✅ <b>PAID SIGNAL চালু হয়েছে!</b>

🎯 <b>Wins:</b> {wins}
💰 <b>কাটা হয়েছে:</b> {cost} টাকা
📊 <b>ব্যালেন্স:</b> {remaining:.2f} টাকা

🚀 Signal শুরু হচ্ছে...
"""
            bot.edit_message_text(msg, call.message.chat.id, call.message.message_id, parse_mode='HTML')
            threading.Thread(target=paid_signal_engine, args=(user_id, wins), daemon=True).start()
            bot.answer_callback_query(call.id)

        elif call.data.startswith("pkg_ns_"):
            wins = 5
            cost = wins * NUMBER_SHOT_PER_WIN
            
            cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
            data = cursor.fetchone()
            balance = data[0] if data else 0
            
            if balance < cost:
                bot.answer_callback_query(call.id, f"❌ ব্যালেন্সে {cost} টাকা নেই!", show_alert=True)
                return
            
            cursor.execute("UPDATE users SET balance = balance - ? WHERE user_id = ?", (cost, user_id))
            conn.commit()
            remaining = balance - cost
            
            msg = f"""
✅ <b>NUMBER SHOT চালু হয়েছে!</b>

🎯 <b>Target:</b> {wins} WIN
💰 <b>কাটা হয়েছে:</b> {cost} টাকা
📊 <b>ব্যালেন্স:</b> {remaining:.2f} টাকা

🚀 Number Shot Signal শুরু হচ্ছে...
"""
            bot.edit_message_text(msg, call.message.chat.id, call.message.message_id, parse_mode='HTML')
            threading.Thread(target=number_shot_engine, args=(user_id, wins), daemon=True).start()
            bot.answer_callback_query(call.id)

        elif call.data.startswith("accept_recharge_"):
            if call.from_user.id != OWNER_ID:
                bot.answer_callback_query(call.id, "❌ অনুমোদিত নন!", show_alert=True)
                return
            target_user_id = int(call.data.split("_")[2])
            bot.answer_callback_query(call.id, "✅ Accept!")
            bot.send_message(OWNER_ID, f"💰 <b>User ID:</b> <code>{target_user_id}</code>\n\nকত টাকা যোগ করবেন? সংখ্যা লিখে পাঠান:", parse_mode='HTML')
            bot.register_next_step_handler(call.message, process_admin_accept_amount, target_user_id)

        elif call.data.startswith("reject_recharge_"):
            if call.from_user.id != OWNER_ID:
                bot.answer_callback_query(call.id, "❌ অনুমোদিত নন!", show_alert=True)
                return
            target_user_id = int(call.data.split("_")[2])
            bot.answer_callback_query(call.id, "❌ Rejected!")
            try:
                bot.send_message(target_user_id, "❌ <b>দুঃখিত!</b> আপনার Recharge Request Accept হয়নি।\n\nআবার সঠিকভাবে Send Money করে পাঠান।", parse_mode='HTML')
            except: pass

    except Exception as e:
        print(f"❌ Callback error: {e}")

def process_recharge_screenshot(message):
    try:
        user_id = message.from_user.id
        first_name = message.from_user.first_name or "User"
        username = message.from_user.username or "No Username"
        
        if not message.photo:
            bot.reply_to(message, "❌ দয়া করে একটি স্ক্রিনশট (Photo) পাঠান।")
            return
        
        caption = message.caption or ""
        if not caption:
            bot.reply_to(message, "❌ স্ক্রিনশটের সাথে <b>Last 2 Digit</b> লিখে পাঠান।", parse_mode='HTML')
            return
        
        photo_file_id = message.photo[-1].file_id
        
        owner_msg = f"""
🆕 <b>NEW RECHARGE REQUEST</b>

👤 <b>Name:</b> {first_name}
🔗 <b>Username:</b> @{username}
🆔 <b>User ID:</b> <code>{user_id}</code>
📝 <b>Last 2 Digit:</b> <code>{caption}</code>
📅 <b>Time:</b> {get_bd_time().strftime('%d-%m-%Y %H:%M:%S')}

━━━━━━━━━━━━━━━━━━━━━
💳 <b>Accept বা No Accept করুন:</b>
"""
        
        k = telebot.types.InlineKeyboardMarkup(row_width=2)
        k.add(
            telebot.types.InlineKeyboardButton("✅ ACCEPT", callback_data=f"accept_recharge_{user_id}"),
            telebot.types.InlineKeyboardButton("❌ NO ACCEPT", callback_data=f"reject_recharge_{user_id}")
        )
        
        bot.send_photo(OWNER_ID, photo=photo_file_id, caption=owner_msg, parse_mode='HTML', reply_markup=k)
        
        wait_msg = "✅ <b>Payment Proof গ্রহণ করা হয়েছে!</b>\n\n⏳ <b>১০-১৫ মিনিট</b> অপেক্ষা করুন।\n👨‍💻 অ্যাডমিন ব্যালেন্স যোগ করে দেবেন।"
        bot.reply_to(message, wait_msg, parse_mode='HTML')
        
    except Exception as e:
        print(f"❌ Recharge screenshot error: {e}")

def process_admin_accept_amount(message, target_user_id):
    try:
        if message.from_user.id != OWNER_ID:
            return
        try:
            amount = float(message.text.strip())
        except:
            bot.reply_to(message, "❌ শুধু সংখ্যা লিখুন (যেমন: 100, 50)")
            return
        
        if amount <= 0:
            bot.reply_to(message, "❌ অ্যামাউন্ট ০ এর বেশি হতে হবে।")
            return
        
        cursor.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, target_user_id))
        conn.commit()
        cursor.execute("SELECT balance FROM users WHERE user_id = ?", (target_user_id,))
        data = cursor.fetchone()
        new_balance = data[0] if data else 0
        
        bot.reply_to(message, f"✅ <b>Recharge সম্পন্ন!</b>\n\n👤 User: <code>{target_user_id}</code>\n💰 যোগ: {amount:.2f} টাকা\n📊 বর্তমান: {new_balance:.2f} টাকা", parse_mode='HTML')
        
        try:
            bot.send_message(target_user_id, f"🎉 <b>Recharge সফল!</b>\n\n💰 যোগ: {amount:.2f} টাকা\n📊 ব্যালেন্স: {new_balance:.2f} টাকা\n\n👉 এখন Paid Signal কিনতে পারবেন।", parse_mode='HTML')
        except: pass
        
    except Exception as e:
        print(f"❌ Process accept amount error: {e}")

@bot.chat_join_request_handler()
def handle_join_request(request):
    try:
        user_id = request.from_user.id
        first_name = request.from_user.first_name or "ভাই"
        username = request.from_user.username or "No Username"
        chat_id = request.chat.id

        if int(chat_id) != int(JOIN_REQUEST_CHANNEL_ID):
            return

        try:
            bot.approve_chat_join_request(chat_id, user_id)
        except Exception as e:
            print(f"❌ Approve error: {e}")
            return

        try:
            owner_msg = f"""
🆕 <b>NEW JOIN REQUEST ACCEPTED</b>

👤 <b>Name:</b> {first_name}
🔗 <b>Username:</b> @{username}
🆔 <b>User ID:</b> <code>{user_id}</code>
📅 <b>Time:</b> {get_bd_time().strftime('%d-%m-%Y %H:%M:%S')}
"""
            bot.send_message(OWNER_ID, owner_msg, parse_mode='HTML')
        except: pass

        try:
            cursor.execute("INSERT OR IGNORE INTO users (user_id, first_name, join_date) VALUES (?, ?, ?)",
                           (user_id, first_name, get_bd_time().strftime('%Y-%m-%d %H:%M:%S')))
            conn.commit()
        except: pass

        try:
            welcome_verify_text = f"""
💚✨ <b>𝗛𝗘𝗬 {first_name} মামা!</b> 🩷✨
💠 আমি <b>𝗡𝗫 •𝗡𝗘𝗫𝗢𝗥𝗔 𝗚𝗣𝗧• 𝗕𝗢𝗧</b> 🔵 আসসালামু আলাইকুম! 💠

━━━━━━━━━━━━━━━━━━━━━━━━━
🥰 <b>NX Family</b>-তে স্বাগতম জানাচ্ছি! 🎉
✅ আপনার <b>Join Request Accepted</b> হয়েছে!
📢 আপনি এখন <b>NX family</b> এর সদস্য 🔵

🔮<b>𝗡𝗫 𝗧𝗗𝗥 𝗖𝗢𝗠𝗠𝗨𝗡𝗜𝗧𝗬</b> এর পিন মেসেজ দেখবেন, লাইভ এবং প্রতিটা পোস্ট লক্ষ করলে বুঝতে পারবেন তারা অন্যান্য কমিউনিটি থেকে আলাদা ✅
━━━━━━━━━━━━━━━━━━━━━━━━━

🤖 <b>BOT সিগন্যাল নিতে ভেরিফিকেশন করুন</b> 📊
📌 <b>সিগন্যাল পেতে নিচের ৪টি চ্যানেলে জয়েন করুন</b> 🩷

✅ Verification করলে সাথে সাথে <b>১০ টাকা বোনাস</b> পাবেন এবং বট থেকে ইনকাম করতে পারবেন 🩷📈
"""
            bot.send_message(user_id, welcome_verify_text, reply_markup=get_verify_keyboard(), parse_mode='HTML')
        except Exception as e:
            print(f"❌ Welcome+Verify message error to {user_id}: {e}")

        t2 = threading.Timer(20 * 60, send_followup_message, args=(user_id, first_name))
        t2.daemon = True
        t2.start()

    except Exception as e:
        print(f"❌ Join Request handler error: {e}")

@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    try:
        for member in message.new_chat_members:
            user_id = member.id
            first_name = member.first_name or "ভাই"

            welcome_text = f"🎉 <b>𝗪𝗘𝗟𝗖𝗢𝗠𝗘 {first_name}!</b>\n\n👇 Bot-এ /start দিন:\nhttps://t.me/{BOT_USERNAME}"
            k = telebot.types.InlineKeyboardMarkup(row_width=1)
            k.add(telebot.types.InlineKeyboardButton("🚀 𝗦𝗧𝗔𝗥𝗧 𝗕𝗢𝗧", url=f"https://t.me/{BOT_USERNAME}?start=welcome"))

            try:
                bot.send_message(message.chat.id, welcome_text, parse_mode='HTML', reply_markup=k)
            except: pass

            try:
                cursor.execute("INSERT OR IGNORE INTO users (user_id, first_name, join_date) VALUES (?, ?, ?)",
                               (user_id, first_name, get_bd_time().strftime('%Y-%m-%d %H:%M:%S')))
                conn.commit()
            except: pass

            try:
                bot.send_message(user_id, get_welcome_dm(first_name), parse_mode='HTML', reply_markup=get_welcome_keyboard())
            except: pass
    except Exception as e:
        print(f"❌ Welcome handler error: {e}")

def paid_signal_engine(user_id, total_wins):
    try:
        state = {
            "pending_sig": None, "pending_period": None,
            "wins": 0, "total_wins": total_wins,
            "loss_streak": 0, "is_recovery": False,
            "last_period": "0", "signal_sent": False
        }
        
        bot.send_message(user_id, f"💎 <b>PAID SIGNAL ENGINE চালু!</b>\n\n🎯 আপনি {total_wins}টি WIN সিগন্যাল পাবেন।", parse_mode='HTML')
        
        while state["wins"] < state["total_wins"]:
            try:
                res = requests.get(f"{API_URL}?t={int(time.time()*1000)}", timeout=10)
                data = res.json()
                lst = data['data']['list']
                if not lst:
                    time.sleep(1); continue
                    
                current_p = lst[0]['issueNumber']
                current_num = int(lst[0]['number'])
                
                if current_p != state.get("last_period", "0"):
                    if state.get("pending_sig") and state.get("pending_period") == current_p:
                        act_dir = "BIG" if current_num >= 5 else "SMALL"
                        is_win = (state["pending_sig"] == act_dir)
                        sig_display = "𝗕𝗜𝗚" if state['pending_sig'] == "BIG" else "𝗦𝗠𝗔𝗟𝗟"
                        
                        if is_win:
                            state["wins"] += 1
                            state["loss_streak"] = 0
                            state["is_recovery"] = False
                            
                            bot.send_message(user_id, f"""{sig_display} 𝗪𝗜𝗡 ✅
💠𝗣𝗿𝗼𝗴𝗿𝗲𝘀𝘀 : {state['wins']}/{state['total_wins']}""")
                            
                            if state["wins"] >= state["total_wins"]:
                                k_end = telebot.types.InlineKeyboardMarkup(row_width=2)
                                k_end.add(
                                    telebot.types.InlineKeyboardButton("😎 𝗢𝗪𝗡𝗘𝗥", url=PREMIUM_LINK),
                                    telebot.types.InlineKeyboardButton("𝗡𝗫 𝗖𝗢𝗠𝗠𝗨𝗡𝗜𝗧𝗬", url="https://t.me/+XFpXmlGPjMI5N2U1")
                                )
                                bot.send_message(user_id, f"""🏆 <b>𝗦𝗘𝗔𝗦𝗢𝗡 𝗘𝗡𝗗</b> 🎉

✅ আপনার <b>{state['total_wins']}টি WIN</b> সম্পূর্ণ হয়েছে!

📊 মোট WIN: <b>{state['total_wins']}</b>
🔥 <b>𝗔𝗨𝗧𝗢 𝗦𝗜𝗚𝗡𝗔𝗟 𝗕𝗢𝗧</b> — 100% PROFIT

📌 আবার <b>𝗦𝗜𝗚𝗡𝗔𝗟 + 𝗟𝗜𝗙𝗘 𝗧𝗜𝗠𝗘 𝗣𝗥𝗢𝗙𝗜𝗧</b> নিতে চাইলে Owner এর সাথে যোগাযোগ করুন 👇""", parse_mode='HTML', reply_markup=k_end)
                                break
                        else:
                            state["loss_streak"] += 1
                            if state["loss_streak"] >= 3 and not state["is_recovery"]:
                                state["is_recovery"] = True
                            
                            bot.send_message(user_id, f"""{sig_display} 𝗟𝗢𝗦𝗦❌
{state['loss_streak']}step""")
                        
                        state["pending_sig"] = None
                        state["pending_period"] = None
                        state["signal_sent"] = False
                    
                    state["last_period"] = current_p
                    
                    if state["wins"] < state["total_wins"] and not state.get("signal_sent", False):
                        api_prediction = get_prediction_from_api("30s")
                        if api_prediction:
                            prediction = api_prediction["signal"]
                            next_p = api_prediction["target_period"]
                            state["pending_sig"] = prediction
                            state["pending_period"] = next_p
                            state["signal_sent"] = True
                            mode_display = "🟢 NORMAL" if not state["is_recovery"] else "🔴 RECOVERY"
                            confidence = api_prediction["confidence"]
                            confidence_line = f"\n📈 Confidence: {confidence}" if confidence else ""
                            bot.send_message(user_id, f"""💎 <b>PAID SIGNAL</b>

⏰ WIN GO 30SECOND
⚪ Period: #{next_p[-4:]}
🎯 TRADE: {prediction}{confidence_line}
🎰 Mode: {mode_display}
🎯 Progress: {state['wins']}/{state['total_wins']}""", parse_mode='HTML')
                time.sleep(1)
            except Exception as e:
                print(f"⚠️ Paid signal error: {e}")
                time.sleep(2)
    except Exception as e:
        print(f"❌ Paid engine error: {e}")

def number_shot_engine(user_id, total_wins):
    try:
        state = {
            "pending_sig": None, "pending_period": None,
            "pending_nums": None,
            "wins": 0, "total_wins": total_wins,
            "loss_streak": 0, "is_recovery": False,
            "last_period": "0", "signal_sent": False
        }
        
        bot.send_message(user_id, f"𝗡𝗨𝗠𝗕𝗘𝗥 𝗦𝗛𝗢𝗧 🔥\n\n🎯 Target: {total_wins} WIN\n\n🚀 শুরু হচ্ছে...")
        
        while state["wins"] < state["total_wins"]:
            try:
                res = requests.get(f"{API_URL}?t={int(time.time()*1000)}", timeout=10)
                data = res.json()
                lst = data['data']['list']
                if not lst:
                    time.sleep(1); continue
                    
                current_p = lst[0]['issueNumber']
                current_num = int(lst[0]['number'])
                
                if current_p != state.get("last_period", "0"):
                    if state.get("pending_sig") and state.get("pending_period") == current_p:
                        act_dir = "BIG" if current_num >= 5 else "SMALL"
                        is_win = (state["pending_sig"] == act_dir)
                        pending_nums = state.get("pending_nums") or (0, 0)
                        nums_list = list(pending_nums)
                        sig_display = "𝗕𝗜𝗚" if state['pending_sig'] == "BIG" else "𝗦𝗠𝗔𝗟𝗟"
                        
                        if is_win:
                            state["wins"] += 1
                            state["loss_streak"] = 0
                            state["is_recovery"] = False
                            
                            if current_num in nums_list:
                                bot.send_message(user_id, f"""{sig_display} {current_num} 𝗝𝗔𝗖𝗞𝗣𝗢𝗥𝗧 𝗪𝗜𝗡✅
💠𝗣𝗿𝗼𝗴𝗿𝗮𝘀𝗲:{state['wins']}/{state['total_wins']}""")
                            else:
                                bot.send_message(user_id, f"""{sig_display} 𝗪𝗜𝗡✅
💠𝗣𝗿𝗼𝗴𝗿𝗮𝘀𝗲:{state['wins']}/{state['total_wins']}""")
                            
                            if state["wins"] >= state["total_wins"]:
                                k_end = telebot.types.InlineKeyboardMarkup(row_width=2)
                                k_end.add(
                                    telebot.types.InlineKeyboardButton("😎 𝗢𝗪𝗡𝗘𝗥", url=PREMIUM_LINK),
                                    telebot.types.InlineKeyboardButton("𝗡𝗫 𝗖𝗢𝗠𝗠𝗨𝗡𝗜𝗧𝗬", url="https://t.me/+XFpXmlGPjMI5N2U1")
                                )
                                bot.send_message(user_id, f"""🏆 𝗡𝗨𝗠𝗕𝗘𝗥 𝗦𝗛𝗢𝗧 𝗦𝗘𝗔𝗦𝗢𝗡 𝗘𝗡𝗗 🎉

✅ আপনার {state['total_wins']}টি WIN সম্পূর্ণ!

🔥 𝗔𝗨𝗧𝗢 𝗦𝗜𝗚𝗡𝗔𝗟 𝗕𝗢𝗧 — 100% PROFIT

📌 আবার 𝗦𝗜𝗚𝗡𝗔𝗟 + 𝗟𝗜𝗙𝗘 𝗧𝗜𝗠𝗘 𝗣𝗥𝗢𝗙𝗜𝗧 নিতে চাইলে Owner এর সাথে যোগাযোগ করুন 👇""", reply_markup=k_end)
                                break
                        else:
                            state["loss_streak"] += 1
                            bot.send_message(user_id, f"""{sig_display} 𝗟𝗢𝗦𝗦❌
💠𝗣𝗿𝗼𝗴𝗿𝗮𝘀𝗲:{state['wins']}/{state['total_wins']}""")
                        
                        state["pending_sig"] = None
                        state["pending_period"] = None
                        state["pending_nums"] = None
                        state["signal_sent"] = False
                    
                    state["last_period"] = current_p
                    
                    if state["wins"] < state["total_wins"] and not state.get("signal_sent", False):
                        api_prediction = get_prediction_from_api("30s")
                        if api_prediction and len(api_prediction["digits"]) >= 2:
                            prediction = api_prediction["signal"]
                            next_p = api_prediction["target_period"]
                            nums = tuple(api_prediction["digits"][:2])
                            state["pending_sig"] = prediction
                            state["pending_period"] = next_p
                            state["signal_sent"] = True
                            state["pending_nums"] = nums
                            confidence = api_prediction["confidence"]
                            confidence_line = f"\nConfidence: {confidence}" if confidence else ""
                            bot.send_message(user_id, f"""𝗡𝗨𝗠𝗕𝗘𝗥 𝗦𝗛𝗢𝗧 🔥
𝗣𝗥𝗜𝗢𝗗:#{next_p[-4:]}
𝗧𝗿𝗮𝗱𝗲: {prediction}/ {nums[0]}'{nums[1]}{confidence_line}""")
                        elif api_prediction:
                            logging.warning("API returned a signal without two valid digits; Number Shot skipped.")
                time.sleep(1)
            except Exception as e:
                print(f"⚠️ Number shot error: {e}")
                time.sleep(2)
    except Exception as e:
        print(f"❌ Number shot engine error: {e}")

RECOVERY_ON_TEXT = "🔴 RECOVERY MODE Alert ⚠️🚩"
NORMAL_ON_TEXT = "🟢 NORMAL MODE 😎 chill 💯"

def get_win_text_new(period, signal, total_wins):
    sig_display = "BIG" if signal == "BIG" else "SMALL"
    return f"""╭━━━━━━━━━━━━━━╮
│ 🔘 #{period}
│ 🟢 {sig_display} = WIN ✅ [{total_wins}]
╰━━━━━━━━━━━━━━╯"""

def get_loss_text_new(period, signal, step):
    sig_display = "BIG" if signal == "BIG" else "SMALL"
    return f"""╭━━━━━━━━━━━━━━╮
│ 🔘 #{period}
│ 🔴 {sig_display} = LOSS [{step}step]
╰━━━━━━━━━━━━━━╯"""

def get_win_text(period, signal, tw):
    sig_display = "𝗕𝗜𝗚" if signal == "BIG" else "𝗦𝗠𝗔𝗟𝗟"
    return f"𒆜 PERIOD: #{period}={sig_display} > WIN ✅"

def get_loss_text(period, signal, step):
    sig_display = "𝗕𝗜𝗚" if signal == "BIG" else "𝗦𝗠𝗔𝗟𝗟"
    return f"𒆜 PERIOD: #{period}={sig_display} > loss"

def get_ready_message(channel):
    start_time = f"{channel['start_hour']:02d}:{channel['start_min']:02d}"
    target = channel["target_wins"]
    return f"""
হ্যালো, আসসালামু আলাইকুম 🩷🌼

💠 আমি <b>NX XHAWON</b> এর ছোট ভাই <b>NX REAL KNOWLEDGE BOT</b> 🧿🤖

✅ শাওন ভাই থেকে শেখা রুলস ফলো করে সিগন্যাল দিবো
🎯 <b>আজকের Target:</b> {target} Wins
⏰ <b>Signal শুরু:</b> {start_time} AM

🚀 <b>Let's Go!</b>
"""

def get_success_message(channel):
    wins = channel["wins"]
    target = channel["target_wins"]
    history = channel.get("history", [])
    
    history_lines = []
    for h in history:
        sig_display = "𝗕𝗜𝗚" if h["signal"] == "BIG" else "𝗦𝗠𝗔𝗟𝗟"
        if h["status"] == "WIN":
            history_lines.append(f"𒆜 PERIOD: #{h['period']}={sig_display} > WIN ✅")
        else:
            history_lines.append(f"𒆜 PERIOD: #{h['period']}={sig_display} > loss")
    
    history_text = "\n".join(history_lines) if history_lines else "No history"
    
    return f"""🤖 <b>আজ সফল ভাবে ১০০০১% প্রফিট দিছি সবাইকে</b> ✅
🔮 এটাই হচ্ছে <b>NX REAL KNOWLEDGE</b> পাওয়ার ওকে 🟢

━━━━━━━━━━━━━━━━━━━━━
📊 <b>TODAY'S RESULT</b>
━━━━━━━━━━━━━━━━━━━━━
🏆 Target: <b>{target} Wins</b> ✅
✅ Total Wins: <b>{wins}</b>
━━━━━━━━━━━━━━━━━━━━━

📋 <b>RESULT HISTORY:</b>
{history_text}

━━━━━━━━━━━━━━━━━━━━━
📊 <b>Signal:</b> UNDER {channel.get('max_loss_streak', 0)} STEP
━━━━━━━━━━━━━━━━━━━━━

✅ সবাই দ্রুত আমার গুরুর কাছে সিগন্যাল এর রিভিউ পাঠান 😭 
সিগন্যাল এর রিভিউ ভালো দিবেন, সিগন্যাল খারাপ হয়লে চাকরি থাকবে না 🙏😭
"""

def get_premium_promo_message():
    return """
✅ যারা <b>NX PRINIYAM JONE</b> এ জয়েন হতে চান কিন্তু জানেন না আমাদের <b>NX PRINIYAM JONE</b> এ কি কি আছে..? ⚠️

👉 নিচের চ্যানেলে ঘুরে আসুন ✅

━━━━━━━━━━━━━━━━━━━━━
🟢 <b>চ্যানেল লিংক:</b>
https://t.me/NX_ALL_FACALITY

💠 যদি দেখে ভালো লাগে নিচের লিংক থেকে একাউন্ট খুলে ডিপোজিট করুন 🔮📊
https://dkwin9.com/#/register?invitationCode=33553462271

📈🤖 <b>𝗡𝗫 𝗣𝗥𝗜𝗡𝗜𝗬𝗔𝗠 𝗝𝗢𝗡𝗘</b> এ জয়েন হতে নিচের <b>OWNER ID</b> তে যোগাযোগ করুন, ধন্যবাদ 📈💰
━━━━━━━━━━━━━━━━━━━━━
"""

def get_daily_report_message(channel):
    wins = channel["wins"]
    losses = channel["losses"]
    total = wins + losses
    wr = int(wins / total * 100) if total > 0 else 0
    
    history = channel.get("history", [])
    history_lines = []
    for h in history[-25:]:
        sig_display = "𝗕𝗜𝗚" if h["signal"] == "BIG" else "𝗦𝗠𝗔𝗟𝗟"
        if h["status"] == "WIN":
            history_lines.append(f"𒆜 PERIOD: #{h['period']}={sig_display} > WIN ✅")
        else:
            history_lines.append(f"𒆜 PERIOD: #{h['period']}={sig_display} > loss")
    
    history_text = "\n".join(history_lines) if history_lines else "No history"
    
    if channel.get("unlimited", False):
        return f"""
╔═══════════════════════════════════════
║      📊 <b>DAILY REPORT</b> 📊
╠═══════════════════════════════════════
║   📢 <b>{channel['name']}</b>
║
║   ♾️ <b>UNLIMITED 24/7</b>
║   ✅ Wins: <b>{wins}</b>
║   ❌ Losses: <b>{losses}</b>
║   📈 Win Rate: <b>{wr}%</b>
║   📊 Signal: UNDER {channel.get('max_loss_streak', 0)} STEP
║
║   📅 {get_bd_time().strftime('%d-%m-%Y')}
╚═══════════════════════════════════════

📋 <b>LAST RESULTS:</b>
{history_text}

━━━━━━━━━━━━━━━━━━━━━
💠 <b>NX REAL KNOWLEDGE</b> 📈
"""
    else:
        target = channel["target_wins"]
        status = "🏆 COMPLETED" if channel["completed"] else "⚠️ INCOMPLETE"
        return f"""
╔═══════════════════════════════════════
║      📊 <b>DAILY REPORT</b> 📊
╠═══════════════════════════════════════
║   📢 <b>{channel['name']}</b>
║
║   🏆 Target: <b>{target} Wins</b>
║   ✅ Wins: <b>{wins}</b>
║   ❌ Losses: <b>{losses}</b>
║   📈 Win Rate: <b>{wr}%</b>
║   📌 Status: {status}
║   📊 Signal: UNDER {channel.get('max_loss_streak', 0)} STEP
║
║   📅 {get_bd_time().strftime('%d-%m-%Y')}
╚═══════════════════════════════════════

📋 <b>LAST RESULTS:</b>
{history_text}

━━━━━━━━━━━━━━━━━━━━━
💠 <b>NX REAL KNOWLEDGE</b> 📈
"""

def send_70win_report(channel, start_time, end_time, start_wins, end_wins, losses):
    try:
        total = (end_wins - start_wins + 1) + losses
        wr = int((end_wins - start_wins + 1) / total * 100) if total > 0 else 0
        highest_step = channel.get("max_loss_streak", 0)
        report_num = (end_wins // 70)

        report = f"""📊 <b>NX 70 WIN REPORT #{report_num}</b> 📊
━━━━━━━━━━━━━━━━━━━━━
📢 <b>Channel:</b> {channel['name']}
🎯 <b>Wins:</b> {start_wins} → {end_wins}
❌ <b>Losses:</b> {losses}
📈 <b>Win Rate:</b> {wr}%
🔥 <b>Highest Step:</b> {highest_step}
⏰ <b>Start Time:</b> {start_time}
⏰ <b>End Time:</b> {end_time}
📅 <b>Date:</b> {get_bd_time().strftime('%d-%m-%Y')}
━━━━━━━━━━━━━━━━━━━━━
💠 <b>NX REAL KNOWLEDGE</b> 📈"""
        bot.send_message(OWNER_ID, report, parse_mode='HTML')
    except Exception as e:
        print(f"❌ 70-win report error: {e}")

def check_pre_signal_time(channel):
    if channel.get("notified", False) or channel.get("unlimited", False):
        return False
    now = get_bd_time()
    ct = now.hour * 60 + now.minute
    start = channel["start_hour"] * 60 + channel["start_min"]
    return ct == start - 6

def is_channel_active(channel):
    now = get_bd_time()
    ct = now.hour * 60 + now.minute
    start = channel["start_hour"] * 60 + channel["start_min"]
    end = channel["end_hour"] * 60 + channel["end_min"]
    return start <= ct <= end

def send_to_specific_channel(channel_id, text):
    try:
        bot.send_message(channel_id, text, parse_mode='HTML')
        return True
    except Exception as e:
        print(f"❌ Send error {channel_id}: {e}")
        return False

def get_signal_text_channel(period, signal, channel):
    sb = "𝗕𝗜𝗚" if signal == "BIG" else "𝗦𝗠𝗔𝗟𝗟"
    md = "🔴 RECOVERY" if channel["is_recovery"] else "🟢 NORMAL"
    return f"""
┏━━━━━━━━━━━━━━┓
  💠 <b>NX XHAWON SIGNAL</b> 💠
┗━━━━━━━━━━━━━━┛
⏰ WIN GO 30SECOND
⚪ Period: #{period}
📊 Signal: ( <b>{sb}</b> )
🎯 Mode: {md}
"""

def channel_engine_loop(channel):
    channel_name = channel["name"]
    channel_id = channel["id"]
    target = channel["target_wins"]
    success_sent = False
    success_time = 0

    while True:
        try:
            if not channel.get("unlimited", False):
                if channel["completed"] and not success_sent:
                    if success_time == 0:
                        success_time = time.time() + 120
                    if time.time() >= success_time:
                        try:
                            bot.send_message(channel_id, get_success_message(channel), parse_mode='HTML', reply_markup=get_owner_id_button())
                            success_sent = True
                        except: success_sent = True

            if check_pre_signal_time(channel):
                try:
                    bot.send_message(channel_id, get_ready_message(channel), parse_mode='HTML')
                except: pass
                channel["notified"] = True

            if channel["completed"]:
                time.sleep(10); continue

            if not is_channel_active(channel):
                time.sleep(30); continue

            res = requests.get(f"{API_URL}?t={int(time.time()*1000)}", timeout=10)
            data = res.json()
            lst = data['data']['list']
            if not lst:
                time.sleep(1); continue

            current_p = lst[0]['issueNumber']

            if current_p != channel["last_period"]:
                if channel["pending_sig"] and channel["pending_period"] == current_p:
                    actual_num = int(lst[0]['number'])
                    act_dir = "BIG" if actual_num >= 5 else "SMALL"
                    is_win = (channel["pending_sig"] == act_dir)
                    current4 = str(current_p)[-4:]

                    if is_win:
                        if channel.get("max_loss_streak", 0) < channel["current_step"]:
                            channel["max_loss_streak"] = channel["current_step"]
                        
                        channel["loss_count"] = 0
                        channel["current_step"] = 0
                        channel["wins"] += 1
                        
                        if channel.get("unlimited", False):
                            if channel["name"] in ["NX RECOVERY SIGNAL", "NX DUAL MODE SIGNAL"]:
                                if channel.get("report_start_time") is None:
                                    channel["report_start_time"] = get_bd_time().strftime('%I:%M %p')
                                    channel["report_start_wins"] = channel["wins"] - 1
                                    channel["report_losses"] = 0
                                    channel["report_counter"] = 0
                                
                                channel["report_counter"] = channel["wins"] - channel["report_start_wins"]
                                
                                if channel["report_counter"] >= 70:
                                    end_time_str = get_bd_time().strftime('%I:%M %p')
                                    send_70win_report(
                                        channel,
                                        channel["report_start_time"],
                                        end_time_str,
                                        channel["report_start_wins"] + 1,
                                        channel["wins"],
                                        channel["report_losses"]
                                    )
                                    channel["report_start_time"] = None
                                    channel["report_start_wins"] = channel["wins"]
                                    channel["report_losses"] = 0
                                    channel["report_counter"] = 0
                                    channel["max_loss_streak"] = 0
                            
                            send_to_specific_channel(channel_id, get_win_text_new(current4, channel["pending_sig"], channel["wins"]))
                        else:
                            send_to_specific_channel(channel_id, get_win_text(current4, channel["pending_sig"], channel["wins"]))

                        if channel.get("logic") == "normal_recovery" and channel.get("is_recovery", False):
                            channel["is_recovery"] = False
                            send_to_specific_channel(channel_id, NORMAL_ON_TEXT)
                        
                        channel["history"].append({"period": current4, "signal": channel["pending_sig"], "status": "WIN"})
                        
                        if not channel.get("unlimited", False) and channel["wins"] >= target:
                            channel["completed"] = True
                            try:
                                bot.send_message(OWNER_ID, f"🎉 <b>{channel_name}</b> Complete!\n🏆 {channel['wins']} | ❌ {channel['losses']}", parse_mode='HTML')
                            except: pass
                    else:
                        channel["loss_count"] += 1
                        channel["losses"] += 1
                        channel["current_step"] = channel["loss_count"]
                        
                        if channel.get("unlimited", False) and channel["name"] in ["NX RECOVERY SIGNAL", "NX DUAL MODE SIGNAL"]:
                            if channel.get("report_start_time") is not None:
                                channel["report_losses"] = channel.get("report_losses", 0) + 1
                        
                        if channel.get("logic") == "normal_recovery" and channel["loss_count"] >= 3 and not channel.get("is_recovery", False):
                            channel["is_recovery"] = True
                            send_to_specific_channel(channel_id, RECOVERY_ON_TEXT)
                        
                        if channel.get("unlimited", False):
                            send_to_specific_channel(channel_id, get_loss_text_new(current4, channel["pending_sig"], channel["current_step"]))
                        else:
                            send_to_specific_channel(channel_id, get_loss_text(current4, channel["pending_sig"], channel["current_step"]))
                        
                        channel["history"].append({"period": current4, "signal": channel["pending_sig"], "status": "LOSS"})
                    
                    channel["pending_sig"] = None
                    channel["pending_period"] = None

                channel["last_period"] = current_p

                if not channel["completed"] and not channel["pending_sig"]:
                    if channel.get("unlimited", False) or channel["wins"] < target:
                        api_prediction = get_prediction_from_api("30s")
                        if api_prediction:
                            prediction = api_prediction["signal"]
                            next_p = api_prediction["target_period"]
                            channel["pending_sig"] = prediction
                            channel["pending_period"] = next_p
                            send_to_specific_channel(channel_id, get_signal_text_channel(next_p[-4:], prediction, channel))
            time.sleep(1)
        except Exception as e:
            print(f"⚠️ {channel_name} error: {e}")
            time.sleep(5)

def start_all_channel_engines():
    for channel in CHANNELS:
        threading.Thread(target=channel_engine_loop, args=(channel,), daemon=True).start()

def send_good_morning():
    try:
        caption = """
🌅✨ <b>শুভ সকাল সবাইকে</b> 🤍💚💛

🤲 <b>আলহামদুলিল্লাহ</b> — আরও একটি নতুন সকাল,
নতুন আশা আর নতুনভাবে এগিয়ে যাওয়ার সুযোগ। 🌿☀️

📚 শিখুন • 🧠 বুঝুন • 🎯 ধৈর্য ধরে এগিয়ে চলুন।
👑 <b>NX XHAWON</b> 💎📊
"""
        k = telebot.types.InlineKeyboardMarkup(row_width=1)
        k.add(telebot.types.InlineKeyboardButton("🟢 𝗡𝗫 𝗖𝗢𝗠𝗠𝗨𝗡𝗜𝗧𝗬", url="https://t.me/+XFpXmlGPjMI5N2U1"))
        k.add(telebot.types.InlineKeyboardButton("🚀 𝗝𝗢𝗜𝗡 𝗢𝗪𝗡𝗘𝗥 (Premium)", url=PREMIUM_LINK))
        bot.send_photo(PUBLIC_CHANNEL_ID, photo=MORNING_PHOTO_URL, caption=caption, parse_mode='HTML', reply_markup=k)
    except Exception as e:
        print(f"❌ Morning error: {e}")

def send_good_night():
    try:
        caption = """
🌙✨ <b>শুভ রাত্রি সবাইকে</b> 🤍💚💛

🤲 <b>আলহামদুলিল্লাহ</b> — আজকের দিনটি যেমনই কাটুক,
আগামীকাল যেন আরও সুন্দর হয়।

👑 <b>NX XHAWON</b> 📊🔥
"""
        k = telebot.types.InlineKeyboardMarkup(row_width=1)
        k.add(telebot.types.InlineKeyboardButton("🟢 𝗡𝗫 𝗖𝗢𝗠𝗠𝗨𝗡𝗜𝗧𝗬", url="https://t.me/+XFpXmlGPjMI5N2U1"))
        k.add(telebot.types.InlineKeyboardButton("🚀 𝗝𝗢𝗜𝗡 𝗢𝗪𝗡𝗘𝗥 (Premium)", url=PREMIUM_LINK))
        bot.send_photo(PUBLIC_CHANNEL_ID, photo=NIGHT_PHOTO_URL, caption=caption, parse_mode='HTML', reply_markup=k)
    except Exception as e:
        print(f"❌ Night error: {e}")

def daily_reset():
    global daily_flags
    for channel in CHANNELS:
        channel["wins"] = 0
        channel["losses"] = 0
        channel["loss_count"] = 0
        channel["current_step"] = 0
        channel["max_loss_streak"] = 0
        channel["history"] = []
        channel["wins_70_reported"] = False
        if not channel.get("unlimited", False):
            channel["completed"] = False
            channel["last_period"] = "0"
            channel["pending_sig"] = None
            channel["pending_period"] = None
            channel["is_recovery"] = False
            channel["notified"] = False
        else:
            channel["pending_sig"] = None
            channel["pending_period"] = None
            channel["is_recovery"] = channel.get("logic") == "recovery_only"
            channel["report_counter"] = 0
            channel["report_start_time"] = None
            channel["report_start_wins"] = 0
            channel["report_losses"] = 0
    for k in daily_flags:
        daily_flags[k] = False

def schedule_daily_reset():
    while True:
        try:
            now = get_bd_time()
            nm = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            time.sleep((nm - now).total_seconds())
            daily_reset()
        except: time.sleep(60)

def send_daily_user_list_to_owner():
    try:
        cursor.execute("SELECT user_id, first_name, balance FROM users")
        users = cursor.fetchall()
        if not users:
            bot.send_message(OWNER_ID, "📭 আজ কোনো ইউজার নেই।")
            return
        content = f"========== NX XHAWON USER LIST ==========\nDate: {get_bd_time().strftime('%d-%m-%Y')}\nTotal: {len(users)}\n==========================================\n\n"
        for uid, name, bal in users:
            content += f"{name} | {uid} | ৳{bal:.2f}\n"
        file_bytes = io.BytesIO(content.encode('utf-8'))
        file_bytes.name = f"users_{get_bd_time().strftime('%d_%m_%Y')}.txt"
        bot.send_document(OWNER_ID, file_bytes, caption=f"📊 <b>Daily User List</b>\n👥 {len(users)} Users", parse_mode='HTML')
    except Exception as e:
        print(f"❌ User list error: {e}")

def send_daily_reports():
    for channel in CHANNELS:
        try:
            bot.send_message(channel["id"], get_daily_report_message(channel), parse_mode='HTML')
            time.sleep(1)
        except: pass

def post_promo_now():
    try:
        promo_text = get_premium_promo_message()
        k = telebot.types.InlineKeyboardMarkup(row_width=1)
        k.add(telebot.types.InlineKeyboardButton("🟢 𝗝𝗢𝗜𝗡 𝗣𝗥𝗜𝗡𝗜𝗬𝗔𝗠 𝗝𝗢𝗡𝗘 ✅", url=PRINIYAM_JOIN_LINK))
        bot.send_message(PREMIUM_PROMO_CHANNEL, promo_text, parse_mode='HTML', reply_markup=k)
        print(f"✅ Promo posted at {get_bd_time().strftime('%H:%M')}")
    except Exception as e:
        print(f"❌ Promo now error: {e}")

def newsletter_scheduler():
    while True:
        try:
            now = get_bd_time()
            h, m = now.hour, now.minute

            if h == 7 and m == 0 and not daily_flags["morning_sent"]:
                send_good_morning()
                daily_flags["morning_sent"] = True

            if h == 12 and 30 <= m <= 31 and not daily_flags.get("promo_reminder_1230", False):
                post_promo_now()
                daily_flags["promo_reminder_1230"] = True

            if h == 17 and 0 <= m <= 1 and not daily_flags.get("promo_reminder_17", False):
                post_promo_now()
                daily_flags["promo_reminder_17"] = True

            if h == 20 and 0 <= m <= 1 and not daily_flags.get("promo_reminder_20", False):
                post_promo_now()
                daily_flags["promo_reminder_20"] = True

            if h == 21 and 30 <= m <= 35 and not daily_flags["report_2130_sent"]:
                send_daily_reports()
                daily_flags["report_2130_sent"] = True

            if h == 23 and m == 0 and not daily_flags["night_sent"]:
                send_good_night()
                daily_flags["night_sent"] = True

            if h == 0 and 0 <= m <= 5 and not daily_flags["user_list_sent"]:
                send_daily_user_list_to_owner()
                daily_flags["user_list_sent"] = True

            time.sleep(20)
        except: time.sleep(60)

@bot.message_handler(func=lambda message: message.text == "👤 MY ACCOUNT")
def my_account_handler(message):
    user_id = message.from_user.id
    cursor.execute("SELECT is_verified, total_referrals, balance FROM users WHERE user_id = ?", (user_id,))
    data = cursor.fetchone()
    if data:
        status = "✅ Verified" if data[0] == 1 else "❌ Not Verified"
        msg = f"""
👤 <b>আপনার অ্যাকাউন্ট</b>

🆔 User ID: <code>{user_id}</code>
✅ Status: {status}
🎁 Successful Referrals: {data[1]}
💰 Balance: {data[2]:.2f} টাকা
📉 Min Withdraw: {MIN_WITHDRAW} টাকা
"""
        k = telebot.types.InlineKeyboardMarkup(row_width=1)
        k.add(telebot.types.InlineKeyboardButton("💰 DEPOSIT করুন", url="https://t.me/BDT_NX_Owner"))
        bot.reply_to(message, msg, parse_mode='HTML', reply_markup=k)

@bot.message_handler(func=lambda message: message.text == "💰 DEPOSIT")
def balance_recharge_handler(message):
    user_id = message.from_user.id
    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    data = cursor.fetchone()
    balance = data[0] if data else 0
    
    msg = f"""
💰 <b>DEPOSIT</b>

📊 আপনার ব্যালেন্স: <b>{balance:.2f} টাকা</b>

━━━━━━━━━━━━━━━━━━━━━
📱 <b>রিচার্জ নাম্বার (Send Money Please ✅):</b>

🟢 <b>বিকাশ:</b> <code>{BIKASH_NUMBER}</code>
🟠 <b>নগদ:</b> <code>{NAGAD_NUMBER}</code>

📌 Min Deposit: {MIN_RECHARGE} টাকা
━━━━━━━━━━━━━━━━━━━━━
💳 <b>নিয়ম:</b>
১. উপরের নাম্বারে Send Money করুন
২. স্ক্রিনশট + Last 2 Digit পাঠান
৩. ১০-১৫ মিনিট অপেক্ষা করুন
"""
    k = telebot.types.InlineKeyboardMarkup(row_width=1)
    k.add(telebot.types.InlineKeyboardButton("📤 𝗦𝗘𝗡𝗗 𝗣𝗔𝗬𝗠𝗘𝗡𝗧 𝗣𝗥𝗢𝗢𝗙", callback_data="send_payment_proof"))
    bot.reply_to(message, msg, parse_mode='HTML', reply_markup=k)

@bot.message_handler(func=lambda message: message.text == "😎JOIN NX PRINIYAM")
def join_priniyam_handler(message):
    msg = """
😎 <b>JOIN NX PRINIYAM</b>

💎 <b>NX PRINIYAM JONE</b> এ জয়েন হতে চান?

📊 Lifetime Profit — 100% Real Knowledge
🤖 Auto Signal Bot — 24/7
🔥 Free Signal + Paid Signal

👇 নিচের বাটনে ক্লিক করুন
"""
    k = telebot.types.InlineKeyboardMarkup(row_width=1)
    k.add(telebot.types.InlineKeyboardButton("😎 𝗝𝗢𝗜𝗡 𝗡𝗫 𝗔𝗟𝗟 𝗙𝗔𝗖𝗔𝗟𝗜𝗧𝗬", url=PRINIYAM_CHANNEL_LINK))
    bot.reply_to(message, msg, parse_mode='HTML', reply_markup=k)

@bot.message_handler(func=lambda message: message.text == "💎 PAID SIGNAL")
def paid_signal_handler(message):
    user_id = message.from_user.id
    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    data = cursor.fetchone()
    balance = data[0] if data else 0
    
    msg = f"""
💎 <b>PAID SIGNAL PACKAGES</b> 💎

💰 আপনার ব্যালেন্স: <b>{balance:.2f} টাকা</b>

━━━━━━━━━━━━━━━━━━━━━
🎯 <b>Rate:</b> প্রতি WIN = {PAID_SIGNAL_PER_WIN} টাকা

📦 <b>Packages:</b>
🥉 5 WIN = {5*PAID_SIGNAL_PER_WIN}৳
🥈 10 WIN = {10*PAID_SIGNAL_PER_WIN}৳
🥇 20 WIN = {20*PAID_SIGNAL_PER_WIN}৳
💎 50 WIN = {50*PAID_SIGNAL_PER_WIN}৳
━━━━━━━━━━━━━━━━━━━━━
"""
    k = telebot.types.InlineKeyboardMarkup(row_width=1)
    k.add(
        telebot.types.InlineKeyboardButton(f"🥉 5 WIN = {5*PAID_SIGNAL_PER_WIN}৳", callback_data="pkg_paid_5"),
        telebot.types.InlineKeyboardButton(f"🥈 10 WIN = {10*PAID_SIGNAL_PER_WIN}৳", callback_data="pkg_paid_10"),
        telebot.types.InlineKeyboardButton(f"🥇 20 WIN = {20*PAID_SIGNAL_PER_WIN}৳", callback_data="pkg_paid_20"),
        telebot.types.InlineKeyboardButton(f"💎 50 WIN = {50*PAID_SIGNAL_PER_WIN}৳", callback_data="pkg_paid_50"),
        telebot.types.InlineKeyboardButton("🎯 Custom Order", callback_data="pkg_paid_custom")
    )
    bot.reply_to(message, msg, parse_mode='HTML', reply_markup=k)

@bot.message_handler(func=lambda message: message.text == "💵 NUMBER SHOT")
def number_shot_handler(message):
    user_id = message.from_user.id
    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    data = cursor.fetchone()
    balance = data[0] if data else 0
    
    cost = 5 * NUMBER_SHOT_PER_WIN
    
    msg = f"""
💵 <b>NUMBER SHOT</b>

💰 আপনার ব্যালেন্স: <b>{balance:.2f} টাকা</b>

━━━━━━━━━━━━━━━━━━━━━
🎯 <b>Rate:</b> প্রতি WIN = {NUMBER_SHOT_PER_WIN} টাকা
📦 <b>Package:</b> 5 WIN = {cost} টাকা

🎲 BIG/SMALL + Number Match Game
✅ BIG/SMALL সঠিক হলে WIN
🎉 Number ও মিললে JACKPOT
❌ নাহলে LOSS
🏆 5 WIN হলে Session End
━━━━━━━━━━━━━━━━━━━━━
"""
    k = telebot.types.InlineKeyboardMarkup(row_width=1)
    k.add(telebot.types.InlineKeyboardButton(f"💵 5 WIN = {cost}৳", callback_data="pkg_ns_5"))
    bot.reply_to(message, msg, parse_mode='HTML', reply_markup=k)

@bot.message_handler(func=lambda message: message.text == "🟢 JOIN NX COMMUNITY")
def join_community_handler(message):
    k = telebot.types.InlineKeyboardMarkup(row_width=1)
    k.add(telebot.types.InlineKeyboardButton("🟢 𝗝𝗢𝗜𝗡 𝗡𝗫 𝗧𝗗𝗥 𝗖𝗢𝗠𝗠𝗨𝗡𝗜𝗧𝗬", url="https://t.me/+XFpXmlGPjMI5N2U1"))
    bot.reply_to(message, "🟢 <b>JOIN NX COMMUNITY</b>\n\n👇 ক্লিক করুন:", parse_mode='HTML', reply_markup=k)

@bot.message_handler(func=lambda message: message.text == "📞 HELP AND SUPPORT")
def help_support_handler(message):
    k = telebot.types.InlineKeyboardMarkup(row_width=1)
    k.add(telebot.types.InlineKeyboardButton("📞 𝗢𝗪𝗡𝗘𝗥 𝗜𝗗", url=OWNER_LINK))
    bot.reply_to(message, "📞 <b>HELP AND SUPPORT</b>\n\nযেকোনো সমস্যায় যোগাযোগ করুন:", parse_mode='HTML', reply_markup=k)

@bot.message_handler(func=lambda message: message.text == "𝗥𝗘𝗙𝗙𝗘𝗥 𝗔𝗡𝗗 𝗘𝗔𝗥𝗡")
def refer_and_earn_handler(message):
    user_id = message.from_user.id
    
    cursor.execute("SELECT total_referrals, balance, is_verified FROM users WHERE user_id = ?", (user_id,))
    data = cursor.fetchone()
    
    if data:
        total_ref = data[0] if data[0] else 0
        balance = data[1] if data[1] else 0
        is_verified = data[2] if data[2] else 0
    else:
        total_ref = 0
        balance = 0
        is_verified = 0
    
    bot_username = bot.get_me().username
    user_ref_link = f"https://t.me/{bot_username}?start=ref_{user_id}"
    
    if is_verified == 0:
        msg = f"""
🎁 <b>𝗥𝗘𝗙𝗙𝗘𝗥 &amp; 𝗘𝗔𝗥𝗡</b> 🎁

⚠️ <b>আপনি এখনো ভেরিফাই করেননি!</b>

📌 আগে ৪টি চ্যানেলে জয়েন করে ভেরিফাই করুন।
তারপর রেফার করে টাকা ইনকাম করুন 💰
"""
        bot.reply_to(message, msg, parse_mode='HTML', reply_markup=get_verify_keyboard())
        return
    
    msg = f"""
🎁 <b>𝗥𝗘𝗙𝗙𝗘𝗥 &amp; 𝗘𝗔𝗥𝗡</b> 🎁

💰 <b>১টি সফল রেফার = ৪ টাকা</b>

━━━━━━━━━━━━━━━━━━━━━
📊 <b>আপনার স্ট্যাটাস:</b>
👥 সফল রেফার: <b>{total_ref}</b>
💰 বর্তমান ব্যালেন্স: <b>{balance:.2f} টাকা</b>
━━━━━━━━━━━━━━━━━━━━━

🔗 <b>আপনার রেফার লিংক:</b>
<code>{user_ref_link}</code>

📌 <b>নিয়ম:</b>
১. আপনার লিংক বন্ধুদের পাঠান
২. তারা বটে /start দিয়ে জয়েন করবে
৩. ৪টি চ্যানেলে জয়েন করে VERIFY করবে
৪. VERIFY সফল হলেই আপনার একাউন্টে ৪ টাকা যোগ হবে ✅
"""
    
    k = telebot.types.InlineKeyboardMarkup(row_width=1)
    k.add(telebot.types.InlineKeyboardButton(
        "📤 𝗦𝗛𝗔𝗥𝗘 𝗥𝗘𝗙𝗘𝗥 𝗟𝗜𝗡𝗞", 
        url=f"https://t.me/share/url?url={user_ref_link}&text=Join%20NX%20TDR%20Community"
    ))
    
    bot.reply_to(message, msg, parse_mode='HTML', reply_markup=k)

def process_paid_custom(message):
    try:
        user_id = message.from_user.id
        try:
            wins = int(message.text.strip())
        except:
            bot.reply_to(message, "❌ শুধু সংখ্যা লিখুন (যেমন: 5, 10, 20)")
            return
        
        if wins < 1:
            bot.reply_to(message, "❌ কমপক্ষে 1 WIN কিনতে হবে")
            return
        
        cost = wins * PAID_SIGNAL_PER_WIN
        cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
        data = cursor.fetchone()
        balance = data[0] if data else 0
        
        if balance < cost:
            bot.reply_to(message, f"❌ পর্যাপ্ত ব্যালেন্স নেই!\n💰 প্রয়োজন: {cost} টাকা\n📊 আপনার: {balance:.2f} টাকা")
            return
        
        cursor.execute("UPDATE users SET balance = balance - ? WHERE user_id = ?", (cost, user_id))
        conn.commit()
        
        bot.reply_to(message, f"✅ <b>Custom Order সফল!</b>\n\n🎯 Wins: {wins}\n💰 কাটা: {cost} টাকা\n📊 ব্যালেন্স: {balance - cost:.2f} টাকা", parse_mode='HTML')
        threading.Thread(target=paid_signal_engine, args=(user_id, wins), daemon=True).start()
    except Exception as e:
        print(f"❌ Custom paid amount error: {e}")

@bot.message_handler(commands=['invite'])
def invite_command(message):
    try:
        if message.from_user.id != OWNER_ID:
            bot.reply_to(message, "❌ Permission denied.")
            return
        
        full_text = message.text.replace('/invite', '', 1).strip()
        
        if not full_text:
            bot.reply_to(message, """
📌 <b>Invite System</b>

<b>ব্যবহার:</b>
<code>/invite @user1 @user2 7853834431 আপনার মেসেজ</code>

<b>উদাহরণ ১ (custom message):</b>
<code>/invite 7853834431 7961534351 আসসালামু আলাইকুম!</code>

<b>উদাহরণ ২ (default welcome message):</b>
<code>/invite @username</code>
""", parse_mode='HTML')
            return
        
        words = full_text.split()
        targets = []
        msg_words = []
        found_msg_start = False
        
        for word in words:
            if not found_msg_start:
                if word.startswith('@') or word.isdigit():
                    targets.append(word)
                else:
                    found_msg_start = True
                    msg_words.append(word)
            else:
                msg_words.append(word)
        
        if not targets:
            bot.reply_to(message, "❌ কোনো ইউজার আইডি বা ইউজারনেম পাওয়া যায়নি।")
            return
        
        custom_msg = " ".join(msg_words).strip()
        
        if not custom_msg:
            custom_msg = """💚✨ <b>𝗛𝗘𝗬 {name} ❮Ñ𝗫 𝗧𝗿𝗮𝗱𝗲𝗿❯🟢 মামা!</b> 🩷✨
💠 আমি <b>𝗡𝗫 𝗕𝗢𝗧</b> — আসসালামু আলাইকুম! 💠

🎉 <b>NX TDR COMMUNITY</b>-তে আপনাকে স্বাগতম!

⚠️ <b>বাংলাদেশের সেরা ট্রেডিং প্রজেক্ট</b> ⚠️
💠 আমাদের কমিউনিটিতে যা যা পাবেন ইনশাআল্লাহ 💠

◙•════════════════════•◙
🤖 <b>𝗔𝗨𝗧𝗢 𝗧𝗥𝗔𝗗𝗘𝗫</b> — নিজে নিজে DKWIN/HGNICE এ ট্রেড করবে
⏰ <b>𝟮𝟰 𝗛𝗢𝗨𝗥𝗦</b> — আনলিমিটেড সিগন্যাল বট (Under 5 Step)
📊 <b>𝗡𝗫 𝗥𝗘𝗔𝗟 𝗞𝗡𝗢𝗪𝗟𝗘𝗗𝗚𝗘</b> — ১০০% নিখুঁত ট্রেডিং স্ট্র্যাটেজি
◙•═════════════════════•◙

📚 Learn • Practice • Grow 🚀
🔥 <b>NO HACK</b> ❌ | <b>ONLY REAL KNOWLEDGE</b> ✅

👇 নিচের বাটনে ক্লিক করে কমিউনিটিতে জয়েন করুন 👇

👑 <b>WELCOME TO NX FAMILY</b> 💛
✨ <b>STAY WITH NX XHAWON</b> 📊💎"""

        bot.reply_to(message, f"📨 {len(targets)} জনকে মেসেজ পাঠানো হচ্ছে...")
        threading.Thread(target=custom_invite_worker, args=(message.chat.id, targets, custom_msg), daemon=True).start()
        
    except Exception as e:
        print(f"❌ Invite error: {e}")
        bot.reply_to(message, f"❌ Error: {e}")

def custom_invite_worker(chat_id, targets, custom_msg):
    try:
        BATCH_SIZE = 30
        BATCH_WAIT = 180
        USER_WAIT = 0.5
        total = len(targets)
        success = 0
        failed = 0
        failed_list = []
        start_time = time.time()

        for i, target in enumerate(targets):
            target = target.strip()
            if not target: continue
            try:
                if target.startswith('@'):
                    try:
                        user_chat = bot.get_chat(target)
                        user_id = user_chat.id
                        first_name = user_chat.first_name or "ভাই"
                        username = user_chat.username or target
                    except Exception as e:
                        failed += 1
                        failed_list.append(f"{target} (Not Found)")
                        continue
                else:
                    user_id = int(target)
                    try:
                        user_chat = bot.get_chat(user_id)
                        first_name = user_chat.first_name or "ভাই"
                        username = user_chat.username or "N/A"
                    except:
                        first_name = "ভাই"
                        username = "N/A"

                try:
                    cursor.execute("INSERT OR IGNORE INTO users (user_id, first_name, join_date) VALUES (?, ?, ?)",
                                   (user_id, first_name, get_bd_time().strftime('%Y-%m-%d %H:%M:%S')))
                    conn.commit()
                except: pass

                final_msg = custom_msg.replace("{name}", first_name)
                
                if "𝗡𝗫 𝗕𝗢𝗧" in final_msg and "WELCOME TO NX FAMILY" in final_msg:
                    k = telebot.types.InlineKeyboardMarkup(row_width=1)
                    k.add(telebot.types.InlineKeyboardButton("🟢 𝗝𝗢𝗜𝗡 𝗡𝗫 𝗧𝗥𝗗 𝗖𝗢𝗠𝗠𝗨𝗡𝗜𝗧𝗬", url="https://t.me/+XFpXmlGPjMI5N2U1"))
                    k.add(telebot.types.InlineKeyboardButton("🤖 𝗦𝗧𝗔𝗥𝗧 𝗕𝗢𝗧", url=f"https://t.me/{BOT_USERNAME}?start=welcome"))
                    bot.send_message(user_id, final_msg, parse_mode='HTML', reply_markup=k)
                else:
                    bot.send_message(user_id, final_msg, parse_mode='HTML')
                
                success += 1
                print(f"✅ [{i+1}/{total}] {first_name} (@{username})")
                time.sleep(USER_WAIT)

            except Exception as e:
                failed += 1
                error_msg = str(e)[:100]
                failed_list.append(f"{target} — {error_msg}")
                print(f"❌ [{i+1}/{total}] {target}: {error_msg}")

            if (i + 1) % 30 == 0 and (i + 1) < total:
                elapsed = int(time.time() - start_time)
                try:
                    bot.send_message(chat_id,
                        f"📊 <b>PROGRESS</b>\n\n✅ Sent: {i+1}/{total}\n🎯 Success: {success}\n❌ Failed: {failed}\n⏱️ {elapsed//60}m {elapsed%60}s",
                        parse_mode='HTML')
                except: pass

            if (i + 1) % BATCH_SIZE == 0 and (i + 1) < total:
                try:
                    bot.send_message(chat_id, f"⏸️ Batch {i+1}/{total} done. Waiting 3 min...")
                except: pass
                time.sleep(BATCH_WAIT)

        elapsed = int(time.time() - start_time)
        report = f"""
✅ <b>INVITE COMPLETE</b>

📊 <b>Total:</b> {total}
✅ <b>Success:</b> {success}
❌ <b>Failed:</b> {failed}
⏱️ <b>Time:</b> {elapsed//60}m {elapsed%60}s
"""
        if failed_list:
            report += f"\n\n❌ <b>Failed Details:</b>\n"
            for f in failed_list[:15]:
                report += f"• {f}\n"
        try:
            bot.send_message(chat_id, report, parse_mode='HTML')
        except: pass
    except Exception as e:
        print(f"❌ Batch worker error: {e}")

@bot.message_handler(commands=['addbalance'])
def add_balance_command(message):
    if message.from_user.id != OWNER_ID: return
    args = message.text.split()[1:]
    if len(args) < 2:
        bot.reply_to(message, "📌 `/addbalance [user_id] [amount]`", parse_mode='Markdown')
        return
    try:
        target_uid = int(args[0])
        amount = float(args[1])
        cursor.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, target_uid))
        conn.commit()
        bot.reply_to(message, f"✅ {target_uid} কে {amount} টাকা যোগ হয়েছে।")
        try:
            bot.send_message(target_uid, f"💰 আপনার অ্যাকাউন্টে {amount} টাকা যোগ করা হয়েছে।")
        except: pass
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {e}")

@bot.message_handler(commands=['users'])
def users_list_command(message):
    if message.from_user.id != OWNER_ID: return
    
    cursor.execute("SELECT COUNT(*) FROM users")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM users WHERE is_verified = 1")
    verified = cursor.fetchone()[0]
    
    cursor.execute("SELECT user_id, first_name FROM users ORDER BY join_date DESC")
    users = cursor.fetchall()
    
    if not users:
        bot.reply_to(message, "📭 এখনো কোনো user নেই।")
        return
    
    header = f"""📊 <b>NX XHAWON — USER LIST</b>

👥 <b>Total User:</b> {total}
✅ <b>Verified:</b> {verified}
⏳ <b>Unverified:</b> {total - verified}
📅 <b>Date:</b> {get_bd_time().strftime('%d-%m-%Y %H:%M')}
━━━━━━━━━━━━━━━━━━━━━

"""
    
    msg = header
    count = 0
    for u in users:
        count += 1
        msg += f"{count}. <b>{u[1] or 'N/A'}</b> — <code>{u[0]}</code>\n"
        
        if len(msg) > 3500:
            bot.send_message(message.chat.id, msg, parse_mode='HTML')
            msg = ""
    
    if msg.strip():
        bot.send_message(message.chat.id, msg, parse_mode='HTML')

@bot.message_handler(commands=['user'])
def user_list_simple_command(message):
    if message.from_user.id != OWNER_ID: 
        bot.reply_to(message, "❌ Permission denied.")
        return
    
    cursor.execute("SELECT user_id, first_name FROM users ORDER BY join_date DESC")
    users = cursor.fetchall()
    
    if not users:
        bot.reply_to(message, "📭 এখনো কোনো ইউজার নেই।")
        return
    
    header = f"""📋 <b>ALL USER LIST</b>

👥 <b>Total User:</b> {len(users)}
📅 <b>Date:</b> {get_bd_time().strftime('%d-%m-%Y %H:%M')}
━━━━━━━━━━━━━━━━━━━━━

"""
    
    msg = header
    count = 0
    for u in users:
        count += 1
        msg += f"{count}. <b>{u[1] or 'N/A'}</b> — <code>{u[0]}</code>\n"
        
        if len(msg) > 3500:
            bot.send_message(message.chat.id, msg, parse_mode='HTML')
            msg = ""
    
    if msg.strip():
        bot.send_message(message.chat.id, msg, parse_mode='HTML')

@bot.message_handler(commands=['broadcast'])
def broadcast_command(message):
    if message.from_user.id != OWNER_ID: return
    if not message.reply_to_message and len(message.text.split()) < 2:
        bot.reply_to(message, "📌 `/broadcast মেসেজ`", parse_mode='Markdown')
        return
    bmsg = message.reply_to_message if message.reply_to_message else message.text.replace('/broadcast', '', 1).strip()
    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()
    success = 0
    for u in users:
        try:
            if isinstance(bmsg, str):
                bot.send_message(u[0], bmsg, parse_mode='HTML')
            else:
                bot.copy_message(chat_id=u[0], from_chat_id=bmsg.chat.id, message_id=bmsg.message_id)
            success += 1
            time.sleep(0.05)
        except: pass
    bot.reply_to(message, f"✅ Sent to {success}/{len(users)} users.")

@bot.message_handler(commands=['testmorning'])
def test_morning(message):
    if message.from_user.id != OWNER_ID: return
    send_good_morning(); bot.reply_to(message, "✅ Morning sent!")

@bot.message_handler(commands=['testnight'])
def test_night(message):
    if message.from_user.id != OWNER_ID: return
    send_good_night(); bot.reply_to(message, "✅ Night sent!")

@bot.message_handler(commands=['testpromo'])
def test_promo(message):
    if message.from_user.id != OWNER_ID: return
    post_promo_now()
    bot.reply_to(message, "✅ Promo posted to public group!")

@bot.message_handler(commands=['test70report'])
def test_70report(message):
    if message.from_user.id != OWNER_ID: return
    test_channel = {
        "name": "NX DUAL MODE SIGNAL",
        "max_loss_streak": 4,
    }
    send_70win_report(
        test_channel,
        "04:09 PM",
        "05:44 PM",
        1,
        70,
        12
    )
    bot.reply_to(message, "✅ Test 70-win report sent!")

@bot.message_handler(commands=['testreact'])
def test_react_command(message):
    """Manual Test Reaction: /testreact 12345"""
    if message.from_user.id != OWNER_ID:
        return
    try:
        args = message.text.split()
        if len(args) < 2:
            bot.reply_to(message, "📌 ব্যবহার: `/testreact 12345`", parse_mode='Markdown')
            return
        msg_id = int(args[1])
        bot.reply_to(message, f"⏳ Testing Reaction on Message ID: {msg_id}...")
        threading.Thread(target=auto_boost_worker, args=(msg_id,), daemon=True).start()
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("  🤖 NX XHAWON — SYSTEM v25 (AUTO REACTION ALL POSTS)")
    print("=" * 60)
    for c in CHANNELS:
        print(f"  📢 {c['name']} | ID: {c['id']}")
    print("=" * 60)

    start_all_channel_engines()
    threading.Thread(target=schedule_daily_reset, daemon=True).start()
    threading.Thread(target=newsletter_scheduler, daemon=True).start()

    print("✅ All threads started")
    print("=" * 60)
    print("🔍 Channel Post Monitor: ACTIVE (Auto Reaction ALL POSTS)")
    print(f"📢 Monitoring: {PUBLIC_CHANNEL_ID}")
    print("=" * 60)

    try:
        bot.infinity_polling(
            allowed_updates=[
                "message",
                "edited_message",
                "channel_post",
                "edited_channel_post",
                "callback_query",
                "chat_join_request",
                "new_chat_members",
                "chat_member",
                "my_chat_member"
            ]
        )
    except Exception as e:
        print(f"❌ Bot Error: {e}")
        time.sleep(5)