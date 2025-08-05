import os


class Profile:
    def __init__(self,
                 name,
                 photo,
                 tags,
                 online_status="Online",
                 bot_id=f"user_{update.effective_user.id}",
                 monthly_questionnaires=0):
        self.name = name
        self.photo = photo
        self.bot_id = bot_id
        self.online_status = online_status
        self.monthly_questionnaires = monthly_questionnaires
        self.tags = tags

    def change_name(self, new_name):
        self.name = new_name

    def change_photo(self, new_photo):
        self.photo = new_photo

    def change_tags(self, new_tags):
        self.tags = new_tags

    def change_online_status(self):
        if self.online_status == "Online":
            self.online_status = "Offline"
        else:
            self.online_status = "Online"


print(os.getcwd())


async def start_3rd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_id = f"user_{update.effective_user.id}"
    profiles_path = f"D:\Researches\AI\Casteller\Profiles"
    # Create a blank image (e.g., 800x600 pixels, white background)
    image = Image.new("RGB", (800, 600), (255, 255, 255))
    # Save the image to the specified path
    image.save(f"{profiles_path}\photos\{bot_id}.png", "PNG")
    try:
        with open("profiles.json", "r") as file:               
            profiles = json.load(file)
    except Exception:
        profiles = {}

    if f"{bot_id}" in profiles:
        pass
    else:
        profiles[f"{bot_id}"] = {
            "name": "New User",
            "photo": f"{profiles_path}\photos\{bot_id}.png",
            "tags": "ok",
            "online_status": "Online",
            "questionnaires": {}
        }
    with open("profiles.json", "w") as json_file:
        json.dump(profiles, json_file, indent=4)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="""Hello, send your question so i can find the relevant specialist for you.
NOTE: Your message should be a text-only_message, which indicates the major field of your question.""", reply_to_message_id=update.effective_message.id)
    return WAITING_FOR_TEXT







from PIL import Image
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters, _contexttypes,ConversationHandler
import pytz
import os
import json
import datetime
from datetime import datetime, timedelta
from openai import OpenAI



async def get_tag(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    global tags_list
    
    my_message = update.message.text # Get the text message from the user
    API_key = "aa-VIYcdCWFZTHh6GlKSVnyDRmOEjiJWfhDGb6HtCOSTEdQDGVP"
    base_URL = "https://api.avalai.ir/v1"
    model = "gpt-4.1-nano"
    client = OpenAI(api_key=API_key, base_url=base_URL)
    
    completion = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "developer", "content": "extraction tags from a question"},
        {"role": "user", "content": f"""This is a question from my mentoring platform client, give me a single tag from this tag list regarding this question which i can search the mentors by this tag
         tags list: {tags_list} 
         question: {my_message}"""},
    ],
    temperature=0.5,
    max_tokens=2000
)
    tag = completion.choices[0].message.content.strip()
    ###search_tag(tag)###
    return ConversationHandler.END

app = ApplicationBuilder().token(TOKEN).build()

conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start_3rd", start_3rd)],
        states={
            WAITING_FOR_TEXT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_tag)
            ],
        },
        fallbacks=[],
    )

app.add_handler(conv_handler)
app.run_polling()
