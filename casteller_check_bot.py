from PIL import Image
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters, _contexttypes
import pytz
import os
import json
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
            file.write("Online")
        data = {}
        with open("chat_history.json", "w") as json_file:
            json.dump(data, json_file, indent=4)
    else:
        pass  # if the directory already exists, do nothing
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, this is the third command.", reply_to_message_id=update.effective_message.id)


async def my_other_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Shows the profile of the user who issued the command.
    """
    args = context.args
    if args:
        await show_other_profile(update, context)
        return  
    else:
        await show_profile(update, context)
        return


async def show_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(2)
    """
    Shows the profile of the user who issued the command.
    """
    args = context.args
    if args:
        return    
    user_id = update.effective_user.id  # This is the unique Telegram ID for the user
    bot_unique_id = f"user_{user_id}"
    profile_path = f"D:\\Researches\\AI\\Casteller\\Profiles\\{bot_unique_id}"
    profile_path_name = f"{profile_path}\\profile_name.txt"
    profile_path_online_status = f"{profile_path}\\profile_online_status.txt"
    profile_photo_path = f"{profile_path}\\profile_photo.png"

    try:
        with open(profile_path_name, 'r', encoding='utf-8') as file:
            profile_name = file.read()
        with open(profile_path_online_status, "r", encoding='utf-8') as file:
            profile_online_status = file.read()
        caption = f"""Name: {profile_name}
Online_status: {profile_online_status}"""
        with open(profile_photo_path, 'rb') as photo:
            await update.message.reply_photo(photo=photo, caption=caption)
    except FileNotFoundError:
        await update.message.reply_text("You have not created a profile yet. Please create your profile first using /start_3rd.")

async def show_other_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(1)
    """
    Shows the profile of another user by their user ID.
    Some parameters and abilities are disabled for privacy.
    Usage: /show_other_profile <user_id>
    """
    args = context.args
    if not args or not args[0].isdigit():
        await update.message.reply_text("Please provide a valid user ID. Example: /show_other_profile 123456789")
        return

    target_user_id = int(args[0])
    bot_unique_id = f"user_{target_user_id}"
    profile_path = f"D:\\Researches\\AI\\Casteller\\Profiles\\{bot_unique_id}"
    profile_path_name = f"{profile_path}\\profile_name.txt"
    profile_path_online_status = f"{profile_path}\\profile_online_status.txt"
    profile_photo_path = f"{profile_path}\\profile_photo.png"

    try:
        with open(profile_path_name, 'r', encoding='utf-8') as file:
            profile_name = file.read()
        with open(profile_path_online_status, "r", encoding='utf-8') as file:
            profile_online_status = file.read()
        # You can limit what is shown here for privacy
        caption = f"""Name: {profile_name}
Online_status: {profile_online_status}"""
        with open(profile_photo_path, 'rb') as photo:
            await update.message.reply_photo(photo=photo, caption=caption)
    except FileNotFoundError:
        await update.message.reply_text("This user has not created a profile yet.")

async def edit_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id  # Unique Telegram ID
    bot_unique_id = f"user_{user_id}"
    profile_path = f"D:\\Researches\\AI\\Casteller\\Profiles\\{bot_unique_id}"
    profile_path_name = f"{profile_path}\\profile_name.txt"

    # Get the new name from the command argument (e.g., /edit_name NewName)
    args = context.args
    if not args:
        await update.message.reply_text("Please enter the new name after the command. Example: /edit_name New_Name")
        return

    new_name = " ".join(args).strip()
    if not new_name:
        await update.message.reply_text("Name cannot be empty. Please try again.")
        return

    if not os.path.exists(profile_path):
        os.makedirs(profile_path)

    with open(profile_path_name, 'w', encoding='utf-8') as file:
        file.write(new_name)

    await update.message.reply_text(f"Your name has been changed to {new_name}.")


async def change_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    bot_unique_id = f"user_{user_id}"
    profile_path = f"D:\\Researches\\AI\\Casteller\\Profiles\\{bot_unique_id}"
    os.makedirs(profile_path, exist_ok=True)
    context.user_data["awaiting_photo"] = True # Flag to indicate that the bot is waiting for a photo
    await update.message.reply_text("Please send your new profile photo.", reply_to_message_id=update.effective_message.id) # Ask the user to send a photo
    app.add_handler(MessageHandler(filters.PHOTO, receive_photo)) # Register the photo handler to receive the photo

async def receive_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):    
    """Handles the reception of a photo from the user.
    Saves it to the user's profile directory.
    """
    # Check if the user is currently uploading a photo
    if context.user_data.get("awaiting_photo"): 
        user_id = update.effective_user.id
        bot_unique_id = f"user_{user_id}"
        profile_path = f"D:\\Researches\\AI\\Casteller\\Profiles\\{bot_unique_id}"
        profile_path_photo = f"{profile_path}\\profile_photo.png"
        image = await update.message.photo[-1].get_file()  # Get Telegram File object
        await image.download_to_drive(profile_path_photo)            # Download to disk as PNG file (the extension just defines file type)
        context.user_data["awaiting_photo"] = False
        await update.message.reply_text("Your profile photo has been updated successfully.")
    else:
        await update.message.reply_text("You are not currently uploading a photo. Please use /change_photo to start the process.")

async def change_online_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id  # Unique Telegram ID   
    bot_unique_id = f"user_{user_id}"
    profile_path = f"D:\\Researches\\AI\\Casteller\\Profiles\\{bot_unique_id}"
    profile_path_online_status = f"{profile_path}\\profile_online_status.txt"
    with open(profile_path_online_status, 'r', encoding='utf-8') as file:
        current_status = file.read().strip()
    if current_status == "Online":
        new_status = "Offline"
    else:
        new_status = "Online"
    with open(profile_path_online_status, 'w', encoding='utf-8') as file:
        file.write(new_status)
    await update.message.reply_text(f"Your online status has been changed to {new_status}.")

# Dictionary to keep track of pending chat requests: {target_user_id: requester_user_id}
pending_chat_requests = {}

async def chat_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Usage: /chat_request <target_user_id>
    user_id = update.effective_user.id
    args = context.args
    if not args or not args[0].isdigit():
        await update.message.reply_text("Please enter the numeric user ID after the command. Example: /chat_request 123456789")
        return
    target_user_id = int(args[0])
    if target_user_id == user_id:
        await update.message.reply_text("You cannot send a request to yourself.")
        return
    pending_chat_requests[target_user_id] = user_id
    try:
        await context.bot.send_message(
            chat_id=target_user_id,
            text=f"You have received a chat request from user {user_id}.\nTo accept: /accept_request {user_id}\nTo reject: /reject_request {user_id}"
        )
        await update.message.reply_text("Your request has been sent.")
    except Exception as e:
        await update.message.reply_text("Could not send the request to the user. Maybe they haven't started the bot.")

active_chats = {}  # (user1, user2): {"requester": id, "partner": id, "count": int}

async def accept_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args
    if not args or not args[0].isdigit():
        await update.message.reply_text("Please enter the requester ID after the command. Example: /accept_request 123456789")
        return
    requester_id = int(args[0])
    if pending_chat_requests.get(user_id) == requester_id:
        await update.message.reply_text("You have accepted the chat request. Starting chat...")
        await context.bot.send_message(
            chat_id=requester_id,
            text=f"Your chat request has been accepted by user {user_id}.\nYou can now chat. The chat will end after you send 14 messages."
        )
        del pending_chat_requests[user_id]
        await start_private_chat(requester_id, user_id, context)
    else:
        await update.message.reply_text("No request from this user exists.")

async def start_private_chat(requester_id, partner_id, context):
    # Register the chat session
    chat_key = tuple(sorted([requester_id, partner_id]))
    active_chats[chat_key] = {"requester": requester_id, "partner": partner_id, "count": 0}

    # Notify both users
    await context.bot.send_message(
        chat_id=requester_id,
        text="You are now connected. Send messages, photos, or files. The chat will end after you send 14 messages."
    )
    await context.bot.send_message(
        chat_id=partner_id,
        text="You are now connected. Send messages, photos, or files. The chat will end when the requester sends 14 messages."
    )
    user_id = update.effective_user.id
    bot_unique_id = f"user_{user_id}"
    profile_path = f"D:\\Researches\\AI\\Casteller\\Profiles\\{bot_unique_id}"
    profile_path_chat_history = f"{profile_path}\\chat_history.json"


    # Load existing chat history or create a new one   
    
async def relay_chat(update: Update,
                     context: ContextTypes.DEFAULT_TYPE):
    """
    Relay messages, photos, and documents
    between users in an active chat session.
    Ends chat after 14 messages from requester.
    """
    user_id = update.effective_user.id
    # Find if user is in an active chat
    for chat_key, chat_info in active_chats.items():
        if user_id in chat_key:
            requester = chat_info["requester"]
            partner = chat_info["partner"]
            # count = chat_info["count"]  # Removed unused variable

            # Determine the other user
            other_user = (
                partner if user_id == requester
                else requester
            )

            # Relay text
            if update.message.text:
                await context.bot.send_message(
                    chat_id=other_user,
                    text=update.message.text
                )
                # Only increment if requester sends a message
                if user_id == requester:
                    chat_info["count"] += 1
                    remaining = (
                        14 - chat_info["count"]
                    )
                    if remaining > 0:
                        await context.bot.send_message(
                            chat_id=requester,
                            text=(
                                f"You have {remaining} "
                                "messages left before "
                                "the chat ends."
                            )
                        )
                    if chat_info["count"] >= 14:
                        await context.bot.send_message(
                            chat_id=requester,
                            text=(
                                "Chat ended. You have "
                                "sent 14 messages."
                            )
                        )
                        await context.bot.send_message(
                            chat_id=partner,
                            text=(
                                "Chat ended. The "
                                "requester has sent "
                                "14 messages."
                            )
                        )
                        del active_chats[chat_key]
                return

            # Relay photo
            if update.message.photo:
                photo_file = (
                    await update.message.photo[-1].get_file()
                )
                await context.bot.send_photo(
                    chat_id=other_user,
                    photo=photo_file.file_id,
                    caption=(
                        update.message.caption
                        or ""
                    )
                )
                if user_id == requester:
                    chat_info["count"] += 1
                    remaining = (
                        14 - chat_info["count"]
                    )
                    if remaining > 0:
                        await context.bot.send_message(
                            chat_id=requester,
                            text=(
                                f"You have {remaining} "
                                "messages left before "
                                "the chat ends."
                            )
                        )
                    if chat_info["count"] >= 14:
                        await context.bot.send_message(
                            chat_id=requester,
                            text=(
                                "Chat ended. You have "
                                "sent 14 messages."
                            )
                        )
                        await context.bot.send_message(
                            chat_id=partner,
                            text=(
                                "Chat ended. The "
                                "requester has sent "
                                "14 messages."
                            )
                        )
                        del active_chats[chat_key]
                return

            # Relay document
            if update.message.document:
                doc_file = (
                    await update.message.document.get_file()
                )
                await context.bot.send_document(
                    chat_id=other_user,
                    document=doc_file.file_id,
                    caption=(
                        update.message.caption
                        or ""
                    )
                )
                if user_id == requester:
                    chat_info["count"] += 1
                    remaining = (
                        14 - chat_info["count"]
                    )
                    if remaining > 0:
                        await context.bot.send_message(
                            chat_id=requester,
                            text=(
                                f"You have {remaining} "
                                "messages left before "
                                "the chat ends."
                            )
                        )
                    if chat_info["count"] >= 14:
                        await context.bot.send_message(
                            chat_id=requester,
                            text=(
                                "Chat ended. You have "
                                "sent 14 messages."
                            )
                        )
                        await context.bot.send_message(
                            chat_id=partner,
                            text=(
                                "Chat ended. The "
                                "requester has sent "
                                "14 messages."
                            )
                        )
                        del active_chats[chat_key]
                return
    # If not in any active chat, do nothing

async def reject_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args
    if not args or not args[0].isdigit():
        await update.message.reply_text("Please enter the requester ID after the command. Example: /reject_request 123456789")
        return
    requester_id = int(args[0])
    if pending_chat_requests.get(user_id) == requester_id:
        await update.message.reply_text("You have rejected the chat request.")
        try:
            await context.bot.send_message(
                chat_id=requester_id,
                text=f"Your chat request has been rejected by user {user_id}."
            )
        except Exception:
            pass
        del pending_chat_requests[user_id]
    else:
        await update.message.reply_text("No request from this user exists.")

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
    bot_unique_id = f"user_{user_id}"
    print(update.message)
    await update.message.reply_text(f"Hello! Your unique ID is: {bot_unique_id}")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Hello! Your unique ID is: {bot_unique_id}")
    keyboard = [
        [InlineKeyboardButton("Physiology", callback_data='physiology')],
        [InlineKeyboardButton("Anatomy", callback_data='anatomy')],
        [InlineKeyboardButton("Biochemistry", callback_data='biochemistry')],
        [InlineKeyboardButton("Histology", callback_data='histology')],
        [InlineKeyboardButton("Embryology", callback_data='embryology')],
        [InlineKeyboardButton("Health Principles", callback_data='health')]
    ]
    await update.message.reply_text("Please select your desired subject:", reply_markup=InlineKeyboardMarkup(keyboard))

async def first(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Hello, this is the first command.", reply_to_message_id=update.effective_message.id)


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(f"You selected: {query.data}")


async def send_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Replace with your desired photo URL or local path
    photo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Example.jpg/640px-Example.jpg"
    await update.message.reply_photo(photo=photo_url, caption="This is a sample photo.")


async def server_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Replace 'path/to/your/image.jpg' with the actual file path on your server
    with open(r"C:\Users\Asus\Downloads\Screenshot 2025-07-28 132304.png", 'rb') as photo:
        await update.message.reply_photo(photo=photo, caption="This image is from my server.")


async def start_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [KeyboardButton(text="profile"), KeyboardButton(text="coin")],
        [KeyboardButton(text="help")]
    ]
    reply_markup = ReplyKeyboardMarkup(
        buttons, resize_keyboard=True, one_time_keyboard=False)
    await update.message.reply_text("Please select one of the options:", reply_markup=reply_markup)


async def on_button_press(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_profiles:
        user_profiles[user_id] = {"name": "Homer", "age": 20}

    pressed_button = update.message.text

    if pressed_button == "profile":
        # Delete user's message "profile" to remove it from chat
        try:
            await update.message.delete()
        except Exception as e:
            pass  # Ignore if unable to delete
        app.add_handler(MessageHandler(
        filters.TEXT & (~filters.COMMAND), store_chat_history))
        app.add_handler(MessageHandler(
        filters.TEXT & (~filters.COMMAND), on_button_press))
    # Register relay_chat handler for forwarding messages
        app.add_handler(MessageHandler(
        filters.TEXT | filters.PHOTO | filters.Document.ALL,
        relay_chat
    ))
        app.run_polling()
        # Inline buttons shown attached to the bot's new message
        inline_buttons = [
            [InlineKeyboardButton("Change Name", callback_data="change_name")],
            [InlineKeyboardButton("Change Age", callback_data="change_age")]
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
            text="Select an option to change your profile:",
            reply_markup=inline_markup
        )

    else:
        # For other buttons, handle normally or send some message
        await update.message.reply_text(f"You selected the button: {pressed_button}.")


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
            "Please enter your new name:",
            reply_markup=ReplyKeyboardRemove()
        )
    # Your other callback_data handlers here...

# This message handler catches the next text after "Change Name" is pressed


async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if context.user_data.get("awaiting_name"):
        new_name = update.message.text.strip()
        if not new_name:
            await update.message.reply_text("Name cannot be empty. Please try again.")
            return

        user_profiles[user_id]["name"] = new_name
        context.user_data["awaiting_name"] = False  # Reset the flag

        # Send updated profile info to the user
        updated_info = f"Your profile has been updated:\nname: {new_name}, Age: {user_profiles[user_id]['age']}"
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
    # Register command handler
    app.add_handler(CommandHandler("change_photo", change_photo))

# Register photo message handler
    app.add_handler(MessageHandler(filters.PHOTO, receive_photo))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("start_2", start_2))
    app.add_handler(CommandHandler("show_profile", my_other_profile))
    app.add_handler(CommandHandler("edit_name", edit_name))
    app.add_handler(CommandHandler("change_online_status", change_online_status))
    app.add_handler(CommandHandler("chat_request", chat_request))
    app.add_handler(CommandHandler("accept_request", accept_request))
    app.add_handler(CommandHandler("reject_request", reject_request))
    # Relay chat handler: relay text, photo, and document messages between users in active chat
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO | filters.Document.ALL, relay_chat))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(
        filters.TEXT & (~filters.COMMAND), store_chat_history))
    app.add_handler(MessageHandler(
        filters.TEXT & (~filters.COMMAND), on_button_press))
    app.run_polling()
