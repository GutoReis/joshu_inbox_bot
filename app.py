from flask import Flask, request
import telegram
from joshu.credentials import BOT_TOKEN, BOT_USER_NAME, URL

bot = telegram.Bot(token=BOT_TOKEN)

app = Flask(__name__)

@app.route('/{}'.format(BOT_TOKEN), methods=["POST"])
def responde():
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode("utf-8").decode()
    # for debugging purposes only
    print("got the message: ", text)

    # The first time you chat with the bot A.K.A the welcome message
    if text == "/start":
        # Print the welcoming message
        bot_welcome = """
            Hi, I am Joshu, and I'm will help you freeing your mind, so you can
            leave space to create, to wonder, to have ideas, to be present, while
            I save things for later, and don't worry, I'm here to help you!
        """
        # Send the message
        bot.sendMessage(chat_id=chat_id,
                        text=bot_welcome,
                        reply_to_message_id=msg_id)
    
    else:
        try:
            # Just sending back the same message to test only
            bot.sendMessage(chat_id=chat_id,
                            text=text,
                            reply_to_message_id=msg_id)
        except Exception:
            bot.sendMessage(chat_id=chat_id,
                            text="Something went wrong",
                            reply_to_message_id=msg_id)
    return "ok"


@app.route("/setwebhook", methods=["GET", "POST"])
def set_webhook():
    # We use the bot object to link the bot to our app which live in the URL
    hook = bot.setWebhook(f"{URL}{BOT_TOKEN}")
    # Something to let us know things worked
    if hook:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

@app.route("/")
def index():
    return "<p>Hello, I'm Joshu, check me in Telegram ;)</p>"

if __name__ == "__main__":
    # Note the threaded arg which allow our app to have more tan one thread
    app.run(threaded=True, host="0.0.0.0", port=80)