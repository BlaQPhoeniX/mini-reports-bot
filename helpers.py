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

import re
import pytz

report_re = re.compile(r"""^(?P<icon>🔱?🛡|⚔) (?:Battle )?[Aa]t (?P<castle>.*?) (?:the )?(?:defenders|warriors|was).*(?P<battle>easily fought off|slight edge|break into|slightly stronger|wiped out|stood victorious).*$
^.*$
^.*$
🏆Attackers have (?P<status>pillaged|lost).*?(?P<gold>\d+) gold(?: and (?P<stock>\d+) stock)?\.$""", re.M | re.U)

bored_re = re.compile(r"""^(?P<icon>🛡) Defenders of (?P<castle>.*?) were (?P<battle>bored) - no one has attacked them.""", re.M | re.U)

warmoji_map = {
    "easily fought off": "👌",
    "slight edge": "⚡️",
    "break into": " ",
    "bored": "😴",
    "slightly stronger": "⚡️",
    "wiped out": "😎",
    "stood victorious": " "
}


def parse_report(report):
    report_text = report.text
    report_json = {}

    report_date = report_text.splitlines()[0]
    report_json["date"] = report_date
    report_json["original_date"] = report.date
    # TODO: fix link generation, not working for some reason?
    report_json["link"] = f"http://t.me/{report.sender_chat}/{report.id}"

    for line in report_text.splitlines():
        if line.startswith("Scores"):
            report_json["scores"] = ""
            continue
        if "scores" in report_json:
            report_json["scores"] += f"{line}\n"

    matches = report_re.finditer(report_text)
    report_json["reports"] = [m.groupdict() for m in matches]
    matches = bored_re.finditer(report_text)
    for m in matches:
        report_json["reports"].append(m.groupdict())

    for stanza in report_json["reports"]:
        if "status" in stanza:
            if stanza["status"] == "pillaged":
                stanza["gold"] = -1*int(stanza["gold"])
                stanza["stock"] = -1*int(stanza["stock"])
            else:
                stanza["gold"] = int(stanza["gold"])
                del stanza["stock"]
            del stanza["status"]
        else:
            # TODO: better handling of bored defender designation 
            stanza["gold"] = 0
        # TODO: use the proper crossed sword emoji with variation selector
        stanza["warmoji"] = f"{stanza['icon']}{warmoji_map[stanza['battle']]}"
    return report_json


def build_mini_report(report_json):
    mini_report = "<b>⛳️Battle results:</b>\n"
    for stanza in sorted(report_json["reports"], key=lambda x: x["gold"], reverse=True):
        # TODO: find better way to get castle emoji, current method cuts off variation selector
        if stanza["gold"] != 0:
            mini_report += f'{stanza["castle"][0]}: {stanza["warmoji"]} {stanza["gold"]:+d}💰 '
        else:
            mini_report += f'{stanza["castle"][0]}: {stanza["warmoji"]}'
        if "stock" in stanza:
            mini_report += f'{stanza["stock"]}📦\n'
        else:
            mini_report += "\n"
    
    mini_report += "\n<b>🏆Scores:</b>\n<i>"
    mini_report += report_json["scores"]
    mini_report += "</i>"
    mini_report += f'\n\n<a href="{report_json["link"]}">Battle</a> {report_json["date"]}\n'
    # TODO: automatically detect system timezone instead of hardcoded
    SAST = pytz.timezone("Africa/Harare")
    report_date = report_json["original_date"].replace(minute=0, tzinfo=SAST).astimezone(tz=pytz.UTC)
    mini_report += f'{report_date:%d/%m/%y %H:%M %Z}'

    return mini_report
