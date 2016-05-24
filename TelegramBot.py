import sys
import datetime
from twx.botapi import TelegramBot, ReplyKeyboardMarkup,Update,Message,InputFile,InputFileInfo
from TrainMonitor import viaggiatreno


def is_valid_timestamp(ts):
    return (ts is not None) and (ts > 0) and (ts < 2147483648000)


def format_timestamp(ts, fmt='%H:%M:%S'):
    if is_valid_timestamp(ts):
        return datetime.datetime.fromtimestamp(ts / 1000).strftime(fmt)
    else:
        return 'N/A'



def trainInfo(number, chat_id):

    output=list()

    def write(text):
        bot.send_message(chat_id, text).wait()

    trainNumber = number
    api = viaggiatreno.API()

    departures = api.call('cercaNumeroTrenoTrenoAutocomplete', trainNumber)

    if len(departures) == 0:
        output.append("Train {0} does not exists.".format(trainNumber))
        sys.exit()

    # TODO: handle not unique train numbers, when len(departures) > 1

    departure_ID = departures[0][1]
    train_status = api.call('andamentoTreno', departure_ID, trainNumber)

    if train_status['tipoTreno'] == 'ST' or train_status['provvedimento'] == 1:
        output.append("Train {0} cancelled \n".format(trainNumber))

    elif train_status['oraUltimoRilevamento'] is None:
        output.append("Train {0} has not yet departed".format(trainNumber))
        output.append("Scheduled departure {0} from {1} \n".format(
            format_timestamp(train_status['orarioPartenza']),
            train_status['origine']
        ))

    else:
        if train_status['tipoTreno'] in ('PP', 'SI', 'SF'):
            output.append("Train partially cancelled: " + train_status['subTitle'] +"\n")

        output.append('Last tracking in {0} at {1}'.format(
            train_status['stazioneUltimoRilevamento'],
            format_timestamp(train_status['oraUltimoRilevamento'])
        ))

        for f in train_status['fermate']:
            station = f['stazione']
            scheduled = format_timestamp(f['programmata'])
            if f['tipoFermata'] == 'P':
                actual = format_timestamp(f['partenzaReale'])
                delay = f['ritardoPartenza']
                descr = 'Departure'
            else:
                actual = format_timestamp(f['arrivoReale'])
                delay = f['ritardoArrivo']
                descr = 'Arrival'

            description = '{0} {1}: {2} (scheduled {3} - delay: {4})'.format(station, descr, actual, scheduled, delay)

            if f['actualFermataType'] == 3:
                output.append(station + "cancelled\n")
            elif f['actualFermataType'] == 0:
                output.append(station + "data not available\n")
            else:
                output.append(description)

    message=''
    for s in output:
        message=message+' '+s
    write(message)

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
    if "treno" in update.message.text:
        number=update.message.text[5:]
        trainInfo(int(number), update.message.chat.id)

var = 1
offset = 0
while(var == 1):
  updates = bot.get_updates(offset).wait()
  for update in updates:      
      offset = update.update_id + 1              
      print(update.message.sender.id)
      reply(update)



bot.send_message(user_id, 'please enter a number', reply_markup=reply_markup).wait()







