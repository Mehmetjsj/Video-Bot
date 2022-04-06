from pyrogram import Client, filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from config import BOT_USERNAME, IMG_3
from driver.decorators import authorized_users_only
from driver.filters import command, other_filters
from driver.jennie import call_py
from driver.queues import QUEUE, clear_queue
from driver.utils import skip_current_song, skip_item

bttn = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Geri", callback_data="cbmenu")]])


bcl = InlineKeyboardMarkup([[InlineKeyboardButton("🗑 Mkapat", callback_data="cls")]])


@Client.on_message(command(["reload", f"reload@{BOT_USERNAME}"]) & other_filters)
@authorized_users_only
async def update_admin(client, message):
    global admins
    new_admins = []
    new_ads = await client.get_chat_members(message.chat.id, filter="administrators")
    for u in new_ads:
        new_admins.append(u.user.id)
    admins[message.chat.id] = new_admins
    await message.reply_text(
        f"✅ {R('bot_reload')}\n"
        f"✅ {R('admin_update')}"
    )


@Client.on_message(command(["atla", f"atla@{BOT_USERNAME}", "vatla"]) & other_filters)
@authorized_users_only
async def skip(client, m: Message):

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="• Mᴇɴᴜ", callback_data="cbmenu"),
                InlineKeyboardButton(text="• Geri", callback_data="cls"),
            ]
        ]
    )

    chat_id = m.chat.id
    if len(m.command) < 2:
        op = await skip_current_song(chat_id)
        if op == 0:
            await m.reply("❌ Şu anda bir şey oynatılmıyor")
        elif op == 1:
            await m.reply(
                "✅  __Sırada__ **şarkı yok.**\n\n**• userbot sesli sohbetten Ayrılıyor**"
            )
        elif op == 2:
            await m.reply(
                "🗑️ **sıraları temizleme**\n\n**• userbot sesli sohbetten ayrılıyor**"
            )
        else:
            await m.reply_photo(
                photo=f"{IMG_3}",
                caption=f"⏭ **sonraki parçaya atlandı.**\n\n🏷 **İsim:** [{op[0]}]({op[1]})\n💭 **Chat:** `{chat_id}`\n💡 **Durum:** `Oynuyor`\n🎧 **İsteyen:** {m.from_user.mention()}",
                reply_markup=keyboard,
            )
    else:
        skip = m.text.split(None, 1)[1]
        OP = "🗑 **Kuyruktan şarkı atlatıldı:**"
        if chat_id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x == 0:
                    pass
                else:
                    hm = await skip_item(chat_id, x)
                    if hm == 0:
                        pass
                    else:
                        OP = OP + "\n" + f"**#{x}** - {hm}"
            await m.reply(OP)


@Client.on_message(
    command(["bitir", f"bitir@{BOT_USERNAME}", "vbitir", f"son@{BOT_USERNAME}", "vson"])
    & other_filters
)
@authorized_users_only
async def stop(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await m.reply("✅ Asistan sesli sohbetten ayrıldı .")
        except Exception as e:
            await m.reply(f"🚫 **Hata:**\n\n`{e}`")
    else:
        await m.reply("❌ **Zaten şarkı çalınmıyor**")


@Client.on_message(
    command(["durdur", f"durdur@{BOT_USERNAME}", "vdurdur"]) & other_filters
)
@authorized_users_only
async def pause(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await m.reply(
                "⏸ **Durduruldu**\n\n• **Durdurduğunuz şarkıya Devam etmek için**\n» /devam komutunu kullanın ."
            )
        except Exception as e:
            await m.reply(f"🚫 **error:**\n\n`{e}`")
    else:
        await m.reply("❌ **Zaten şarkı çalınmıyor**")


@Client.on_message(
    command(["devam", f"devam@{BOT_USERNAME}", "vdevam"]) & other_filters
)
@authorized_users_only
async def resume(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await m.reply(
                "▶️ **Parça devam ettirildi.**\n\n• **Yayını duraklatmak için**\n» /durdur komutunu kullanın."
            )
        except Exception as e:
            await m.reply(f"🚫 **Hata:**\n\n`{e}`")
    else:
        await m.reply("❌ **Zaten şarkı çalınmıyor**")


@Client.on_message(
    command(["kapat", f"kapat@{BOT_USERNAME}", "vkapat"]) & other_filters
)
@authorized_users_only
async def mute(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.mute_stream(chat_id)
            await m.reply(
                "🔇 **Asistanın sesi kapatıldı.**\n\n• **Asistanın sesini açmak için**\n» /ac komutunu kullanın."
            )
        except Exception as e:
            await m.reply(f"🚫 **Hata:**\n\n`{e}`")
    else:
        await m.reply("❌ **Zaten şarkı çalınmıyor**")


@Client.on_message(command(["ac", f"ac@{BOT_USERNAME}", "vac"]) & other_filters)
@authorized_users_only
async def unmute(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.unmute_stream(chat_id)
            await m.reply(
                "🔊 **Asistanın sesi açıldı.**\n\n• **Asistanın sesini kapatmak için**\n» /kapat komutunu kullanın."
            )
        except Exception as e:
            await m.reply(f"🚫 **error:**\n\n`{e}`")
    else:
        await m.reply("❌ **Zaten bir şey oynatılmıyor**")


@Client.on_callback_query(filters.regex("cbpause"))
async def cbpause(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer(
            "Bir Anonim Yöneticisiniz !\n\n» Anonim kullanıcılara hizmet edilmeyecek şekilde tasarlandım üzgünüm."
        )
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 Sadece adminler !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await query.edit_message_text("⏸ Akış duraklatıldı", reply_markup=bttn)
        except Exception as e:
            await query.edit_message_text(f"🚫 **error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ Aktif bir yayın bulunamadı", show_alert=True)


@Client.on_callback_query(filters.regex("cbresume"))
async def cbresume(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer(
            "Bir Anonim Yöneticisiniz !\n\n» Anonim kullanıcılara hizmet edilmeyecek şekilde tasarlandım üzgünüm."
        )
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 Sadece adminler !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await query.edit_message_text("▶️ Akış devam etti", reply_markup=bttn)
        except Exception as e:
            await query.edit_message_text(f"🚫 **error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ Aktif bir yayın bulunamadı", show_alert=True)


@Client.on_callback_query(filters.regex("cbstop"))
async def cbstop(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer(
            "Bir Anonim Yöneticisiniz !\n\n» Anonim kullanıcılara hizmet edilmeyecek şekilde tasarlandım üzgünüm."
        )
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 Sadece adminler !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await query.edit_message_text("✅ **Akış sona erdi**", reply_markup=bcl)
        except Exception as e:
            await query.edit_message_text(f"🚫 **error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ Aktif bir yayın bulunamadı", show_alert=True)


@Client.on_callback_query(filters.regex("cbmute"))
async def cbmute(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer(
            "Bir Anonim Yöneticisiniz !\n\n» Anonim kullanıcılara hizmet edilmeyecek şekilde tasarlandım üzgünüm."
        )
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 Sadece adminler !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.mute_stream(chat_id)
            await query.edit_message_text(
                "🔇 Asistan Başarıyla sesize alındı", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"🚫 **error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ Aktif yayın bulunamadı", show_alert=True)


@Client.on_callback_query(filters.regex("cbunmute"))
async def cbunmute(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer(
            "Bir Anonim Yöneticisiniz !\n\n» Anonim kullanıcılara hizmet edilmeyecek şekilde tasarlandım üzgünüm."
        )
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 Sadece adminler !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.unmute_stream(chat_id)
            await query.edit_message_text(
                "🔊 Asistan Başarıyla açıldı", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"🚫 **Hata:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ Aktif yayın bulunamadı", show_alert=True)


@Client.on_message(command(["ayarla", f"ayarla@{BOT_USERNAME}", "aya"]) & other_filters)
@authorized_users_only
async def change_volume(client, m: Message):
    range = m.command[1]
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.change_volume_call(chat_id, volume=int(range))
            await m.reply(f"✅ **Ses ayarlandı {range}`%**")
        except Exception as e:
            await m.reply(f"🚫 **Hata:**\n\n`{e}`")
    else:
        await m.reply("❌ **Aktif yayın bulunamadı**")
