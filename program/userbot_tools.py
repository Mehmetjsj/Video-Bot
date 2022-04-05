import asyncio

from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant
from pyrogram.types import Message

from config import BOT_USERNAME, SUDO_USERS
from driver.decorators import authorized_users_only, sudo_users_only
from driver.filters import command
from driver.jennie import user


@Client.on_message(
    command(["katıl", f"userbotjoin@{BOT_USERNAME}"]) & ~filters.private & ~filters.bot
)
@authorized_users_only
async def join_chat(c: Client, m: Message):
    chat_id = m.chat.id
    try:
        invite_link = await m.chat.export_invite_link()
        if "+" in invite_link:
            link_hash = (invite_link.replace("+", "")).split("t.me/")[1]
            await user.join_chat(f"https://t.me/joinchat/{link_hash}")
        await m.chat.promote_member(
            (await user.get_me()).id, can_manage_voice_chats=True
        )
        return await user.send_message(chat_id, "✅ Senin isteğin üzerine geldim")
    except UserAlreadyParticipant:
        admin = await m.chat.get_member((await user.get_me()).id)
        if not admin.can_manage_voice_chats:
            await m.chat.promote_member(
                (await user.get_me()).id, can_manage_voice_chats=True
            )
            return await user.send_message(chat_id, "✅ Asistan zaten sohbette")
        return await user.send_message(chat_id, "✅ Asistan zaten sohbette")


@Client.on_message(
    command(["ayril", f"ayril@{BOT_USERNAME}"]) & filters.group & ~filters.edited
)
@authorized_users_only
async def leave_chat(_, m: Message):
    chat_id = m.chat.id
    try:
        await user.leave_chat(chat_id)
        return await _.send_message(
            chat_id,
            "✅ Asistan ayrıldı",
        )
    except UserNotParticipant:
        return await _.send_message(
            chat_id,
            "❌ Asistan sohbetten ayrıldı",
        )


@Client.on_message(command(["birak", f"birak@{BOT_USERNAME}"]))
@sudo_users_only
async def leave_all(client, message):
    if message.from_user.id not in SUDO_USERS:
        return

    left = 0
    failed = 0
    lol = await message.reply("🔄 **aaistan** tüm sohbetlerden ayrılıyor !")
    async for dialog in user.iter_dialogs():
        try:
            await user.leave_chat(dialog.chat.id)
            left += 1
            await lol.edit(
                f"asistan tüm sohbetlerden ayrılıyor...\n\nLeft: {left} chats.\nFailed: {failed} chats."
            )
        except BaseException:
            failed += 1
            await lol.edit(
                f"asistan ayrılıyor...\n\nLeft: {left} chats.\nFailed: {failed} chats."
            )
        await asyncio.sleep(0.7)
    await client.send_message(
        message.chat.id, f"✅ gelen{left} chats.\n❌ Failed in: {failed} chats."
    )


@Client.on_message(filters.left_chat_member)
async def ubot_leave(c: Client, m: Message):
    ass_id = (await user.get_me()).id
    bot_id = (await c.get_me()).id
    chat_id = m.chat.id
    left_member = m.left_chat_member
    if left_member.id == bot_id:
        await user.leave_chat(chat_id)
    elif left_member.id == ass_id:
        await c.leave_chat(chat_id)
