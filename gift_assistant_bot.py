
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext

# Define the questions and options
questions = [
    "Кому предназначен подарок? (возраст, пол, кем вам приходится)",
    "Какие у него/неё интересы, хобби, увлечения?",
    "Какой у тебя бюджет?",
    "Какой тип подарка ты предпочитаешь?"
]

options = {
    "Какой у тебя бюджет?": [
        ["До 1000 ₽", "До 5000 ₽", "Без ограничений"]
    ],
    "Какой тип подарка ты предпочитаешь?": [
        ["Материальный", "Впечатление", "Ручной работы", "Оригинальный и креативный", "Неважно, главное — чтобы понравилось"]
    ]
}

# Store user responses
user_responses = {}

# Start command handler
def start(update: Update, context: CallbackContext) -> None:
    user_responses[update.effective_user.id] = []
    update.message.reply_text("Привет! Я помогу тебе выбрать идеальный подарок на день рождения 🎉")
    ask_question(update, context, 0)

# Ask question function
def ask_question(update: Update, context: CallbackContext, question_index: int) -> None:
    if question_index < len(questions):
        question = questions[question_index]
        if question in options:
            keyboard = [[InlineKeyboardButton(opt, callback_data=opt) for opt in row] for row in options[question]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(question, reply_markup=reply_markup)
        else:
            update.message.reply_text(question)
    else:
        generate_gift_ideas(update, context)

# Handle text responses
def handle_text_response(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    user_responses[user_id].append(update.message.text)
    ask_question(update, context, len(user_responses[user_id]))

# Handle button responses
def handle_button_response(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    user_id = query.message.chat_id
    user_responses[user_id].append(query.data)
    ask_question(query, context, len(user_responses[user_id]))

# Generate gift ideas
def generate_gift_ideas(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    responses = user_responses[user_id]
    # Here you can add logic to generate gift ideas based on responses
    gift_ideas = [
        "🎧 Портативная колонка JBL — для любителя музыки и вечеринок",
        "🎨 Мастер-класс по керамике — творческий и запоминающийся опыт",
        "📚 Персонализированная книга — с именем получателя в сюжете",
        "🎟️ Билет на концерт или спектакль",
        "🧘 Сертификат в СПА или на массаж"
    ]
    update.message.reply_text("Вот несколько идей подарков, которые могут подойти:")
    for idea in gift_ideas:
        update.message.reply_text(idea)
    update.message.reply_text("Надеюсь, эти идеи тебе помогли! 🎁")

# Main function to start the bot
def main() -> None:
    # Replace 'YOUR_TOKEN_HERE' with your actual bot token
    updater = Updater("8105830161:AAHhAvOa3OegaiO6MRV4duJR8pbAFz0RRww")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text_response))
    dispatcher.add_handler(CallbackQueryHandler(handle_button_response))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
