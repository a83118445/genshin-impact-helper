import time
import uuid

from .utils import CONFIG, log, req, to_python, get_ds


class Base(object):
    def __init__(self, cookie: str=None):
        self._cookie = cookie
        self._user_agent = CONFIG.WB_USER_AGENT
        self._referer = CONFIG.OS_REFERER_URL
        self._info_url = CONFIG.OS_INFO_URL
        self._reward_url = CONFIG.OS_REWARD_URL
        self._sign_url = CONFIG.OS_SIGN_URL
        self._data = {'act_id': CONFIG.OS_ACT_ID}

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
    
    

    @property
    def message(self):
        return CONFIG.MESSAGE_TEMPLATE


class MHYLab(Base):
    def data_handler(self, **kwargs):
        uid = kwargs.get('uid', 12345678)
        info = kwargs.get('info', {})
        rewards = kwargs.get('rewards', {})

        data_dict = {
            'uid': str(uid).replace(str(uid)[2:-2], '*****', 1),
            'region_name': 'Global',
            'total_sign_day': info.get('data', {}).get('total_sign_day', 0),
            'today': info.get('data', {}).get('today', '1970-01-01'),
            'is_sign': info.get('data', {}).get('is_sign'),
            'first_bind': info.get('data', {}).get('first_bind'),
            'awards': rewards.get('data', {}).get('awards', []),
            'end': ''
        }

        return data_dict

    def run(self, message=None):
        if not message:
            raise Exception('Empty message data')
        if not isinstance(message, dict):
            raise TypeError('Message data must be a dict')

        uid = message.get('uid', 88888888)
        total_sign_day = message.get('total_sign_day', 0)
        is_sign = message.get('is_sign')
        first_bind = message.get('first_bind')
        awards = message.get('awards', [])

        log.info(f'准备为旅行者 {uid} 签到...')
        time.sleep(10)

        if not is_sign:
            message.update({
                'award_name':
                awards[total_sign_day - 1].get('name'),
                'award_cnt':
                awards[total_sign_day - 1].get('cnt'),
                'status':
                "👀 Traveler, you've already checked in today"
            })

            return ''.join(self.message.format(**message))
        else:
            message['award_name'] = awards[total_sign_day].get('name')
            message['award_cnt'] = awards[total_sign_day].get('cnt')

        if first_bind:
            message['status'] = f'💪 Please check in manually once'

            return ''.join(self.message.format(**message))

        try:
            response = to_python(
                req.request(
                    'post',
                    self._sign_url,
                    headers=self.get_header(),
                    data=self._data).text)
            print('签到')
        except Exception as e:
            raise Exception(e)
        code = response.get('retcode', 99999)
        # 0:      success
        # -5003:  already checked in
        if code != 0:
            return response
        message['total_sign_day'] = total_sign_day + 1
        message['status'] = response.get('message')

        log.info('签到完毕')

        return ''.join(self.message.format(**message))


class MHYBbs(Base):
    def __init__(self, cookie: str=None):
        self._cookie = cookie
        self._user_agent = CONFIG.USER_AGENT
        self._referer = CONFIG.REFERER_URL
        self._role_url = CONFIG.ROLE_URL
        self._info_url = CONFIG.INFO_URL
        self._reward_url = CONFIG.REWARD_URL
        self._sign_url = CONFIG.SIGN_URL
        
        
        self._data = ''

    def get_header(self):
        header = super(MHYBbs, self).get_header()
        header.update({
            'x-rpc-device_id':
            str(uuid.uuid3(uuid.NAMESPACE_URL, self._cookie)).replace(
                '-', '').upper(),
            # 1:  ios
            # 2:  android
            # 4:  pc web
            # 5:  mobile web
            'x-rpc-client_type':
            '5',
            'x-rpc-app_version':
            CONFIG.APP_VERSION,
            'DS':
            get_ds()
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
    
    def get_info_url(self):
        pass
    
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
                region = role.get('region', 'NA')
                region_name = role.get('region_name', 'NA')
                uid = role.get('game_uid', 'NA')
                
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
                    'data': data
                })
                
            return roles_data
        else:
            uid = kwargs.get('uid', 123456789)
            info = kwargs.get('info', {})
            rewards = kwargs.get('rewards', {})
    
            data_dict = {
                'uid': str(uid).replace(str(uid)[2:-2], '*****', 1),
                'region_name': '天空岛',
                'total_sign_day': info.get('data', {}).get('total_sign_day', 0),
                'today': info.get('data', {}).get('today', '1970-01-01'),
                'is_sign': info.get('data', {}).get('is_sign'),
                'first_bind': info.get('data', {}).get('first_bind'),
                'awards': rewards.get('data', {}).get('awards', []),
                'end': ''
            }

            return data_dict

