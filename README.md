# dearpygui_async

[![PyPI - Version](https://img.shields.io/pypi/v/dearpygui-async.svg)](https://pypi.org/project/dearpygui-async)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dearpygui-async.svg)](https://pypi.org/project/dearpygui-async)

A simple way to integrate some async functionality into your dearpygui application.

## Key Features

* Ease of use
* Async callbacks
* Setup & Teardown functions for use with other async applications

## Installation

```console
pip install dearpygui-async
```
### Note: you will need to install dearpygui separately in order to use this!


## Simple Example

```py
import asyncio
import dearpygui.dearpygui as dpg
from dearpygui_async import DearPyGuiAsync # import

dpg_async = DearPyGuiAsync() # initialize

async def save_callback():
    await asyncio.sleep(3)
    print("Save Clicked")

dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()

with dpg.window(label="Example Window"):
    dpg.add_text("Hello world")
    dpg.add_button(label="Save", callback=save_callback)
    dpg.add_input_text(label="string")
    dpg.add_slider_float(label="float")

dpg.show_viewport()
dpg_async.run() # run; replaces `dpg.start_gui()`
dpg.destroy_context()

```

## License

`dearpygui-async` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
