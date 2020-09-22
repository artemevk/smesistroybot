#!/usr/bin/env python
# coding: utf-8

# In[5]:


import requests
from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from bot_config import token


# In[6]:


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Бот Магазина Смесистрой\nДоброго дня\nЧтобы узнать цены просто напишите запрос\nНАПРИМЕР: Гипсовая штукатурка\nНаш магазин:www.smesistroy.ru')


# def help_command(update, context):
#     """Send a message when the command /help is issued."""
#     update.message.reply_text('Help!')


def bot_answer(update, context):
    """Echo the user message."""
    question = update.message.text
    answear = find_answear(question)
    update.message.reply_text(answear)


def find_answear(question):
    """Поиск по сайту"""
    search_phrase = question.replace(' ', '%20') # Подготовка данных для адресной строки
    url = 'https://smesistroy.ru/search/?sort=rating&order=DESC&search='+search_phrase+'&limit=120' # Создание ссылки
    html = requests.get(url) # Получение кода страницы
    soup = BeautifulSoup(html.text, 'html.parser') # Парсинг страницы
    
    data = soup.find('div', attrs={'class': 'row products_category'}) # Получение блока данных по запрашиваемому товару

    reply = '' # Ответ
    
    try:
        items = [] # Список товаров
        prices = [] # Список цен
        
        
        for item in data.find_all('span', attrs={'itemprop': 'name'}, limit=3): # Извлечение списка товаров
            items.append(item.text.strip())

        for price in data.find_all('meta', attrs={'itemprop': 'price'}, limit=3): # Извлечение списка цен
            prices.append(int(price.attrs['content']))

        # Формирование ответа
        for i in range(len(items)):
            reply += '{}, {} руб.\n'.format(items[i], prices[i])

        reply += 'и др. по ссылке: {}'.format(url)

    # Заглушка
    except (AttributeError, TypeError):
        reply += 'Товары не найдены. Попробуйте запросить другой товар.'
        
    return reply


def main():
    """Start the bot."""
    updater = Updater(token, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
#     dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, bot_answer))

    # Start the Bot
    updater.start_polling()
    updater.idle()


# In[ ]:


main()


# In[ ]:




