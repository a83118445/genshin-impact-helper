"""Utilities"""

import logging
import json
import hashlib
import time
import random
import string

import requests
from requests.exceptions import HTTPError

from config import OS_LANG

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

log = logger = logging


class _Config:
    GIH_VERSION = '1.7.0.a2'
    WBH_VERSION = '1.0.2'
    # miHoYo BBS
    APP_VERSION = '2.3.0'
    ACT_ID = 'e202009291139501'
    USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) miHoYoBBS/{}'.format(
        APP_VERSION)
    REFERER_URL = 'https://webstatic.mihoyo.com/bbs/event/signin-ys/index.html?bbs_auth_required={}&act_id={}&utm_source={}&utm_medium={}&utm_campaign={}'.format(
        'true', ACT_ID, 'bbs', 'mys', 'icon')
    ROLE_URL = 'https://api-takumi.mihoyo.com/binding/api/getUserGameRolesByCookie?game_biz={}'.format(
        'hk4e_cn')
    INFO_URL = 'https://api-takumi.mihoyo.com/event/bbs_sign_reward/info?region={}&act_id={}&uid={}'
    REWARD_URL = 'https://api-takumi.mihoyo.com/event/bbs_sign_reward/home?act_id={}'.format(
        ACT_ID)
    SIGN_URL = 'https://api-takumi.mihoyo.com/event/bbs_sign_reward/sign'
    # HoYoLAB
    OS_ACT_ID = 'e202102251931481'
    OS_REFERER_URL = 'https://webstatic-sea.mihoyo.com/ys/event/signin-sea/index.html?act_id={}'.format(
        OS_ACT_ID)
    OS_ROLE_URL = 'https://api-os-takumi.mihoyo.com/auth/api/getUserAccountInfoByLToken?t={}&ltoken={}&uid={}'
    OS_INFO_URL = 'https://hk4e-api-os.mihoyo.com/event/sol/info?lang={}&act_id={}'.format(
        OS_LANG, OS_ACT_ID)
    OS_REWARD_URL = 'https://hk4e-api-os.mihoyo.com/event/sol/home?lang={}&act_id={}'.format(
        OS_LANG, OS_ACT_ID)
    OS_SIGN_URL = 'https://hk4e-api-os.mihoyo.com/event/sol/sign?lang={}'.format(
        OS_LANG)
    # weibo
    CONTAINER_ID = '100808fc439dedbb06ca5fd858848e521b8716'
    WB_USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
    SUPER_URL = 'https://m.weibo.cn/api/container/getIndex?containerid={}'.format(
        '100803_-_page_my_follow_super')
    YS_URL = 'https://m.weibo.cn/api/container/getIndex?containerid={}_-_feed'.format(
        CONTAINER_ID)
    KA_URL = 'https://ka.sina.com.cn/innerapi/draw'
    BOX_URL = 'https://ka.sina.com.cn/html5/mybox'


class HttpRequest(object):
    def request(self,
                method: str,
                url: str,
                max_retry: int = 2,
                params=None,
                data=None,
                json=None,
                headers=None,
                **kwargs):
        for i in range(max_retry + 1):
            try:
                response = requests.Session().request(
                    method,
                    url,
                    params=params,
                    data=data,
                    json=json,
                    headers=headers,
                    **kwargs)
            except HTTPError as e:
                log.error(f'HTTP error:\n{e}')
                log.error(f'The NO.{i + 1} request failed, retrying...')
            except KeyError as e:
                log.error(f'Wrong response:\n{e}')
                log.error(f'The NO.{i + 1} request failed, retrying...')
            except Exception as e:
                log.error(f'Unknown error:\n{e}')
                log.error(f'The NO.{i + 1} request failed, retrying...')
            else:
                return response

        raise Exception(f'All {max_retry + 1} HTTP requests failed, die.')


def to_python(json_str: str):
    return json.loads(json_str)


def to_json(obj):
    return json.dumps(obj, indent=4, ensure_ascii=False)


def hexdigest(text):
    md5 = hashlib.md5()
    md5.update(text.encode())
    return md5.hexdigest()


def get_ds():
    # v2.3.0-web @povsister & @journey-ad
    n = 'h8w582wxwgqvahcdkpvdhbh2w9casgfl'
    i = str(int(time.time()))
    r = ''.join(random.sample(string.ascii_lowercase + string.digits, 6))
    c = hexdigest(f'salt={n}&t={i}&r={r}')
    return f'{i},{r},{c}'


MESSAGE_TEMPLATE = '''
    {today:#^18}
    🔅[{region_name}]{uid}
    今日奖励: {award_name} × {award_cnt}
    本月累签: {total_sign_day} 天
    签到结果: {status}
    {end:#^18}'''

req = HttpRequest()
CONFIG = _Config
CONFIG.MESSAGE_TEMPLATE = MESSAGE_TEMPLATE
