import asyncio
import os

import dearpygui.dearpygui as dpg
import discord
from basic_async import dpg_start, dpg_stop
from dearpygui_async import DearPyGuiAsync

client = discord.Client(intents=discord.Intents.all())

dpg_async = DearPyGuiAsync(loop=client.loop)


async def send_message_from_gui_on_send():
    channel = client.get_channel(1088861021126541394)
    msg = dpg.get_value("input")
    print(msg)
    await channel.send(msg)


def get_roles():
    guild = client.get_guild(365633712945102848)
    for role in guild.roles:
        dpg.add_text(f"{role.name}:{role.id}", parent="Window")


@client.event
async def on_ready():
    print("logged in")


async def setup_hook():
    asyncio.create_task(dpg_async.start())


async def teardown():
    await client.close()


dpg_async.teardown = teardown

client.setup_hook = setup_hook

dpg_start()

dpg.add_button(
    label="Send Message",
    parent="Window",
    callback=send_message_from_gui_on_send,
    before="input",
)

dpg.add_button(label="Get Roles", parent="Window", callback=get_roles)

client.run(os.environ.get("TOKEN"))
dpg_stop()
