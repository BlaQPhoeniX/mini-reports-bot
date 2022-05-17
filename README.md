# Mini Reports Bot

Simple telegram bot to automatically generate a summarised battle report summary for any instance of Chat Wars.

## Description

This bot will listen to battle reports from a specified channel and then automatically generate and post a summarised miniature version for easy consumption. Eventually will make the bot addable to any group and have it automatically post the miniature report in the subscribed group.

## Getting Started

### Dependencies

* Telegram API ID and HASH.
* Telegram account with access to the source report channel.
* Bot token (from [@BotFather](https://t.me/botfather) for bot that has posting permissions in target channel.

### Installing

```
$ pipenv sync
```

### Configuration

* Copy the example `config.py`
```
cp config.py.example config.py
```
* Add relevant configurations
```python
API_ID = 69999
API_HASH = "123456789abcdefghijklmnopqrstuvw"

BOT_TOKEN = "696942069:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"

SOURCE_REPORTS = "ChatWarsReports"
TARGET_REPORTS = "cweminireports"
```
* Save 

### Executing program

```
$ pipenv run python3 bot.py
```

## Authors

[J J](https://t.me/smtgthot)

## Version History
* 0.1
    * Initial Release

## License

This project is licensed under the MIT License - see the LICENSE.md file for details
