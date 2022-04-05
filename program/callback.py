from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from config import (
    ASSISTANT_NAME,
    BOT_NAME,
    BOT_USERNAME,
    GROUP_SUPPORT,
    OWNER_NAME,
    UPDATES_CHANNEL,
)
from driver.queues import QUEUE


@Client.on_callback_query(filters.regex("cbstart"))
async def cbstart(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""✨ **Merhaba {query.from_user.mention} !**\n
💭 **[{BOT_NAME}](https://t.me/{BOT_USERNAME}) Botu sesli sohbetlerde canlı yayın video ve müzik akışını sağlar  !**
❂ **Detaylı bilgi ve tüm komutlar için komutlar butonuna tıklayın !**
❂ **Botun temel komutları için temel komutlar butonuna tıklayın !**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕ Gruba Ekle ➕",
                        url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "❓ Basit komutlar ", callback_data="cbhowtouse"
                    ),
                ],
                [
                    InlineKeyboardButton("🧐 komutlar", callback_data="cbcmds"),
                    InlineKeyboardButton("❤ sahip", url=f"https://t.me/{OWNER_NAME}"),
                ],
                [
                    InlineKeyboardButton(
                        "👥 Destek Grup", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "📣 Kanal destek", url=f"https://t.me/{UPDATES_CHANNEL}"
                    ),
                ],
                [
                    InlineKeyboardButton("🌐 Sohbet grubu", url="https://t.me/gycyolcu"),
                ],
            ]
        ),
        disable_web_page_preview=True,
    )


@Client.on_callback_query(filters.regex("cbhowtouse"))
async def cbguides(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""❓ **Başlangıç aşağıdaki adımları uygulayın:**
1.) **başlangıç beni gruba ekle.**
2.) **bana yetki verin aonim yetkisi vermeyin.**
3.) **Ardından /reload komutu ile admin listesini yenileyin .**
3.) **grubunuza @{ASSISTANT_NAME} ekleyin veya /oynat komutuyla davet edin.**
4.) **botu başlatmadan önce sesli sohbeti açın .**
5.) **Bazen /reload komutunu kullanarak botu daha sağlıklı bir hale getirebilirsiniz .**
📌 **bot sesli sohbete katılmadıysa sesli sohbetin açık olup olmadığını kontrol edin veya /ayril yapıp tekrar /oynat yapın .**
💡 **çözüm ve önerileriniz için iletişime geçebilirsiniz : @{GROUP_SUPPORT}**
⚡ __keyifli dinlemeler 🙋‍♂️_""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🔙 geri git", callback_data="cbstart"),
                ],
            ],
        ),
    )


@Client.on_callback_query(filters.regex("cbcmds"))
async def cbcmds(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""✨ **Merhaba [{query.message.chat.first_name}](tg://user?id={query.message.chat.id}) !**
» **aşağıdaki butonları kullanarak mevcut komutları görebilirsiniz !**
⚡ __Daha fazla bilgi için @botsohbetdestek__"",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("👷🏻 Admin komut", callback_data="cbadmin"),
                    InlineKeyboardButton("🧙🏻 geliştirci", callback_data="cbsudo"),
                ],
                [
                    InlineKeyboardButton("📚 basit komutlar", callback_data="cbbasic"),
                ],
                [
                    InlineKeyboardButton("🔙 geri dön", callback_data="cbstart"),
                ],
            ]
        ),
    )

@Client.on_callback_query(filters.regex("cbbasic"))
async def cbbasic(_, query: CallbackQuery):
    await query.edit_message_text(
       f"""🏮 Basit komutlar listesi: \n\n» /oynat istediğiniz şarkıyı direk bulup oynatır \n» /voynat isteidğin videoyu direk bulup oynatır \n» /atla sıradaki şarkıya geçer \n» /video videoyu bulup indirir \n» /indir müziği bulup indirir \n» /devam duraklatığınız şarkıyı devam ettirir \n» /durdur akışı durdurur \n» /bitir akışı bitirip sesli sohbetten ayrılır \n» /canlı canlı yayın akışını sağlar \n\n⚡️ Daha fazla bilgi icin @botsohbetdestek""",

        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🔙 Geri Git", callback_data="cbcmds"),
                ],
            ],
        ),
    )


@Client.on_callback_query(filters.regex("cbadmin"))
async def cbadmin(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""🏮 admin komutu:
» /durdur - akışı durdurur 
» /devam - akışa devam eder 
» /atla - sıradaki parçaya geçer
» /son - sonlandırır
» /kapat - asistanın sesini kapatır 
» /ac - asistanın sesini açar 
» /canlı canlı yayın akışını sağlar

⚡️ __Daha fazla bilgi için @botsohbetdestek__""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🔙 Geri Git", callback_data="cbcmds"),
                ],
            ],
        ),
    )


@Client.on_callback_query(filters.regex("cbsudo"))
async def cbsudo(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""🏮 geliştirci komutları:
» bu komutlar sadece geliştirciye aittir bilgi ve destek @botsohbetdestek
⚡ __keyifli dinlemeler 🙋‍♂️__""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🔙 Geri git", callback_data="cbcmds"),
                ],
            ],
        ),
    )


@Client.on_callback_query(filters.regex("cbmenu"))
async def cbmenu(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer(
            "Bir Anonim Yöneticisiniz !\n\n» Anonim kullanıcılara hizmet edilmeyecek şekilde tasarlandım üzgünüm ."
        )
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 Sadece adminler !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        await query.edit_message_text(
            f"⚙️ **ayarlar kapat** {query.message.chat.title}\n\n⏸ : durdur\n▶️ : devam et\n🔇 : sesize al\n🔊 : sesi ac asistan\n⏹ : Bitir",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("⏹", callback_data="cbstop"),
                        InlineKeyboardButton("⏸", callback_data="cbpause"),
                        InlineKeyboardButton("▶️", callback_data="cbresume"),
                    ],
                    [
                        InlineKeyboardButton("🔇", callback_data="cbmute"),
                        InlineKeyboardButton("🔊", callback_data="cbunmute"),
                    ],
                    [
                        InlineKeyboardButton("🗑 mkapat", callback_data="cls"),
                    ],
                ]
            ),
        )
    else:
        await query.answer("❌ **Zaten bir şey oynatılmıyor**", show_alert=True)


@Client.on_callback_query(filters.regex("cls"))
async def close(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 Sadece adminler !", show_alert=True)
    await query.message.delete()
