# Koder Sakir Bey
# Copy Paster yer yok kaybol
# Kod bitiş tarihi 04.04.2022

import asyncio
import re

from pyrogram import Client
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioVideoPiped
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    HighQualityVideo,
    LowQualityVideo,
    MediumQualityVideo,
)
from youtubesearchpython import VideosSearch

from config import ASSISTANT_NAME, BOT_USERNAME, IMG_1, IMG_2
from driver.filters import command, other_filters
from driver.jennie import call_py, user
from driver.queues import QUEUE, add_to_queue


def ytsearch(query: str):
    try:
        search = VideosSearch(query, limit=1).result()
        data = search["result"][0]
        songname = data["title"]
        url = data["link"]
        duration = data["duration"]
        thumbnail = f"https://i.ytimg.com/vi/{data['id']}/hqdefault.jpg"
        return [songname, url, duration, thumbnail]
    except Exception as e:
        print(e)
        return 0


async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        "best[height<=?720][width<=?1280]",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()


@Client.on_message(command(["vplay", f"voynat@{BOT_USERNAME}"]) & other_filters)
async def vplay(c: Client, m: Message):
    await m.delete()
    replied = m.reply_to_message
    chat_id = m.chat.id
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="• Mᴇɴᴜ", callback_data="cbmenu"),
                InlineKeyboardButton(
                    text="• Group", url=f"https://t.me/botsohbetdestek"
                ),
            ]
        ]
    )
    if m.sender_chat:
        return await m.reply_text(
            "__Anonim__ bir Yöneticisiniz!\n\n» yönetici haklarından kullanıcı hesabına geri dönün."
        )
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await m.reply_text(
            f"💡 Beni kullanmak için aşağıdaki **izinlere** sahip bir **Yönetici** olmam gerekiyor:\n\n» ❌ __Mesajları sil__\n» ❌ __Kullanıcı ekle__\n» ❌ __Görüntülü sohbeti yönet__\n\nVeri **güncellendi**, siz **beni terfi ettirdikten sonra** otomatik olarak"
        )
        return
    if not a.can_manage_voice_chats:
        await m.reply_text(
            "gerekli izin eksik:" + "\n\n» ❌ __Görüntülü sohbeti yönet__"
        )
        return
    if not a.can_delete_messages:
        await m.reply_text("gerekli izin eksik:" + "\n\n» ❌ __Mesajları sil__")
        return
    if not a.can_invite_users:
        await m.reply_text("gerekli izin eksik:" + "\n\n» ❌ __Kullanıcı ekle__")
        return
    try:
        ubot = (await user.get_me()).id
        b = await c.get_chat_member(chat_id, ubot)
        if b.status == "kicked":
            await m.reply_text(
                f"@{ASSISTANT_NAME} **grupta yasaklandı** {m.chat.title}\n\n» **Bu botu kullanmak istiyorsanız önce userbotun banını kaldırın.**"
            )
            return
    except UserNotParticipant:
        if m.chat.username:
            try:
                await user.join_chat(m.chat.username)
            except Exception as e:
                await m.reply_text(f"❌ **userbot **\n\n**nedeni katılamadı**: `{e}`")
                return
        else:
            try:
                invitelink = await c.export_chat_invite_link(m.chat.id)
                if invitelink.startswith("https://t.me/+"):
                    invitelink = invitelink.replace(
                        "https://t.me/+", "https://t.me/joinchat/"
                    )
                await user.join_chat(invitelink)
            except UserAlreadyParticipant:
                pass
            except Exception as e:
                return await m.reply_text(
                    f"❌ **userbot **\n\n**nedeni katılamadı**: `{e}`"
                )

    if replied:
        if replied.video or replied.document:
            loser = await replied.reply("📥 **Vide İndiriliyor...**")
            dl = await replied.download()
            link = replied.link
            if len(m.command) < 2:
                Q = 720
            else:
                pq = m.text.split(None, 1)[1]
                if pq == "720" or "480" or "360":
                    Q = int(pq)
                else:
                    Q = 720
                    await loser.edit(
                        "» __only 720, 480, 360 allowed__ \n💡 **şimdi video akışı 720p**"
                    )
            try:
                if replied.video:
                    songname = replied.video.file_name[:70]
                elif replied.document:
                    songname = replied.document.file_name[:70]
            except BaseException:
                songname = "Video"

            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await loser.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                await m.reply_photo(
                    photo=f"{IMG_1}",
                    caption=f"💡 **Parça sıraya eklendi »** `{pos}`\n\n🏷 **İsim:** [{songname}]({link}) | `video`\n💭 **Sohbet:** `{chat_id}`\n🎧 **Request by:** {requester}",
                    reply_markup=keyboard,
                )
            else:
                if Q == 720:
                    amaze = HighQualityVideo()
                elif Q == 480:
                    amaze = MediumQualityVideo()
                elif Q == 360:
                    amaze = LowQualityVideo()
                await loser.edit("🔄 **vc'ye katıl...**")
                await call_py.join_group_call(
                    chat_id,
                    AudioVideoPiped(
                        dl,
                        HighQualityAudio(),
                        amaze,
                    ),
                    stream_type=StreamType().local_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await loser.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                await m.reply_photo(
                    photo=f"{IMG_2}",
                    caption=f"🏷 **İsim:** [{songname}]({link})\n💭 **Chat:** `{chat_id}`\n💡 **durum:** `Playing`\n🎧 **talep eden:** {requester}\n📹 **şarkı türü:** `Video`",
                    reply_markup=keyboard,
                )
        else:
            if len(m.command) < 2:
                await m.reply(
                    "» bir **video dosyasına** yanıt verin veya **arayacak bir şey verin.**"
                )
            else:
                loser = await c.send_message(chat_id, "🔍 **Arıyor...**")
                query = m.text.split(None, 1)[1]
                search = ytsearch(query)
                Q = 720
                amaze = HighQualityVideo()
                if search == 0:
                    await loser.edit("❌ **Sonuç bulunamadı.**")
                else:
                    songname = search[0]
                    url = search[1]
                    duration = search[2]
                    thumbnail = search[3]
                    jennie, ytlink = await ytdl(url)
                    if jennie == 0:
                        await loser.edit(f"❌ yt-dl issues detected\n\n» `{ytlink}`")
                    else:
                        if chat_id in QUEUE:
                            pos = add_to_queue(
                                chat_id, songname, ytlink, url, "Video", Q
                            )
                            await loser.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            await m.reply_photo(
                                photo=thumbnail,
                                caption=f"💡 **Parça sıraya eklendi »** `{pos}`\n\n🏷 **isim:** [{songname}]({url}) | `video`\n⏱ **süre:** `{duration}`\n🎧 **talep eden:** {requester}",
                                reply_markup=keyboard,
                            )
                        else:
                            try:
                                await loser.edit("🔄 ** vc'ye Katıl...**")
                                await call_py.join_group_call(
                                    chat_id,
                                    AudioVideoPiped(
                                        ytlink,
                                        HighQualityAudio(),
                                        amaze,
                                    ),
                                    stream_type=StreamType().local_stream,
                                )
                                add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                                await loser.delete()
                                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                                await m.reply_photo(
                                    photo=thumbnail,
                                    caption=f"🏷 **isim:** [{songname}]({url})\n⏱ **süre:** `{duration}`\n💡 **durum:** `Playing`\n🎧 **talep eden:** {requester}\n📹 **şarkı türü:** `Video`",
                                    reply_markup=keyboard,
                                )
                            except Exception as ep:
                                await loser.delete()
                                await m.reply_text(f"🚫 error: `{ep}`")

    else:
        if len(m.command) < 2:
            await m.reply(
                "» bir **video dosyasına** yanıt verin veya **arayacak bir şey verin.**"
            )
        else:
            loser = await c.send_message(chat_id, "🔍 **Arıyor...**")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            Q = 720
            amaze = HighQualityVideo()
            if search == 0:
                await loser.edit("❌ **Sonuç bulunamadı.**")
            else:
                songname = search[0]
                url = search[1]
                duration = search[2]
                thumbnail = search[3]
                veez, ytlink = await ytdl(url)
                if veez == 0:
                    await loser.edit(f"❌ yt-dl issues detected\n\n» `{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                        await loser.delete()
                        requester = (
                            f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                        )
                        await m.reply_photo(
                            photo=thumbnail,
                            caption=f"💡 **Parça sıraya eklendi »** `{pos}`\n\n🏷 **isim:** [{songname}]({url}) | `video`\n⏱ **süre:** `{duration}`\n🎧 **talep eden:** {requester}",
                            reply_markup=keyboard,
                        )
                    else:
                        try:
                            await loser.edit("🔄 **oynatılıyor...**")
                            await call_py.join_group_call(
                                chat_id,
                                AudioVideoPiped(
                                    ytlink,
                                    HighQualityAudio(),
                                    amaze,
                                ),
                                stream_type=StreamType().local_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                            await loser.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            await m.reply_photo(
                                photo=thumbnail,
                                caption=f"🏷 **isim:** [{songname}]({url})\n⏱ **süre:** `{duration}`\n💡 **Durum:** `Playing`\n🎧 **talep eden:** {requester}\n📹 **şarkı türü:** `Video`",
                                reply_markup=keyboard,
                            )
                        except Exception as ep:
                            await loser.delete()
                            await m.reply_text(f"🚫 error: `{ep}`")


@Client.on_message(command(["canli", f"vstream@{BOT_USERNAME}"]) & other_filters)
async def vstream(c: Client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="• Mᴇɴᴜ", callback_data="cbmenu"),
                InlineKeyboardButton(text="• Cʟᴏsᴇ", callback_data="cls"),
            ]
        ]
    )
    if m.sender_chat:
        return await m.reply_text(
            "you're an __Anonymous__ Admin !\n\n» kendi hesabınıza geri dönün."
        )
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await m.reply_text(
            f"💡 Beni kullanmak için aşağıdaki **izinlere** sahip bir **Yönetici** olmam gerekiyor:\n\n» ❌ __Mesajları sil__\n» ❌ __Kullanıcı ekle__\n» ❌ __Görüntülü sohbeti yönet__\n\nVeri * *güncellendi**, siz **beni terfi ettirdikten sonra** otomatik olarak"
        )
        return
    if not a.can_manage_voice_chats:
        await m.reply_text(
            "gerekli izin eksik:" + "\n\n» ❌ __Görüntülü sohbeti yönet__"
        )
        return
    if not a.can_delete_messages:
        await m.reply_text("gerekli izin eksik:" + "\n\n» ❌ __Mesajları sil__")
        return
    if not a.can_invite_users:
        await m.reply_text("gerekli izin eksik:" + "\n\n» ❌ __Kullanıcı ekle__")
        return
    try:
        ubot = (await user.get_me()).id
        b = await c.get_chat_member(chat_id, ubot)
        if b.status == "kicked":
            await m.reply_text(
                f"@{ASSISTANT_NAME} **grupta yasaklandı** {m.chat.title}\n\n» **Bu botu kullanmak istiyorsanız önce userbotun banını kaldırın.**"
            )
            return
    except UserNotParticipant:
        if m.chat.username:
            try:
                await user.join_chat(m.chat.username)
            except Exception as e:
                await m.reply_text(f"❌ **userbot **\n\n**nedeni katılamadı**: `{e}`")
                return
        else:
            try:
                invitelink = await c.export_chat_invite_link(m.chat.id)
                if invitelink.startswith("https://t.me/+"):
                    invitelink = invitelink.replace(
                        "https://t.me/+", "https://t.me/joinchat/"
                    )
                await user.join_chat(invitelink)
            except UserAlreadyParticipant:
                pass
            except Exception as e:
                return await m.reply_text(
                    f"❌ **userbot **\n\n**nedeni katılamadı**: `{e}`"
                )

    if len(m.command) < 2:
        await m.reply("» give me a live-link/m3u8 url/youtube link to stream.")
    else:
        if len(m.command) == 2:
            link = m.text.split(None, 1)[1]
            Q = 720
            loser = await c.send_message(chat_id, "🔄 **aktarılıyor...**")
        elif len(m.command) == 3:
            op = m.text.split(None, 1)[1]
            link = op.split(None, 1)[0]
            quality = op.split(None, 1)[1]
            if quality == "720" or "480" or "360":
                Q = int(quality)
            else:
                Q = 720
                await m.reply(
                    "» __only 720, 480, 360 allowed__ \n💡 **şimdi video akışı 720p**"
                )
            loser = await c.send_message(chat_id, "🔄 **işleme akışı...**")
        else:
            await m.reply("**/vstream {link} {720/480/360}**")

        regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
        match = re.match(regex, link)
        if match:
            veez, livelink = await ytdl(link)
        else:
            livelink = link
            veez = 1

        if veez == 0:
            await loser.edit(f"❌ yt-dl issues detected\n\n» `{livelink}`")
        else:
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, "Live Stream", livelink, link, "Video", Q)
                await loser.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                await m.reply_photo(
                    photo=f"{IMG_1}",
                    caption=f"💡 **Parça sıraya eklendi»** `{pos}`\n\n💭 **Chat:** `{chat_id}`\n🎧 **talep eden:** {requester}",
                    reply_markup=keyboard,
                )
            else:
                if Q == 720:
                    amaze = HighQualityVideo()
                elif Q == 480:
                    amaze = MediumQualityVideo()
                elif Q == 360:
                    amaze = LowQualityVideo()
                try:
                    await loser.edit("🔄 **katılıyorum...**")
                    await call_py.join_group_call(
                        chat_id,
                        AudioVideoPiped(
                            livelink,
                            HighQualityAudio(),
                            amaze,
                        ),
                        stream_type=StreamType().live_stream,
                    )
                    add_to_queue(chat_id, "Live Stream", livelink, link, "Video", Q)
                    await loser.delete()
                    requester = (
                        f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                    )
                    await m.reply_photo(
                        photo=f"{IMG_2}",
                        caption=f"💡 **[Video canlıe]({link}) akışı başladı.**\n\n💭 **Chat:** `{chat_id}`\n💡 **durum:** `Playing`\n🎧 **talep eden:** {requester}",
                        reply_markup=keyboard,
                    )
                except Exception as ep:
                    await loser.delete()
                    await m.reply_text(f"🚫 error: `{ep}`")
