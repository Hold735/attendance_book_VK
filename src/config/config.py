"""
Модуль с конфигурационными данными
"""
import json


def read_configs() -> dict:
    #TODO: добавить проверку на существование конфигурационного файла
    with open("config/config_data.json", "r") as config_file:
        config = json.load(config_file)
    return config

def write_config(config_new: dict):
    with open("config/config_data.json", "w") as config_file:
        json.dump(config_new, config_file, indent=4)

def update_config(config_new: dict):
    #TODO: добавить проверку на существование конфигурационного файла
    config = read_configs()
    
    config.update(config_new)
    
    write_config(config_new)


config = read_configs()

VK_TOKEN = config["VK_TOKEN"]

ADMINS = config["ADMINS"]

CHAT_ID = config["CHAT_ID"]

CHAT_ID_KICK = config["CHAT_ID_KICK"]

PERCENT = config["PERCENT"]

GOOGLE_SHEET_NAME = config["GOOGLE_SHEET_NAME"]

GOOGLE_CREDENTIALS_PATH = config["GOOGLE_CREDENTIALS_PATH"]
