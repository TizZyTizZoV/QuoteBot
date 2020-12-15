from bs4 import BeautifulSoup
import requests
import telebot
from telebot import types

bot = telebot.TeleBot("1350631111:AAFebP9c4vUMtI7RSHQx5T2v3pFm2OdlGPg")

quoteButton = types.KeyboardButton(text = '📜Получить новую цитату📜')
quoteKeyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
quoteKeyboard.add(quoteButton)

def GetQuote():
    url = "https://quote-citation.com/random"

    try:
        header = { 
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 YaBrowser/20.11.3.183 Yowser/2.5 Safari/537.36', 
            'upgrade-insecure-requests': '1', 
            'cookie': 'mos_id=CllGxlx+PS20pAxcIuDnAgA=; session-cookie=158b36ec3ea4f5484054ad1fd21407333c874ef0fa4f0c8e34387efd5464a1e9500e2277b0367d71a273e5b46fa0869a; NSC_WBS-QUBG-jo-nptsv-WT-443=ffffffff0951e23245525d5f4f58455e445a4a423660; rheftjdd=rheftjddVal; _ym_uid=1552395093355938562; _ym_d=1552395093; _ym_isad=2'
        }
        page = requests.get(url, headers = header)
    except (err):
        print("Не удалось подключиться к серверу.")

    soup = BeautifulSoup(page.text, "lxml")

    mainBlock = soup.find("div", class_ = "quote-text")

    needBlock = mainBlock.find_all("p")
    quote, author = needBlock[0], needBlock[1]

    quote = str(quote)
    quote = quote.replace("<p>", "")
    quote = quote.replace("</p>", "")
    quote = quote.replace("<br>", "")

    author = BeautifulSoup(str(author.find_all("a")), "lxml").a.text

    gotQuote = quote + "\n\n" + author

    return gotQuote

@bot.message_handler(commands=['start'])
def start_msg(msg):
    bot.send_message(msg.from_user.id, "Привет!\nЯ тот кто будет радовать тебя случайными цитатами😉\nЧтобы получить цитату, жмякай на кнопку👇", reply_markup = quoteKeyboard)

@bot.message_handler(content_types=['text'])
def get_msg(msg):
    if (msg.text == "📜Получить новую цитату📜"):
        bot.send_message(msg.from_user.id, GetQuote(), reply_markup = quoteKeyboard)
    else:
        bot.send_message(msg.from_user.id, "Для получения цитаты нажми на кнопку👇", reply_markup = quoteKeyboard)

bot.polling(none_stop = True, interval = 0)
