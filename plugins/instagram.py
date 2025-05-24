# plugins/instagram.py

import re
import urllib.parse
import requests
import logging

from telethon import events
from telethon.tl.types import InputMediaPhotoExternal

log = logging.getLogger(__name__)

CMD_DL   = ["igdl", "دانلود اینستاگرام"]
CMD_HELP = ["ighelp", "راهنمای اینستاگرام"]

API_URL = "https://api.mr-amiri.ir/api/instagram1.php"
API_KEY = "Khddgjkourfhkoigb"

HELP = """
📥 **دانلود اینستاگرام**

▪️ دانلود: `.igdl <لینک>` یا `.دانلود اینستاگرام <لینک>`
▪️ راهنما: `.ighelp` یا `.راهنمای اینستاگرام`
"""

def cmd_pattern(cmds):
    names = "|".join(re.escape(c) for c in cmds)
    return rf"^\.({names})(?:\s+(https?://\S+))?$"

def help_pattern(cmds):
    names = "|".join(re.escape(c) for c in cmds)
    return rf"^\.({names})$"

def register(client):
    session_admin = getattr(client, 'session_admin', None)
    if not session_admin:
        return

    async def fetch_instagram(url):
        try:
            encoded = urllib.parse.quote(url)
            params = {'key': API_KEY, 'type': 'download', 'url': encoded}
            res = requests.get(API_URL, params=params, timeout=10)
            return res.json() if res.ok else None
        except Exception as e:
            log.warning(f"Instagram fetch failed: {e}")
            return None

    async def send_album(event, urls, caption):
        try:
            media = [
                InputMediaPhotoExternal(url=u, caption=caption if i == 0 else None)
                for i, u in enumerate(urls[:10])
            ]
            await client.send_file(event.chat_id, media, reply_to=event.id)
        except Exception as e:
            log.error(f"Album send error: {e}")
            return False
        return True

    @client.on(events.NewMessage(pattern=cmd_pattern(CMD_DL)))
    async def handler(event):
        if event.sender_id != client.session_admin:
            return

        url = event.pattern_match.group(2)
        if not url or not url.startswith("https://www.instagram.com"):
            return await event.reply("❌ لطفاً لینک معتبر اینستاگرام وارد کنید.")

        msg = await event.reply("⏳ در حال پردازش...")
        result = await fetch_instagram(url)

        if not result or not result.get("ok"):
            return await msg.edit("❌ خطا در دریافت محتوا. لینک را بررسی کنید.")

        res = result["result"]
        cap = f"📥 محتوای دانلودی\n"
        if res.get("caption"): cap += f"📝 {res['caption']}\n"
        if res.get("likes"): cap += f"❤️ لایک: {res['likes']}  "
        if res.get("comments"): cap += f"💬 کامنت: {res['comments']}\n"

        try:
            if res.get("video"):
                await client.send_file(event.chat_id, res['video'], caption=cap, reply_to=event.id, supports_streaming=True)
            elif res.get("carousel"):
                ok = await send_album(event, res['carousel'], cap)
                if not ok:
                    await client.send_file(event.chat_id, res['carousel'][0], caption=cap, reply_to=event.id)
                    for u in res['carousel'][1:10]:
                        await client.send_file(event.chat_id, u, reply_to=event.id)
            elif res.get("images"):
                await client.send_file(event.chat_id, res['images'][0], caption=cap, reply_to=event.id)
            else:
                return await msg.edit("❌ نوع محتوای پشتیبانی‌نشده.")
        except Exception as e:
            log.warning(f"Send error: {e}")
            return await msg.edit("❌ خطا در ارسال. دوباره تلاش کنید.")

        await msg.delete()

    @client.on(events.NewMessage(pattern=help_pattern(CMD_HELP)))
    async def help_cmd(event):
        if event.sender_id != client.session_admin:
            return
        await event.reply(HELP)
