'''
A more useful use case to add a GUI to a discord bot using discord.py (https://discordpy.readthedocs.io)
'''

import os

import dearpygui.dearpygui as dpg
import discord
from basic_async import dpg_start, dpg_stop
from dearpygui_async import DearPyGuiAsync

dpg_async = DearPyGuiAsync()

client = discord.Client(intents=discord.Intents.all())

async def send_message_from_gui_on_send():
    channel = client.get_channel(1088861021126541394) # replace with your guild ID
    msg = dpg.get_value("input")
    print(f'Sent Message: {msg}')
    await channel.send(msg)


def get_roles():
    guild = client.get_guild(365633712945102848) # replace with your channel ID
    for role in guild.roles:
        dpg.add_text(f"{role.name}:{role.id}", parent="Window")


@client.event
async def on_ready():
    print("logged in")

@client.event
async def on_message(message:discord.Message):
    slider_value = dpg.get_value('slider')
    dpg.set_value('slider', slider_value+1)


async def setup():
        await client.start(os.environ.get("TOKEN"))


async def teardown():
    await client.close()

dpg_async.teardown = teardown

dpg_async.setup = setup

dpg_start()

dpg.add_button(
    label="Send Message",
    parent="Window",
    callback=send_message_from_gui_on_send,
    before="input",
)

dpg.add_button(label="Get Roles", parent="Window", callback=get_roles)

dpg_async.run()
dpg_stop()
