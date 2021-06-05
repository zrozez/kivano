import pandas
import telebot
import parser

class KivanoBot:
    help_text = '''
    /categories - все категории
    /categories {название категории} - для получения товара данной категории
    /product {название продукта} - информация о товаре
    '''

    __tovars = pandas.read_csv('tovary.csv')
    tovarset = set(__tovars.names_of_categories.to_list())

    def show(self, args):
        if len(args)<=0:
            return '\n'.join(self.tovarset)
        else:
            tovar = args

        if tovar not in self.tovarset:
            return f'Категории с названием: {args} не существует'
        else:
            tovar = self.__tovars[self.__tovars.names_of_categories == tovar]
            tovar = tovar[['names', 'links']].to_string()
        return tovar

TOKEN = '1742989719:AAEtlHefZicCOd5l8qqulfp7qu7ISGenq7o'

bot = telebot.TeleBot(TOKEN)
kbot= KivanoBot()
 
@bot.message_handler(commands=['start', 'help'])
def show(message):
    bot.send_message(message.chat.id, kbot.help_text)
 
@bot.message_handler(commands=['categories'])
def tovars(message):
    args = message.text[11:]
    bot.send_message(message.chat.id, kbot.show(args))
 
if __name__ == '__main__':
    bot.polling()
