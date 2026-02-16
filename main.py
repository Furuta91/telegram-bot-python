import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8580138615:AAFBl6xtLtnhEvCExhE3cB7ubOboTXy4euw"
CHANNEL = "@ChannelKamu"   # contoh: @ChannelFuruta

bot = telebot.TeleBot(TOKEN)

# cek apakah user join channel
def is_joined(user_id):
    try:
        member = bot.get_chat_member(CHANNEL, user_id)
        return member.status in ["member", "creator", "administrator"]
    except:
        return False


# tombol join
def join_markup():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("JOIN CHANNEL 1", url=f"https://t.me/{CHANNEL.replace('@','')}"),
        InlineKeyboardButton("JOIN CHANNEL 2", url=f"https://t.me/{CHANNEL.replace('@','')}"),
        InlineKeyboardButton("JOIN CHANNEL 3", url=f"https://t.me/{CHANNEL.replace('@','')}")
    )
    markup.add(
        InlineKeyboardButton("COBA LAGI", callback_data="retry")
    )
    return markup


@bot.message_handler(commands=['start'])
def start(message):
    if not is_joined(message.from_user.id):
        bot.send_message(
            message.chat.id,
            f"Hello {message.from_user.first_name}\n\n"
            "Anda harus bergabung di Channel atau Group terlebih dahulu "
            "untuk melihat file yang saya bagikan.\n\n"
            "Silakan join terlebih dahulu.",
            reply_markup=join_markup()
        )
    else:
        bot.send_message(message.chat.id, "Silakan upload foto atau video.")


@bot.callback_query_handler(func=lambda call: call.data == "retry")
def retry(call):
    if not is_joined(call.from_user.id):
        bot.answer_callback_query(call.id, "Masih belum join.")
    else:
        bot.send_message(call.message.chat.id, "Silakan upload file sekarang.")


# upload foto
@bot.message_handler(content_types=['photo'])
def photo(message):
    if not is_joined(message.from_user.id):
        bot.send_message(message.chat.id, "Join channel dulu.", reply_markup=join_markup())
        return

    file_id = message.photo[-1].file_id
    link = f"https://api.telegram.org/file/bot{TOKEN}/{file_id}"
    bot.send_message(message.chat.id, f"Link file:\n{link}")


# upload video
@bot.message_handler(content_types=['video'])
def video(message):
    if not is_joined(message.from_user.id):
        bot.send_message(message.chat.id, "Join channel dulu.", reply_markup=join_markup())
        return

    file_id = message.video.file_id
    link = f"https://api.telegram.org/file/bot{TOKEN}/{file_id}"
    bot.send_message(message.chat.id, f"Link file:\n{link}")


bot.infinity_polling()
