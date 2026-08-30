import telebot
import base
import music_api

bot = telebot.TeleBot(base.TOKEN)
print("music bot created")

@bot.message_handler(commands=["start"])
def start_music(message):
    msg = bot.send_message(message.chat.id, text="خوش امدید")
    bot.register_next_step_handler(msg,ask_song_name)

@bot.message_handler(commands=["music"])
def ask_song_name(message):
    msg = bot.send_message(message.chat.id, text="نام آهنگ یا خواننده مورد نظر را وارد کنید:")
    bot.register_next_step_handler(msg, send_music_results)


def send_music_results(message):
    query = message.text
    bot.send_chat_action(message.chat.id, "typing")

    results = music_api.search_music(query, limit=5)

    if results is None:
        bot.send_message(message.chat.id, text="خطا در اتصال به سرویس موسیقی، لطفا بعدا تلاش کنید")
        return

    if not results:
        bot.send_message(message.chat.id, text="نتیجه‌ای برای این جستجو پیدا نشد")
        return

    for song in results:
        caption = (
            f" {song['track_name']}\n"
            f" {song['artist_name']}\n"
            f"{song['album_name']}\n"
            f" {song['release_date']}"
        )

        if song["preview_url"]:
            bot.send_audio(
                message.chat.id,
                song["preview_url"],
                caption=caption,
                performer=song["artist_name"],
                title=song["track_name"],
            )
        else:
            bot.send_message(message.chat.id, text=caption)


if __name__ == "__main__":
    bot.infinity_polling()