from PIL import Image
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters, _contexttypes,ConversationHandler,Updater, CallbackContext, Application
import pytz
import os
import json
import datetime
from datetime import datetime, timedelta
from openai import OpenAI
timezone = pytz.timezone("UTC")
TOKEN = '7673808687:AAFDC11CSpQLYKMZnZPmo0nsWK7Ex09hX2Y'
tags_list = ["Physician","Surgeon","Pediatrician","Psychiatrist","Dentist","Pharmacist","Nurse","Physical Therapist","occupational Therapist","Audiologist","Ultrasound Technician","Health Administrator","Medical Director","Chief Medical Officer","Clinical Information Specialist","Business Analyst","Chief Technology Officer","Data Scientist","Compliance Professional","Cyber Architect", "Entrance exam"]
os.chdir("D:\Researches\AI\Casteller\profiles")


def count_last_30_days_questionnaires(data):
    today = datetime.today()
    thirty_days_ago = today - timedelta(days=30)

    count = 0
    for timestamp_str in data.values():
        timestamp = datetime.fromisoformat(timestamp_str)
        if thirty_days_ago <= timestamp <= today:
            count += 1

    return count


def search_tag(tag):
    with open("profiles.json", "r") as file:
        profiles = json.load(file)
    matching_profiles = []
    for bot_id, profile in profiles.items():
        if tag in profile["tags"]:
            matching_profiles.append(bot_id)
    return matching_profiles


WAITING_FOR_TEXT = 1
async def start_3rd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    user = update.effective_user
    user_id = user.id
    bot_id = f"user_{update.effective_user.id}"
    profiles_path = f"D:\Researches\AI\Casteller\Profiles\photos"
    
    

    try:
        with open("profiles.json", "r") as file:               
            profiles = json.load(file)
    except Exception:
        profiles = {}

    if f"{bot_id}" in profiles:
        pass
    else:
        photos = await context.bot.get_user_profile_photos(user_id)
        if photos.total_count > 0:
            file_id = photos.photos[0][0].file_id
            file = await context.bot.get_file(file_id)
            file_path = f"{profiles_path}\{bot_id}.png"
            await file.download_to_drive(file_path)  # Async download to disk
            photo_saved = True
        else:
            image = Image.new("RGB", (800, 600), (255, 255, 255))
            image.save(f"{profiles_path}\{bot_id}.png", "PNG")
        profiles[f"{bot_id}"] = {
            "name": user.first_name,
            "photo": f"{profiles_path}\{bot_id}.png",
            "tags": [],
            "online_status": "Online",
            "questionnaires": {}
        }
        with open("profiles.json", "w") as json_file:
            json.dump(profiles, json_file, indent=4)

    await context.bot.send_message(chat_id=update.effective_chat.id, text="""Hello, send your question so i can find the relevant specialist for you.
NOTE: Your message should be a text-only_message, which indicates the major field of your question.""", reply_to_message_id=update.effective_message.id)
    
    return WAITING_FOR_TEXT


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
    print(tag)
    for i in search_tag(tag):
        await return_profile(update, context, i)
    return ConversationHandler.END


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
    
    bot_id = f"user_{update.effective_user.id}"
    with open("profiles.json", "r") as file:
        profiles = json.load(file)

    if f"{bot_id}" not in profiles:
        await update.message.reply_text("You have not created a profile yet. Please create your profile first using /start_3rd.")
        return
    
    profile_name = profiles[bot_id]["name"]
    profile_online_status = profiles[bot_id]["online_status"]
    profile_tags = profiles[bot_id]["tags"]
    mq = count_last_30_days_questionnaires(profiles[bot_id]["questionnaires"])

    caption = f"""Name: {profile_name}
Online_status: {profile_online_status}
Monthly questionnaires: {mq}
Tags: {profile_tags}"""
    with open(profiles[f"{bot_id}"]["photo"], 'rb') as photo:
        await update.message.reply_photo(photo=photo, caption=caption)


async def show_other_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):

    bot_id = f"user_{context.args[0]}" 
    with open("profiles.json", "r") as file:
        profiles = json.load(file)

    if f"{bot_id}" not in profiles:
        await update.message.reply_text("You have not created a profile yet. Please create your profile first using /start_3rd.")
        return
    
    profile_name = profiles[bot_id]["name"]
    profile_online_status = profiles[bot_id]["online_status"]
    profile_tags = profiles[bot_id]["tags"]
    mq = count_last_30_days_questionnaires(profiles[bot_id]["questionnaires"])

    caption = f"""Name: {profile_name}
Online_status: {profile_online_status}
Monthly questionnaires: {mq}
Tags: {profile_tags}"""
    with open(profiles[f"{bot_id}"]["photo"], 'rb') as photo:
        await update.message.reply_photo(photo=photo, caption=caption)


async def return_profile(update: Update, context: ContextTypes.DEFAULT_TYPE, bot_id):
    """Returns the profile of the user with the given bot_id."""
    with open("profiles.json", "r") as file:
        profiles = json.load(file)  
    if f"{bot_id}" not in profiles:
        return None
    profile_name = profiles[bot_id]["name"]
    profile_online_status = profiles[bot_id]["online_status"]
    profile_tags = profiles[bot_id]["tags"]
    mq = count_last_30_days_questionnaires(profiles[bot_id]["questionnaires"])

    caption = f"""Name: {profile_name}
Online_status: {profile_online_status}
Monthly questionnaires: {mq}
Tags: {profile_tags}"""
    with open(profiles[f"{bot_id}"]["photo"], 'rb') as photo:
        await update.message.reply_photo(photo=photo, caption=caption)
    

async def edit_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    bot_id = f"user_{update.effective_user.id}"


    # Get the new name from the command argument (e.g., /edit_name NewName)
    args = context.args
    if not args:
        await update.message.reply_text("Please enter the new name after the command. Example: /edit_name New_Name")
        return

    new_name = " ".join(args).strip()
    if not new_name:
        await update.message.reply_text("Name cannot be empty. Please try again.")
        return

    # Load the profiles from the JSON file
    with open("profiles.json", "r") as file:
        profiles = json.load(file)
    # Check if the user has a profile
    if f"{bot_id}" not in profiles:
        await update.message.reply_text("You have not created a profile yet. Please create your profile first using /start_3rd.")
        return
    # Update the name in the profile
    profiles[bot_id]["name"] = new_name
    # Save the updated profiles back to the JSON file
    with open("profiles.json", "w") as file:
        json.dump(profiles, file, indent=4) 
    
    await update.message.reply_text(f"Your name has been changed to {new_name}.")


async def change_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_id = f"user_{update.effective_user.id}"
    profile_path = f"D:\\Researches\\AI\\Casteller\\Profiles\\photos\\{bot_id}"
    context.user_data["awaiting_photo"] = True # Flag to indicate that the bot is waiting for a photo
    await update.message.reply_text("Please send your new profile photo.", reply_to_message_id=update.effective_message.id) # Ask the user to send a photo


async def receive_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):    
    """Handles the reception of a photo from the user.
    Saves it to the user's profile directory.
    """
    # Check if the user is currently uploading a photo
    if context.user_data.get("awaiting_photo"): 
        bot_id = f"user_{update.effective_user.id}"
        profile_path = f"D:\\Researches\\AI\\Casteller\\Profiles\\photos\\{bot_id}.png"
        image = await update.message.photo[-1].get_file()  # Get Telegram File object
        await image.download_to_drive(profile_path)            # Download to disk as PNG file (the extension just defines file type)
        context.user_data["awaiting_photo"] = False
        await update.message.reply_text("Your profile photo has been updated successfully.")
    else:
        await update.message.reply_text("You are not currently uploading a photo. Please use /change_photo to start the process.")


async def change_online_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    

    bot_id = f"user_{update.effective_user.id}"
    with open("profiles.json", "r") as file:
        profiles = json.load(file)
    # Check if the user has a profile
    if f"{bot_id}" not in profiles:
        await update.message.reply_text("You have not created a profile yet. Please create your profile first using /start_3rd.")
        return
    # Update the name in the profile
    if profiles[bot_id]["online_status"] == "Online":
        new_status = "Offline"
    else:
        new_status = "Online"
    profiles[bot_id]["online_status"] = new_status
    # Save the updated profiles back to the JSON file
    with open("profiles.json", "w") as file:
        json.dump(profiles, file, indent=4) 

    
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
        await start_private_chat(requester_id, user_id, update, context)
    else:
        await update.message.reply_text("No request from this user exists.")


async def start_private_chat(requester_id, partner_id, update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    with open(profile_path_chat_history, 'r', encoding='utf-8') as file:
        a = json.load(file)
    print(type(a))
    a[f"{requester_id}"] = datetime.datetime.now().isoformat()
    with open(profile_path_chat_history, "w", encoding="utf-8") as file:
        json.dump(a, file, indent=4)


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


async def end_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text("Conversation ended.")
    return ConversationHandler.END


user_selections = {}
MAX_SELECTIONS = 3
def build_keyboard(selected_buttons):
    keyboard = []
    row = []
    for i, name in enumerate(tags_list, start=1):
        text = name
        if i in selected_buttons:
            text = f"✅ {text}"
        callback_data = f"toggle_{i}"
        row.append(InlineKeyboardButton(text, callback_data=callback_data))
        
        # Put 5 buttons per row for better layout
        if i % 1 == 0:
            keyboard.append(row)
            row = []

    # Add "Done" button on a separate row
    keyboard.append([InlineKeyboardButton("Done", callback_data="done")])
    return InlineKeyboardMarkup(keyboard)


async def change_tags(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_selections[user_id] = set()
    keyboard = build_keyboard(user_selections[user_id])
    await update.message.reply_text("Please select up to 3 options:", reply_markup=keyboard)


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if user_id not in user_selections:
        user_selections[user_id] = set()

    data = query.data
    
    if data == "done":
        selected = user_selections[user_id]
        selection_text = ", ".join(tags_list[i-1] for i in sorted(selected)) or "Nothing"
        selection_list = selection_text.split(", ")
        bot_id = f"user_{user_id}"
        with open("profiles.json", "r") as file:
            profiles = json.load(file)
        profiles[bot_id]["tags"] = selection_list
        with open("profiles.json", "w") as file:
            json.dump(profiles, file, indent=4)
        await query.edit_message_text(text=f"Tags changed to: {selection_text}")
        user_selections[user_id] = set()
    elif data.startswith("toggle_"):
        option_num = int(data.split("_")[1])
        selected = user_selections[user_id]

        if option_num in selected:
            selected.remove(option_num)
        else:
            if len(selected) < MAX_SELECTIONS:
                selected.add(option_num)
            else:
                await query.answer(text=f"Max {MAX_SELECTIONS} selections allowed", show_alert=True)
                return

        keyboard = build_keyboard(selected)
        await query.edit_message_reply_markup(reply_markup=keyboard)


if __name__ == "__main__":
    print("ربات در حال اجراست...")
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start_3rd", start_3rd)],
    states={
        WAITING_FOR_TEXT: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, get_tag)
        ],
    },
    fallbacks=[CommandHandler("cancel", end_conversation)],
)

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("change_tags", change_tags))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(CommandHandler("start_3rd", start_3rd))
    app.add_handler(CommandHandler("show_chat_history", show_chat_history))
    app.add_handler(CommandHandler("change_photo", change_photo))
    app.add_handler(MessageHandler(filters.PHOTO, receive_photo))
    app.add_handler(CommandHandler("start_2", start_2))
    app.add_handler(CommandHandler("show_profile", my_other_profile))
    app.add_handler(CommandHandler("edit_name", edit_name))
    app.add_handler(CommandHandler("change_online_status", change_online_status))
    app.add_handler(CommandHandler("chat_request", chat_request))
    app.add_handler(CommandHandler("accept_request", accept_request))
    app.add_handler(CommandHandler("reject_request", reject_request))
    # Relay chat handler: relay text, photo, and document messages between users in active chat
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO | filters.Document.ALL, relay_chat))
    app.add_handler(CommandHandler("get_tag", get_tag))
    app.add_handler(MessageHandler(
        filters.TEXT & (~filters.COMMAND), on_button_press))
    app.run_polling()
