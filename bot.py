#!/usr/bin/env python3
# 
# MIT License
# 
# Copyright (c) 2022 Joel Williams
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import logging
import json
from pyrogram import Client, filters, enums

from helpers import parse_report, build_mini_report
import config

logging.basicConfig(format='[%(asctime)s - %(levelname)s] - %(name)s - %(message)s',
                     level=logging.INFO)

logger = logging.getLogger()

userbot = Client("userbot", api_hash=config.API_HASH, api_id=config.API_ID)
apibot = Client("apibot", bot_token=config.BOT_TOKEN, api_id=config.API_ID, api_hash=config.API_HASH)


# TODO: add handler for when added to groups to track which groups to send reports to.

@userbot.on_message(filters.chat(config.SOURCE_REPORTS))
async def reports_listener(client, message):
    logger.debug(str(message))
    report = parse_report(message)
    report_json = json.dumps(report["reports"], indent=2)
    print(report_json)
    mini_report = build_mini_report(report)
    await apibot.send_message(config.TARGET_REPORTS, mini_report, parse_mode=enums.ParseMode.HTML)


apibot.start()
userbot.run()