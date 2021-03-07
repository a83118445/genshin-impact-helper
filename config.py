"""Configuration"""

import os

# ***** BEGIN CONFIG BLOCK *****
# Github Actions users please go to
# Repo's Settings->Secrets to set the variables, the name of the variable
# MUST be the same as the name of the following parameter variable,
# otherwise it is invalid!!!
# e.g. Name=COOKIE, Value=<cookie>
#
# Github Actions用户请到Repo的Settings->Secrets里设置变量,变量名字必须与下面的参数变量名字完全一致,否则无效!!!
# 例如: Name=<变量名字>, Value=<获取的值>

# Cookie from https://bbs.mihoyo.com/ys/
COOKIE = ''
# Cookie from https://www.hoyolab.com/genshin/
OS_COOKIE = ''
# Language
OS_LANG = 'en-us'
# Cookie from https://m.weibo.cn
WB_COOKIE = ''
# Cookie from https://ka.sina.com.cn
KA_COOKIE = ''

# Server Chan
SCKEY = ''

# Cool Push
COOL_PUSH_SKEY = ''
COOL_PUSH_MODE = 'send'

# iOS Bark App
BARK_KEY = ''
BARK_SOUND = 'healthnotification'

# Telegram Bot
TG_BOT_TOKEN = ''
TG_USER_ID = ''

# DingTalk Bot
DD_BOT_TOKEN = ''
DD_BOT_SECRET = ''

# WeChat Work Bot
WW_BOT_KEY = ''

# WeChat Work App
WW_ID = ''
WW_APP_SECRET = ''
WW_APP_USERID = '@all'
WW_APP_AGENTID = ''

# iGot
IGOT_KEY = ''

# pushplus
PUSH_PLUS_TOKEN = ''
PUSH_PLUS_USER = ''

# Custom Push Config
PUSH_CONFIG = ''

# ***** END CONFIG BLOCK *****

if 'LANG' in os.environ:
    LANG = os.environ['LANG']

if 'COOKIE' in os.environ:
    COOKIE = os.environ['COOKIE']
if 'OS_COOKIE' in os.environ:
    OS_COOKIE = os.environ['OS_COOKIE']
if 'WB_COOKIE' in os.environ:
    WB_COOKIE = os.environ['WB_COOKIE']
if 'KA_COOKIE' in os.environ:
    KA_COOKIE = os.environ['KA_COOKIE']

if 'SCKEY' in os.environ:
    SCKEY = os.environ['SCKEY']

if 'COOL_PUSH_SKEY' in os.environ:
    COOL_PUSH_SKEY = os.environ['COOL_PUSH_SKEY']
if 'COOL_PUSH_MODE' in os.environ:
    COOL_PUSH_MODE = os.environ['COOL_PUSH_MODE']

if 'BARK_KEY' in os.environ:
    # customed server
    if os.environ['BARK_KEY'].find(
            'https') != -1 or os.environ['BARK_KEY'].find('http') != -1:
        BARK_KEY = os.environ['BARK_KEY']
    else:
        BARK_KEY = f"https://api.day.app/{os.environ['BARK_KEY']}"
# official server
elif BARK_KEY and BARK_KEY.find('https') == -1 and BARK_KEY.find('http') == -1:
    BARK_KEY = f'https://api.day.app/{BARK_KEY}'
if 'BARK_SOUND' in os.environ:
    BARK_SOUND = os.environ['BARK_SOUND']

if 'TG_BOT_TOKEN' in os.environ:
    TG_BOT_TOKEN = os.environ['TG_BOT_TOKEN']
if 'TG_USER_ID' in os.environ:
    TG_USER_ID = os.environ['TG_USER_ID']

if 'DD_BOT_TOKEN' in os.environ:
    DD_BOT_TOKEN = os.environ['DD_BOT_TOKEN']
if 'DD_BOT_SECRET' in os.environ:
    DD_BOT_SECRET = os.environ['DD_BOT_SECRET']

if 'WW_BOT_KEY' in os.environ:
    WW_BOT_KEY = os.environ['WW_BOT_KEY']

if 'WW_ID' in os.environ:
    WW_ID = os.environ['WW_ID']
if 'WW_APP_SECRET' in os.environ:
    WW_APP_SECRET = os.environ['WW_APP_SECRET']
if 'WW_APP_USERID' in os.environ:
    WW_APP_USERID = os.environ['WW_APP_USERID']
if 'WW_APP_AGENTID' in os.environ:
    WW_APP_AGENTID = os.environ['WW_APP_AGENTID']

if 'IGOT_KEY' in os.environ:
    IGOT_KEY = os.environ['IGOT_KEY']

if 'PUSH_PLUS_TOKEN' in os.environ:
    PUSH_PLUS_TOKEN = os.environ['PUSH_PLUS_TOKEN']
if 'PUSH_PLUS_USER' in os.environ:
    PUSH_PLUS_USER = os.environ['PUSH_PLUS_USER']

if 'PUSH_CONFIG' in os.environ:
    PUSH_CONFIG = os.environ['PUSH_CONFIG']
