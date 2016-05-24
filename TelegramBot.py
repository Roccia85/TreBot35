import time 
from twx.botapi import TelegramBot, ReplyKeyboardMarkup,Update,Message,InputFile,InputFileInfo

"""
Setup the bot
"""

bot = TelegramBot('204368082:AAEfHT1b1pXmBJM3OfbSHUaL5Th30zdsmtI')
bot.update_bot_info().wait()
print(bot.username)

"""
Send a message to a user
"""
user_id = int(153170813)

result = bot.send_message(user_id, bot.username + " is Online!").wait()
print(result)

"""
Use a custom keyboard
"""
keyboard = [[':joy:', '8', '9'],
    ['4', '5', '6'],
    ['1', '2', '3'],
         ['0']]
reply_markup = ReplyKeyboardMarkup.create(keyboard)

"""
Get updates sent to the bot
"""

def reply(update):
  if update.message is not None :
    if update.message.text == 'ciao' or update.message.text == 'Ciao'  :
      bot.send_message(update.message.chat.id, 'Ma ciao!').wait()
    if update.message.text == 'Rossella?' :
      bot.send_message(update.message.chat.id, 'Gluglugluglugluglugluglu :heart:').wait()
    if update.message.text == 'Marco?' :
      bot.send_message(update.message.chat.id, 'Cheffigo!!').wait()
    if "grazie" in update.message.text :
      bot.send_message(update.message.chat.id, 'Grazie graziella grazie al cazzone!').wait()
    #if "foto?" in update.message.text:
    #  fp = open('foto.jpg', 'rb')
    #  file_info = InputFileInfo('foto.jpg', fp, 'image/jpg')
    #  input=InputFile('photo', file_info)
    #  bot.send_photo(chat_id=update.message.chat.id,photo=input)
    if "gattino" in update.message.text:
      fp = open('gattino.jpg', 'rb')
      file_info = InputFileInfo('gattino.jpg', fp, 'image/jpg')
      input = InputFile('photo', file_info)
      bot.send_photo(chat_id=update.message.chat.id,photo=input)
    if "pene" in update.message.text:
      fp = open('p.jpg', 'rb')
      file_info = InputFileInfo('p.jpg', fp, 'image/jpg')
      input = InputFile('photo', file_info)
      bot.send_photo(chat_id=update.message.chat.id,photo=input)

var = 1
offset = 0
while(var == 1):
  updates = bot.get_updates(offset).wait()
  for update in updates:      
      offset = update.update_id + 1              
      print(update.message.sender.id)
      reply(update)



bot.send_message(user_id, 'please enter a number', reply_markup=reply_markup).wait()









