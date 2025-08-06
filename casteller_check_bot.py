import re
from PIL import Image
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters, _contexttypes,ConversationHandler,Updater, CallbackContext, Application
import pytz
import os
import json
import datetime
from openai import OpenAI
timezone = pytz.timezone("UTC")
TOKEN = '7673808687:AAFDC11CSpQLYKMZnZPmo0nsWK7Ex09hX2Y'
tags_list = ["Physician","Surgeon","Pediatrician","Psychiatrist","Dentist","Pharmacist","Nurse","Physical Therapist","occupational Therapist","Audiologist","Ultrasound Technician","Health Administrator","Medical Director","Chief Medical Officer","Clinical Information Specialist","Business Analyst","Chief Technology Officer","Data Scientist","Compliance Professional","Cyber Architect", "Entrance exam"]
os.chdir("D:\Researches\AI\Casteller\profiles")





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


def search_tag(tag):
    with open("profiles.json", "r") as file:
        profiles = json.load(file)
    matching_profiles = []
    for bot_id, profile in profiles.items():
        if tag in profile["tags"]:
            matching_profiles.append(bot_id)
    return matching_profiles


async def end_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text("Conversation ended.")
    return ConversationHandler.END




async def my_other_profile(update: Update, context: ContextTypes.DEFAULT_TYPE, input_id):
    bot_id = f"user_{update.effective_user.id}"
    if input_id == bot_id:
        await show_my_profile(update, context)  
    else:
        await return_profile(update, context, input_id)


async def show_my_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
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

    caption = f"""ID: /{bot_id}
Name: {profile_name}
Online_status: {profile_online_status}
Monthly questionnaires: {mq}
Tags: {profile_tags}"""
    with open(profiles[f"{bot_id}"]["photo"], 'rb') as photo:
        await update.message.reply_photo(photo=photo, caption=caption)

active_chats = {}
async def return_profile(update: Update, context: ContextTypes.DEFAULT_TYPE, bot_id):
    with open("profiles.json", "r") as file:
        profiles = json.load(file)  
    
    if f"{bot_id}" not in profiles:
        print(f"there is no profile with the ID: {bot_id}")
        return
    profile_name = profiles[bot_id]["name"]
    profile_online_status = profiles[bot_id]["online_status"]
    profile_tags = profiles[bot_id]["tags"]
    mq = count_last_30_days_questionnaires(profiles[bot_id]["questionnaires"])

    caption = f"""ID: /{bot_id}
Name: {profile_name}
Online_status: {profile_online_status}
Monthly questionnaires: {mq}
Tags: {profile_tags}"""
    keyboard = [
    [
        InlineKeyboardButton("DM them", callback_data=f"dm_request_{bot_id}")
    ]
]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    with open(profiles[f"{bot_id}"]["photo"], 'rb') as photo:
        await update.message.reply_photo(photo=photo, caption=caption, reply_markup=reply_markup)
    
async def button_callback(update, context):
    query = update.callback_query
    await query.answer()  # Acknowledge the callback query

    data = query.data
    if data.startswith("dm_request_"):
        target_user_id = str(data[len("dm_request_user_"):])
        user_id = int(update.effective_user.id)  # Extract user ID from the bot's ID
        await chat_request(update, context, user_id, target_user_id)  # Define this function according to your logic



async def handle_user_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    # Extract the user ID from the command, e.g. /user_123456 -> 123456
    match = re.match(r'^/user_(\d+)$', text)
    if match:
        user_id = match.group(1)
        # Here you implement logic to show the profile related to user_id
        # For demonstration, we just reply with the extracted user_id
        await update.message.reply_text(f"Showing profile for user ID: {user_id}")
        await my_other_profile(update, context, f"user_{user_id}")
    else:
        # In case pattern does not match exactly — optional fallback
        await update.message.reply_text("Invalid user command format.")




def count_last_30_days_questionnaires(data):
    today = datetime.datetime.today()
    thirty_days_ago = today - datetime.timedelta(days=30)

    count = 0
    for timestamp_str in data.values():
        timestamp = datetime.datetime.fromisoformat(timestamp_str)
        if thirty_days_ago <= timestamp <= today:
            count += 1

    return count


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
    with open("profiles.json", "r") as file:
        profiles = json.load(file)  
    profile_path = profiles[f"{bot_id}"]["photo"]
    context.user_data["awaiting_photo"] = True # Flag to indicate that the bot is waiting for a photo
    await update.message.reply_text("Please send your new profile photo.", reply_to_message_id=update.effective_message.id) # Ask the user to send a photo


async def receive_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):    
    """Handles the reception of a photo from the user.
    Saves it to the user's profile directory.
    """
    # Check if the user is currently uploading a photo
    if context.user_data.get("awaiting_photo"): 
        bot_id = f"user_{update.effective_user.id}"
        with open("profiles.json", "r") as file:
            profiles = json.load(file)  
        profile_path = profiles[f"{bot_id}"]["photo"]
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



pending_chat_requests = {}
async def chat_request(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int, target_user_id: str):
    with open("profiles.json", "r") as file:
        profiles = json.load(file)

    pending_chat_requests[target_user_id] = user_id

    try:
        await context.bot.send_message(
            chat_id=int(target_user_id),
            text=(
                f"You have received a chat request from /user_{user_id}.\n"
                f"To accept: /accept_request {user_id}\n"
                f"To reject: /reject_request {user_id}"
            )
        )
        # Safely reply to callback query or fallback
        query = update.callback_query
        if query and query.message:
            await query.message.reply_text("Your request has been sent.")
        else:
            # fallback to sending a direct message to the sender
            await context.bot.send_message(chat_id=user_id, text="Your request has been sent.")
    except Exception as e:
        print(f"Error sending chat request: {e}")
        query = update.callback_query
        if query and query.message:
            await query.message.reply_text(
                "Could not send the request to the user. Maybe they haven't started the bot."
            )
        else:
            await context.bot.send_message(chat_id=user_id, text="Could not send the request to the user. Maybe they haven't started the bot.")
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
    print(requester_id) # Debugging line to check requester_id
    print(partner_id) # Debugging line to check partner_id
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
    
    bot_id = f"user_{update.effective_user.id}"
    with open("profiles.json", "r") as file:
        profiles = json.load(file)
    
    profiles[f"{bot_id}"]["questionnaires"][f"user_{requester_id}"] = datetime.datetime.now().isoformat()
    with open("profiles.json", "w", encoding="utf-8") as file:
        json.dump(profiles, file, indent=4)


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










if __name__ == "__main__":
    print("ربات در حال اجراست...")
    app = ApplicationBuilder().token(TOKEN).build()
    
    user_command_pattern = r'^/user_\d+$'
    user_command_handler = MessageHandler(filters.Regex(user_command_pattern), handle_user_command)
    app.add_handler(user_command_handler)
    
    conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start_3rd", start_3rd)],
    states={
        WAITING_FOR_TEXT: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, get_tag)],},fallbacks=[CommandHandler("cancel", end_conversation)],)
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("change_tags", change_tags))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(CommandHandler("start_3rd", start_3rd))
    app.add_handler(CommandHandler("change_photo", change_photo))
    app.add_handler(MessageHandler(filters.PHOTO, receive_photo))
    app.add_handler(CommandHandler("show_profile", show_my_profile))
    app.add_handler(CommandHandler("edit_name", edit_name))
    app.add_handler(CommandHandler("change_online_status", change_online_status))
    app.add_handler(CommandHandler("chat_request", chat_request))
    app.add_handler(CommandHandler("accept_request", accept_request))
    app.add_handler(CommandHandler("reject_request", reject_request))
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO | filters.Document.ALL, relay_chat))
    app.add_handler(CommandHandler("get_tag", get_tag))
    app.run_polling()
