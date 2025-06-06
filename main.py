from pyrogram import Client, filters
from pyrogram.types import ForceReply
import config
import datetime
import random
import json
from FusionBrain_AI import generate
import base64
import keyboards

bot = Client(
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    name="programm_bot"
)
def button_filter(button):
    async def func(_,__, msg):
        return msg.text == button.text
    return filters.create(func, 'ButtonFilter', button=button)

@bot.on_message(filters.command('start'))
async def start(bot, message):
    await message.reply('Welcome!',
                        reply_markup=keyboards.kb_main)
    with open('users.json', 'r') as file:
        users = json.load(file)
    if str(message.from_user.id) not in users.keys():
        users[message.from_user.id] = 100
        with open('users.json', 'w') as file:

            json.dump(users, file)

@bot.on_message(filters.command('info')  |  button_filter(keyboards.btn_info))
async def info(bot, message):
    await message.reply('Hello! Here is a command and knowledge list of this bot')

@bot.on_message(filters.command('time'))
async def time(bot, message):
    await message.reply(f'Current date and time: {datetime.datetime()}')

query_text = 'Enter a prompt to generate images'
@bot.on_message(button_filter(keyboards.btn_image))
async def image_command(bot, message):
    await message.reply(query_text, reply_markup=ForceReply(True))

@bot.on_message(filters.command('games'))
async def games(bot, message):
    await message.reply('Chose your game', reply_markup=keyboards.kb_games)

@bot.on_message(filters.command('back'))
async def back(bot, message):
    await message.reply('Return to main menu',reply_markup=keyboards.kb_main)

@bot.on_message(filters.command('quest')  |  button_filter(keyboards.btn_quest))
async def kvest(bot, message):
    await message.reply_text('Do you want to go to an interesting adventure full of mysteries?',
                             reply_markup=keyboards.inline_kb_start_quest)

@bot.on_message(filters.reply)
async def reply(bot, message):
    if message.reply_to_message.text == query_text:
        query = message.text
        await message.reply_text(f'Generating image to prompt **{query}**. Wait time within a minute')
        images = await generate(query)
        if images:
            image_data = base64.b64decode(images[0])
            img_num = random.randint(1, 99)
            with open(f"images/image{img_num}.jpg", "wb") as file:
                file.write(image_data)
            await bot.send_photo(message.chat.id, f'image/image{img_num}.jpg',
                                            reply_to_message_id=message.id,
                                            reply_markup=keyboards.kb_main)
        else:
            await message.reply_text('Occured an error, try again',
                                            reply_to_message_id=message.id,
                                            reply_markup=keyboards.kb_main)

@bot.on_callback_query()
async def handle_query(bot, query):
    if query.data == 'start_quest':
        await bot.answer_callback_query(query.id,
            text='Welcome to the quest that is called the hunt of the lost treasure',
            show_alert=True)
        await query.message.reply_text('You are standing in front of two doors. Which one would you chose?:',
                    reply_markup=keyboards.inline_kb_choice_door)
    elif query.data == 'left_door':
        await query.message.reply_text('You enter the room and see a golden dragon. You have two choices:',
                                       reply_markup=keyboards.inline_kb_left_door)
    elif query.data =='right_door':
        await query.message.reply_text('You enter the room, that is filled with treasures! But you can chose only one of them',
                                       reply_markup=keyboards.inline_kb_right_door)
    elif query.data == 'front_door':
        await query.message.reply_text('You enter a grey room that has tho levitating objects. You can touch only one, if you dare so.',
                                       reply_markup=keyboards.inline_kb_front_door)
    elif query.data == 'trapdoor':
        await query.message.reply_text('As you jump in to the trapdoor, you appear in the same room, but there are only two doors and the trap door above you disappears.')

    elif query.data == 'dragon':
        await bot.answer_callback_query(query.id, text='You fight with the dragon, but he turns out to be more powerfull than expected. You die',
                                                show_alert=True)
    elif query.data == 'run':
        await bot.answer_callback_query(query.id, text='You try to run away, but he catches you and eats you.',
                                                show_alert=True)
    elif query.data == 'gold_crown':
        await bot.answer_callback_query(query.id, text='You take the golden crown and exit the room. Congrats! You won the game',
                                                show_alert=True)
    elif query.data == 'silver_dagger':
        await bot.answer_callback_query(query.id, text='You take the silver dagger and exit the room. Unfortunatly its has no cost',
                                                show_alert=True)
    elif query.data == 'old_book':
        await bot.answer_callback_query(query.id, text='You take an old book and exit the room. Actually, the book was magical! As you open it, you disappear.',
                                                show_alert=True)
    elif query.data == 'shiny_object':
        await bot.answer_callback_query(query.id, text='As you touch it, you feel dizzy and eventually lose your mind.',
                                                show_alert=True)
    elif query.data == 'very_dark_object':
        await bot.answer_callback_query(query.id, text='As you touch it, it starts to convert you in a dark mass.',
                                                show_alert=True)
    elif query.data == 'a_door':
        await bot.answer_callback_query(query.id, text='As you touch the doors handle, something wispers you to get out of here by getting back. You trust its words and behind you appears another door. Congrats! you won the game.',
                                                show_alert=True)
    elif query.data == 'another_door':
        await bot.answer_callback_query(query.id, text='As you open the door, you appear in the same room again, you continue to open all of the doors in all of the rooms but nothing changes, suddenly you feel dizzy and eventually pass away.',
                                                show_alert=True)


bot.run()