import os
import telebot
import requests

# سحب التوكن تلقائياً من إعدادات Railway لضمان الأمان
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك في بوت تحميل مقاطع تيك توك! 🤖\nأرسل لي رابط المقطع الآن وسأقوم بتحميله لك مباشرة.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    if "tiktok.com" in url:
        status_msg = bot.reply_to(message, "جاري معالجة الرابط وتحميل المقطع، انتظر لحظة... ⏳")
        try:
            # استخدام واجهة برمجة مجانية لسحب فيديو التيك توك بدون علامة مائية
            api_url = f"https://www.tikwm.com/api/?url={url}"
            response = requests.get(api_url).json()
            
            if response.get("code") == 0:
                video_url = response["data"]["play"]
                bot.send_video(message.chat.id, video_url, reply_to_message_id=message.message_id)
                bot.delete_message(message.chat.id, status_msg.message_id)
            else:
                bot.edit_message_text("عذراً، تعذر تحميل هذا المقطع. تأكد أن الحساب ليس خاصاً.", message.chat.id, status_msg.message_id)
        except Exception as e:
            bot.edit_message_text("حدث خطأ أثناء محاولة تحميل المقطع. حاول لاحقاً.", message.chat.id, status_msg.message_id)
    else:
        bot.reply_to(message, "رجاءً أرسل رابط تيك توك صحيح (tiktok.com) ⚠️")

if __name__ == "__main__":
    print("البوت يعمل الآن بنجاح...")
    bot.infinity_polling()
