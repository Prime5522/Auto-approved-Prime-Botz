import asyncio
from pyrogram import Client, filters, enums
from config import LOG_CHANNEL, API_ID, API_HASH, NEW_REQ_MODE, AUTH_CHANNEL, ADMINS
from plugins.database import db
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery  # CallbackQuery এখানে ইম্পোর্ট করুন
from pyrogram.errors import InputUserDeactivated, UserNotParticipant, FloodWait, UserIsBlocked, PeerIdInvalid
import datetime
import time
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

LOG_TEXT = """<b>#NewUser Approved Bot

ID - <code>{}</code>

Name - {}</b> """

async def get_fsub(bot, message):
    target_channel_id = AUTH_CHANNEL  # Your channel ID
    user_id = message.from_user.id
    try:
        # Check if user is a member of the required channel
        await bot.get_chat_member(target_channel_id, user_id)
    except UserNotParticipant:
        # Generate the channel invite link
        channel_link = (await bot.get_chat(target_channel_id)).invite_link
        join_button = InlineKeyboardButton("✇ ᴊᴏɪɴ ᴏᴜʀ ᴜᴘᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ ✇", url=channel_link)
        try_again_button = InlineKeyboardButton("🔄 ᴛʀʏ ᴀɢᴀɪɴ", url="https://t.me/Auto_Approved_Prime_Bot?start=start")

        # Keyboard setup
        keyboard = [[join_button], [try_again_button]]

        # Send message with image ɪ ᴄᴀɴ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴀᴘᴘʀᴏᴠᴇ ɴᴇᴡ ᴀꜱ ᴡᴇʟʟ ᴀꜱ ᴘᴇɴᴅɪɴɢ ᴊᴏɪɴ ʀᴇQᴜᴇꜱᴛꜱ ɪɴ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟꜱ ᴏʀ ɢʀᴏᴜᴘꜱ.  ᴊᴜꜱᴛ ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟꜱ ᴀɴᴅ ɢʀᴏᴜᴘꜱ ᴡɪᴛʜ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ᴛᴏ ᴀᴅᴅ ɴᴇᴡ ᴍᴇᴍʙᴇʀꜱ
        await message.reply_photo(
            photo="https://i.postimg.cc/7Zpf9s1C/IMG-20250514-223544-954.jpg",
            caption=(
                "ɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴜꜱᴇ ᴍᴇ, ʏᴏᴜ ᴍᴜꜱᴛ ꜰɪʀꜱᴛ ᴊᴏɪɴ ᴏᴜʀ ᴜᴘᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ.\n\n"
                "ᴄʟɪᴄᴋ ᴏɴ **'✇ ᴊᴏɪɴ ᴏᴜʀ ᴜᴘᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ ✇'** ʙᴜᴛᴛᴏɴ.\n"
                "ᴛʜᴇɴ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ **'ʀᴇǫᴜᴇꜱᴛ ᴛᴏ ᴊᴏɪɴ'** ʙᴜᴛᴛᴏɴ.\n"
                "ᴀꜰᴛᴇʀ ᴊᴏɪɴɪɴɢ, ᴄʟɪᴄᴋ ᴏɴ **'🔄 ᴛʀʏ ᴀɢᴀɪɴ'** ʙᴜᴛᴛᴏɴ."
            ),
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return False
    else:
        return True

async def broadcast_messages(user_id, message):
    try:
        await message.copy(chat_id=user_id)
        return True, "Success"
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await broadcast_messages(user_id, message)
    except InputUserDeactivated:
        await db.delete_user(int(user_id))
        logging.info(f"{user_id}-Removed from Database, since deleted account.")
        return False, "Deleted"
    except UserIsBlocked:
        await db.delete_user(int(user_id))
        logging.info(f"{user_id} -Blocked the bot.")
        return False, "Blocked"
    except PeerIdInvalid:
        await db.delete_user(int(user_id))
        logging.info(f"{user_id} - PeerIdInvalid")
        return False, "Error"
    except Exception as e:
        return False, "Error"

@Client.on_message(filters.command('start'))
async def start_message(c, m):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id, m.from_user.first_name)
        await c.send_message(LOG_CHANNEL, LOG_TEXT.format(m.from_user.id, m.from_user.mention))

    is_subscribed = await get_fsub(c, m)
    if not is_subscribed:
        return

    await m.reply_photo(
        photo="https://i.postimg.cc/0j8Tsvvz/IMG-20250514-223240-290.jpg",  # এখানে আপনার ইমেজ লিংক দিন ɪ ᴄᴀɴ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴀᴘᴘʀᴏᴠᴇ ɴᴇᴡ ᴀꜱ ᴡᴇʟʟ ᴀꜱ ᴘᴇɴᴅɪɴɢ ᴊᴏɪɴ ʀᴇQᴜᴇꜱᴛꜱ ɪɴ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟꜱ ᴏʀ ɢʀᴏᴜᴘꜱ.  ᴊᴜꜱᴛ ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟꜱ ᴀɴᴅ ɢʀᴏᴜᴘꜱ ᴡɪᴛʜ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ᴛᴏ ᴀᴅᴅ ɴᴇᴡ ᴍᴇᴍʙᴇʀꜱ
        caption=(
            f"{m.from_user.mention},\n\n"
            "ɪ ᴀᴍ ꜱɪᴍᴘʟᴇ ʙᴜᴛ ᴀᴅᴠᴀɴᴄᴇ ᴀᴜᴛᴏ ᴀᴘᴘʀᴏᴠᴇᴅ ʙᴏᴛ.\n\n"
            "ɪ ᴄᴀɴ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴀᴘᴘʀᴏᴠᴇ ɴᴇᴡ ᴀꜱ ᴡᴇʟʟ ᴀꜱ ᴘᴇɴᴅɪɴɢ ᴊᴏɪɴ ʀᴇQᴜᴇꜱᴛꜱ ɪɴ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟꜱ ᴏʀ ɢʀᴏᴜᴘꜱ.\n\n"
            "ᴊᴜꜱᴛ ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟꜱ ᴀɴᴅ ɢʀᴏᴜᴘꜱ ᴡɪᴛʜ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ᴛᴏ ᴀᴅᴅ ɴᴇᴡ ᴍᴇᴍʙᴇʀs.\n\n"
            "**<blockquote> 🌿 ᴍᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ  <a href='https://t.me/Prime_Botz'>ᴘʀɪᴍᴇ ʙᴏᴛz 🔥</a></blockquote>**"
        ),
        reply_markup=InlineKeyboardMarkup(
            [[
                InlineKeyboardButton("⇆ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘs ⇆", url=f"https://telegram.me/Auto_Approved_Prime_Bot?startgroup=true&admin=invite_users"),
            ],[
                InlineKeyboardButton("• ᴍᴏᴠɪᴇꜱ ᴄʜᴀɴɴᴇʟ", url="https://telegram.me/PRIMECINEZONE"),
                InlineKeyboardButton("• ʜᴇʟᴘ •", callback_data="help_menu")
            ],[
                InlineKeyboardButton("• ᴜᴩᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ •", url="https://telegram.me/PrimeXBots"),
                InlineKeyboardButton("• ꜱᴜᴩᴩᴏʀᴛ ɢʀᴏᴜᴘ •", url="https://telegram.me/Prime_Support_Group")
            ],[
                InlineKeyboardButton("✧ 𝗖𝗥𝗘𝗔𝗧𝗢𝗥 ✧", url="https://t.me/Prime_Nayem")
            ],[
                InlineKeyboardButton("⇆ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ ⇆", url=f"https://telegram.me/Auto_Approved_Prime_Bot?startchannel=true&admin=invite_users")
            ]]
        )
    )

@Client.on_callback_query(filters.regex("help_menu"))
async def help_callback(c, query: CallbackQuery):
    await query.message.edit_text(
        f"{query.from_user.mention},\n\n"
        "𝖱𝖾𝖺𝖽 𝗍𝗁𝗂𝗌 𝗆𝖾𝗌𝗌𝖺𝗀𝖾 𝖼𝖺𝗋𝖾𝖿𝗎𝗅𝗹𝗒 𝗌𝗈 𝗒𝗈𝗎 𝖽𝗈𝗇'𝗍 𝗁𝖺𝗏𝖾 𝖺𝗇𝗒 𝗉𝗋𝗈𝖻𝗅𝖾𝗆𝗌 𝗐𝗁𝗂𝗅𝖾 𝗎𝗌𝗂𝗇𝗀 𝗆𝖾.\n\n"
        "📌 **𝟏. 𝐇𝐨𝐰 𝐭𝐨 𝐚𝐜𝐜𝐞𝐩𝐭 𝐧𝐞𝐰 𝐣𝐨𝐢𝐧 𝐫𝐞𝐪𝐮𝐞𝐬𝐭𝐬?**\n"
        "👉 𝖩𝗎𝗌𝗍 𝖺𝖽𝖽 𝗆𝖾 𝗂𝗇 𝗒𝗈𝗎𝗋 𝖼𝗁𝖺𝗇𝗇𝖾𝗅 𝗈𝗋 𝗀𝗋𝗈𝗎𝗉 𝖺𝗌 𝖺𝗂𝗆 𝖺𝗇𝖽 𝗐𝗂𝗍𝗁 𝗉𝖾𝗋𝗆𝗂𝗌𝗌𝗂𝗈𝗇 𝗍𝗈 𝖺𝖽𝖽 𝗇𝖾𝗐 𝗆𝖾𝗆𝖻𝖾𝗋𝗌.\n\n"
        "📌 **𝟐. 𝐇𝐨𝐰 𝐭𝐨 𝐚𝐜𝐜𝐞𝐩𝐭 𝐩𝐞𝐧𝐝𝐢𝐧𝐠 𝐣𝐨𝐢𝐧 𝐫𝐞𝐪𝐮𝐞𝐬𝐭𝐬?**\n"
        "👉 𝖥𝗂𝗋𝗌𝗍 𝖺𝖽𝖽 𝗆𝖾 𝖺𝗌 𝖺𝗂𝗆 𝗂𝗇 𝗒𝗈𝗎𝗋 𝖼𝗁𝖺𝗇𝗇𝖾𝗅 𝗈𝗋 𝗀𝗋𝗈𝗎𝗉 𝗐𝗂𝗍𝗁 𝗉𝖾𝗋𝗆𝗂𝗌𝗌𝗂𝗈𝗇 𝗍𝗈 𝖺𝖽𝖽 𝗇𝖾𝗐 𝗆𝖾𝗆𝖻𝖾𝗋𝗌.\n"
        "👉 𝖳𝗁𝖾𝗇 𝗅𝗈𝗀𝗂𝗇 𝗂𝗇𝗍𝗈 𝗍𝗁𝖾 𝖻𝗈𝗍 𝗆𝗒 𝗎𝗌𝗂𝗇𝗀 /login 𝖼𝗈𝗆𝗆𝖺𝗇𝖽.\n"
        "👉 𝖭𝗈𝗐 𝗎𝗌𝖾 /accept 𝖼𝗈𝗆𝗆𝖺𝗇𝖽 𝗍𝗈 𝖺𝖼𝖼𝗾𝖾𝗉𝗍 𝖺𝗅𝗅 𝗉𝖾𝗇𝖽𝗂𝗇𝗀 𝗋𝖾𝗊𝗎𝖾𝗌𝗍.\n\n"
        "**𝖨𝖿 𝗒𝗈𝗎 𝗌𝗍𝗂𝗅𝗅 𝖿𝖺𝖼𝖾 𝖺𝗇𝗒 𝗂𝗌𝗌𝗎𝖾, ᴊᴏɪɴ ᴏᴜʀ ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ 👇**",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("💬 ᴘʀɪᴍᴇ ʙᴏᴛᴢ ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ 💬", url="https://telegram.me/Prime_Support_Group")]])
    )
    
@Client.on_message(filters.command('help'))
async def help_message(c,m):
    await m.reply_text(f"{m.from_user.mention},\n\n𝖱𝖾𝖺𝖽 𝗍𝗁𝗂𝗌 𝗆𝖾𝗌𝗌𝖺𝗀𝖾 𝖼𝖺𝗋𝖾𝖿𝗎𝗅𝗅𝗒 𝗌𝗈 𝗒𝗈𝗎 𝖽𝗈𝗇'𝗍 𝗁𝖺𝗏𝖾 𝖺𝗇𝗒 𝗉𝗋𝗈𝖻𝗅𝖾𝗆𝗌 𝗐𝗁𝗂𝗅𝖾 𝗎𝗌𝗂𝗇𝗀 𝗆𝖾.\n\n𝟏. 𝐇𝐨𝐰 𝐭𝐨 𝐚𝐜𝐜𝐞𝐩𝐭 𝐧𝐞𝐰 𝐣𝐨𝐢𝐧 𝐫𝐞𝐪𝐮𝐞𝐬𝐭𝐬?\n\n👉 𝖩𝗎𝗌𝗍 𝖺𝖽𝖽 𝗆𝖾 𝗂𝗇 𝗒𝗈𝗎 𝖼𝗁𝖺𝗇𝗇𝖾𝗅 𝗈𝗋 𝗀𝗋𝗈𝗎𝗉 𝖺𝗌 𝖺𝖽𝗆𝗂𝗇 𝖺𝗇𝖽 𝗐𝗂𝗍𝗁 𝗉𝖾𝗋𝗆𝗂𝗌𝗌𝗂𝗈𝗇 𝗍𝗈 𝖺𝖽𝖽 𝗇𝖾𝗐 𝗆𝖾𝗆𝖻𝖾𝗋𝗌.\n\n𝟐. 𝐇𝐨𝐰 𝐭𝐨 𝐚𝐜𝐜𝐞𝐩𝐭 𝐩𝐞𝐧𝐝𝐢𝐧𝐠 𝐣𝐨𝐢𝐧 𝐫𝐞𝐪𝐮𝐞𝐬𝐭𝐬?\n\n👉 𝖥𝗂𝗋𝗌𝗍 𝖺𝖽𝖽 𝗆𝖾 𝖺𝗌 𝖺𝖽𝗆𝗂𝗇 𝗂𝗇 𝗒𝗈𝗎𝗋 𝖼𝗁𝖺𝗇𝗇𝖾𝗅 𝗈𝗋 𝗀𝗋𝗈𝗎𝗉 𝗐𝗂𝗍𝗁 𝗉𝖾𝗋𝗆𝗂𝗌𝗌𝗂𝗈𝗇 𝗍𝗈 𝖺𝖽𝖽 𝗇𝖾𝗐 𝗆𝖾𝗆𝖻𝖾𝗋𝗌.\n\n👉 𝖳𝗁𝖾𝗇 𝗅𝗈𝗀𝗂𝗇 𝗂𝗇𝗍𝗈 𝗍𝗁𝖾 𝖻𝗈𝗍 𝗆𝗒 𝗎𝗌𝗂𝗇𝗀 /login 𝖼𝗈𝗆𝗆𝖺𝗇𝖽.\n\n👉 𝖭𝗈𝗐 𝗎𝗌𝖾 /accept 𝖼𝗈𝗆𝗆𝖺𝗇𝖽 𝗍𝗈 𝖺𝖼𝖼𝖾𝗉𝗍 𝖺𝗅𝗅 𝗉𝖾𝗇𝖽𝗂𝗇𝗀 𝗋𝖾𝗊𝗎𝖾𝗌𝗍.\n\n👉 𝖭𝗈𝗐 𝗃𝗎𝗌𝗍 𝗎𝗌𝖾 /logout 𝖼𝗈𝗆𝗆𝖺𝗇𝖽 𝖿𝗈𝗋 𝗅𝗈𝗀𝗈𝗎𝗍.\n\n<b>𝖨𝖿 𝗒𝗈𝗎 𝗌𝗍𝗂𝗅𝗅 𝖿𝖺𝖼𝖾 𝖺𝗇𝗒 𝗂𝗌𝗌𝗎𝖾 𝗍𝗁𝖾𝗇 𝖼𝗈𝗇𝗍𝖺𝖼𝗍 @Prime_Support_Group</b>")

@Client.on_message(filters.command("users") & filters.user(ADMINS))
async def users(bot, message):
    total_users = await db.total_users_count()
    await message.reply_text(
        text=f'◉ ᴛᴏᴛᴀʟ ᴜꜱᴇʀꜱ: {total_users}'
    )

@Client.on_message(filters.command("broadcast") & filters.user(ADMINS) & filters.reply)
async def verupikkals(bot, message):
    users = await db.get_all_users()
    b_msg = message.reply_to_message
    sts = await message.reply_text(
        text='Broadcasting your messages...'
    )
    start_time = time.time()
    total_users = await db.total_users_count()
    done = 0
    blocked = 0
    deleted = 0
    failed =0

    success = 0
    async for user in users:
        if 'id' in user:
            pti, sh = await broadcast_messages(int(user['id']), b_msg)
            if pti:
                success += 1
            elif pti == False:
                if sh == "Blocked":
                    blocked += 1
                elif sh == "Deleted":
                    deleted += 1
                elif sh == "Error":
                    failed += 1
            done += 1
            if not done % 20:
                await sts.edit(f"Broadcast in progress:\n\nTotal Users {total_users}\nCompleted: {done} / {total_users}\nSuccess: {success}\nBlocked: {blocked}\nDeleted: {deleted}")    
        else:
            # Handle the case where 'id' key is missing in the user dictionary
            done += 1
            failed += 1
            if not done % 20:
                await sts.edit(f"Broadcast in progress:\n\nTotal Users {total_users}\nCompleted: {done} / {total_users}\nSuccess: {success}\nBlocked: {blocked}\nDeleted: {deleted}")    

    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    await sts.edit(f"Broadcast Completed:\nCompleted in {time_taken} seconds.\n\nTotal Users {total_users}\nCompleted: {done} / {total_users}\nSuccess: {success}\nBlocked: {blocked}\nDeleted: {deleted}")

@Client.on_message(filters.command('accept') & filters.private)
async def accept(client, message):
    show = await message.reply("Please Wait.....")
    user_data = await db.get_session(message.from_user.id)
    if user_data is None:
        await show.edit("For Accepte Pending Request You Have To /login First.")
        return
    try:
        acc = Client("joinrequest", session_string=user_data, api_hash=API_HASH, api_id=API_ID)
        await acc.connect()
    except:
        return await show.edit("Your Login Session Expired. So /logout First Then Login Again By - /login")
    show = await show.edit("Now Forward A Message From Your Channel Or Group With Forward Tag\n\nMake Sure Your Logged In Account Is Admin In That Channel Or Group With Full Rights.")
    vj = await client.listen(message.chat.id)
    if vj.forward_from_chat and not vj.forward_from_chat.type in [enums.ChatType.PRIVATE, enums.ChatType.BOT]:
        chat_id = vj.forward_from_chat.id
        try:
            info = await acc.get_chat(chat_id)
        except:
            await show.edit("Error - Make Sure Your Logged In Account Is Admin In This Channel Or Group With Rights.")
    else:
        return await message.reply("Message Not Forwarded From Channel Or Group.")
    await vj.delete()
    msg = await show.edit("Accepting all join requests... Please wait until it's completed.")
    try:
        while True:
            await acc.approve_all_chat_join_requests(chat_id)
            await asyncio.sleep(1)
            join_requests = [request async for request in acc.get_chat_join_requests(chat_id)]
            if not join_requests:
                break
        await msg.edit("Successfully accepted all join requests.")
    except Exception as e:
        await msg.edit(f"An error occurred: {str(e)}")


@Client.on_chat_join_request()
async def approve_new(client, m):
    if not NEW_REQ_MODE:
        return
    try:
        if not await db.is_user_exist(m.from_user.id):
            await db.add_user(m.from_user.id, m.from_user.first_name)
            await client.send_message(LOG_CHANNEL, LOG_TEXT.format(m.from_user.id, m.from_user.mention))

        # Approve the request
        await client.approve_chat_join_request(m.chat.id, m.from_user.id)

        try:
            # Get the channel invite link
            chat_info = await client.get_chat(m.chat.id)
            channel_link = chat_info.invite_link or f"https://t.me/{chat_info.username}"

            # Get bot username for start link
            bot_info = await client.get_me()
            bot_username = bot_info.username

            # Inline keyboard with two buttons
            keyboard = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("🔗 ᴊᴏɪɴ ᴛʜᴇ ɢʀᴏᴜᴘ/ᴄʜᴀɴɴᴇʟ", url=channel_link)],
                    [InlineKeyboardButton("🤖 sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ", url=f"https://t.me/{bot_username}?start=start")]
                ]
            )

            # Send welcome image + message
            photo_url = "https://i.postimg.cc/KzvWp2yQ/IMG-20250514-224151-977.jpg"
            caption_text = (
                f"👋 ʜᴇʏ {m.from_user.mention},\n\n"
                f"✅ ʏᴏᴜʀ ʀᴇQᴜᴇsᴛ ᴛᴏ ᴊᴏɪɴ 『{m.chat.title}』 ʜᴀs ʙᴇᴇɴ ᴀᴄᴄᴇᴘᴛᴇᴅ!\n"
                f"📢 ɴᴏᴡ ʏᴏᴜ ᴄᴀɴ ᴇɴᴛᴇʀ ᴛʜᴇ ɢʀᴏᴜᴘ/ᴄʜᴀɴɴᴇʟ ᴀɴᴅ ᴇɴᴊᴏʏ ᴛʜᴇ ᴄᴏɴᴛᴇɴᴛ.\n\n"
                f"🤖 ᴘʟᴇᴀsᴇ ᴄʟɪᴄᴋ 'ꜱᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ' ᴛᴏ ᴀᴄᴛɪᴠᴀᴛᴇ ʏᴏᴜʀ ᴀᴄᴄᴇss."
            )

            await client.send_photo(
                m.from_user.id,
                photo=photo_url,
                caption=caption_text,
                reply_markup=keyboard
            )

        except Exception as e:
            logger.error(f"❌ Failed to send message to user {m.from_user.id}: {e}")

    except Exception as e:
        logger.error(f"❌ Error in approve_new: {e}")


        
