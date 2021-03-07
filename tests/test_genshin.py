import sys
import os
sys.path.append(os.path.dirname(__file__) + os.sep + '../')
print('')
import genshin_helper as gih
from config import COOKIE, OS_COOKIE


def run_bbs():
    print('Start testing...')

    print('\nPreparing to get account information...\n')
    roles = bbs.get_roles()
    print(roles)

    print('\nPreparing to parse roles data...\n')
    roles_data = bbs.data_handler(roles=roles)
    print(roles_data)

    for role_data in roles_data:
        print('\nPreparing to get sign information...\n')
        bbs.set_info_url(role_data.get('info_url', ''))
        info = bbs.get_info()
        print(info)

        print('\nPreparing to get rewards information...\n')
        rewards = bbs.get_rewards()
        print(rewards)

        print('\nPreparing to parse sign data...\n')
        sign_data = bbs.data_handler(
            role_data=role_data, info=info, rewards=rewards)
        print(sign_data)

        print('\nPreparing to run sign job...\n')
        msg = bbs.run(sign_data)
        print(msg)

    print('\nTest completed\n')


def run_lab():
    pass

    #os_rewards = gih.Hoyolab(OS_COOKIE).get_rewards()
    # print(os_rewards)
    #info_list = gih.Hoyolab(OS_COOKIE).get_info()
    # print(info)
    # d = lab.data_handler()
    # d = bbs.data_handler()
    #a = gih.Hoyolab(OS_COOKIE).run(d)

    #rewards = gih.Mihoyo(COOKIE).get_rewards()
    # print(rewards)

    # r = bbs.get_roles()
    # # r = {'data': None, 'message': '登录失效，请重新登录', 'retcode': -100}
    # d = bbs.data_handler(roles=r)

    # for i in d:
    #     print("yuanshi",i,"\n")
    #     # url = i.get('info_url', '')
    #     # uid = i.get('uid', 123456789)
    #     # a = bbs.set_info_url(url)

    #     # info = bbs.get_info()
    #     # d2 = bbs.data_handler(uid=uid,info=info)

    #     # print("url\n",a,d2)
    #     # exit()

    # #d = gih.MHYBbs('COOKIE')


    #
    # print(d)
if __name__ == '__main__':
    bbs = gih.MHYBbs(COOKIE)
    lab = gih.MHYLab(OS_COOKIE)
    run_bbs()
