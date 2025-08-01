from PIL import Image
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters, _contexttypes
import pytz
import os
timezone = pytz.timezone("UTC")
TOKEN = '7673808687:AAFDC11CSpQLYKMZnZPmo0nsWK7Ex09hX2Y'
user_profiles = {}  # Dictionary to store user profiles
chat_history = []  # List to store chat history


async def start_3rd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id  # This is the unique Telegram ID for the user
    # You can create a unique botID string, for example:
    bot_unique_id = f"user_{user_id}"
    profile_path = f"D:\Researches\AI\Casteller\Profiles\{bot_unique_id}"
    if not os.path.exists(profile_path):
        os.makedirs(profile_path)
        os.chdir(profile_path)
        # Create a blank image (e.g., 800x600 pixels, white background)
        image = Image.new("RGB", (800, 600), (255, 255, 255))
        # Save the image to the specified path
        image.save(f"{profile_path}\profile_photo.png", "PNG")
        with open("profile_name.txt","w") as file:
            file.write("")
        with open("profile_online_status.txt", "w") as file:
            file.write("")
    else:
        pass  # if the directory already exists, do nothing
    await context.bot.send_message(chat_id=update.effective_chat.id, text="سلام، این کامند سوم است.", reply_to_message_id=update.effective_message.id)

async def show_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id  # This is the unique Telegram ID for the user
    # You can create a unique botID string, for example:
    bot_unique_id = f"user_{user_id}"
    profile_path = f"D:\Researches\AI\Casteller\Profiles\{bot_unique_id}"
    profile_path_name = f"{profile_path}\profile_name"
    profile_path_online_status = f"{profile_path}\profile_online_status"
    caption = f"""Name: {profile_path_name}
                  Online_status: {profile_path_online_status}"""
    with open(f"{profile_path}\profile_photo", 'rb') as photo:
        await update.message.reply_photo(photo=photo, caption= caption)

async def store_chat_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Guard in case update.message or text is None
    if update.message and update.message.text:
        chat_history.append(update.message.text)
    

async def show_chat_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if chat_history:
        history_text = "\n".join(chat_history)
        await update.message.reply_text(f"Chat History:\n{history_text}")
    else:
        await update.message.reply_text("No chat history available.")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id  # This is the unique Telegram ID for the user
    # You can create a unique botID string, for example:
    bot_unique_id = f"user_{user_id}"
    # Use this bot_unique_id to store/retrieve user data uniquely
    print(update.message)
    await update.message.reply_text(f"سلام! شناسه منحصر به فرد شما: {bot_unique_id}")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"سلام! شناسه منحصر به فرد شما: {bot_unique_id}")
    keyboard = [
        [InlineKeyboardButton("فیزیولوژی", callback_data='physiology')],
        [InlineKeyboardButton("آناتومی", callback_data='anatomy')],
        [InlineKeyboardButton("بیوشیمی", callback_data='biochemistry')],
        [InlineKeyboardButton("بافت‌شناسی", callback_data='histology')],
        [InlineKeyboardButton("جنین‌شناسی", callback_data='embryology')],
        [InlineKeyboardButton("اصول خدمات سلامت", callback_data='health')]
    ]
    await update.message.reply_text("لطفاً درس مورد نظر را انتخاب کنید:", reply_markup=InlineKeyboardMarkup(keyboard))


async def first(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="سلام، این کامند اول است.", reply_to_message_id=update.effective_message.id)


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(f"شما انتخاب کردید: {query.data}")


async def send_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Replace with your desired photo URL or local path
    photo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Example.jpg/640px-Example.jpg"
    await update.message.reply_photo(photo=photo_url, caption="این یک عکس نمونه است.")


async def server_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Replace 'path/to/your/image.jpg' with the actual file path on your server
    with open(r"C:\Users\Asus\Downloads\Screenshot 2025-07-28 132304.png", 'rb') as photo:
        await update.message.reply_photo(photo=photo, caption="این تصویر از سرور من است.")


async def start_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [KeyboardButton(text="profile"), KeyboardButton(text="سکه")],
        [KeyboardButton(text="راهنما")]
    ]
    reply_markup = ReplyKeyboardMarkup(
        buttons, resize_keyboard=True, one_time_keyboard=False)
    await update.message.reply_text("لطفاً یکی از گزینه‌ها را انتخاب کنید:", reply_markup=reply_markup)


async def on_button_press(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_profiles:
        user_profiles[user_id] = {"name": "Homer", "age": 20}

    pressed_button = update.message.text

    if pressed_button == "profile":
        # Delete user's message "profile" to remove it from chat
        try:
            await update.message.delete()
        except:
            pass  # Ignore if unable to delete

        profile = user_profiles[user_id]

        # Inline buttons shown attached to the bot's new message
        inline_buttons = [
            [InlineKeyboardButton("تغییر نام", callback_data="change_name")],
            [InlineKeyboardButton("تغییر سن", callback_data="change_age")]
        ]
        inline_markup = InlineKeyboardMarkup(inline_buttons)

        text = f"name: {profile['name']}, Age: {profile['age']}"

        # Send new message with profile info and inline keyboard,
        # and remove the reply keyboard (so "profile" button is gone)
        await update.effective_chat.send_message(
            text=text,
            reply_markup=ReplyKeyboardRemove()  # hides the previous custom keyboard
        )
        # Then edit this message to add inline keyboard (cannot add in send_message reply_markup with ReplyKeyboardRemove),
        # So send it in one go by creating message with both inline keyboard and ReplyKeyboardRemove:

        # Actually, ReplyKeyboardRemove can't be combined with InlineKeyboardMarkup in one message via telegram API.
        # So a trick is to first send a message with ReplyKeyboardRemove, then edit the same message to attach InlineKeyboardMarkup.

        # But to keep it simple, first remove keyboard, then send inline keyboard in a second message:
        await update.effective_chat.send_message(
            text="برای تغییر profile گزینه‌ای را انتخاب کنید:",
            reply_markup=inline_markup
        )

    else:
        # For other buttons, handle normally or send some message
        await update.message.reply_text(f"شما دکمه {pressed_button} را انتخاب کردید.")


async def on_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    if user_id not in user_profiles:
        user_profiles[user_id] = {"name": "Homer", "age": 20}

    if query.data == "change_name":
        await query.answer()  # Acknowledge the button press to remove the loading animation
        context.user_data["awaiting_name"] = True
        # Ask the user to send new name
        await query.message.reply_text(
            "لطفا نام جدید خود را وارد کنید:",
            reply_markup=ReplyKeyboardRemove()
        )
    # Your other callback_data handlers here...

# This message handler catches the next text after "تغییر نام" is pressed


async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if context.user_data.get("awaiting_name"):
        new_name = update.message.text.strip()
        if not new_name:
            await update.message.reply_text("نام نمی‌تواند خالی باشد. لطفاً دوباره امتحان کنید.")
            return

        user_profiles[user_id]["name"] = new_name
        context.user_data["awaiting_name"] = False  # Reset the flag

        # Send updated profile info to the user
        updated_info = f"پروفایل شما بروز شد:\nname: {new_name}, Age: {user_profiles[user_id]['age']}"
        await update.message.reply_text(updated_info)
    else:
        # Handle other text messages or ignore
        pass

if __name__ == "__main__":
    print("ربات در حال اجراست...")
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("send_photo", send_photo))
    app.add_handler(CommandHandler("start_3rd", start_3rd))
    app.add_handler(CommandHandler("show_chat_history", show_chat_history))
    app.add_handler(CommandHandler("first", first))
    app.add_handler(CommandHandler("server_photo", server_photo))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("start_2", start_2))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(
        filters.TEXT & (~filters.COMMAND), store_chat_history))
    app.add_handler(MessageHandler(
        filters.TEXT & (~filters.COMMAND), on_button_press))
    app.run_polling()
