# Copyright (C) 2021 By Rishabh Music-Project
# Commit Start Date 1/11/2021
# Finished On 7/1/2022


from pyrogram import Client
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped
from youtubesearchpython import VideosSearch

from config import ASSISTANT_NAME, BOT_USERNAME, IMG_1, IMG_2
from driver.filters import command, other_filters
from driver.jennie import call_py, user
from driver.queues import QUEUE, add_to_queue
from driver.utils import bash


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


async def ytdl(format: str, link: str):
    stdout, stderr = await bash(f'youtube-dl -g -f "{format}" {link}')
    if stdout:
        return 1, stdout.split("\n")[0]
    return 0, stderr


@Client.on_message(
    command(["oynat", f"play@{BOT_USERNAME}"]) & other_filters
)  # Developer SakirBey
async def play(c: Client, m: Message):
    await m.delete()
    replied = m.reply_to_message
    chat_id = m.chat.id
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="• Mᴇɴᴜ", callback_data="cbmenu"),
                InlineKeyboardButton(
                    text="• Grup", url=f"https://t.me/botsohbetdestek"
                ),
            ]
        ]
    )
    if m.sender_chat:
        return await m.reply_text(
            "Bir Anonim Yöneticisiniz !\n\n» Anonim kullanıcılara hizmet edilmeyecek şekilde tasarlandım üzgünüm."
        )
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        return await m.reply_text(
            f"💡 Beni kullanabilmeniz için yönetici olmam gerekiyor"
        )
    if not a.can_manage_voice_chats:
        await m.reply_text(
            "gerekli izin eksik:" + "\n\n» ❌ __Görüntülü sohbeti yönet__"
        )
        return
    if not a.can_delete_messages:
        await m.reply_text("Gerekli izin eksik:" + "\n\n» ❌ _mesajları silme_")
        return
    if not a.can_invite_users:
        await m.reply_text("Gerekli izin eksik:" + "\n\n» ❌ __Kullanıcı ekle_")
        return
    try:
        ubot = (await user.get_me()).id
        b = await c.get_chat_member(chat_id, ubot)
        if b.status == "kicked":
            await m.reply_text(
                f"@{ASSISTANT_NAME} **Bu grupta yasaklandı** {m.chat.title}\n\n» **botu kullanmak istiyorsanız asistan yasağını kaldırın.**"
            )
            return
    except UserNotParticipant:
        if m.chat.username:
            try:
                await user.join_chat(m.chat.username)
            except Exception as e:
                await m.reply_text(f"❌ **asistan katılamadı**\n\n**sebep**: `{e}`")
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
                    f"❌ **asistan katılamadı**\n\n**sebep**: `{e}`"
                )
    if replied:
        if replied.audio or replied.voice:
            suhu = await replied.reply("📥 **indiriliyor...**")
            dl = await replied.download()
            link = replied.link
            if replied.audio:
                if replied.audio.title:
                    songname = replied.audio.title[:70]
                else:
                    if replied.audio.file_name:
                        songname = replied.audio.file_name[:70]
                    else:
                        songname = "audio"
            elif replied.voice:
                songname = "Voice note"
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "audio", 0)
                await suhu.delete()
                await m.reply_photo(
                    photo=f"{IMG_1}",
                    caption=f"💡 **Sıraya Eklendi »** `{pos}`\n\n🏷 **isim:** [{songname}]({link}) | `music`\n💭 **Chat:** `{chat_id}`\n🎧 **isteyen:** {m.from_user.mention()}",
                    reply_markup=keyboard,
                )
            else:
                try:
                    await suhu.edit("🔄 **katılma vc...**")
                    await call_py.join_group_call(
                        chat_id,
                        AudioPiped(
                            dl,
                        ),
                        stream_type=StreamType().local_stream,
                    )
                    add_to_queue(chat_id, songname, dl, link, "audio", 0)
                    await suhu.delete()
                    requester = (
                        f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                    )
                    await m.reply_photo(
                        photo=f"{IMG_2}",
                        caption=f"🏷 **isim:** [{songname}]({link})\n💭 **Chat:** `{chat_id}`\n💡 **durum:** `oynatılıyor`\n🎧 **İsteyen:** {requester}\n📹 **şarkı türü:** `music`",
                        reply_markup=keyboard,
                    )
                except Exception as e:
                    await suhu.delete()
                    await m.reply_text(f"🚫 error:\n\n» {e}")
        else:
            if len(m.command) < 2:
                await m.reply(
                    "» bir **ses dosyasına yanıt verin** veya **arayacak bir şey verin.**"
                )
            else:
                suhu = await c.send_message(chat_id, "🔍 **aranıyor...**")
                query = m.text.split(None, 1)[1]
                search = ytsearch(query)
                if search == 0:
                    await suhu.edit("❌ Sonuç bulundu.**")
                else:
                    songname = search[0]
                    url = search[1]
                    duration = search[2]
                    thumbnail = search[3]
                    format = "bestaudio[ext=m4a]"
                    jennie, ytlink = await ytdl(format, url)
                    if jennie == 0:
                        await suhu.edit(f"❌ yt-dl issues detected\n\n» `{ytlink}`")
                    else:
                        if chat_id in QUEUE:
                            pos = add_to_queue(
                                chat_id, songname, ytlink, url, "Audio", 0
                            )
                            await suhu.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            await m.reply_photo(
                                photo=thumbnail,
                                caption=f"💡 **Sıraya eklendi »** `{pos}`\n\n🏷 **isim:** [{songname}]({url}) | `music`\n**⏱ süre:** `{duration}`\n🎧 **isteyen:** {requester}",
                                reply_markup=keyboard,
                            )
                        else:
                            try:
                                await suhu.edit("🔄 **birleştirme vc...**")
                                await call_py.join_group_call(
                                    chat_id,
                                    AudioPiped(
                                        ytlink,
                                    ),
                                    stream_type=StreamType().local_stream,
                                )
                                add_to_queue(chat_id, songname, ytlink, url, "audio", 0)
                                await suhu.delete()
                                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                                await m.reply_photo(
                                    photo=thumbnail,
                                    caption=f"🏷 **isim:** [{songname}]({url})\n**⏱ süre:** `{duration}`\n💡 **Durum:** `oynatılıyor`\n🎧 **isteyen:** {requester}\n📹 **şarkı türü:** `Music`",
                                    reply_markup=keyboard,
                                )
                            except Exception as ep:
                                await suhu.delete()
                                await m.reply_text(f"🚫 hatta: `{ep}`")

    else:
        if len(m.command) < 2:
            await m.reply(
                "» bir **ses dosyasına** yanıt verin veya **arayacak bir şey verin.**"
            )
        else:
            suhu = await c.send_message(chat_id, "🔍 **aranıyor...**")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            if search == 0:
                await suhu.edit("❌ **sonuç bulunamadı.**")
            else:
                songname = search[0]
                url = search[1]
                duration = search[2]
                thumbnail = search[3]
                format = "bestaudio[ext=m4a]"
                veez, ytlink = await ytdl(format, url)
                if veez == 0:
                    await suhu.edit(f"❌ sorun-dl algılandı\n\n» `{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "audio", 0)
                        await suhu.delete()
                        requester = (
                            f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                        )
                        await m.reply_photo(
                            photo=thumbnail,
                            caption=f"💡 **Sıraya eklendi »** `{pos}`\n\n🏷 **isim:** [{songname}]({url}) | `music`\n**⏱ ses:** `{duration}`\n🎧 **isteyen:** {requester}",
                            reply_markup=keyboard,
                        )
                    else:
                        try:
                            await suhu.edit("🔄 **katılma vc...**")
                            await call_py.join_group_call(
                                chat_id,
                                AudioPiped(
                                    ytlink,
                                ),
                                stream_type=StreamType().local_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "audio", 0)
                            await suhu.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            await m.reply_photo(
                                photo=thumbnail,
                                caption=f"🏷 **isim:** [{songname}]({url})\n**⏱ süre:** `{duration}`\n💡 **durum:** `oynatılıyor`\n🎧 **isteyen:** {requester}\n📹 **şarkı türü:** `Music`",
                                reply_markup=keyboard,
                            )
                        except Exception as ep:
                            await suhu.delete()
                            await m.reply_text(f"🚫 error: `{ep}`")
