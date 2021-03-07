import time
import uuid

from .utils import CONFIG, log, req, to_python, get_ds


class Base(object):
    def __init__(self, cookie: str = None):
        self._cookie = cookie
        self._user_agent = CONFIG.WB_USER_AGENT
        self._referer = CONFIG.OS_REFERER_URL
        self._info_url = CONFIG.OS_INFO_URL
        self._reward_url = CONFIG.OS_REWARD_URL
        self._sign_url = CONFIG.OS_SIGN_URL

    def get_header(self):
        header = {
            'Cookie': self._cookie,
            'User-Agent': self._user_agent,
            'Referer': self._referer,
            'Accept-Encoding': 'gzip, deflate, br'
        }
        return header

    def get_info(self):
        log.info('准备获取签到信息...')
        response = {}
        try:
            response = to_python(
                req.request('get', self._info_url, headers=self.get_header())
                .text)
        except Exception as e:
            raise Exception(e)

        log.info('签到信息获取完毕')
        return response

    def get_rewards(self):
        response = {}
        try:
            response = to_python(
                req.request(
                    'get', self._reward_url, headers=self.get_header()).text)
        except Exception as e:
            raise Exception(e)

        return response

    def _get_data(self, uid, info, rewards):
        data = {
            'uid': str(uid).replace(str(uid)[2:-2], '*****', 1),
            'total_sign_day': info.get('data', {}).get('total_sign_day', 0),
            'today': info.get('data', {}).get('today', '1970-01-01'),
            'is_sign': info.get('data', {}).get('is_sign'),
            'first_bind': info.get('data', {}).get('first_bind'),
            'awards': rewards.get('data', {}).get('awards', []),
            'end': ''
        }

        return data

    def run(self, sign_data=None):
        if not sign_data:
            raise Exception('Empty sign data')
        if not isinstance(sign_data, dict):
            raise TypeError('Sign data must be a dict')

        uid = sign_data.get('uid', 123456789)
        total_sign_day = sign_data.get('total_sign_day', 0)
        is_sign = sign_data.get('is_sign')
        first_bind = sign_data.get('first_bind')
        awards = sign_data.get('awards', [])
        data = sign_data.get('post_data', {})
        message = sign_data

        log.info(f'准备为旅行者 {uid} 签到...')
        time.sleep(10)

        if is_sign:
            message['award_name'] = awards[total_sign_day - 1].get('name')
            message['award_cnt'] = awards[total_sign_day - 1].get('cnt')
            message['status'] = '👀 旅行者, 你已经签到过了哦'

            # return ''.join(self.message.format(**message))
            return self.message.format(**message)
        else:
            message['award_name'] = awards[total_sign_day].get('name')
            message['award_cnt'] = awards[total_sign_day].get('cnt')
        if first_bind:
            message['status'] = '💪 旅行者, 请先手动签到一次'

            return self.message.format(**message)

        try:
            response = to_python(req.request(
                'post', self._sign_url, headers=self.get_header(), data=data).text)
        except Exception as e:
            raise Exception(e)
        # 0:      success
        # -5003:  already checked in
        code = response.get('retcode', 99999)
        if code != 0:
            return response
        message['total_sign_day'] = total_sign_day + 1
        message['status'] = response.get('message')

        log.info('签到完毕')
        return self.message.format(**message)

    @property
    def message(self):
        return CONFIG.MESSAGE_TEMPLATE


class MHYLab(Base):
    def data_handler(self, **kwargs):
        uid = kwargs.get('uid', 12345678)
        info = kwargs.get('info', {})
        rewards = kwargs.get('rewards', {})

        data = self._get_data(uid, info, rewards)
        data['region_name'] = 'Global'
        data['post_data'] = {'act_id': CONFIG.OS_ACT_ID}

        return data


class MHYBbs(Base):
    def __init__(self, cookie: str = None):
        self._cookie = cookie
        self._user_agent = CONFIG.USER_AGENT
        self._referer = CONFIG.REFERER_URL
        self._role_url = CONFIG.ROLE_URL
        self._reward_url = CONFIG.REWARD_URL
        self._sign_url = CONFIG.SIGN_URL

    def get_header(self):
        header = super(MHYBbs, self).get_header()
        header.update({
            'x-rpc-device_id': str(uuid.uuid3(uuid.NAMESPACE_URL, self._cookie)).replace(
                '-', '').upper(),
            # 1:  ios
            # 2:  android
            # 4:  pc web
            # 5:  mobile web
            'x-rpc-client_type': '5',
            'x-rpc-app_version': CONFIG.APP_VERSION,
            'DS': get_ds()
        })
        return header

    def get_roles(self):
        log.info('准备获取账号信息...')
        response = {}
        header = super(MHYBbs, self).get_header()
        try:
            response = to_python(
                req.request('get', self._role_url, headers=header).text)
        except Exception as e:
            raise Exception(e)

        log.info('账号信息获取完毕')
        return response

    def set_info_url(self, url: str = None):
        self._info_url = url

        return self._info_url

    def data_handler(self, **kwargs):
        roles = kwargs.get('roles', {})
        if roles and (roles.get('retcode', 1) != 0 or not roles.get('data')):
            raise Exception(roles.get('message', 'Empty roles data'))
        role_list = roles.get('data', {}).get('list', [])
        if roles and not role_list:
            raise Exception(roles.get('message', 'Empty roles list'))
        elif role_list:
            log.info(f'当前账号绑定了 {len(role_list)} 个角色')
            roles_data = []
            for role in role_list:
                # cn_gf01:  天空岛
                # cn_qd01:  世界树
                region = role.get('region', 'cn')
                region_name = role.get('region_name', 'CN')
                uid = role.get('game_uid', 123456789)

                info_url = CONFIG.INFO_URL.format(
                    region, CONFIG.ACT_ID, uid)
                data = {
                    'act_id': CONFIG.ACT_ID,
                    'region': region,
                    'uid': uid
                }

                roles_data.append({
                    'region': region,
                    'region_name': region_name,
                    'uid': uid,
                    'info_url': info_url,
                    'post_data': data
                })

            return roles_data
        else:
            role_data = kwargs.get('role_data', {})
            uid = role_data.get('uid', 123456789)
            info = role_data.get('info', {})
            rewards = role_data.get('rewards', {})

            data = self._get_data(uid, info, rewards)
            data['region_name'] = role_data.get('name', 'CN')
            data['post_data'] = role_data.get('post_data', {})

            return data
