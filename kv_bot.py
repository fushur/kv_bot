from transitions import Machine
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext


class OrderFood(object):
    states = ['waiting_for_pizza_size', 'waiting_for_payment_method', 'waiting_for_confirmation', 'final']
    messages = ['Какую Вы хотите пиццу? Большую или маленькую?', 'Как Вы будете платить?',
                'Вы хотите {} пиццу, оплата - {}?', 'Спасибо за заказ']

    def __init__(self):
        self.pizza_size = None

        self.payment_method = None

        self.machine = Machine(model=self, states=OrderFood.states, initial='waiting_for_pizza_size')

        self.machine.add_transition(trigger='/start', source='*', dest='waiting_for_pizza_size')

        self.machine.add_transition(trigger='Большую', source='waiting_for_pizza_size',
                                    dest='waiting_for_payment_method')

        self.machine.add_transition(trigger='Маленькую', source='waiting_for_pizza_size',
                                    dest='waiting_for_payment_method')

        self.machine.add_transition(trigger='Наличкой', source='waiting_for_payment_method',
                                    dest='waiting_for_confirmation')

        self.machine.add_transition(trigger='Картой', source='waiting_for_payment_method',
                                    dest='waiting_for_confirmation')

        self.machine.add_transition(trigger='Да', source='waiting_for_confirmation', dest='final')

        self.machine.add_transition(trigger='Нет', source='waiting_for_confirmation', dest='waiting_for_pizza_size')

    def pizza_size(self):
        self.pizza_size = self.states
        self.message = 'Как Вы будете платить?'

    def payment(self):
        self.payment_method = self.states
        self.message = f'Вы хотите {self.pizza_size} пиццу, оплата - {self.payment_method}?'

    def reset(self):
        self.pizza_size = None
        self.payment_method = None


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Какую Вы хотите пиццу? Большую или маленькую?')


def main():
    updater = Updater('TOKEN')

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))

    updater.start_polling()
    updater.idle()


main()
